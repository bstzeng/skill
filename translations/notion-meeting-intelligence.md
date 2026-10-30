<!--meta
{"title":"Notion 會議準備","category":"文件與辦公","tags":["Notion","會議","議程","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：從 Notion 拉取過去的筆記、規格、OKR 與決策作為脈絡，依會議類型（狀態更新、決策、規劃、回顧、一對一、腦力激盪）挑選模板，草擬議程與會前閱讀資料，並以附來源的研究補充內容。",
"usage":"- Codex：`$skill-installer notion-meeting-intelligence`；首次使用依步驟 0 加入並登入 Notion MCP\n- 說「幫我準備週四和行銷團隊的季度規劃會議議程」\n- 每個議程項目都會標上負責人、時間與預期產出；模板在 `reference/`"}
-->
---
name: notion-meeting-intelligence
description: 運用 Notion 脈絡與 Codex 研究準備會議資料；在蒐集脈絡、草擬議程/會前閱讀資料，並依與會者調整資料時使用。
metadata:
  short-description: 以 Notion 脈絡與量身打造的議程準備會議
---

# 會議情報

透過拉取 Notion 脈絡、量身調整議程/會前閱讀資料，並以 Codex 研究加以充實，來準備會議。

## 快速開始
1) 確認會議目標、與會者、日期/時間，以及需要做出的決策。
2) 蒐集脈絡：用 `Notion:notion-search` 搜尋，然後用 `Notion:notion-fetch` 抓取（先前的筆記、規格、OKR、決策）。
3) 透過 `reference/template-selection-guide.md` 挑選合適的模板（狀態、決策、規劃、回顧、一對一、腦力激盪）。
4) 用 `Notion:notion-create-pages` 在 Notion 中草擬議程/會前閱讀資料，嵌入來源連結以及負責人/時間框。
5) 以 Codex 研究（產業洞察、基準、風險）加以充實，並在計畫改變時用 `Notion:notion-update-page` 更新頁面。

## 工作流程
### 0) 如果有任何 MCP 呼叫因 Notion MCP 未連線而失敗，就暫停並設定它：
1. 加入 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true`，**或**執行 `codex --enable rmcp_client`
3. 以 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 codex。你應該結束你的回答並告訴他們這一點，這樣他們再試一次時就能從步驟 1 繼續。

### 1) 蒐集輸入
- 詢問目標、期望的成果/決策、與會者、時長、日期/時間，以及先前的資料。
- 在 Notion 中搜尋相關文件、過去的筆記、規格與待辦事項（`Notion:notion-search`），然後抓取關鍵頁面（`Notion:notion-fetch`）。
- 一開始就記錄阻礙/風險與待解問題。

### 2) 選擇格式
- 狀態/更新 → 狀態模板。
- 決策/核准 → 決策模板。
- 規劃（衝刺/專案）→ 規劃模板。
- 回顧/回饋 → 回顧模板。
- 一對一 → 一對一模板。
- 發想 → 腦力激盪模板。
- 用 `reference/template-selection-guide.md` 確認。

### 3) 建立議程/會前閱讀資料
- 從 `reference/` 中所選的模板開始，並調整各節（脈絡、目標、議程、每項的負責人/時間、決策、風險、準備事項）。
- 包含拉取到的 Notion 頁面連結，以及任何必要的會前閱讀。
- 為每個議程項目指派負責人；標出時間框與預期產出。

### 4) 以研究充實
- 在有幫助之處加入簡潔的 Codex 研究：市場/產業事實、基準、風險、最佳實踐。
- 主張要附來源連結；把事實與意見分開。

### 5) 定稿並分享
- 加入後續步驟與追蹤事項的負責人。
- 如果產生任務，就在相關的 Notion 資料庫中建立/連結任務。
- 細節改變時透過 `Notion:notion-update-page` 更新頁面；如果多次編輯，保留一份簡短的變更紀錄。

## 參考與範例
- `reference/` ——模板選擇器與會議模板（例如 `template-selection-guide.md`、`status-update-template.md`、`decision-meeting-template.md`、`sprint-planning-template.md`、`one-on-one-template.md`、`retrospective-template.md`、`brainstorming-template.md`）。
- `examples/` ——端到端的會議準備（例如 `executive-review.md`、`project-decision.md`、`sprint-planning.md`、`customer-meeting.md`）。
