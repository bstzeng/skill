<!--meta
{"title":"Sentry 錯誤監控查詢","category":"雲端與 DevOps","tags":["Sentry","錯誤監控","可觀測性","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：用 Sentry CLI 以唯讀方式查詢 Sentry——列出最近的 issue、查看 issue 與事件細節、摘要正式環境錯誤，還能請 Sentry 的 AI 分析根本原因並產生修復計畫。輸出會遮蔽個資、不印原始堆疊追蹤。",
"usage":"- Codex：`$skill-installer sentry`；先 `curl https://cli.sentry.dev/install -fsS | bash` 安裝並 `sentry auth login`\n- 說「列出過去 24 小時正式環境前 10 個未解決的錯誤」「幫我分析 ABC-123 這個 issue 的原因」\n- 預設：時間 24h、環境 production、最多 20 筆；org/project 會從 DSN 自動偵測"}
-->
---
name: "sentry"
description: "當使用者要求檢視 Sentry 的 issue 或事件、摘要近期的正式環境錯誤，或透過 Sentry CLI 取得基本的 Sentry 健康資料時使用；使用 `sentry` 指令執行唯讀查詢。"
---


# Sentry（唯讀的可觀測性）

## 快速開始

- 如果尚未驗證，請使用者執行 `sentry auth login`，或把 `SENTRY_AUTH_TOKEN` 設為環境變數。
- CLI 會從 `.env` 檔中的 DSN、原始碼、設定預設值與目錄名稱自動偵測 org/project。只有在自動偵測失敗或選錯目標時，才指定 `<org>/<project>`。
- 預設值：時間範圍 `24h`、環境 `production`、上限 20。
- 以程式處理輸出時一律使用 `--json`。使用 `--json --fields` 選擇特定欄位並縮小輸出。
- 使用 `sentry schema <resource>` 快速探索 API 端點。

如果沒有安裝 CLI，給使用者這些步驟：
1. 安裝 Sentry CLI：`curl https://cli.sentry.dev/install -fsS | bash`
2. 驗證：`sentry auth login`
3. 確認驗證：`sentry auth status`
- 絕不要求使用者在對話中貼上完整的 token。請他們在本機設定，並在準備好時確認。

## 核心任務（使用 Sentry CLI）

所有查詢都使用 `sentry` CLI。它會自動處理驗證、org/project 偵測、分頁與重試。使用 `--json` 取得機器可讀的輸出。

### 1) 列出 issue（依最近排序）

{{CODE:1}}

如果自動偵測無法解析 org/project，就明確傳入：
{{CODE:2}}

### 2) 把 issue 短 ID 解析為 issue 細節

{{CODE:3}}

使用短 ID 格式（例如 `ABC-123`），而不是數字 ID。

### 3) Issue 細節

{{CODE:4}}

### 4) Issue 事件

{{CODE:5}}

### 5) 事件細節

{{CODE:6}}

### 6) AI 驅動的根本原因分析

{{CODE:7}}

### 7) AI 驅動的修復計畫

{{CODE:8}}

## 備案：任意 API 存取

對於沒有專用 CLI 指令的端點，使用 `sentry api`：
{{CODE:9}}

使用 `sentry schema` 探索可用的 API 端點：
{{CODE:10}}

## 輸入與預設值

- `org_slug`、`project_slug`：由 CLI 從 DSN、環境變數與目錄名稱自動偵測。自動偵測失敗時，以位置參數 `{your-org}/{your-project}` 覆寫。
- `time_range`：預設 `24h`（以 `--period 24h` 傳入）。
- `environment`：預設 `prod`（作為 `--query` 的一部分傳入，例如 `environment:production`）。
- `limit`：預設 20（以 `--limit` 傳入）。
- `search_query`：選填的 `--query` 參數，使用 Sentry 搜尋語法（例如 `is:unresolved`、`assigned:me`）。
- `issue_short_id`：直接搭配 `sentry issue view` 使用。

## 輸出格式規則

- Issue 清單：顯示標題、short_id、狀態、first_seen、last_seen、次數、環境、主要標籤；依最近排序。
- 事件細節：包含 culprit、時間戳記、環境、版本、url。
- 如果沒有結果，要明確說明。
- 在輸出中遮蔽個資（電子郵件、IP）。不要印出原始的堆疊追蹤。
- 絕不回顯驗證 token。

## 標準測試輸入

- Org：`{your-org}`
- Project：`{your-project}`
- Issue 短 ID：`{ABC-123}`

範例提示：「列出過去 24 小時正式環境前 10 個開啟中的 issue。」
預期：附標題、短 ID、次數、最後出現時間的排序清單。
