<!--meta
{"title": "妙搭應用開發", "category": "雲端與 DevOps", "tags": ["飛書", "妙搭", "Spark", "低程式碼", "部署", "lark-cli"], "summary": "飛書妙搭（Spark/Miaoda）應用的開發與託管：建立應用、本機全端開發、雲端生成迭代、設計 mockup／原型／簡報、整合 AI 與飛書能力、查詢日誌與監控指標、管理環境變數、協作者與角色，以及設定定時、記錄變更、Webhook、審批觸發的自動化。原文為簡體中文，以 OpenCC 轉為台灣繁體。", "usage": "- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-apps`（需 `lark-cli`）\n- 說「幫我做一個團隊請假系統並部署到妙搭」「這個妙搭應用最近錯誤量變多，幫我查日誌」「審批通過後自動寄通知」\n- 一般雲端檔案上傳請用 lark-drive，飛書文件編輯請用 lark-doc"}
-->
---
name: lark-apps
version: 1.0.0
description: "妙搭（Spark/Miaoda）應用開發與託管：應用建立、本地全棧開發、雲端生成迭代、創意設計（UI mockup / 可互動原型 / 線框圖 / 落地頁 / 儀表盤 / 幻燈片 deck / 視覺探索）、AI相關能力和飛書平臺能力或者其他外部能力整合、日誌/Trace/監控指標/PV/UV 查詢、環境變數管理、應用協作者與協作許可權設定、應用角色與成員管理、自動化觸發器（定時/記錄變更/Webhook/飛書審批）。當使用者要開發/新建一個系統·工具·平臺·應用，或要本地開發 / 雲端開發 / 修改 / 部署 / 釋出 / 上線 / 拿可分享連結，或用 HTML 做頁面·網站·部署到妙搭，或要設計 / design / mockup / prototype / wireframe / 做 PPT / deck / 視覺探索，或提到妙搭/Spark/Miaoda 應用（連結形如 `/app/app_xxx` 或 `/page/<token>`，執行時域名形如 *.aiforce.cloud）、應用資料庫、應用檔案儲存、開放 API Key、可見範圍、應用協作者/開發許可權、應用角色/角色成員、線上日誌、介面請求量、錯誤量、延遲、訪問量、環境變數、給妙搭應用配自動化任務/定時觸發/審批透過後自動觸發時使用。不負責普通雲盤檔案上傳（lark-drive）、飛書文件編輯（lark-doc）、原生幻燈片建立（lark-slides）。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli apps --help; lark-cli apps +<cmd> --help"
---

# apps (v1)

妙搭應用屬於使用者資產。預設用 `--as user`；認證、scope、exit-10、高風險確認、`_notice` 等通用處理只讀 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，不要在本 skill 裡複製。妙搭應用有兩條開發路徑：**本地開發**（拉原始碼本地寫）/ **雲端會話**（妙搭 AI 生成）。

## 身份與授權

妙搭應用是使用者的個人資產，統一 `--as user`（見開頭）。已有使用者身份可用時直接執行業務命令，**不要為了預防許可權問題主動重新登入**，否則可能中斷原任務並觸發不必要的裝置授權。僅當 CLI 明確返回未登入或缺少本域 scope 時，一次性執行：

{{CODE:1}}

因缺許可權失敗（`error.subtype == "missing_scope"`）時的通用處理見 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，同樣按 `--domain apps` 授權；授權成功後只恢復原業務操作，不擴充套件任務範圍。

## 意圖路由

按具體操作查命令（開發路徑先用下方「選擇開發路徑」判定表定好再進來取命令）：

