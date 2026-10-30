<!--meta
{"title":"Notion 知識擷取","category":"文件與辦公","tags":["Notion","知識管理","Wiki","決策紀錄","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：把對話與筆記轉成結構化、可互相連結的 Notion 頁面——決策紀錄、操作說明、FAQ、學習筆記或 Wiki 條目——依資料庫 schema 填好摘要、脈絡、來源連結、標籤與負責人，並連回相關頁面。",
"usage":"- Codex：`$skill-installer notion-knowledge-capture`；首次使用依步驟 0 加入並登入 Notion MCP\n- 說「把剛剛關於快取策略的討論整理成團隊 Wiki 的決策紀錄」「把這段對話變成 FAQ」\n- 資料庫 schema 與模板在 `reference/`，範例在 `examples/`"}
-->
---
name: notion-knowledge-capture
description: 把對話與決策擷取成結構化的 Notion 頁面；在把聊天/筆記轉成 Wiki 條目、操作說明、決策或 FAQ 並適當連結時使用。
metadata:
  short-description: 把對話擷取成結構化的 Notion 頁面
---

# 知識擷取

把對話與筆記轉成結構化、可連結的 Notion 頁面，方便重複使用。

## 快速開始
1) 釐清要擷取什麼（決策、操作說明、FAQ、學習、文件）以及目標讀者。
2) 在 `reference/` 中找出合適的資料庫/模板（團隊 Wiki、操作說明、FAQ、決策紀錄、學習、文件）。
3) 用 `Notion:notion-search` → `Notion:notion-fetch` 從 Notion 拉取任何先前的脈絡（要更新/連結的既有頁面）。
4) 用 `Notion:notion-create-pages` 依資料庫的 schema 草擬頁面；包含摘要、脈絡、來源連結與標籤/負責人。
5) 從中心頁面與相關紀錄連結過來；隨著來源演變，用 `Notion:notion-update-page` 更新狀態/負責人。

## 工作流程
### 0) 如果有任何 MCP 呼叫因 Notion MCP 未連線而失敗，就暫停並設定它：
1. 加入 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true`，**或**執行 `codex --enable rmcp_client`
3. 以 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 codex。你應該結束你的回答並告訴他們這一點，這樣他們再試一次時就能從步驟 1 繼續。

### 1) 定義要擷取的內容
- 詢問目的、讀者、時效性，以及這是新內容還是更新。
- 確定內容類型：決策、操作說明、FAQ、概念/Wiki 條目、學習/筆記、文件頁面。

### 2) 找出目的地
- 用 `reference/*-database.md` 指南挑選正確的資料庫；確認必要的屬性（標題、標籤、負責人、狀態、日期、關聯）。
- 如果有多個候選資料庫，詢問使用者要用哪一個；否則就在主要的 Wiki/文件資料庫中建立。

### 3) 擷取並結構化
- 從對話中擷取事實、決策、行動與理由。
- 對於決策，記錄替代方案、理由與結果。
- 對於操作說明/文件，記錄步驟、前置條件、素材/程式碼的連結以及邊界情況。
- 對於 FAQ，寫成問答形式，附上簡潔的答案以及更深入文件的連結。

### 4) 在 Notion 中建立/更新
- 用 `Notion:notion-create-pages` 並帶正確的 `data_source_id`；設定屬性（標題、標籤、負責人、狀態、日期、關聯）。
- 使用 `reference/` 中的模板組織內容（章節標題、檢查清單）。
- 如果是更新既有頁面，先抓取，再透過 `Notion:notion-update-page` 編輯。

### 5) 連結並呈現
- 為中心頁面、相關的規格/文件與團隊加入關聯/反向連結。
- 為未來的讀者加上簡短的摘要/變更紀錄。
- 如果有後續任務，就在相關的資料庫中建立任務並連結。

## 參考與範例
- `reference/` ——資料庫 schema 與模板（例如 `team-wiki-database.md`、`how-to-guide-database.md`、`faq-database.md`、`decision-log-database.md`、`documentation-database.md`、`learning-database.md`、`database-best-practices.md`）。
- `examples/` ——實際的擷取模式（例如 `decision-capture.md`、`how-to-guide.md`、`conversation-to-faq.md`）。
