#!/usr/bin/env python3
"""扫描根目录下的系列文件夹，生成 collections.json。

GitHub Actions 会在每次 push 后自动运行它；本地也可以手动运行：
    python3 build_collections.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "collections.json"
PHOTO_SUFFIXES = {".jpg", ".jpeg", ".png"}
IGNORED_DIRS = {"node_modules", "__pycache__", "venv", ".venv"}


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
            key=lambda name: (
                0 if name.lower().endswith((".jpg", ".jpeg")) else 1,
                natural_key(name),
            ),
        )
        if photos:
            collections.append({"dir": folder.name, "photos": photos})
    return collections


def write_manifest():
    collections = scan_collections()
    MANIFEST.write_text(
        json.dumps({"collections": collections}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    total = sum(len(item["photos"]) for item in collections)
    print(f"已生成 collections.json：{len(collections)} 个系列，{total} 张图片")
    for item in collections:
        print(f"  {item['dir']}/  {len(item['photos'])} 张")
    return collections


if __name__ == "__main__":
    write_manifest()