| 使用者意圖 | 先用 | 按需讀取 |
|---|---|---|
| 建立**新**應用資產、拿 app_id | `+create` | [`lark-apps-create.md`](references/lark-apps-create.md) |
| 找已有 app_id、按名字過濾應用 | `+list --keyword <name>` | [`lark-apps-list.md`](references/lark-apps-list.md) |
| 查單個應用詳情（型別、名稱、釋出狀態等） | `+get --app-id <app_id>` | [`lark-apps-get.md`](references/lark-apps-get.md) |
| 改應用名或描述 | `+update` | [`lark-apps-update.md`](references/lark-apps-update.md) |
| HTML 應用 / 創意模式 — 寫 HTML 頁面/網站、靜態頁、PPT/deck、落地頁、儀表盤、UI mockup、原型、線框圖、視覺探索 | 載入 [`creative-design/creative-design.md`](creative-design/creative-design.md)（含完整開發與釋出流程） | [`creative-design/creative-design.md`](creative-design/creative-design.md) |
| 舊版存量 HTML 應用（無 Git 管理）繼續上傳已有靜態產物 | `+html-publish`（僅相容舊鏈路；新建 html / 創意模式 / creative-design 產物不得使用） | [`lark-apps-html-publish.md`](references/lark-apps-html-publish.md) |
| 開發已有應用 / 初始化本地倉庫（開發方式已定為本地後；先解析 app_id，勿 `+create` 新建） | `+init`（或手動 `+git-credential-init` + 原生 git）。**執行前必讀** [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md)，含端到端流程和領域規則 | [`lark-apps-init.md`](references/lark-apps-init.md), [`lark-apps-git-credential.md`](references/lark-apps-git-credential.md) |
| 閱讀 / 分析 / 總結一個妙搭應用的內容（任意應用模式，含創意模式應用的 `/page/<token>` 連結）；只要一份原始碼快照、不做本地開發；或要取**別人分享給你的**應用原始碼（你對其倉庫無許可權） | `+export`（下載 zip 後解壓讀原始碼；不配 git 憑證、不建工作區）。創意模式應用的 `/page/` 連結直接傳 `--meta-token <token>`，不必先 `+get` 換 app_id。要繼續開發用 `+init` 而非本命令 | [`lark-apps-export.md`](references/lark-apps-export.md) |
| 本地開發時 `.env.local` 損壞/丟失，重新拉取啟動期環境變數 | `+env-pull` | [`lark-apps-env-pull.md`](references/lark-apps-env-pull.md) |
| 管理應用環境變數（檢視/設定/刪除） | `+env-list`, `+env-set`, `+env-delete` | [`lark-apps-env.md`](references/lark-apps-env.md) |
| 網頁/另一臺電腦開通資料庫後同步本地環境變數 | `+env-pull`（之後重啟本地開發程序） | [`lark-apps-env-pull.md`](references/lark-apps-env-pull.md) |
| 查應用是否已開啟資料庫；給應用開啟資料庫 | `+features --app-id <app_id>`；確認需求後 `+feature-enable --feature database --app-id <app_id>` | [`lark-apps-features.md`](references/lark-apps-features.md) |
| 查線上日誌、Trace、請求數、錯誤率、延遲、CPU、memory、PV/UV/訪問量 | `+log-list`, `+log-get`, `+trace-list`, `+trace-get`, `+metric-list`, `+analytics-list` | [`lark-apps-observability.md`](references/lark-apps-observability.md) |
| 看錶 / 看結構 / 初始化多環境 / 匯入匯出資料 / 變更追溯 / 行級審計 / dev→online 釋出 / 時間點恢復 / 查 DB 用量 | `+db-table-list`、`+db-table-get`、`+db-env-create`、`+db-data-export`/`+db-data-import`、`+db-changelog-list`、`+db-audit-status`/`+db-audit-enable`/`+db-audit-disable`/`+db-audit-list`、`+db-env-diff`/`+db-env-migrate`、`+db-recovery-diff`/`+db-recovery-apply`、`+db-quota-get` | [`lark-apps-db.md`](references/lark-apps-db.md) |
| 逐條執行 SQL（SELECT / DML / DDL）；建表 / 改表 / 寫 SQL 的平臺規範 | `+db-execute` | [`lark-apps-db-execute.md`](references/lark-apps-db-execute.md)（含「平臺 SQL 規範」：審計列 / RLS / `user_profile` / 禁用 SQL / PG 陷阱） |
| 管理應用檔案儲存：上傳/下載本地檔案、列出/檢視/刪除已存檔案、生成臨時分享連結、查儲存用量 | `+file-upload`/`+file-download`/`+file-list`/`+file-get`/`+file-sign`/`+file-delete`/`+file-quota-get` | [`lark-apps-file.md`](references/lark-apps-file.md) |
| 除錯應用執行時快取：檢視/刪除單個業務 key、清空指定環境快取 | `+cache-get`/`+cache-delete`/`+cache-clear` | [`lark-apps-cache.md`](references/lark-apps-cache.md) |
| **部署/上線應用**（"部署""上線""推上去並部署""釋出到雲端"）；查釋出狀態/歷史 | 本地開發鏈路先按 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) 確認本次改動已 git commit + git push，再用 `+release-create` / `+release-get`；查歷史用 `+release-list` | [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md), [`lark-apps-release-create.md`](references/lark-apps-release-create.md), [`lark-apps-release-get.md`](references/lark-apps-release-get.md), [`lark-apps-release-list.md`](references/lark-apps-release-list.md) |
| 設定或檢視執行時可見範圍 | `+access-scope-set`, `+access-scope-get` | 對應 access-scope reference |
| 管理應用協作者（列出/新增/改許可權/移除）或協作許可權設定 | `+member-list`, `+member-add`, `+member-update`, `+member-remove`, `+member-settings-get`, `+member-settings-set` | 本文「應用協作者與協作許可權設定」 |
| 創意模式（html）應用的評論相關操作 | 創意模式應用評論走 lark-drive 文件評論體系，讀取 [`../lark-drive/SKILL.md`](../lark-drive/SKILL.md) 瞭解評論能力 | [`../lark-drive/SKILL.md`](../lark-drive/SKILL.md) |
| 管理 `app_...` 應用內角色、角色成員，或查詢使用者匹配角色 | `+role-list/get/create/update/delete`, `+role-member-list/add/remove`, `+role-match-list` | [`lark-apps-role.md`](references/lark-apps-role.md) |
| 雲端 Agent 生成/迭代應用（開發方式已定為雲端後） | `+session-create` -> `+chat` -> `+session-get` | [`lark-apps-cloud-dev.md`](references/lark-apps-cloud-dev.md) |
| 管理妙搭應用開放 API Key（建立/檢視/啟停/重置/刪除憑證；金鑰僅 create/reset 一次性返回） | `+openapi-key-list/get/create/update/enable/disable/delete/reset` | [`lark-apps-openapi-key.md`](references/lark-apps-openapi-key.md) |
| 管理妙搭應用自動化觸發器（定時/記錄變更/Webhook/飛書審批四類觸發器的查詢/建立/更新/啟停；Webhook URL·Token 一次性回顯、不落盤） | `+automation-list/get/create/update/enable/disable` | [`lark-apps-automation.md`](references/lark-apps-automation.md) |
| 檢視某次會話某一輪（turn）的回覆訊息（含仍在生成中的本輪）/ 匯出上一輪模型回覆（"這一輪迴復了什麼""上一輪的回覆""匯出某輪訊息"） | 先 `+session-get`（取 `latest_turn.turn_id`）-> `+session-messages-list --turn-id <id>`（僅 user 身份；分頁用 `--page-token`） | [`lark-apps-session-messages-list.md`](references/lark-apps-session-messages-list.md) |
| 外部能力(AI模型能力和飛書平臺能力)整合/外掛/Plugin/Capability | `+plugin-install`, `+plugin-list`, `+plugin-uninstall` | [`lark-apps-plugin-install.md`](references/lark-apps-plugin-install.md), [`lark-apps-plugin-uninstall.md`](references/lark-apps-plugin-uninstall.md), [`lark-apps-plugin-list.md`](references/lark-apps-plugin-list.md) |
| 把一批 ID 在妙搭 user_id ↔ 飛書 open_id / union_id / 飛書 user_id 之間互轉（例如拿到 open_id 但下游要 user_id） | `+user-id-convert --convert-type <方向> --ids <id1,id2,...>` | [`lark-apps-user-id-convert.md`](references/lark-apps-user-id-convert.md) |

