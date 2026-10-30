import json, os, re, hashlib
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = S + "/src"
L = json.load(open(S + "/lists/lists.json"))
old = json.load(open("/home/user/skill/data/sources.json"))
oldkey = {(o["repo"], o["path"]): o["slug"] for o in old}
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
MOVED = {  # Skill Store entries whose pinned folder is gone; use the current location
    ("Skill Store", 11): ("alirezarezvani/claude-skills", "marketing-skill/skills/content-creator/SKILL.md"),
    ("Skill Store", 40): ("C0ntr0lledCha0s/claude-code-plugin-automations", "claude-component-builder/skills/building-agents/SKILL.md"),
    ("Skill Store", 48): ("K-Dense-AI/claude-scientific-skills", "skills/venue-templates/SKILL.md"),
    ("Awesome Claude", 41): ("obra/superpowers", "skills/systematic-debugging/root-cause-tracing.md"),
}
SS = json.load(open(S + "/web/ss-rec.json"))["data"]
items, seen = [], {}
for x in L:
    key = None; text = None; src = None
    if x["site"] == "Skill Store" and os.path.exists(f"{S}/raw/skillstore/{x['rank']:02d}.md"):
        text = open(f"{S}/raw/skillstore/{x['rank']:02d}.md").read()
        m = re.match(r"https://github.com/([^/]+/[^/]+)/tree/([^/]+)/?(.*)", SS[x["rank"] - 1]["repo"])
        x["path"] = (m.group(3).strip("/") + "/SKILL.md").lstrip("/")
        x["ref"] = m.group(2)
        src = "skillstore-pinned"
    elif (x["site"], x["rank"]) in MOVED:
        x["repo"], x["path"] = MOVED[(x["site"], x["rank"])]
    if text is None and x.get("path"):
        text = open(f"{SRC}/{x['repo'].replace('/', '_')}/{x['path']}", encoding="utf-8", errors="replace").read()
        src = "repo"
    if text is None and x["site"] == "Skills.sh" and os.path.exists(f"{S}/raw/skillssh/{x['name']}.md"):
        text = open(f"{S}/raw/skillssh/{x['name']}.md").read(); src = "skills.sh-page"
    x["src"] = src
    if text is None:
        x["slug"] = None; items.append(x); continue
    k = (x["repo"], x.get("path"))
    h = hashlib.sha1(re.sub(r"\s+", " ", text).encode()).hexdigest()[:12]
    x["hash"] = h
    if k in oldkey:
        x["slug"] = oldkey[k]
    elif h in seen:
        x["slug"] = seen[h]
    else:
        base = re.sub(r"[^a-z0-9]+", "-", (os.path.basename(os.path.dirname(x["path"])) if x.get("path") and x["path"].endswith("SKILL.md") and os.path.dirname(x["path"]) else x["name"]).lower()).strip("-")
        slug = base; n = 2
        used = set(oldkey.values()) | set(seen.values())
        while slug in used:
            slug = f"{base}-{x['repo'].split('/')[0].lower()}" if n == 2 else f"{base}-{n}"; n += 1
        x["slug"] = slug
        x["new"] = True
        x["chars"] = len(FENCE.sub("", text))
        os.makedirs(S + "/new", exist_ok=True)
        open(f"{S}/new/{slug}.md", "w").write(text)
    seen.setdefault(h, x["slug"])
    items.append(x)
json.dump(items, open(S + "/lists/manifest.json", "w"), indent=1, ensure_ascii=False)
from collections import defaultdict
tot = defaultdict(lambda: [0, 0])
for x in items:
    if x.get("new"): tot[x["site"]][0] += 1; tot[x["site"]][1] += x["chars"]
print(dict(tot), "new unique:", sum(v[0] for v in tot.values()), "chars:", sum(v[1] for v in tot.values()))
print("missing:", [(x["site"], x["rank"], x["name"]) for x in items if not x["slug"]])
