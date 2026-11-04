#!/usr/bin/env python3
"""本地预览：每次请求都重新扫描文件夹，不把合集列表写死进 HTML。

用法：
    python3 preview.py
    python3 preview.py --port 8080

GitHub Pages 上不需要运行它：页面会直接读取仓库的目录。
"""
from __future__ import annotations

import argparse
import functools
import json
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
PHOTO_SUFFIXES = {".jpg", ".jpeg"}
IGNORED_DIRS = {"node_modules", "__pycache__", "venv", ".venv"}
LOCAL_MANIFEST_PATH = "/__local_collections.json"


def natural_key(value: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def scan_collections():
    collections = []
    for folder in sorted(ROOT.iterdir(), key=lambda item: natural_key(item.name)):
        if not folder.is_dir() or folder.name.startswith(".") or folder.name in IGNORED_DIRS:
            continue
        photos = sorted(
            (
                file.name
                for file in folder.iterdir()
                if file.is_file() and file.suffix.lower() in PHOTO_SUFFIXES
            ),
            key=natural_key,
        )
        if photos:
            collections.append({"dir": folder.name, "photos": photos})
    return collections


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == LOCAL_MANIFEST_PATH:
            payload = json.dumps(
                {"collections": scan_collections()},
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store, max-age=0")
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def end_headers(self):
        if urlsplit(self.path).path in ("/", "/index.html"):
            self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


def main() -> int:
    parser = argparse.ArgumentParser(description="本地预览安玖的小站")
    parser.add_argument("--port", type=int, default=8000, help="端口，默认 8000")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1")
    args = parser.parse_args()

    handler = functools.partial(Handler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as error:
        print(f"无法启动服务器：{error}", file=sys.stderr)
        return 1

    print(f"本地预览：http://{args.host}:{args.port}/")
    print("增删文件夹或照片后刷新页面即可，Ctrl+C 停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