## 高頻路徑

- **Base 到應用資料庫同步**：使用者說“Base 同步到資料庫 / 整庫同步 / 多張表同步 / 批次任務重新啟用 / operation-not-allowed”時，先讀 [`lark-apps-db.md`](references/lark-apps-db.md) 的 Base 資料同步段落，再查 app_id 或處理授權。先形成計劃再動手：`+db-sync-create` 一次只處理一張 Base 表，整庫/多表必須拆成多份單表配置和多次 preview/create；batch/import 任務是一次性任務，不能重新 enable，遇 operation-not-allowed 先解釋生命週期邊界，再用 `+db-sync-get` 查狀態/結果，持續同步要新建 streaming 任務。
- **效能/監控/觀測指標**：使用者問“介面請求量、錯誤量、錯誤率、介面慢、延遲、CPU、記憶體、最近一小時/七天趨勢”時，不要去當前工作區搜尋監控檔案，也不要詢問“監控資料在哪”。先按「app_id 獲取」解析應用：`lark-cli apps +list --keyword "<應用名>" --as user`；拿到 `app_id` 後讀 [`lark-apps-observability.md`](references/lark-apps-observability.md)，用 `+metric-list`。
- **請求量 + 錯誤量 + 延遲**：請求量/錯誤量用 `lark-cli apps +metric-list --app-id <app_id> --metric requests --since <range> --as user`（不傳 `--series` 會同時返回 total/error）；延遲用 `--metric latency`（不傳 `--series` 會返回 p50/p99）。如果使用者給了具體介面，再加 `--api <path-or-name>`；不要臆造 group-by 引數。
- **PV/UV/訪問量/活躍使用者**：先解析 `app_id`，再用 `+analytics-list`，不要誤用 `+metric-list`。
- **設定環境變數**：如果使用者只給應用名，仍先 `+list --keyword` 解析 app_id；設定 online 環境且使用者已經明確說“確認/直接執行”時，呼叫 `+env-set --environment online ... --yes`，不要再次要求確認。回覆和日誌摘要裡只提 key / env / app，不回顯真實 value；需要傳複雜值時優先用 `@file` 或 stdin。
- **刪除環境變數**：`+env-delete` 是破壞性操作。除非使用者在同一輪已經明確確認刪除這個 app/env/key，否則先向使用者確認應用、環境、key 和刪除後果；確認後再加 `--yes`。不要因為認證失敗/重登完成就自動繼續刪除，必須保留確認門檻。

