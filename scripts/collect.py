"""Copy each picked SKILL.md into skills/<slug>/ and write a code-masked copy for translation.

Usage: python3 scripts/collect.py <clones-dir> data/pick.txt <repo-root>
Each pick line is `slug owner/repo [skill-folder]`; the repo must be cloned as <clones-dir>/owner_repo.
"""
import json, os, re, shutil, sys

SRC, PICK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
# Skills whose license does not allow redistribution: keep only a link + our own summary.
NO_REDIST = {"docx", "pdf", "pptx", "xlsx", "remotion-best-practices"}
FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)

def find(repo, name):
    hits = []
    for root, dirs, files in os.walk(os.path.join(SRC, repo)):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        if "SKILL.md" in files and os.path.basename(root) == name:
            hits.append(os.path.join(root, "SKILL.md"))
    return min(hits, key=len)

index = []
for line in open(PICK):
    parts = line.split()
    if not parts:
        continue
    slug, repo = parts[0], parts[1]
    repo_dir = repo.replace("/", "_")
    path = find(repo_dir, parts[2] if len(parts) > 2 else slug)
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, os.path.join(SRC, repo_dir))
    redist = slug not in NO_REDIST
    d = os.path.join(OUT, "skills", slug)
    os.makedirs(d, exist_ok=True)
    if redist:
        shutil.copy(path, os.path.join(d, "SKILL.md"))
    n = [0]
    def mask(m):
        n[0] += 1
        return "{{CODE:%d}}" % n[0]
    masked = FENCE.sub(mask, text)
    os.makedirs(os.path.join(OUT, ".masked"), exist_ok=True)
    open(os.path.join(OUT, ".masked", slug + ".md"), "w").write(masked)
    index.append({"slug": slug, "repo": repo, "path": rel,
                  "redistributable": redist, "code_blocks": n[0], "chars": len(masked)})
json.dump(index, open(os.path.join(OUT, "data", "sources.json"), "w"), indent=1, ensure_ascii=False)
for i in index:
    print(i["slug"], i["chars"], i["code_blocks"], i["redistributable"])
print(sum(i["chars"] for i in index))
