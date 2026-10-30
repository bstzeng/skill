<!--meta
{"title":"委派給 Google Jules","category":"AI 整合與開發工具","tags":["Jules","Google","非同步代理","GitHub","PR"],
"summary":"把程式工作委派給 Google 的 Jules AI 代理在 GitHub repo 上非同步執行：修 bug、補文件、加功能、寫測試、重構、審查 PR，完成後可自動開 PR 或把變更套用到新分支。支援互動式的 Jules CLI 與無介面的 API 金鑰兩種方式，會自動偵測 repo、注入目前的脈絡，並提供常用任務的提示範本與輪詢等待完成的指令。",
"usage":"- 互動式：安裝 Jules CLI 並 `jules login`；無介面：設定 `JULES_API_KEY`（到 jules.google.com/settings 取得）\n- 說「叫 Jules 修這個 bug」「委派給 Jules 補測試」「看一下 Jules 的工作階段」「拉回 Jules 的結果」\n- 只支援 GitHub；repo 需先在 jules.google.com 連結\n- 在 repo 根目錄放 `AGENTS.md` 可改善 Jules 的結果"}
-->
---
name: jules
description: "把程式工作委派給 Google Jules AI 代理以非同步執行。當使用者說：「叫 Jules 修」「委派給 Jules」「送給 Jules」「請 Jules」「檢查 Jules 工作階段」「拉回 Jules 的結果」「jules 加測試」「jules 加文件」「jules 審查 pr」時使用。處理：修 bug、文件、功能、測試、重構、程式碼審查。適用於 GitHub repo，會建立 PR。"
license: Apache-2.0
metadata:
  author: sanjay3290
  version: "1.0"
---

# 委派任務給 Jules

把程式工作委派給 Google 的 Jules AI 代理，在 GitHub repository 上執行。

## 環境變數

| 變數 | 必要性 | 說明 |
|----------|----------|-------------|
| `JULES_API_KEY` | API 認證時需要 | 從 [jules.google.com/settings](https://jules.google.com/settings) 取得的 API 金鑰 |

## 設定（第一次執行指令前）

有兩種認證途徑。互動式使用時用 **途徑 1**，無介面／代理使用時用 **途徑 2**。

### 途徑 1：CLI（互動式）

#### 1. 安裝 CLI
{{CODE:1}}

#### 2. 檢查認證
{{CODE:2}}
如果失敗 → 告訴使用者執行 `jules login`（無介面環境用 `--no-launch-browser`）

### 途徑 2：API 金鑰（無介面／代理使用）

#### 1. 取得 API 金鑰
從 [jules.google.com/settings](https://jules.google.com/settings) 取得金鑰（每個帳號最多 3 把）。

#### 2. 設定環境變數
{{CODE:3}}

#### 3. 確認
{{CODE:4}}

### 共同設定（兩種途徑）

#### 自動偵測 Repo
{{CODE:5}}
如果不是 GitHub 或不在 git repo 中 → 請使用者提供 `--repo owner/repo`

#### 確認 Repo 已連結
檢查 repo 是否在 `jules remote list --repo` 中。如果沒有 → 引導到 https://jules.google.com

## 指令（CLI）

### 建立任務
{{CODE:6}}

### 監控
{{CODE:7}}

### 取回結果
{{CODE:8}}

### 最新工作階段的捷徑
{{CODE:9}}

## 指令（API）

### 建立任務
{{CODE:10}}

主要欄位：
- `prompt` —— 任務描述（必要）
- `sourceContext.repository` —— GitHub 的 `owner/repo`（必要）
- `sourceContext.branchName` —— 目標分支（預設：repo 的預設分支）
- `automationMode` —— `"AUTO_CREATE_PR"` 會自動建立 PR，省略則為手動
- `title` —— 工作階段的顯示名稱
- `requirePlanApproval` —— `true` 會在執行前暫停，等待審閱計畫

### 列出工作階段
{{CODE:11}}

### 取得工作階段狀態
{{CODE:12}}

### 輪詢直到完成（API）
{{CODE:13}}

## 智慧注入脈絡

用目前的脈絡豐富提示，以得到更好的結果：

{{CODE:14}}

**建立任務時使用（CLI）：**
{{CODE:15}}

**建立任務時使用（API）：**
{{CODE:16}}

## 提示範本

常見任務的快速指令：

### 加入測試
{{CODE:17}}

### 加入文件
{{CODE:18}}

### 修正 Lint 錯誤
{{CODE:19}}

### 審查 PR
{{CODE:20}}

## Git 整合（套用 + 提交）

Jules 完成後，把變更套用到新的分支：

{{CODE:21}}

## 輪詢直到完成（CLI）

等待工作階段結束：

{{CODE:22}}

## AGENTS.md 範本

在 repo 根目錄建立，以改善 Jules 的結果：

{{CODE:23}}

## 工作階段狀態

| 狀態 | 動作 |
|--------|--------|
| Planning／In Progress | 等待 |
| Awaiting User F | 在網頁介面回應 |
| Completed | 拉回結果 |
| Failed | 查看網頁介面 |

## 注意事項

- **CLI 不能回覆** → 用網頁介面回答 Jules 的問題
- **CLI 不能取消** → 用網頁介面取消
- **只支援 GitHub** → 不支援 GitLab／Bitbucket
- **AGENTS.md** → Jules 會從 repo 根目錄讀取作為脈絡
- **API vs CLI** → 無介面／代理自動化使用 API（`JULES_API_KEY`）；互動式工作階段使用 CLI