## 應用協作者與協作許可權設定

這組命令管理妙搭應用的開發協作者和協作策略，不等同於 `+access-scope-*` 的執行時訪問範圍，也不等同於 `+role-*` 的應用內業務角色。所有命令使用 `app_...` 應用 ID 和 `--as user`。不要讀取或判斷 `app_type` 來預判支援範圍，直接呼叫對應的協作者命令。

- `+member-list`、`+member-settings-get` 是隻讀命令，需要 `spark:app:read`。
- `+member-add`、`+member-update`、`+member-remove`、`+member-settings-set` 是高風險寫命令，需要 `spark:app:write`。先用 `--dry-run` 核對目標、URL 和請求體；dry-run 不需要 `--yes`。使用者已確認具體應用、成員/設定及影響，或已按下方「高影響動作：確認與預授權」對整條流程明確預授權時，真實執行加 `--yes`；否則在 dry-run 後停下請求確認。批次移除成員仍執行「禁止預授權判定底線」，不能從泛化的“直接做”推匯出 `--yes`。
- 新增、更新、移除成員時必須顯式提供匹配的外部 ID 型別，禁止傳內部數字 ID、猜測型別或做隱式轉換：使用者 `--member-type openid --member-id ou_...`；群組 `--member-type openchat --member-id oc_...`；部門 `--member-type opendepartmentid --member-id od-...`。
- `+member-list --member-type` 的篩選列舉是響應物件型別 `user` / `department` / `chat`，與寫命令的 ID 型別列舉不同。可再用 `--role view|edit|full_access` 篩選。
- `+member-list` 一次返回應用的全部直接協作者，不提供分頁引數；可用 `--member-type` 和 `--role` 縮小結果範圍。
- 成員響應不包含應用詳情。需要名稱、型別或釋出狀態時單獨呼叫 `+get --app-id <app_id>`，不要期待成員分頁重複返回 `app`。
- 收到 subtype `feature_not_available`（OpenAPI code `3340005`；直連服務可能為 `40005`）時，立即停止 CLI 自動化，不切換 `app_type`，也不嘗試用 access scope、應用角色或其它成員命令繞過。向使用者說明該應用暫不支援透過 lark-cli 設定協作者，並引導其在妙搭後臺的許可權設定中操作。
- `external_invite` 只在 `+member-settings-get` 的響應中讀取，不能獨立設定；它會跟隨 `external_access`。CLI 不註冊 `--external-invite`，需要改變外部協作能力時只設定 `--external-access`。
- `copy_download_by` 也只在 `+member-settings-get` 的響應中讀取。CCM 當前明確不支援為妙搭物件寫入複製、列印和下載許可權，因此 CLI 不註冊 `--copy-download-by`。保留讀取結果，不要嘗試寫入，也不要改用其它許可權欄位模擬。

