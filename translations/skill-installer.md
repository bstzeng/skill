<!--meta
{"title":"Codex 技能安裝器","category":"技能管理","tags":["Codex","技能安裝","openai/skills","OpenAI Codex"],
"summary":"OpenAI Codex 官方系統技能（預先安裝）：列出可安裝的技能，從 openai/skills 精選清單或任何 GitHub repo 路徑（含私有 repo）安裝技能到 `$CODEX_HOME/skills`。安裝後在下一輪即可使用。",
"usage":"- Codex 內建，不需安裝；說「有哪些技能可以裝？」「幫我裝 gh-fix-ci」「從這個 GitHub 路徑安裝技能」\n- 在 Codex 中直接輸入 `$skill-installer <技能名稱>`\n- 實驗性技能：`scripts/list-skills.py --path skills/.experimental`"}
-->
---
name: skill-installer
description: 從精選清單或 GitHub repo 路徑，把 Codex 技能安裝到 $CODEX_HOME/skills。當使用者要求列出可安裝的技能、安裝一個精選技能，或從其他 repo（包括私有 repo）安裝技能時使用。
metadata:
  short-description: 從 openai/skills 或其他 repo 安裝精選技能
---

# 技能安裝器

協助安裝技能。預設來源是 https://github.com/openai/skills/tree/main/skills/.curated，但使用者也可以提供其他位置。

依任務使用輔助腳本：
- 當使用者詢問有哪些可用的技能，或使用本技能卻沒有指定要做什麼時，列出技能。預設列出 `.curated`，但當他們問到實驗性技能時，可以傳入 `--path skills/.experimental`。
- 當使用者提供技能名稱時，從精選清單安裝。
- 當使用者提供 GitHub repo/路徑（包括私有 repo）時，從其他 repo 安裝。

用輔助腳本安裝技能。

## 溝通

列出技能時，依使用者請求的脈絡，大致輸出如下。如果他們問的是實驗性技能，就從 `.experimental` 而不是 `.curated` 列出，並據此標示來源：
"""
來自 {repo} 的技能：
1. skill-1
2. skill-2（已安裝）
3. ...
你想安裝哪些？
"""

安裝技能後，告訴使用者它會在下一輪可用。

## 腳本

這些腳本全都會使用網路，所以在沙箱中執行時，要請求提升權限。

- `scripts/list-skills.py`（印出技能清單並標註已安裝者）
- `scripts/list-skills.py --format json`
- 範例（實驗性清單）：`scripts/list-skills.py --path skills/.experimental`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`
- 範例（實驗性技能）：`scripts/install-skill-from-github.py --repo openai/skills --path skills/.experimental/<skill-name>`

## 行為與選項

- 公開的 GitHub repo 預設直接下載。
- 如果下載因驗證/權限錯誤而失敗，就退而使用 git sparse checkout。
- 如果目標技能目錄已經存在，就中止。
- 安裝到 `$CODEX_HOME/skills/<skill-name>`（預設為 `~/.codex/skills`）。
- 多個 `--path` 值會在一次執行中安裝多個技能，除非提供了 `--name`，否則每個都以路徑的最後一段命名。
- 選項：`--ref <ref>`（預設 `main`）、`--dest <path>`、`--method auto|download|git`。

## 注意事項

- 精選清單透過 GitHub API 從 `https://github.com/openai/skills/tree/main/skills/.curated` 抓取。如果無法取得，就說明錯誤並結束。
- 私有 GitHub repo 可以透過既有的 git 憑證，或選用的 `GITHUB_TOKEN`/`GH_TOKEN` 下載。
- Git 備案先嘗試 HTTPS，再嘗試 SSH。
- https://github.com/openai/skills/tree/main/skills/.system 中的技能是預先安裝的，所以不需要協助使用者安裝它們。如果他們問起，就說明這一點。如果他們堅持，你可以下載並覆寫。
- 已安裝的標註來自 `$CODEX_HOME/skills`。
