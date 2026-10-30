<!--meta
{"title":"OpenWeb 網站存取","category":"瀏覽器與測試自動化","tags":["網站 API","瀏覽器自動化","資料擷取","CLI"],
"summary":"以具型別的 JSON 存取 90 多個真實網站——Google、Amazon、Reddit、YouTube、GitHub、Instagram、Bloomberg、Zillow 等，涵蓋搜尋、購物、旅遊、金融、社群、新聞與開發工具，可讀取、搜尋、發文、留言、傳訊息。依權限等級執行（讀取直接執行、寫入與刪除先詢問、金流交易一律略過），並依錯誤類別處理需要瀏覽器、需要登入、機器人封鎖等狀況；沒有支援的網站可依指南新增。",
"usage":"- 需安裝 `openweb` CLI（`npm i -g @openweb-org/openweb`）；部分網站需要受管的 Chrome 工作階段\n- `openweb sites` 列出所有網站；`openweb <site>` 查看操作與是否需要登入\n- 說「查一下 Amazon 上這個商品的價格」「搜尋 Reddit 上關於 X 的討論」\n- 需要登入的網站先 `openweb login <site>`"}
-->
---
name: openweb
description: "以具型別的 JSON 存取 90 多個真實網站——Google、Amazon、Reddit、YouTube、GitHub、Instagram、Bloomberg、Zillow 等——涵蓋搜尋、購物、旅遊、金融、社群、新聞與開發工具。用於讀取、搜尋、發文、留言、傳訊息，或以其他方式與這些網站互動（價格、商品、文章、股價、航班、貼文、留言、私訊等）。執行 `openweb sites` 查看完整清單。"
license: MIT
compatibility: "需要 `openweb` CLI（npm：@openweb-org/openweb）。部分網站需要受管的 Chrome 工作階段。執行環境細節請見 references/cli.md。"
metadata:
  version: "0.1.5"
  openclaw:
    links:
      homepage: "https://getopenweb.com"
      repository: "https://github.com/openweb-org/openweb"
    requires:
      bins: [openweb]
      env: [OPENWEB_HOME]
      config: ["$OPENWEB_HOME/config.json"]
    install:
      - kind: node
        package: "@openweb-org/openweb"
        bins: [openweb]
---

# OpenWeb

代理原生的方式存取任何網站。透過 API 連接代理 CLI 與網頁 GUI。

## 載入紀律

- 不要讀這個資料夾中的每一個檔案。
- 從 SKILL.md 開始。一次只走一條路線。

## 使用既有的網站

### 1. 找到網站

{{CODE:1}}

如果網站沒有套件，「不要」說「不支援」。導向 add-site/guide.md。

### 2. 檢查就緒狀態

{{CODE:2}}

- `Requires browser: yes` —— 需要時瀏覽器會自動啟動；不需要手動設定
- `Requires login: yes` —— 使用者必須透過自己的瀏覽器工作階段登入

### 3. 閱讀網站說明

當你的工作區中有網站文件時，優先使用：

- **原始碼 repo：** 先讀 `src/sites/<site>/SKILL.md` 了解工作流程與意圖對應，再讀 `src/sites/<site>/DOC.md` 了解內部細節。
- **發布的／執行環境套件：** 只保證有 `DOC.md`、規格、manifest、範例與轉接器。各網站的 `SKILL.md` 與 `PROGRESS.md` 是原始碼樹的文件，不會發布到 `$OPENWEB_HOME/sites/<site>/`。

如果只有發布的套件可用，就依靠 `openweb <site>`、`openweb <site> <op>`、範例與 `DOC.md`。

### 4. 檢視操作

{{CODE:3}}

執行前檢查操作的權限等級：

| 等級 | 預設 | 行為 |
|---|---|---|
| `read` | 允許 | 類似 GET 的操作——自由執行 |
| `write` | 詢問 | 建立／更新——執行前詢問使用者 |
| `delete` | 詢問 | 破壞性——執行前詢問使用者 |
| `transact` | 拒絕 | 金融／不可逆——一律略過 |

### 5. 執行

{{CODE:4}}

自動溢出：超過 4096 位元組的回應會寫入暫存檔。

`openweb <site> exec <op> '{...}'` 是等效的——當第三個參數是 JSON 時可以省略 `exec`。

### 6. 失敗時

stderr 上的錯誤包含 `failureClass`：

| failureClass | 動作 |
|---|---|
| `needs_browser` | 瀏覽器會自動啟動；如果失敗，檢查 Chrome 的安裝。備案：`openweb browser start` |
| `needs_login` | `openweb login <site>`，然後 `openweb browser restart` |
| `needs_page` | 開一個分頁到該網站的 URL |
| `bot_blocked` | `openweb browser restart --no-headless`，由使用者在可見的瀏覽器中解 CAPTCHA，然後重試。對於持續被擋的網站，在設定中設定 `"browser": {"headless": false}` |
| `permission_denied` | 更新 `$OPENWEB_HOME/config.json` 中的 `permissions` |
| `permission_required` | 請使用者確認，然後重試 |
| `retriable` | 等幾秒後重試（最多 2 次） |
| `fatal` | 不要重試——修正參數或檢查網站名稱 |

如果上表無法解決，閱讀 references/troubleshooting.md。

### 7. 缺少網站或涵蓋範圍

網站不存在或缺少需要的操作？閱讀 add-site/guide.md。

## 新增／擴充／升級網站

閱讀 add-site/guide.md

## 修正問題

閱讀 references/troubleshooting.md

## 檔案地圖

所有路徑都相對於 `skills/openweb/`。

### add-site/（工作流程——依序載入）

| 檔案 | 何時載入 |
|---|---|
| `add-site/guide.md` | 新增／擴充工作流程的進入點 |
| `add-site/probe.md` | 探測步驟：CDP 瀏覽器端探索 |
| `add-site/capture.md` | 擷取步驟：記錄瀏覽器流量 |
| `add-site/review.md` | 審閱步驟：閱讀 analysis-summary.json |
| `add-site/curate-operations.md` | 整理：命名、雜訊、參數、權限 |
| `add-site/curate-runtime.md` | 整理：認證、傳輸、擷取 |
| `add-site/curate-schemas.md` | 整理：回應結構、範例、個資 |
| `add-site/verify.md` | 驗證：執行環境 + 規格 + 文件的循環 |
| `add-site/document.md` | 文件：各網站的 SKILL.md + DOC.md + PROGRESS.md、知識更新 |

### references/（查詢——獨立載入）

| 檔案 | 何時載入 |
|---|---|
| `references/cli.md` | CLI 指令語法、旗標、stdout/stderr |
| `references/x-openweb.md` | 完整的 x-openweb 欄位結構 |
| `references/troubleshooting.md` | 出問題了——分類、診斷、修正 |

### knowledge/（模式——在決策點載入）

| 檔案 | 何時載入 |
|---|---|
| `knowledge/archetypes.md` | 依網站類別預期的操作 |
| `knowledge/auth-routing.md` | 不知道認證類型——從訊號查詢家族 |
| `knowledge/auth-primitives.md` | 設定認證——設定與陷阱 |
| `knowledge/bot-detection.md` | 傳輸／擷取的決策 |
| `knowledge/extraction.md` | 擷取訊號——SSR/DOM 模式 |
| `knowledge/graphql.md` | GraphQL——持久化查詢、批次 |
| `knowledge/ws.md` | WebSocket——訊息／連線模式 |
| `knowledge/adapter-recipes.md` | 轉接器模式、程式碼範本、陷阱 |
| `knowledge/transport-upgrade.md` | 傳輸等級決策、node 可行性、API 探索 |
