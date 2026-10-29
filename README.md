# AI Skill 中文典藏

收錄 50 個熱門 Agent Skills（Claude Code、Codex、Cursor 等代理通用的 `SKILL.md` 技能），每一個都附：

- **敘述**：一句話說明這個 skill 做什麼
- **用法**：安裝指令與實際怎麼觸發、怎麼用
- **Skill 原文**：從各 skill 的 GitHub 儲存庫取得的 `SKILL.md`
- **中文翻譯**：全文繁體中文翻譯（程式碼區塊保留原樣）
- **分類與標籤**：12 個分類、175 個標籤

網頁版：`docs/index.html`（可直接用瀏覽器開啟，或在 GitHub Pages 指定 `docs/` 資料夾發布）。

## 收錄來源

| 來源 | 收錄方式 |
| --- | --- |
| Skills.sh | 全站歷史安裝排行。skills.sh 本站在收集環境中無法連線，改用 [LinklyAI/best-skills](https://github.com/LinklyAI/best-skills) 每日更新的 skills.sh 鏡像資料（CC BY 4.0）。 |
| Anthropic Skills | [anthropics/skills](https://github.com/anthropics/skills) 官方範例 |
| OpenAI Plugins / Codex | [openai/skills](https://github.com/openai/skills) 官方精選 |
| Awesome Claude | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)、[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) 所推薦的儲存庫 |
| SkillsMP、Skill Store | 網站無法連線，這一版尚未收錄 |

**選取規則**：skills.sh 排行原始前 50 名有 20 個是飛書 `lark-*` 系列、還有多個重複鏡像（同一個 skill 被不同帳號重新發布），直接取前 50 會失去參考價值。因此先去除重複，同系列最多收 2–3 個，取排行前段 31 個；再補上 Anthropic 官方 8 個、OpenAI Codex 官方 6 個、Awesome Claude 推薦的 Superpowers 5 個，共 50 個。

**授權**：Anthropic 的 `docx`、`pdf`、`pptx`、`xlsx` 是專有授權，Remotion 的 skill 沒有標示授權，這 5 個只收錄中文介紹與用法，不轉載原文與翻譯。其餘皆為 MIT 或 Apache-2.0，原文保留在 `skills/<名稱>/SKILL.md`。

## 檔案結構

```
skills/<slug>/SKILL.md     英文原文（可轉載者）
translations/<slug>.md     中文翻譯 + 中繼資料（中文名、分類、標籤、敘述、用法）
data/sources.json          每個 skill 的來源儲存庫與路徑
data/skills.json           建置後的完整資料（給網頁或其他程式使用）
site/template.html         網頁模板
docs/index.html            建置後的網頁（GitHub Pages 用）
scripts/collect.py         從已 clone 的儲存庫收集原文
scripts/build.py           合併原文與翻譯，產生 data/skills.json 與網頁
```

`translations/*.md` 開頭的 `<!--meta {...} -->` 是 JSON 中繼資料；內文中的 `{{CODE:n}}` 代表原文中第 n 個程式碼區塊，建置時會自動換回原文的程式碼，所以翻譯檔不需要重複貼程式碼。

## 新增一個 skill

1. 把來源儲存庫 clone 到某個資料夾，並在挑選清單（每行 `slug 資料夾名稱 [skill 資料夾名稱]`）加上一行
2. `python3 scripts/collect.py <clone 根目錄> <挑選清單> .`：複製原文並在 `.masked/` 產生「程式碼已換成 `{{CODE:n}}`」的版本
3. 依 `.masked/<slug>.md` 翻譯，存成 `translations/<slug>.md`，開頭加上 meta 區塊
4. `python3 scripts/build.py [skills-sh.csv]`：重新產生資料與網頁；傳入 best-skills 的 `data/latest/raw/skills-sh.csv` 可同時更新安裝數

資料日期：2026-10-29。
