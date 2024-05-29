from urllib import parse
from urllib.parse import quote_plus

class ToHttp:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("http", help="make http requests")
        parser.add_argument("-u", "--url", help="URL", required=True)
        parser.add_argument("-H", "--headers", action="extend", nargs="+", help="Request header")
        parser.add_argument("-X", "--method", help="Request method")
        parser.add_argument("-d", "--body", help="Request body", default="")
        parser.add_argument('--double-encode', action='store_true', help="Double URL encode")
        parser.set_defaults(run=self.run)

    def make_headers(self, headers: dict = {}) -> str:
        raw_headers = ""
        for header in list(headers.keys()):
            raw_headers += f"{header}: {headers[header]}\r\n"
        
        raw_headers += "\r\n"
        return raw_headers

    def make_request(self, method: str, uri: str, headers: dict, body: str = "") -> str:
        request = f"{method} {uri} HTTP/1.1\r\n"
        request += self.make_headers(headers)

        if len(body) > 0:
            request += body

        return request

    def encode(self, request: str) -> str:
        return quote_plus(request).replace("+", "%20")

    def run(self, args) -> str:
        url_parsed = parse.urlsplit(args.url)
        
        host = url_parsed.netloc
        uri = f"{url_parsed.path}?{url_parsed.query}"

        headers = {
            "host": host,
            "user-agent": "curl/8.0",
            "connection": "close",
        }

        if not args.method:
            if args.body:
                args.method = "POST"
            else:
                args.method = "GET"

        if args.method.upper() not in ['GET', 'DELETE']:
            headers['content-type'] = 'application/x-www-form-urlencoded'
            headers['content-length'] = len(args.body)

        if args.headers:
            for header in args.headers:
                name, value = header.split(':')
                headers[name.lower().strip()] = value.strip()

        payload = self.make_request(args.method.upper(), uri, headers, args.body)
        payload = self.encode(payload)

        if args.double_encode:
            payload = self.encode(payload)

        print(f"gopher://{host}/_{payload}")