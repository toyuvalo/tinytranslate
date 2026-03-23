#!/usr/bin/env python3
"""
Download an Argos Translate language pack.
Called by install.ps1. Can also be run manually.

Usage:
    python download_model.py en fr
    python download_model.py en es
"""
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: download_model.py <from_code> <to_code>")
        print("Example: download_model.py en fr")
        sys.exit(1)

    from_code = sys.argv[1].lower().strip()
    to_code   = sys.argv[2].lower().strip()

    print(f"Fetching package index...")
    from argostranslate import package
    package.update_package_index()

    available = package.get_available_packages()
    pack = next(
        (p for p in available if p.from_code == from_code and p.to_code == to_code),
        None,
    )

    if not pack:
        print(f"ERROR: No package available for {from_code} -> {to_code}.")
        print("\nAvailable packages:")
        for p in sorted(available, key=lambda x: (x.from_code, x.to_code)):
            print(f"  {p.from_code} -> {p.to_code}  ({p.from_name} -> {p.to_name})")
        sys.exit(1)

    print(f"Downloading: {pack.from_name} -> {pack.to_name} ...")
    path = pack.download()
    print(f"Installing...")
    package.install_from_path(path)
    print(f"[OK] {from_code} -> {to_code} language pack installed.")


if __name__ == "__main__":
    main()
