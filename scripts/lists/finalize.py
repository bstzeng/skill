import json, os, re
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "/home/user/skill"
M = json.load(open(S + "/lists/manifest.json"))
SS = {i: x for i, x in enumerate(json.load(open(S + "/web/ss-rec.json"))["data"], 1)}
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
OK = re.compile(r"(?i)^(MIT|Apache|BSD|MPL|CC|GPL|AGPL)")
FIX = {"lean-ctx": "Apache-2.0", "reddit-fetch": "All Rights Reserved"}
for x in M:
    if x.get("slug") in FIX: x["license"] = FIX[x["slug"]]
    if x.get("license", "").startswith("Other") and x["repo"] in ("openai/skills", "openai/plugins"): x["license"] = "Figma Developer Terms"

# keep the first 50 resolvable entries of the Awesome list
aw = [x for x in M if x["site"] == "Awesome Claude"]
keep, r = [], 0
for x in aw:
    if r == 50: break
    r += 1; x["rank"] = r; keep.append(x)
M = [x for x in M if x["site"] != "Awesome Claude"] + keep

sources = {s["slug"]: s for s in json.load(open(R + "/data/sources.json"))}
lists = {}
os.makedirs(R + "/.masked", exist_ok=True)
for x in M:
    e = {"rank": x["rank"], "label": x["name"], "url": x["url"], "slug": x.get("slug")}
    if x["site"] == "Skills.sh": e["installs"] = x["installs"]
    if x["site"] == "Skill Store":
        e["score"] = SS[x["rank"]]["qualityScore"]; e["risk"] = SS[x["rank"]]["riskLevel"]
        e["label"] = SS[x["rank"]]["displayName"]
    if x["site"] == "OpenAI" and x.get("plugin"): e["plugin"] = x["plugin"]
    if not x.get("slug"): e["missing"] = True
    lists.setdefault(x["site"], []).append(e)
    if x.get("new") and x["slug"] not in sources:
        text = open(f"{S}/new/{x['slug']}.md").read()
        redist = bool(OK.match(x["license"]))
        n = [0]
        def mask(m):
            n[0] += 1; return "{{CODE:%d}}" % n[0]
        masked = FENCE.sub(mask, text)
        open(f"{R}/.masked/{x['slug']}.md", "w").write(masked)
        if redist:
            os.makedirs(f"{R}/skills/{x['slug']}", exist_ok=True)
            open(f"{R}/skills/{x['slug']}/SKILL.md", "w").write(text)
        sources[x["slug"]] = {"slug": x["slug"], "repo": x["repo"], "path": x.get("path"), "ref": x.get("ref", "main"),
                              "via": x["src"], "license": x["license"], "redistributable": redist,
                              "code_blocks": n[0], "chars": len(masked)}
for s in lists.values(): s.sort(key=lambda e: e["rank"])
json.dump(lists, open(R + "/data/lists.json", "w"), indent=1, ensure_ascii=False)
json.dump(list(sources.values()), open(R + "/data/sources.json", "w"), indent=1, ensure_ascii=False)
print({k: len(v) for k, v in lists.items()}, "unique skills:", len(sources))
print("todo full:", sum(1 for s in sources.values() if not os.path.exists(f"{R}/translations/{s['slug']}.md") and s["redistributable"]),
      "todo summary-only:", sum(1 for s in sources.values() if not os.path.exists(f"{R}/translations/{s['slug']}.md") and not s["redistributable"]))
