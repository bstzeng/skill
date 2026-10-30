<!--meta
{"title":"Notion 規格轉實作計畫","category":"需求與規劃","tags":["Notion","PRD","任務拆解","進度追蹤","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：讀取 Notion 中的 PRD 或功能規格，解析需求與模糊之處，建立實作計畫頁、在任務資料庫中建立 1–2 天大小的任務，並把規格、計畫、任務互相連結，持續更新進度。",
"usage":"- Codex：`$skill-installer notion-spec-to-implementation`；首次使用依步驟 0 加入並登入 Notion MCP\n- 說「把 Notion 上『通知中心』這份 PRD 拆成實作計畫和任務」\n- 簡單變更用快速計畫模板，多階段功能用標準計畫模板"}
-->
---
name: notion-spec-to-implementation
description: 把 Notion 規格轉成實作計畫、任務與進度追蹤；在實作 PRD/功能規格，並據此建立 Notion 計畫與任務時使用。
metadata:
  short-description: 把 Notion 規格轉成實作計畫、任務與進度追蹤
---

# 規格轉實作

把一份 Notion 規格轉成相互連結的實作計畫、任務與持續的狀態更新。

## 快速開始
1) 用 `Notion:notion-search` 找到規格，然後用 `Notion:notion-fetch` 抓取它。
2) 用 `reference/spec-parsing.md` 解析需求與模糊之處。
3) 用 `Notion:notion-create-pages` 建立計畫頁（挑選模板：快速 vs. 完整）。
4) 找到任務資料庫、確認 schema，然後用 `Notion:notion-create-pages` 建立任務。
5) 連結規格 ↔ 計畫 ↔ 任務；用 `Notion:notion-update-page` 保持狀態最新。

## 工作流程

### 0) 如果有任何 MCP 呼叫因 Notion MCP 未連線而失敗，就暫停並設定它：
1. 加入 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true`，**或**執行 `codex --enable rmcp_client`
3. 以 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 codex。你應該結束你的回答並告訴他們這一點，這樣他們再試一次時就能從步驟 1 繼續。

### 1) 找到並閱讀規格
- 先搜尋（`Notion:notion-search`）；如果有多個結果，詢問使用者要用哪一個。
- 抓取頁面（`Notion:notion-fetch`），掃描需求、驗收條件、限制與優先順序。擷取模式見 `reference/spec-parsing.md`。
- 在繼續之前，把缺口/假設記錄在一個釐清區塊中。

### 2) 選擇計畫深度
- 簡單變更 → 使用 `reference/quick-implementation-plan.md`。
- 多階段的功能/遷移 → 使用 `reference/standard-implementation-plan.md`。
- 透過 `Notion:notion-create-pages` 建立計畫，包含：概述、連結的規格、需求摘要、階段、相依/風險，以及成功標準。連回規格。

### 3) 建立任務
- 找到任務資料庫（`Notion:notion-search` → `Notion:notion-fetch` 以確認資料來源與必要屬性）。模式見 `reference/task-creation.md`。
- 把任務大小控制在 1–2 天。內容使用 `reference/task-creation-template.md`（脈絡、目標、驗收條件、相依、資源）。
- 設定屬性：標題/動作動詞、狀態、優先度、與規格 + 計畫的關聯，以及有提供時的截止日/故事點/被指派者。
- 用 `Notion:notion-create-pages` 並帶資料庫的 `data_source_id` 建立頁面。

### 4) 連結產出物
- 計畫連結到規格；任務同時連結到計畫與規格。
- 選擇性地用 `Notion:notion-update-page` 在規格中加上一個簡短的「實作」段落，指向計畫與任務。

### 5) 追蹤進度
- 使用 `reference/progress-tracking.md` 中的節奏。
- 用 `reference/progress-update-template.md` 發布更新；用 `reference/milestone-summary-template.md` 結束各階段。
- 讓計畫/任務中的檢查清單與狀態欄位保持同步；記錄阻礙與決策。

## 參考與範例
- `reference/` ——解析模式、計畫/任務模板、進度節奏（例如 `spec-parsing.md`、`standard-implementation-plan.md`、`task-creation.md`、`progress-tracking.md`）。
- `examples/` ——端到端的實作範例（例如 `ui-component.md`、`api-feature.md`、`database-migration.md`）。
