"""Write translations/<slug>.md for skills whose original is Simplified Chinese, via OpenCC (s2twp).

Usage: python3 scripts/opencc_translate.py meta.json   (needs `pip install opencc-python-reimplemented`)
meta.json maps slug -> {"title", "category", "tags", "summary", "usage"}; the body comes from .masked/<slug>.md.
"""
import json, os, sys
from opencc import OpenCC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cc = OpenCC("s2twp")
for slug, meta in json.load(open(sys.argv[1], encoding="utf-8")).items():
    body = cc.convert(open(os.path.join(ROOT, ".masked", slug + ".md"), encoding="utf-8").read())
    with open(os.path.join(ROOT, "translations", slug + ".md"), "w", encoding="utf-8") as f:
        f.write("<!--meta\n" + json.dumps(meta, ensure_ascii=False) + "\n-->\n" + body)
    print("wrote", slug)
