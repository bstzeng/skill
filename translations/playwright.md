<!--meta
{"title":"Playwright 瀏覽器操控","category":"瀏覽器與測試自動化","tags":["Playwright","瀏覽器自動化","截圖","爬蟲","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：透過 `playwright-cli` 從終端機操控真實瀏覽器——導航、填表、快照、截圖、擷取資料、用 trace 除錯 UI 流程。以 CLI 操作為主，而不是寫測試檔。",
"usage":"- Codex：`$skill-installer playwright`\n- 需要 Node.js / npx；內附包裝腳本，不必全域安裝 playwright-cli\n- 說「打開這個網站填好表單並截圖」\n- 核心循環：open → snapshot 取得元素參照（如 e12）→ 用參照互動 → 頁面變動後重新 snapshot"}
-->
---
name: "playwright"
description: "當任務需要從終端機透過 `playwright-cli` 或內附的包裝腳本自動化真實瀏覽器時使用（導航、填寫表單、快照、截圖、資料擷取、UI 流程除錯）。"
---


# Playwright CLI 技能

使用 `playwright-cli` 從終端機驅動真實瀏覽器。優先使用內附的包裝腳本，這樣即使 CLI 沒有全域安裝也能運作。
把本技能當作以 CLI 為主的自動化。除非使用者明確要求測試檔，否則不要轉向 `@playwright/test`。

## 前置檢查（必要）

在提出指令之前，先檢查 `npx` 是否可用（包裝腳本依賴它）：

{{CODE:1}}

如果不可用，就暫停並請使用者安裝 Node.js/npm（會提供 `npx`）。逐字提供以下步驟：

{{CODE:2}}

一旦有了 `npx`，就使用包裝腳本繼續。全域安裝 `playwright-cli` 是選擇性的。

## 技能路徑（設定一次）

{{CODE:3}}

使用者範圍的技能安裝在 `$CODEX_HOME/skills` 之下（預設：`~/.codex/skills`）。

## 快速開始

使用包裝腳本：

{{CODE:4}}

如果使用者偏好全域安裝，這樣也可以：

{{CODE:5}}

## 核心流程

1. 開啟頁面。
2. 取得快照以獲得穩定的元素參照。
3. 使用最新快照中的參照進行互動。
4. 導航或 DOM 大幅變動後重新快照。
5. 有用時擷取產出物（截圖、pdf、trace）。

最小循環：

{{CODE:6}}

## 何時重新快照

在以下情況後重新快照：

- 導航
- 點擊會大幅改變 UI 的元素
- 開啟/關閉對話框或選單
- 切換分頁

參照可能會過期。當指令因為找不到參照而失敗時，重新快照。

## 建議模式

### 填寫並送出表單

{{CODE:7}}

### 用 trace 除錯 UI 流程

{{CODE:8}}

### 多分頁作業

{{CODE:9}}

## 包裝腳本

包裝腳本使用 `npx --package @playwright/cli playwright-cli`，讓 CLI 不需全域安裝也能執行：

{{CODE:10}}

除非 repo 已經統一採用全域安裝，否則優先使用包裝腳本。

## 參考資料

只開啟你需要的：

- CLI 指令參考：`references/cli.md`
- 實用流程與疑難排解：`references/workflows.md`

## 防護規則

- 在引用像 `e12` 這樣的元素 id 之前，一律先快照。
- 參照似乎過期時重新快照。
- 除非必要，優先使用明確的指令，而非 `eval` 與 `run-code`。
- 沒有新的快照時，使用像 `eX` 這樣的占位參照並說明原因；不要用 `run-code` 繞過參照。
- 視覺檢查有幫助時使用 `--headed`。
- 在這個 repo 中擷取產出物時，使用 `output/playwright/`，避免新增頂層的產出物資料夾。
- 預設使用 CLI 指令與流程，而非 Playwright 測試規格。
