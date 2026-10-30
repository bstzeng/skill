import json, re, os, glob, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = S + "/src"
out = []

# Skills.sh
for o in json.load(open(S + "/web/skillssh-top50.json")):
    h = o["href"]
    if h.startswith("site/open.feishu.cn/"):
        repo, name = "larksuite/cli", h.split("/")[-1]
    elif h.startswith("site/"):
        repo, name = None, h.split("/")[-1]
    else:
        a, b, name = h.split("/", 2)
        repo = a + "/" + b
    out.append(dict(site="Skills.sh", rank=o["rank"], name=name, repo=repo, dir=None,
                    url="https://www.skills.sh/" + h, installs=o["installs"]))
assert sum(1 for x in out if x["site"] == "Skills.sh") == 50

# Skill Store (Recommended order = quality score)
for i, x in enumerate(json.load(open(S + "/web/ss-rec.json"))["data"], 1):
    m = re.match(r"https://github.com/([^/]+/[^/]+)/tree/[^/]+/?(.*)", x["repo"])
    out.append(dict(site="Skill Store", rank=i, name=x["displayName"], repo=m.group(1), dir=m.group(2).strip("/") or None,
                    url="https://skillstore.io/skills/" + x["slug"], score=x["qualityScore"], risk=x["riskLevel"]))

# Anthropic: every skill in the official repo
for i, d in enumerate(sorted(os.listdir(SRC + "/anthropics_skills/skills")), 1):
    out.append(dict(site="Anthropic", rank=i, name=d, repo="anthropics/skills", dir="skills/" + d,
                    url=f"https://github.com/anthropics/skills/tree/main/skills/{d}"))

# OpenAI: openai/skills (system + curated), then first plugins of the official marketplace
r = 0
for grp in (".system", ".curated"):
    for d in sorted(os.listdir(f"{SRC}/openai_skills/skills/{grp}")):
        if os.path.exists(f"{SRC}/openai_skills/skills/{grp}/{d}/SKILL.md"):
            r += 1
            out.append(dict(site="OpenAI", rank=r, name=d, repo="openai/skills", dir=f"skills/{grp}/{d}",
                            url=f"https://github.com/openai/skills/tree/main/skills/{grp}/{d}"))
mk = json.load(open(SRC + "/openai_plugins/.agents/plugins/marketplace.json"))
for p in mk["plugins"]:
    if r >= 50: break
    path = p["source"].get("path")
    if not path: continue
    base = os.path.normpath(path).lstrip("./")
    sk = sorted(os.path.basename(os.path.dirname(s)) for s in glob.glob(f"{SRC}/openai_plugins/{base}/skills/*/SKILL.md"))
    if not sk: continue
    pick = p["name"] if p["name"] in sk else sk[0]
    r += 1
    out.append(dict(site="OpenAI", rank=r, name=pick, repo="openai/plugins", dir=f"{base}/skills/{pick}",
                    url=f"https://github.com/openai/plugins/tree/main/{base}/skills/{pick}", plugin=p["name"]))

# Awesome Claude: ComposioHQ list order (skills section), GitHub entries only
lines = open(SRC + "/ComposioHQ_awesome-claude-skills/README.md").read().splitlines()
start = lines.index("## Skills"); end = next(i for i, l in enumerate(lines) if l.startswith("### App Automation"))
r = 0
for l in lines[start:end]:
    m = re.match(r"- \[([^\]]+)\]\(([^)]+)\)", l)
    if not m: continue
    label, link = m.groups()
    if link.startswith("./"):
        repo, d = "ComposioHQ/awesome-claude-skills", link[2:].strip("/")
    else:
        g = re.match(r"https://github.com/([^/]+/[^/#?]+)(?:/(?:tree|blob)/[^/]+/?(.*))?", link)
        if not g: continue
        repo, d = g.group(1), (g.group(2) or "").strip("/") or None
    r += 1
    out.append(dict(site="Awesome Claude", rank=r, name=label, repo=repo, dir=d, url=link if link.startswith("http") else
                    "https://github.com/ComposioHQ/awesome-claude-skills/tree/master/" + d))
    if r == 60: break   # a few spares in case some do not resolve to a SKILL.md
json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(x["site"] for x in out)); print(sorted({x["repo"] for x in out if x["repo"]}))
