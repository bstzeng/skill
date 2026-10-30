<!--meta
{"title":"Notion 研究彙整","category":"文件與辦公","tags":["Notion","研究","報告","引用","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：跨多個 Notion 頁面蒐集資料，依需求選擇格式（快速簡報、研究摘要、方案比較、完整報告），綜合整理成附引用與來源連結的結構化文件，並標出缺口、矛盾與待解問題。",
"usage":"- Codex：`$skill-installer notion-research-documentation`；首次使用依步驟 0 加入並登入 Notion MCP\n- 說「整理我們 Notion 裡所有關於競品的資料，做成一份比較報告」\n- 格式選擇指南在 `reference/format-selection-guide.md`，引用規則在 `reference/citations.md`"}
-->
---
name: notion-research-documentation
description: 跨 Notion 進行研究並綜合整理成結構化的文件；在從多個 Notion 來源蒐集資訊，以產出附引用的簡報、比較或報告時使用。
metadata:
  short-description: 研究 Notion 內容並產出簡報/報告
---

# 研究與文件

拉取相關的 Notion 頁面、綜合發現，並發布清楚的簡報或報告（附引用與來源連結）。

## 快速開始
1) 用 `Notion:notion-search` 以針對性的查詢找出來源；與使用者確認範圍。
2) 透過 `Notion:notion-fetch` 抓取頁面；記下關鍵段落並擷取引用（`reference/citations.md`）。
3) 用 `reference/format-selection-guide.md` 選擇輸出格式（簡報、摘要、比較、完整報告）。
4) 用 `Notion:notion-create-pages` 以相符的模板（快速、摘要、比較、完整）在 Notion 中草擬。
5) 連結來源並加入參考/引用一節；有新資訊時用 `Notion:notion-update-page` 更新。

## 工作流程
### 0) 如果有任何 MCP 呼叫因 Notion MCP 未連線而失敗，就暫停並設定它：
1. 加入 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true`，**或**執行 `codex --enable rmcp_client`
3. 以 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 codex。你應該結束你的回答並告訴他們這一點，這樣他們再試一次時就能從步驟 1 繼續。

### 1) 蒐集來源
- 先搜尋（`Notion:notion-search`）；精煉查詢，如果出現多個結果就請使用者確認。
- 抓取相關頁面（`Notion:notion-fetch`），快速瀏覽事實、指標、主張、限制與日期。
- 追蹤每個來源的 URL/ID 以便之後引用；關鍵事實優先使用直接引述。

### 2) 選擇格式
- 快速報告 → 快速簡報。
- 單一主題深入 → 研究摘要。
- 方案取捨 → 比較。
- 深入探討 / 給主管看的 → 完整報告。
- 何時選哪一種，見 `reference/format-selection-guide.md`。

### 3) 綜合整理
- 寫之前先列大綱；依主題/問題分組發現。
- 以來源 ID 記錄證據；標出缺口或矛盾。
- 隨時記著使用者的目標（決策、摘要、計畫、建議）。

### 4) 建立文件
- 從 `reference/` 挑選相符的模板（簡報、摘要、比較、完整）並調整。
- 用 `Notion:notion-create-pages` 建立頁面；包含標題、摘要、關鍵發現、佐證，以及相關時的建議/下一步。
- 加入行內引用與參考一節；連回來源頁面。

### 5) 定稿與交接
- 加入重點、風險與待解問題。
- 如果使用者需要後續行動，就在頁面中建立任務或檢查清單；適用時連結任何任務資料庫的條目。
- 更新時，用 `Notion:notion-update-page` 分享一份簡短的變更紀錄或狀態。

## 參考與範例
- `reference/` ——搜尋策略、格式選擇、模板與引用規則（例如 `advanced-search.md`、`format-selection-guide.md`、`research-summary-template.md`、`comparison-template.md`、`citations.md`）。
- `examples/` ——端到端的實作範例（例如 `competitor-analysis.md`、`technical-investigation.md`、`market-research.md`、`trip-planning.md`）。