{{CODE:2}}

## 選擇開發路徑（進意圖路由前先判這步）

新建必先定 **app_type** 和**開發方式**兩件正交的事；修改已有先按「app_id 獲取」指認到 app，指認不到就問使用者，不擅自 `+create`。開發方式（本地 vs 雲端）只看使用者對"誰來寫程式碼"的偏好，與應用複雜度、要不要資料庫無關。

**app_type 三類邊界**（先判"要不要把資料存到服務端"，再判"純展示還是有互動"）：

| 訊號 | 判定 |
|---|---|
| 含資料庫 / 後端持久化：登入 / 增刪改查 / 報名·投票·站會存記錄 / 多人協作 / 泛稱"系統·工具"且明確要存資料 | `app_type=full_stack`；建立後用 `+features` 看 `database` 的 `enabled`，為 `false` 時按 [`lark-apps-features.md`](references/lark-apps-features.md) 用 `+feature-enable --feature database` 開資料庫 |
| 純靜態展示（給人"看"的物料，無 JS 互動）：PPT/deck / demo / 落地頁 / 海報 / UI mockup / 線框圖 / 靜態儀表盤 / 視覺探索 | `app_type=html`，載入 [`creative-design/creative-design.md`](creative-design/creative-design.md)（含完整開發與釋出流程） |
| 有 JS 互動但無資料庫（給人"用"的前端應用）：可互動原型 / SPA / 表單校驗 / 動態計算 / 呼叫外部 API / 泛稱"工具·系統"但未明確要存資料 | `app_type=frontend`（**預設傾向**：使用者未明確提出資料庫需求時預設引導 frontend，不預設 full_stack） |
| 型別模糊（尤其"要不要存資料"不清） | **追問**，話術偏向 frontend，例："看起來是個前端應用，需要儲存資料嗎？"；確認要存資料再轉 full_stack，確認純展示再轉 html |
| 使用者要自己寫 / 本地 IDE·code agent / 拉原始碼到本地 / 交研發 | 本地開發，讀 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) |
| 讓妙搭 AI 雲端生成 / 對話式 / 自己不碰程式碼 | 雲端會話，讀 [`lark-apps-cloud-dev.md`](references/lark-apps-cloud-dev.md) |
| 未表達"誰來寫"偏好 | **必須先問**（原生代碼開發 vs 雲端 AI 生成）；選定前不擅自選邊、不暗示預設，不得以"需求不模糊"為由跳過提問直接 `+init` / `git clone` / `+session-create` / 首輪 `+chat` |
| 修改已有 + 當前目錄是 `.spark/meta.json` 專案 | 直接繼續本地按意圖路由，不必問也不必判雲端 |
| 修改已有 + 有云端偏好 | 雲端會話；未表達偏好且非本地專案 → 預設本地；判不準先問 |

**後續加資料庫 / 型別升級**：應用後續需要資料庫時，先 `+features --app-id <app_id>`：列出 `database` 且 `enabled=false` 時經使用者確認後 `+feature-enable --feature database`，再 `+env-pull` 並重啟本地開發程序（見 [`lark-apps-features.md`](references/lark-apps-features.md)）；沒列出 `database`、`+features` 報錯或服務端拒絕啟用時，本地 CLI 不提供型別升級，引導使用者到雲端會話（開啟 `https://miaoda.feishu.cn/app/{app_id}`），用自然語言描述後端需求（如"給這個應用加登入和資料儲存"）即可觸發升級，無需特殊指令。

## 釋出態護欄

