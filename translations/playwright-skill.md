<!--meta
{"title":"Playwright 瀏覽器自動化","category":"瀏覽器與測試自動化","tags":["Playwright","瀏覽器自動化","網站測試","截圖"],
"summary":"用 Playwright 完成各種瀏覽器自動化：自動偵測本機開發伺服器、撰寫可重用的測試腳本，支援截圖、響應式檢查、UX 驗證、登入流程、連結檢查與任意的瀏覽器操作。預設開啟可見的瀏覽器、偏好以角色與標籤為主的定位器與自動等待斷言，並可連接既有的 Chrome 工作階段；附輔助函式與環境變數設定。",
"usage":"- 需要 Node.js 20+ 與 npm；第一次使用先在技能目錄執行安裝（會下載 Playwright 與 Chromium）\n- 說「幫我測試 localhost 的登入流程」「檢查這個網站在手機、平板、桌機的排版」「截一張首頁的圖」\n- 執行腳本：`node \"$SKILL_DIR/run.js\" <script.js>`\n- 想保留腳本或截圖可設定 `PW_SCRIPT_DIR`、`PW_ARTIFACT_DIR`"}
-->
---
name: playwright-skill
description: 以 Playwright 完成瀏覽器自動化。自動偵測開發伺服器、撰寫可重用的測試腳本，並支援截圖、響應式檢查、UX 驗證、登入流程、連結檢查與任意的瀏覽器自動化。當使用者想測試網站、自動化瀏覽器互動、驗證網頁功能或進行以瀏覽器為基礎的測試時使用。
license: MIT
compatibility: 需要 Node.js 20+、npm，以及第一次設定時用來安裝 Playwright 與 Chromium 的網路存取。
metadata:
  author: lackeyjb
  version: "5.0.0"
allowed-tools: Bash(node:*) Bash(npm:*) Read Write
---

# Playwright 瀏覽器自動化

針對使用者的請求，撰寫並執行聚焦的 Playwright 腳本。偏好使用本技能的執行器與輔助函式，但需要時使用完整的 Playwright API。

## 解析路徑

本技能可能安裝在不同的位置，所以先解析它的目錄。把 `SKILL_DIR` 設為包含這份 SKILL.md 的目錄，然後照原樣執行下方的指令：

{{CODE:1}}

如果指令之間不會保留 shell 狀態，就在每個指令中把 `$SKILL_DIR` 與 `$TMP_DIR` 換成實際的路徑。

常見的安裝路徑：

- 外掛系統：`~/.claude/plugins/marketplaces/playwright-skill/skills/playwright-skill`
- 手動全域安裝：`~/.claude/skills/playwright-skill`
- 專案專屬：`<project>/.claude/skills/playwright-skill`

## 工作流程

1. 處理 localhost 時，在寫 URL 之前先偵測執行中的伺服器：

   ```bash
   node -e "require('$SKILL_DIR/lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
   ```

   只有一個結果時自動使用它。有多個結果時詢問要用哪個 URL。一個都沒有時，請使用者提供 URL，或提議啟動伺服器。
2. 除非使用者要求存在專案中，否則把可重用的腳本寫到 `$TMP_DIR/playwright-test-*.js`。使用 `PW_SCRIPT_DIR` 保留腳本。
3. 預設使用可見的瀏覽器。只有在被要求或環境沒有顯示器時才使用 `headless: true`。
4. 把目標 URL 放在常數或環境變數中。
5. 用 `node "$SKILL_DIR/run.js" <script.js>` 執行腳本。
6. 回報動作、失敗與產物路徑。沒有檢查結果頁面之前，不要宣稱成功。

## 設定

執行一次：

{{CODE:2}}

這會安裝 Playwright 與 Chromium。需要 Firefox 或 WebKit 時，使用 `cd "$SKILL_DIR" && npm run install-all-browsers`。

## 最小範例

{{CODE:3}}

執行它：

{{CODE:4}}

對於簡短的一次性任務，使用行內執行：

{{CODE:5}}

`-e` 程序會在程式片段結束時立即退出，所以要在片段內關閉瀏覽器。

## 目前的 Playwright 模式

偏好描述使用者所見內容的定位器，依此順序：

1. 帶可存取名稱的 `page.getByRole()`
2. 表單控制項用 `page.getByLabel()`
3. 可見的內容用 `page.getByText()`
4. 當應用程式有提供測試契約時用 `page.getByTestId()`

動作會自動等待元素可操作。使用以網頁為優先的斷言或定位器的 `waitFor()`，而不是 `waitForSelector()`、固定的 sleep 或 `networkidle`。

{{CODE:6}}

## 常見任務

### 響應式檢查

{{CODE:7}}

### 登入流程

使用使用者提供的測試憑證。絕不捏造或暴露真實的憑證。同時驗證頁面導覽與登入後的元素。

{{CODE:8}}

### 儲存腳本與產物

{{CODE:9}}

`PW_SCRIPT_DIR` 會在執行前複製以檔案為基礎的腳本，檔名已存在時加上時間戳。`PW_ARTIFACT_DIR` 控制輔助函式截圖的輸出位置；預設是作業系統的暫存目錄。

### 連接既有的 Chrome 工作階段

以開啟遠端除錯的方式啟動 Chrome，然後用 Playwright 連接：

{{CODE:10}}

這會重用該工作階段中的 Cookie 與擴充功能。除非使用者明確要求，不要用它處理機密；連接的瀏覽器擁有使用者的存取權限。

## 輔助函式

{{CODE:11}}

可用的輔助函式有 `detectDevServers`、`getExtraHeadersFromEnv`、`launchBrowser`、`createContext`、`handleCookieBanner` 與 `takeScreenshot`。動作、等待、擷取、認證、表格與重試，直接使用 Playwright 的定位器與斷言。

## 設定

- `PW_BROWSER`：`launchBrowser()` 使用的 `chromium`、`firefox` 或 `webkit`。
- `PW_CHANNEL`：已安裝的瀏覽器通道，例如 `chrome` 或 `msedge`。
- `PW_EXECUTABLE_PATH`：明確的瀏覽器執行檔路徑。
- `PW_HEADLESS`：`true` 或 `false`；預設為可見模式。
- `SLOW_MO`：動作延遲的毫秒數。
- `PW_HEADER_NAME` 與 `PW_HEADER_VALUE`：一個額外的 HTTP 標頭。
- `PW_EXTRA_HEADERS`：額外 HTTP 標頭的 JSON 物件。
- `PW_SCRIPT_DIR`：保留以檔案為基礎之腳本的目錄。
- `PW_ARTIFACT_DIR`：輔助函式產生之截圖的目錄。

網路攔截、API mock、認證狀態、影片、視覺檢查、裝置模擬與 CI 模式，請見 [API_REFERENCE.md](API_REFERENCE.md)。
