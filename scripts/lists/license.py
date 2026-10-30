import json, os, re
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = S + "/src"
M = json.load(open(S + "/lists/manifest.json"))
SS = {i: x for i, x in enumerate(json.load(open(S + "/web/ss-rec.json"))["data"], 1)}
def detect(text):
    t = text[:3000]
    if re.search(r"MIT License|Permission is hereby granted, free of charge", t): return "MIT"
    if "Apache License" in t: return "Apache-2.0"
    if re.search(r"BSD", t): return "BSD"
    if "Mozilla Public License" in t: return "MPL-2.0"
    if "GNU GENERAL PUBLIC" in t.upper(): return "GPL"
    if "Creative Commons" in t or "CC BY" in t: return "CC"
    if "All rights reserved" in t or "Proprietary" in t: return "Proprietary"
    return "Other"
for x in M:
    if not x.get("slug") or not x.get("new"): continue
    lic = None
    root = f"{SRC}/{(x['repo'] or 'none').replace('/', '_')}"
    d = os.path.dirname(x["path"]) if x.get("path") else ""
    cands = []
    while True:
        cands.append(os.path.join(root, d))
        if not d: break
        d = os.path.dirname(d)
    for c in cands:
        if os.path.isdir(c):
            for f in os.listdir(c):
                if re.match(r"(?i)licen[cs]e", f) and os.path.isfile(os.path.join(c, f)):
                    lic = detect(open(os.path.join(c, f), errors="replace").read()); break
        if lic: break
    fm = re.search(r"^license:\s*(.+)$", open(f"{S}/new/{x['slug']}.md").read()[:2000], re.M)
    if not lic and fm: lic = fm.group(1).strip().strip('"')
    if not lic and x["site"] == "Skill Store": lic = SS[x["rank"]]["license"]
    x["license"] = lic or "未標示授權"
json.dump(M, open(S + "/lists/manifest.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(x["license"] for x in M if x.get("new")))
for x in M:
    if x.get("new") and not re.match(r"(?i)(MIT|Apache|BSD|MPL|CC)", x["license"]): print(x["site"], x["rank"], x["slug"], x["repo"], x["license"])
