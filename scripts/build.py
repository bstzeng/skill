"""Merge originals + translations into data/skills.json and render the web page.

Usage: python3 scripts/build.py [path/to/skills-sh.csv]
The optional CSV (from LinklyAI/best-skills, data/latest/raw/skills-sh.csv) refreshes
install counts; without it the counts already stored in data/skills.json are kept.
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
META = re.compile(r"<!--meta\n(.*?)\n-->\n?", re.S)

LICENSES = {
    "vercel-labs/skills": "MIT", "mattpocock/skills": "MIT", "heygen-com/hyperframes": "Apache-2.0",
    "vercel-labs/agent-browser": "Apache-2.0", "flowkit-labs/skills": "MIT", "designed-by-ai/skills": "MIT",
    "101-skills/superpowers": "MIT", "vercel-labs/agent-skills": "MIT", "larksuite/cli": "MIT",
    "remotion-dev/skills": "未標示授權", "leonxlnx/taste-skill": "MIT", "juliusbrussee/caveman": "Apache-2.0",
    "microsoft/azure-skills": "MIT", "anthropics/skills": "Apache-2.0", "openai/skills": "Apache-2.0",
    "obra/superpowers": "MIT",
}
PROPRIETARY = {"docx", "pdf", "pptx", "xlsx"}
# Repos that the curated "awesome" lists (travisvn / ComposioHQ awesome-claude-skills) link to.
AWESOME = {"anthropics/skills", "obra/superpowers"}
# Name the skill is published under on skills.sh, when it differs from the folder name.
SKILLSSH_NAME = {}


def split_front(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end], text[end + 4:].lstrip("\n")
    return "", text


def front_desc(front):
    m = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", front, re.M | re.S)
    if not m:
        return ""
    v = m.group(1).strip()
    if v[:2] in (">-", ">\n") or v.startswith(">") or v.startswith("|"):
        v = v.split("\n", 1)[1] if "\n" in v else ""
    v = " ".join(line.strip() for line in v.splitlines()).strip()
    return v.strip('"')


def load_installs(path):
    out = {}
    for row in csv.DictReader(open(path, encoding="utf-8")):
        if row["view"] == "all-time":
            out[(row["source"], row["name"])] = (int(row["rank"]), int(row["installs"] or 0))
    return out


def main():
    sources = json.load(open(os.path.join(ROOT, "data", "sources.json"), encoding="utf-8"))
    old = {}
    old_path = os.path.join(ROOT, "data", "skills.json")
    if os.path.exists(old_path):
        old = {s["slug"]: s for s in json.load(open(old_path, encoding="utf-8"))["skills"]}
    installs = load_installs(sys.argv[1]) if len(sys.argv) > 1 else None

    skills = []
    for i, s in enumerate(sources, 1):
        slug, repo = s["slug"], s["repo"]
        raw = open(os.path.join(ROOT, "translations", slug + ".md"), encoding="utf-8").read()
        m = META.match(raw)
        meta = json.loads(m.group(1))
        zh = raw[m.end():]

        original = ""
        orig_path = os.path.join(ROOT, "skills", slug, "SKILL.md")
        if s["redistributable"]:
            original = open(orig_path, encoding="utf-8").read()
            blocks = [b.group(0) for b in FENCE.finditer(original)]
            zh = re.sub(r"\{\{CODE:(\d+)\}\}", lambda c: blocks[int(c.group(1)) - 1], zh)
        ofront, _ = split_front(original)
        zfront, _ = split_front(zh)

        if installs is not None:
            rank_inst = installs.get((repo, SKILLSSH_NAME.get(slug, slug)))
        else:
            prev = old.get(slug, {})
            rank_inst = (prev["skillssh_rank"], prev["installs"]) if prev.get("installs") else None

        site = []
        if rank_inst:
            site.append("Skills.sh")
        if repo == "anthropics/skills":
            site.append("Anthropic 官方")
        if repo == "openai/skills":
            site.append("OpenAI Codex")
        if repo in AWESOME:
            site.append("Awesome Claude")

        skills.append({
            "rank": i,
            "slug": slug,
            "title": meta["title"],
            "category": meta["category"],
            "tags": meta["tags"],
            "summary": meta["summary"],
            "usage": meta["usage"],
            "sites": site,
            "repo": repo,
            "path": s["path"],
            "github_url": f"https://github.com/{repo}/blob/main/{s['path']}",
            "skillssh_url": f"https://skills.sh/{repo}/{slug}" if rank_inst else "",
            "skillssh_rank": rank_inst[0] if rank_inst else None,
            "installs": rank_inst[1] if rank_inst else None,
            "license": "Anthropic 專有授權" if slug in PROPRIETARY else LICENSES.get(repo, ""),
            "redistributable": s["redistributable"],
            "description_en": front_desc(ofront),
            "description_zh": front_desc(zfront),
            "original": original,
            "translation": zh.strip() if s["redistributable"] else "",
        })

    data = {
        "updated": "2026-10-29",
        "method": "Skills.sh 全站安裝排行（取自 LinklyAI/best-skills 每日鏡像）去重後取前段，"
                  "同系列（飛書 lark-*、HyperFrames）最多收 2–3 個，再以 Anthropic 官方、OpenAI Codex 官方與 "
                  "Awesome Claude 精選清單中的代表作補足 50 個。",
        "skills": skills,
    }
    with open(old_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("__DATA__", payload)
    open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(
        "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + page.replace("<!--BODY-->", "</head>\n<body>", 1) + "\n</body>\n</html>\n")
    # Artifact build: the host adds the document skeleton itself.
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "site", "artifact.html")
    open(out, "w", encoding="utf-8").write(page.replace("<!--BODY-->", "", 1))
    print(len(skills), "skills;", sum(1 for s in skills if s["installs"]), "with installs")


if __name__ == "__main__":
    main()
