"""Merge originals, translations and the per-site lists into data/skills.json and render the web page.

Usage: python3 scripts/build.py
Inputs: data/sources.json (one entry per unique skill), data/lists.json (each site's Top 50),
skills/<slug>/SKILL.md (originals that may be redistributed), translations/<slug>.md.
A skill without a translation yet is still listed, with its original and a "翻譯中" note.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
META = re.compile(r"<!--meta\n(.*?)\n-->\n?", re.S)
SITES = ["Skills.sh", "Skill Store", "Anthropic", "OpenAI", "Awesome Claude"]

# Licenses of the first batch, which predates per-skill license detection.
LICENSES = {
    "vercel-labs/skills": "MIT", "mattpocock/skills": "MIT", "heygen-com/hyperframes": "Apache-2.0",
    "vercel-labs/agent-browser": "Apache-2.0", "flowkit-labs/skills": "MIT", "designed-by-ai/skills": "MIT",
    "101-skills/superpowers": "MIT", "vercel-labs/agent-skills": "MIT", "larksuite/cli": "MIT",
    "remotion-dev/skills": "未標示授權", "leonxlnx/taste-skill": "MIT", "juliusbrussee/caveman": "Apache-2.0",
    "microsoft/azure-skills": "MIT", "anthropics/skills": "Apache-2.0", "openai/skills": "Apache-2.0",
    "obra/superpowers": "MIT",
}
PROPRIETARY = {"docx", "pdf", "pptx", "xlsx"}


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
    if v.startswith(">") or v.startswith("|"):
        v = v.split("\n", 1)[1] if "\n" in v else ""
    v = " ".join(line.strip() for line in v.splitlines()).strip()
    return v.strip('"').strip("'")


def main():
    sources = json.load(open(os.path.join(ROOT, "data", "sources.json"), encoding="utf-8"))
    lists = json.load(open(os.path.join(ROOT, "data", "lists.json"), encoding="utf-8"))
    ranks = {}
    for site, entries in lists.items():
        for e in entries:
            if e.get("slug"):
                ranks.setdefault(e["slug"], {}).setdefault(site, e["rank"])

    skills = []
    for s in sources:
        slug, repo = s["slug"], s["repo"]
        original = ""
        if s["redistributable"]:
            original = open(os.path.join(ROOT, "skills", slug, "SKILL.md"), encoding="utf-8").read()
        tpath = os.path.join(ROOT, "translations", slug + ".md")
        meta, zh = {}, ""
        if os.path.exists(tpath):
            raw = open(tpath, encoding="utf-8").read()
            m = META.match(raw)
            meta = json.loads(m.group(1))
            zh = raw[m.end():]
            if original:
                blocks = [b.group(0) for b in FENCE.finditer(original)]
                zh = re.sub(r"\{\{CODE:(\d+)\}\}", lambda c: blocks[int(c.group(1)) - 1], zh)
        ofront, _ = split_front(original)
        zfront, _ = split_front(zh)
        ref = s.get("ref", "main")
        if s.get("via") == "skills.sh-page":
            github_url = next(e["url"] for e in lists["Skills.sh"] if e.get("slug") == slug)
        elif repo:
            github_url = f"https://github.com/{repo}/blob/{ref}/{s['path']}"
        else:
            github_url = ""
        license_ = s.get("license") or ("Anthropic 專有授權" if slug in PROPRIETARY else LICENSES.get(repo, ""))
        skills.append({
            "slug": slug,
            "title": meta.get("title", ""),
            "category": meta.get("category", "待分類"),
            "tags": meta.get("tags", []),
            "summary": meta.get("summary", ""),
            "usage": meta.get("usage", ""),
            "translated": bool(meta),
            "ranks": ranks.get(slug, {}),
            "repo": repo or "",
            "path": s.get("path") or "",
            "ref": ref,
            "github_url": github_url,
            "license": license_,
            "redistributable": s["redistributable"],
            "description_en": front_desc(ofront) or s.get("description_en", ""),
            "description_zh": front_desc(zfront),
            "original": original,
            "translation": zh.strip() if s["redistributable"] else "",
        })

    data = {
        "updated": "2026-10-30",
        "sites": SITES,
        "lists": lists,
        "skills": skills,
    }
    with open(os.path.join(ROOT, "data", "skills.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("__DATA__", payload)
    open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(
        "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + page.replace("<!--BODY-->", "</head>\n<body>", 1) + "\n</body>\n</html>\n")
    # Artifact build: the host adds the document skeleton itself.
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "site", "artifact.html")
    open(out, "w", encoding="utf-8").write(page.replace("<!--BODY-->", "", 1))
    done = sum(1 for s in skills if s["translated"])
    print(f"{len(skills)} skills, {done} translated, page {len(page) // 1024} KB")


if __name__ == "__main__":
    main()
