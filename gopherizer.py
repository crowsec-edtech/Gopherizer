#!/usr/bin/python3

import argparse
from importlib import import_module
from pathlib import Path

def load_tools(subparsers):
    for filename in Path("tools").glob("[a-z]*.py"):
        module_name = filename.stem
        module = import_module(f"tools.{module_name}")
        for name in dir(module):
            Class = getattr(module, name)
            if isinstance(Class, type):
                Class(subparsers)

def main():
    try:
        parser = argparse.ArgumentParser(description="gopher protocol payload generator to exploit Server Side Request Forgery (SSRF)")
        subparsers = parser.add_subparsers(title="Tools", dest="tool")

        load_tools(subparsers)

        args = parser.parse_args()
        args.run(args)

    except AttributeError:
        parser.print_help()

if __name__ == "__main__":
    main()
