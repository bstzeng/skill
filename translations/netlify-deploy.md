<!--meta
{"title":"部署到 Netlify","category":"雲端與 DevOps","tags":["Netlify","部署","預覽環境","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：用 Netlify CLI（`npx netlify`）把網頁專案部署到 Netlify——檢查登入、偵測框架與 netlify.toml、連結既有網站或建立新網站，再部署到預覽或正式環境，並回報部署網址與日誌連結。",
"usage":"- Codex：`$skill-installer netlify-deploy`\n- 說「把這個 Vite 專案部署到 Netlify」「先給我一個預覽連結」\n- 未登入時會引導 `npx netlify login`，或改用 `NETLIFY_AUTH_TOKEN`\n- 既有網站預設先做預覽部署，你明確要求才 `--prod`"}
-->
---
name: netlify-deploy
description: 使用 Netlify CLI（`npx netlify`）把網頁專案部署到 Netlify。當使用者要求在 Netlify 上部署、託管、發布或連結網站/repo（包括預覽與正式部署）時使用。
---

# Netlify 部署技能

使用 Netlify CLI，搭配對專案設定與部署脈絡的智慧偵測，把網頁專案部署到 Netlify。

## 概述

本技能透過以下方式自動化 Netlify 部署：
- 驗證 Netlify CLI 的登入狀態
- 偵測專案設定與框架
- 連結到既有網站或建立新網站
- 部署到正式或預覽環境

## 前置條件

- **Netlify CLI**：透過 npx 安裝（不需全域安裝）
- **驗證**：有啟用中登入 session 的 Netlify 帳號
- **專案**：目前目錄中有效的網頁專案
- 當沙箱阻擋了部署的網路呼叫時，以 `sandbox_permissions=require_escalated` 重新執行。
- 部署可能需要幾分鐘。使用適當的逾時值。

## 驗證模式

本技能使用**預先驗證的 Netlify CLI** 做法：

1. 用 `npx netlify status` 檢查驗證狀態
2. 如果未驗證，引導使用者完成 `npx netlify login`
3. 如果無法建立驗證，就優雅地失敗

驗證使用以下其中之一：
- **以瀏覽器進行的 OAuth**（主要）：`netlify login` 會開啟瀏覽器進行驗證
- **API 金鑰**（替代）：設定 `NETLIFY_AUTH_TOKEN` 環境變數

## 工作流程

### 1. 驗證 Netlify CLI 的登入狀態

檢查使用者是否已登入 Netlify：

{{CODE:1}}

**預期的輸出模式**：
- ✅ 已驗證：顯示已登入使用者的電子郵件與網站連結狀態
- ❌ 未驗證：「Not logged into any site」或驗證錯誤

**如果未驗證**，引導使用者：

{{CODE:2}}

這會開啟一個瀏覽器視窗進行 OAuth 驗證。等待使用者完成登入，然後再用 `netlify status` 驗證一次。

**替代方式：API 金鑰驗證**

如果無法使用瀏覽器驗證，使用者可以設定：

{{CODE:3}}

Token 可在以下網址產生：https://app.netlify.com/user/applications#personal-access-tokens

### 2. 偵測網站連結狀態

從 `netlify status` 的輸出判斷：
- **已連結**：網站已連接到 Netlify（顯示網站名稱/URL）
- **未連結**：需要連結或建立網站

### 3. 連結到既有網站或建立新網站

**如果已連結** → 跳到步驟 4

**如果未連結**，嘗試透過 Git remote 連結：

{{CODE:4}}

**如果連結失敗**（Netlify 上不存在該網站）：

{{CODE:5}}

這會引導使用者：
1. 選擇團隊/帳號
2. 設定網站名稱
3. 設定建置選項
4. 需要時建立 netlify.toml

### 4. 驗證相依套件

部署之前，確保專案的相依套件已安裝：

{{CODE:6}}

### 5. 部署到 Netlify

依脈絡選擇部署類型：

**預覽/草稿部署**（既有網站的預設）：

{{CODE:7}}

這會建立一個有唯一 URL 的部署預覽供測試。

**正式部署**（用於新網站或明確的正式部署）：

{{CODE:8}}

這會部署到線上的正式 URL。

**部署流程**：
1. CLI 偵測建置設定（從 netlify.toml，或詢問使用者）
2. 在本機建置專案
3. 把建置好的資產上傳到 Netlify
4. 回傳部署 URL

### 6. 回報結果

部署之後，向使用者回報：
- **部署 URL**：這次部署的唯一 URL
- **網站 URL**：正式 URL（如果是正式部署）
- **部署日誌**：Netlify 後台日誌的連結
- **下一步**：建議用 `netlify open` 檢視網站或後台

## 處理 netlify.toml

如果存在 `netlify.toml` 檔，CLI 會自動使用它。如果沒有，CLI 會詢問：
- **建置指令**：例如 `npm run build`、`next build`
- **發布目錄**：例如 `dist`、`build`、`.next`

常見框架的預設值：
- **Next.js**：建置指令 `npm run build`，發布 `.next`
- **React（Vite）**：建置指令 `npm run build`，發布 `dist`
- **靜態 HTML**：沒有建置指令，發布目前目錄

本技能應盡可能從 `package.json` 偵測框架，並建議適當的設定。

## 完整工作流程範例

{{CODE:9}}

## 錯誤處理

常見問題與解法：

**「Not logged in」**
→ 執行 `npx netlify login`

**「No site linked」**
→ 執行 `npx netlify link` 或 `npx netlify init`

**「Build failed」**
→ 檢查 netlify.toml 或 CLI 提示中的建置指令與發布目錄
→ 確認相依套件已安裝
→ 檢視建置日誌中的具體錯誤

**「Publish directory not found」**
→ 確認建置指令成功執行
→ 檢查發布目錄路徑是否正確

## 疑難排解

### 提升的網路存取

如果部署因網路問題（逾時、DNS 錯誤、連線重設）而失敗，就以提升的權限重新執行部署（使用 `sandbox_permissions=require_escalated`）。當沙箱網路阻擋對外請求時，部署需要提升的網路存取。

給使用者的指引範例：

{{CODE:10}}

## 環境變數

對於機密與設定：

1. 絕不把機密 commit 進 Git
2. 在 Netlify 後台設定：Site Settings → Environment Variables
3. 在建置中透過 `process.env.VARIABLE_NAME` 存取

## 訣竅

- 先用 `netlify deploy`（不加 `--prod`）測試，再上正式環境
- 執行 `netlify open` 在 Netlify 後台檢視網站
- 執行 `netlify logs` 檢視函式日誌（如果有使用 Netlify Functions）
- 使用 `netlify dev` 在本機搭配 Netlify Functions 開發

## 參考

- Netlify CLI 文件：https://docs.netlify.com/cli/get-started/
- netlify.toml 參考：https://docs.netlify.com/configure-builds/file-based-configuration/

## 內附參考（視需要載入）

- [CLI 指令](references/cli-commands.md)
- [部署模式](references/deployment-patterns.md)
- [netlify.toml 指南](references/netlify-toml.md)