- **釋出意圖判定**：使用者要"可訪問 / 線上 / 分享 / 新連結 / 上線" = 釋出意圖，先走釋出鏈路、確認完成再給連結。
- `+release-create` 的釋出理由按應用型別處理：創意模式 `html` 不需要釋出理由，命令不得傳 `--apply-reason`；`frontend` / `full_stack` 先載入 [`lark-apps-release-create.md`](references/lark-apps-release-create.md)，生成理由並納入現有釋出確認，命令傳入已確認的同一理由。
- `+release-get` 尚未返回 `finished` / `failed`，且返回 `current_node_info.current_status=PENDING` 時（頂層可能是 `publishing` 或 `pending`）立即載入 [`lark-apps-release-get.md`](references/lark-apps-release-get.md)，停止輪詢並告知當前使用者正在等待審批負責人處理；不得假定當前使用者或 `submitted_by` 是審批人。終態優先於可能殘留的 PENDING 節點。
- `+release-create` 或 `+release-get` 僅當服務端錯誤明確說明客戶端版本過舊或要求升級時，才建議執行 `lark-cli update` 後重試原命令（查詢仍使用同一個 `release_id`）。不要硬編碼或猜測最低版本，不要用 `--help` 做能力預檢；`X-Cli-Version` 由 CLI 請求統一攜帶且不是認證資訊，本工作流不增加 CLI 版本門禁。
- 完成 ≠ 釋出：雲端會話完成 / `+list is_published=true` 都不代表最新內容已部署。
- 開發態連結 `https://miaoda.feishu.cn/app/{app_id}`（full_stack / frontend 應用）：進應用編輯/開發態、管理與繼續開發應用的入口，也是 frontend 升級為 full_stack 的入口（雲端會話）。創意模式（html）應用開發態和釋出態是同一個連結，無需額外提供開發態連結。
- 釋出態連結來源：`+release-get` 輪詢 `finished` 給 `online_url` / `failed` 給 `error_logs`（html / frontend / full_stack 統一走 `+release-get`）。
- html 應用的主鏈路是創意模式開發方式：按 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) 初始化倉庫、在倉庫內產出 HTML 及關聯檔案，並透過 git commit / git push / `+release-create` / `+release-get` 釋出部署。任何 git 操作（clone / pull / push）報錯時，先執行 `lark-cli apps +git-credential-init --app-id <app_id> --as user` 重新整理本地 Git 憑證，再重試原 git 命令。如果重新整理憑證也失敗，**停止並向使用者報告**：原始 git 錯誤、憑證重新整理失敗原因，以及是否可能是當前環境（作業系統、沙箱）限制導致（如 macOS Keychain 在沙箱中不可用、Linux 加密檔案目錄不可寫等）。不要改走 `+html-publish`，也不要把 `+html-publish` 當作本地開發鏈路的 fallback。
- 創意模式（html）應用的連結格式為 `https://{租戶域名}/page/{meta_token}`，**開發態和釋出態是同一個連結**（區別於 full_stack 應用兩者分開）。此連結形似飛書文件連結。`+get --app-id <meta_token>` 可獲取應用資訊（含 `app_id`），`+get --app-id <app_id>` 可獲取 `meta_token`。看到 `/page/xxx` 連結時，它是妙搭創意模式應用，不要當成飛書文件跳過；使用者要看懂 / 總結這個應用的內容時，直接 `+export --meta-token <token>` 匯出原始碼閱讀。

## 平臺資源與應用原始碼邊界

- `apps` 命令的 `--path`、`--file`、`--output` 等路徑引數只接受當前工作目錄（cwd）下的相對路徑，傳絕對路徑會報錯。如果目標檔案不在 cwd 下，先 `cd` 到目標目錄再執行命令。
- 圖片、字型、音影片等資源型檔案屬於平臺資源，不應提交到 git 倉庫、引用本地路徑或以 base64 內聯到原始碼中。先透過 `lark-cli apps +file-upload --app-id <app_id> --file <local_path>` 上傳到應用檔案儲存，拿到返回的遠端 URL 後在程式碼中引用。上傳返回的連結按 app 隔離，不同應用必須各自重新上傳，不能跨應用複用同一連結。詳情讀 [`lark-apps-file.md`](references/lark-apps-file.md)。
- `apps +role-*` 只管理平臺角色資源；修改已初始化應用的原始碼（包括當前目錄已經是應用專案）時，先檢視工作區 `.agents/skills/`，完整讀取與任務匹配的領域 skill，再按其路由讀取所需 reference。角色鑑權或執行態角色管理讀應用內 `authz-guide`，不能用本 skill 的平臺命令參考推斷執行時合同。
- `lark-cli` 只用於開發過程中的平臺資源核驗或變更。應用執行時程式碼必須使用工程內領域 skill 規定的 SDK，禁止透過 `exec` 或子程序呼叫 `lark-cli`。
- 平臺回讀出的當前資源 ID、名稱和成員只用於事實核驗，不自動構成業務策略；除非需求或應用內領域 skill 明確定義，禁止把當前樣本硬編碼成 allowlist、denylist、只讀集合或許可權規則。
- 實現領域 SDK 時，以實際包匯出的型別和應用內領域 reference 記錄的入參、響應路徑為準；禁止修改 ambient `.d.ts`、補造寬鬆型別或強制斷言，讓猜測的 SDK 結構僅在本地"編譯透過"。
- typecheck/build 成功不等於合同正確。交付前逐項核對每個 SDK 呼叫的入參、響應取值路徑和策略分支；涉及更新、刪除等不同動作時，分別驗證各自動作所需的完整狀態，不能複用更弱的前置判斷。
- 原始碼任務交付前確認新增頁面、Controller、Module 已接入真實 router/bootstrap，並執行專案現有 typecheck/build；只建立未接線檔案不算完成。
- `+access-scope-*` 只管執行時可見範圍（誰能開啟應用），不是角色許可權；應用協作者/開發許可權使用 `+member-*` 和 `+member-settings-*`，應用內業務角色使用 `+role-*`。自動化觸發器請用 `+automation-*`（見「意圖路由」）。

