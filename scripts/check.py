"""Check that every translation's {{CODE:n}} markers match the original's fenced code blocks."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
META = re.compile(r"<!--meta\n(.*?)\n-->\n?", re.S)
bad = 0
for s in json.load(open(os.path.join(ROOT, "data", "sources.json"), encoding="utf-8")):
    p = os.path.join(ROOT, "translations", s["slug"] + ".md")
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8").read()
    m = META.match(t)
    try:
        meta = json.loads(m.group(1))
        assert all(meta.get(k) for k in ("title", "category", "tags", "summary", "usage"))
    except Exception as e:
        print("META", s["slug"], e); bad += 1; continue
    if not s["redistributable"]:
        continue
    orig = open(os.path.join(ROOT, "skills", s["slug"], "SKILL.md"), encoding="utf-8").read()
    n = len(FENCE.findall(orig))
    got = sorted(set(int(x) for x in re.findall(r"\{\{CODE:(\d+)\}\}", t[m.end():])))
    if got != list(range(1, n + 1)):
        print("CODE", s["slug"], got, n); bad += 1
print("problems:", bad)
sys.exit(1 if bad else 0)
