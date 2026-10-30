<!--meta
{"title":"Linear 專案管理","category":"雲端與 DevOps","tags":["Linear","專案管理","Issue","MCP","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：透過 Linear MCP 伺服器管理 Linear 的 issue、專案與團隊流程——讀取、建立、更新工單，並提供衝刺規劃、Bug 分類、文件稽核、工作量平衡、發版規劃、跨專案相依等實用流程。",
"usage":"- Codex：`$skill-installer linear`；首次使用依步驟 0 執行 `codex mcp add linear --url https://mcp.linear.app/mcp` 並 `codex mcp login linear`\n- 說「列出這週 Platform 團隊的高優先 bug」「依優先度建立下個 sprint」「誰的工作量太滿？」\n- 會先讀取建立脈絡，再批次建立或更新，大量操作前會先說明分組方式"}
-->
---
name: linear
description: 在 Linear 中管理 issue、專案與團隊工作流程。當使用者想在 Linear 中讀取、建立或更新工單時使用。
metadata:
  short-description: 在 Codex 中管理 Linear issue
---

# Linear

## 概述

本技能提供在 Linear 中管理 issue、專案與團隊工作流程的結構化工作流程。它確保與 Linear MCP 伺服器的整合一致，該伺服器提供以自然語言進行的專案管理，涵蓋 issue、專案、文件與團隊協作。

## 前置條件
- Linear MCP 伺服器必須已連線，且可透過 OAuth 存取
- 確認可以存取相關的 Linear 工作區、團隊與專案

## 必要工作流程

**依序遵循這些步驟。不要略過步驟。**

### 步驟 0：設定 Linear MCP（如果尚未設定）

如果有任何 MCP 呼叫因 Linear MCP 未連線而失敗，就暫停並設定它：

1. 加入 Linear MCP：
   - `codex mcp add linear --url https://mcp.linear.app/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features] rmcp_client = true`，**或**執行 `codex --enable rmcp_client`
3. 以 OAuth 登入：
   - `codex mcp login linear`

成功登入後，使用者必須重新啟動 codex。你應該結束你的回答並告訴他們這一點，這樣他們再試一次時就能從步驟 1 繼續。

**Windows/WSL 注意事項：** 如果你在 Windows 上看到連線錯誤，試著把 Linear MCP 設定為透過 WSL 執行：
{{CODE:1}}

### 步驟 1
釐清使用者的目標與範圍（例如 issue 分類、衝刺規劃、文件稽核、工作量平衡）。視需要確認團隊/專案、優先度、標籤、週期與截止日期。

### 步驟 2
選擇適當的工作流程（見下方的實用工作流程），並找出你會需要的 Linear MCP 工具。在呼叫工具之前，確認必要的識別碼（issue ID、專案 ID、團隊代碼）。

### 步驟 3
以合乎邏輯的批次執行 Linear MCP 工具呼叫：
- 先讀取（list/get/search）以建立脈絡。
- 接著建立或更新（issue、專案、標籤、留言），並填入所有必要欄位。
- 對於大量操作，在套用變更之前先說明分組的邏輯。

### 步驟 4
摘要結果，指出剩下的缺口或阻礙，並提議下一步行動（額外的 issue、標籤變更、指派或後續留言）。

## 可用工具

Issue 管理：`list_issues`、`get_issue`、`create_issue`、`update_issue`、`list_my_issues`、`list_issue_statuses`、`list_issue_labels`、`create_issue_label`

專案與團隊：`list_projects`、`get_project`、`create_project`、`update_project`、`list_teams`、`get_team`、`list_users`

文件與協作：`list_documents`、`get_document`、`search_documentation`、`list_comments`、`create_comment`、`list_cycles`

## 實用工作流程

- 衝刺規劃：檢視目標團隊的開啟中 issue，依優先度挑出最重要的項目，並建立一個新的週期（例如「Q1 效能衝刺」）並指派。
- Bug 分類：列出嚴重/高優先度的 bug，依使用者影響排序，並把最前面的項目移到「In Progress」。
- 文件稽核：搜尋文件（例如 API 驗證），然後為缺口或過時的章節開立標上「documentation」的 issue，並附詳細的修正。
- 團隊工作量平衡：依被指派者分組開啟中的 issue，標出負載過高的人，並建議或套用重新分配。
- 發版規劃：建立一個專案（例如「v2.0 Release」）並設定里程碑（功能凍結、beta、文件、上線），然後產生附估計值的 issue。
- 跨專案相依：找出所有「blocked」的 issue，辨識阻擋者，並在缺少時建立連結的 issue。
- 自動狀態更新：找出你更新已過時的 issue，並依目前狀態/阻礙加上狀態留言。
- 智慧標籤：分析未加標籤的 issue，建議/套用標籤，並建立缺少的標籤類別。
- 衝刺回顧：為最近完成的週期產生報告，記錄完成與延後的工作，並為發現的模式開立討論 issue。

## 發揮最高生產力的訣竅

- 相關的變更以批次處理；對於反覆出現的 issue 結構，考慮使用智慧模板。
- 盡可能使用自然的查詢（「告訴我 John 這週在做什麼」）。
- 善用脈絡：在新請求中參照先前的 issue。
- 把大型更新拆成較小的批次，以避免速率限制；頻繁列出時快取或重用篩選條件。

## 疑難排解

- 驗證：清除瀏覽器 cookie、重新執行 OAuth、確認工作區權限、確保已啟用 API 存取。
- 工具呼叫錯誤：確認模型支援多次工具呼叫、提供所有必要欄位，並拆分複雜的請求。
- 缺少資料：更新 token、確認工作區存取權、檢查是否有已封存的專案，並確認選對了團隊。
- 效能：記得 Linear API 的速率限制；以批次處理大量操作、使用具體的篩選條件，或快取頻繁的查詢。
