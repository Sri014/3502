#!/usr/bin/env python3

import os
import sys
import urllib.request
from pathlib import Path

SOURCES = {
    # Public IPTV-ORG playlists
    "iptv_org.m3u":
        "https://iptv-org.github.io/iptv/index.m3u",

    # Add more PUBLIC/LEGAL M3U sources here.
    # "source2.m3u": "https://example.com/playlist.m3u",
}


def download(name, url, out_dir):
    path = out_dir / name

    print(f"[+] Downloading: {url}")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()

        if not data:
            print(f"[!] Empty response: {url}")
            return False

        path.write_bytes(data)

        print(
            f"[OK] {name}: "
            f"{len(data):,} bytes"
        )

        return True

    except Exception as e:
        print(f"[!] Failed: {url}")
        print(f"    {e}")
        return False


def main():
    out_dir = Path("sources")
    out_dir.mkdir(parents=True, exist_ok=True)

    success = 0

    for name, url in SOURCES.items():
        if download(name, url, out_dir):
            success += 1

    print()
    print("==============================")
    print(f"Sources downloaded: {success}/{len(SOURCES)}")
    print("==============================")


if __name__ == "__main__":
    main()
