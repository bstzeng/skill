import json, os, re, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = S + "/src"
L = json.load(open(S + "/lists/lists.json"))

def skills_in(repo):
    root = f"{SRC}/{repo.replace('/', '_')}"
    res = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules")]
        if "SKILL.md" in fn:
            res.append(os.path.relpath(os.path.join(dp, "SKILL.md"), root))
    return root, res

def fm_name(p):
    try:
        t = open(p, encoding="utf-8", errors="replace").read(3000)
    except Exception:
        return ""
    m = re.search(r"^name:\s*['\"]?([^'\"\n]+)", t, re.M)
    return m.group(1).strip() if m else ""

cache = {}
for x in L:
    x["path"] = None
    if not x["repo"] or not os.path.isdir(f"{SRC}/{x['repo'].replace('/', '_')}"):
        continue
    if x["repo"] not in cache:
        cache[x["repo"]] = skills_in(x["repo"])
    root, all_ = cache[x["repo"]]
    cand = []
    if x["dir"]:
        d = x["dir"].rstrip("/")
        if d.endswith("SKILL.md"): d = os.path.dirname(d)
        cand = [p for p in all_ if os.path.dirname(p) == d] or [p for p in all_ if p.startswith(d + "/")]
    else:
        n = x["name"].lower()
        cand = [p for p in all_ if os.path.basename(os.path.dirname(p)).lower() == n] or \
               [p for p in all_ if fm_name(os.path.join(root, p)).lower() == n] or \
               ([p for p in all_ if os.path.dirname(p) == ""]) or (all_ if len(all_) == 1 else [])
    if len(cand) > 1 and x["dir"] is None:
        cand.sort(key=len)
    if len(cand) > 1 and x["dir"]:
        # a pack folder: prefer the skill named like the entry, else the shortest
        n = re.sub(r"[^a-z0-9]+", "-", x["name"].lower()).strip("-")
        named = [p for p in cand if os.path.basename(os.path.dirname(p)).lower() == n]
        cand = named or sorted(cand, key=len)
        x["pack"] = len(cand) > 1 and not named
    if cand:
        x["path"] = cand[0]
json.dump(L, open(S + "/lists/lists.json", "w"), indent=1, ensure_ascii=False)
for x in L:
    if not x["path"] or x.get("pack"):
        print("UNRESOLVED" if not x["path"] else "PACK", x["site"], x["rank"], x["name"], x["repo"], x["dir"], x["path"])
