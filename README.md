# AI Skill 中文典藏

從 5 個 Agent Skills 網站各自收錄熱門清單（Claude Code、Codex、Cursor 等代理通用的 `SKILL.md` 技能），共 219 筆排名、206 個不重複的技能。每一個都附：

- **敘述**：一句話說明這個 skill 做什麼
- **用法**：安裝指令與實際怎麼觸發、怎麼用
- **Skill 原文**：從各 skill 的 GitHub 儲存庫取得的 `SKILL.md`
- **中文翻譯**：全文繁體中文翻譯（程式碼區塊保留原樣）
- **分類與標籤**：12 個分類，以及每個技能 3–5 個標籤

網頁版：<https://bstzeng.github.io/skill/>（原始檔 `docs/index.html`，可直接用瀏覽器開啟）。網頁上方可切換各網站的排行，也可依分類、標籤或關鍵字搜尋全部技能。

## 收錄來源

| 網站 | 筆數 | 收錄方式 |
| --- | --- | --- |
| Skills.sh | 50 | 全站歷史安裝排行前 50 名 |
| Skill Store（skillstore.io） | 50 | 「Recommended」品質分數排序前 50 名；5 筆的來源儲存庫已移除，標示為無法取得 |
| Anthropic Skills | 19 | [anthropics/skills](https://github.com/anthropics/skills) 官方技能全部收錄（官方只有 19 個） |
| OpenAI Plugins / Codex | 50 | [openai/skills](https://github.com/openai/skills) 官方精選與外掛中的技能 |
| Awesome Claude | 50 | [travisvn](https://github.com/travisvn/awesome-claude-skills)、[ComposioHQ](https://github.com/ComposioHQ/awesome-claude-skills) 等 awesome 清單推薦的技能；4 筆已失效 |
| SkillsMP | — | 網站有機器人驗證，無法自動收集，這一版略過 |

**重複的技能**：同一個技能出現在多個網站時，每個網站的排行各列一次，但共用同一份翻譯；技能頁面會顯示它在各網站的名次。

**授權**：可轉載授權（MIT、Apache-2.0、BSD、MPL、CC、GPL 等）的技能收錄英文原文與全文翻譯。未標示授權、All Rights Reserved、Anthropic 專有授權（`docx`、`pdf`、`pptx`、`xlsx` 等）或 Figma 開發者條款的 31 個技能，只收錄中文介紹與用法，原文請點來源連結閱讀。

**原文為中文的技能**：飛書 `lark-*` 系列等原文是簡體中文的技能，以 OpenCC（s2twp）轉為繁體；原文為西班牙文等其他語言的則直接翻譯成中文。

## 檔案結構

```
data/sources.json          每個不重複技能的來源儲存庫、路徑、版本與授權
data/lists.json            各網站的排行（名次、連結、安裝數或分數）
data/skills.json           建置後的完整資料（給網頁或其他程式使用）
translations/<slug>.md     中文翻譯 + 中繼資料（中文名、分類、標籤、敘述、用法）
site/template.html         網頁模板
docs/index.html            建置後的網頁（GitHub Pages 用）
scripts/lists/             收集各網站排行的腳本（make → resolve → manifest → license → finalize）
scripts/collect.py         從已 clone 的儲存庫收集原文
scripts/opencc_translate.py  把簡體中文原文轉成繁體翻譯檔
scripts/check.py           檢查翻譯檔的中繼資料與程式碼佔位符是否完整
scripts/build.py           合併原文、翻譯與排行，產生 data/skills.json 與網頁
```

`translations/*.md` 開頭的 `<!--meta {...} -->` 是 JSON 中繼資料；內文中的 `{{CODE:n}}` 代表原文中第 n 個程式碼區塊，建置時會自動換回原文的程式碼，所以翻譯檔不需要重複貼程式碼。只提供中文介紹的技能，翻譯檔只有中繼資料。

## 更新或新增技能

1. 用 `scripts/lists/` 重新抓取排行，或直接在 `data/lists.json` 與 `data/sources.json` 加入條目
2. `python3 scripts/collect.py`：下載原文，並在 `.masked/` 產生「程式碼已換成 `{{CODE:n}}`」的版本
3. 依 `.masked/<slug>.md` 翻譯，存成 `translations/<slug>.md`，開頭加上 meta 區塊
4. `python3 scripts/check.py` 確認沒有問題，再執行 `python3 scripts/build.py` 重新產生資料與網頁

資料日期：2026-10-30。