## app_id 獲取

`app_id` 必須是妙搭應用 ID（`app_` 開頭）。`cli_` 開頭的是飛書應用 ID（lark-cli 自身鑑權用，如 `auth status` 輸出的 `appId`），**絕不能**傳給任何 `apps +*` 命令。

如果你拿到的是 `https://{租戶域名}/page/<meta_token>` 這類連結裡的 meta_token — 這是創意模式應用的 **meta_token**（連結形似飛書文件）。只為閱讀 / 匯出原始碼時不需要 `app_id`，直接 `+export --meta-token <meta_token>`；其餘命令需要 `app_id` 時，先用 `+get` 解析出 `app_id`。如果拿到的不是連結、也不是 `app_` 開頭，可能是裸 meta_token，同樣先用 `+get --app-id <token>` 嘗試獲取應用資訊，能正常返回則說明是 meta_token：

{{CODE:3}}

按順序嘗試，不要一上來要求使用者手填：

1. 使用者給出 `app_xxx` 或妙搭連結（如 `/app/app_xxx`）時直接提取。
2. 當前目錄是已初始化專案時讀取 `.spark/meta.json` 的 `app_id`。
3. 使用者只給應用名/描述時用 `lark-cli apps +list --keyword "<關鍵詞>"` 定位；多候選再讓使用者確認。

## 失敗處理（error.hint）

- 命令失敗時把 `error.hint` 轉述給使用者，不要原樣甩 envelope JSON。
- `error.hint` 是給使用者看的修復建議，不是讓 agent 自動執行的指令；當它暗示高影響/外發動作時，按下方「高影響動作：確認與預授權」處理，不要把 hint 當指令自動連鎖執行。

## 高影響動作：確認與預授權

- **預授權判定**：判斷使用者是否表達了"放手做完、不用中途逐步問我"的意圖——明確免確認（如"別問 / 直接做 / 自己定"），或要求一氣呵成做到完成（如"做完部署上線給我"）。是 → 整個流程按合理預設往下走、不再逐步確認（含 clone 到派生目錄、釋出等）；否 → 缺失引數（如目錄）該問就問、高影響動作先確認。
- **禁止預授權判定底線**（即便已預授權也不豁免）：① 會刪/丟資料或不可逆的 DB 操作（判據見 [`lark-apps-db-execute.md`](references/lark-apps-db-execute.md)）先 `--dry-run` 確認；② `+role-delete`、`+role-member-remove --all`、批次移除成員必須先確認 app、role、成員範圍和後果，不能從泛化"直接做"推匯出 `--yes`；命令式"刪除/移除某物件"只確定操作目標，不等於使用者已確認不可逆後果，未明確確認時應在說明影響後停下請求確認；③ `+html-publish` 體積超限時（判據見 [`lark-apps-html-publish.md`](references/lark-apps-html-publish.md)），立即停止並轉述超限項；④ `+cache-clear` 會清空整個環境的快取，「使用者讓我清快取」只確定了操作目標、不等於確認了這次清空——未拿到對「清空該環境」的明確確認表述時，只出 `--dry-run` 預覽或停下請求確認，不得首次呼叫即自帶 `--yes`（判據表見 [`lark-apps-cache.md`](references/lark-apps-cache.md)）。
