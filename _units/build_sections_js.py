#!/usr/bin/env python3
"""source/pi_sections.json → learning_site/data/pi_sections.js（依 sec 排序、去掉 page）。"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT / "source" / "pi_sections.json"
OUT = HERE.parent / "data" / "pi_sections.js"
FIELDS = ["k", "src", "label", "sec", "ph", "e", "also", "zh", "de", "en", "gist", "list"]


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows = []
    for i, d in enumerate(data):
        rows.append((d["sec"], i, {f: d[f] for f in FIELDS if f in d}))
    rows.sort(key=lambda r: (r[0], r[1]))
    items = [r[2] for r in rows]
    head = (
        "// 此檔由 learning_site/_units/build_sections_js.py 自動產生，請勿手改。\n"
        "// 來源：source/pi_sections.json\n"
        "// 德文為原文短句引用；中文與英文為本系列自譯。\n"
    )
    body = "window.PI_SECTIONS = " + json.dumps(items, ensure_ascii=False, indent=1) + ";\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(head + body, encoding="utf-8")
    print(f"wrote {OUT} ({len(items)} items)")


if __name__ == "__main__":
    main()
