<!--meta
{"title":"飛書多維表格","category":"文件與辦公","tags":["飛書","Lark","多維表格","Bitable","自動化流程","lark-cli"],
"summary":"飛書（Lark）官方 CLI 技能：操作多維表格（Base / Bitable）——建表、欄位、記錄、檢視、統計、公式/lookup、表單、儀表板、應用模式頁面與元件、Workspace、自動化流程、角色權限與模板中心。原文為簡體中文，此處以 OpenCC 轉為台灣繁體。",
"usage":"- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-base`（需 `lark-cli` 與 lark-shared）\n- 貼上 `/base/` 連結並說「幫我統計這張表上週的新增筆數」「新增一個『負責人』欄位」「建一個新進員工資料收集表單」\n- 建議一律以 `--as user` 身分操作；大量寫入每批最多 200 筆、同一張表需序列寫入\n- 匯入匯出 Excel/CSV 請改用 lark-drive"}
-->
---
name: lark-base
version: 1.2.23
description: "飛書多維表格（Base）操作：建表、欄位、記錄、檢視、統計、公式/lookup、表單、儀表盤、應用模式（BaseApp/AppMode 頁面與元件）、Workspace 目錄、workflow、角色許可權、模板中心（多維表格模板分類/列表/搜尋）；遇到 Base/多維表格/bitable、BaseApp/AppMode、/base/ 或 /app/ 連結時使用。BaseApp 不走 lark-apps；檔案匯入/匯出轉 lark-drive，認證/授權轉 lark-shared。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli base --help"
---

# Base

普通 Base 是資料容器，由一棵 Base Block 資源樹和 Base 級配置組成。`folder`、`table`、`docx`、`dashboard`、`workflow` 都是 Block 型別；Advanced Permission / Role 是 Base 級配置，不屬於 Block。Table 是其中承載業務資料的核心 Block。Workspace 是組織 Base 與 BaseApp 的外層容器；BaseApp（AppMode）透過 Page 和元件組織 Base 資料，不是 Base 的別名。

## 身份選擇（優先）

操作 Base 優先使用 `--as user`；使用者明確要求應用身份時使用 `--as bot`。許可權失敗按 `lark-shared` 以原身份修復 scope 或資源 ACL；只有使用者明確同意更換操作者時才切換身份。

## 進入前必做：解析目標實體

開始操作前先確定 `base_token` 和目標實體型別；上下文已提供 `<bitable>` / `<base_refer>` 標籤及資源 ID 時直接使用。其餘情況按意圖選擇入口：

1. **URL 或分享連結：** `lark-cli base +url-resolve --url '<url>' --as user`。Base URL 根據返回的 `resource_type` / `block_type` 及 `table_id`、`view_id`、`record_id`、`dashboard_id`、`workflow_id`、`docx_token`、`share_token` 等座標進入對應模組；BaseApp `/app/` URL 返回 `app_token`，並在連結攜帶時返回 `workspace_token` 和 `page_id`。實體型別以解析結果為準。
2. **Base 標題或關鍵詞：** `lark-cli base +title-resolve --title '<keyword>' --as user`。單一結果直接取得 `base_token`；多個候選結合標題、所有者和更新時間消歧，仍無法唯一確定時請使用者選擇。隨後按下方 Base Block 資源模型定位目標實體。
3. **已有 Base 候選列表：** 使用者要列出已有 Base 候選，且需要按最近訪問、owner、建立人、時間、型別等維度篩選/排序時，轉 `lark-cli drive +search --doc-types bitable --as user`。按標題/關鍵詞定位單個 Base 仍用 `+title-resolve`。常見候選列表命令：
   - 最近訪問：`lark-cli drive +search --doc-types bitable --sort open_time --opened-since 3m --page-size 20 --as user`
   - 只列我擁有的：加 `--mine`；如果要列“我建立的”，用 `--created-by-me`。
   - 從候選項拿到 URL 或 token 後，再用 `+url-resolve` 或 `+base-get` 進入 Base 業務命令。
4. **BaseApp：** 優先使用真實 `/app/` URL；已有 `workspace_token` 時可用 `+workspace-entity-list --type baseapp` 定位。兩者都沒有時請使用者補充應用連結或 Workspace，不按名稱全域性猜測 `app_token`。

**讀取 Base：** Base 資訊用 `+base-get`，資源目錄按下方 Base Block 資源模型讀取。

**寫入 Base：** 建立新 Base 使用一次 `+base-create --name <base-name> --table-name <table-name> --fields '<field-array>'` 同時建立 Base、首表和 fields；`+base-copy` 複製整個 Base；Base 內資源統一按下方 Block 生命週期管理。

## Base 模板中心

模板中心是公開的 Base 模板庫，不是使用者雲空間裡的已有 Base。使用者想用現成模板建立新 Base，且沒有指向已有物件的錨點（沒有 Base URL、沒有“我的/最近訪問的表”、沒有具體已存在的 Base 名）時，可讀取 [lark-base-template-center.md](references/lark-base-template-center.md) 查詢模板中心模板；`+template-categories` 列出公開模板分類，`+template-list` 按分類列出公開模板，`+template-search` 按業務關鍵詞搜尋公開模板。

## Base Block 資源模型

{{CODE:1}}

每個 Base Block 都有 `id`、`type`、可修改的 `name`、所在 Folder 的 `parent_id`，並在同級目錄中具有順序。`+base-block-list` 是統一發現入口；`+base-block-create` 建立 Block，`+base-block-rename` 修改名稱，`+base-block-move` 透過 `--parent-id` 調整目錄並透過 `--before-id` / `--after-id` 調整順序，`+base-block-delete` 刪除 Block。型別專屬內容再由對應模組命令處理。

建立時已經明確型別專屬初始內容，可直接使用對應構造命令一次完成：Table 用 `+table-create --fields`，Dashboard 用 `+dashboard-create` 設定主題，Workflow 用 `+workflow-create --json` 提交完整定義；Folder 和 Docx 使用 `+base-block-create`。

Block 的 `id` 按型別直接作為對應模組座標：

| Block type | 模組座標與內部內容 |
|---|---|
| `table` | `id` 即 `table_id`；內部包含 Field、Record、View 和 Form |
| `dashboard` | `id` 即 `dashboard_id`；內部包含圖表、指標卡和文字等 Dashboard 元件 |
| `workflow` | `id` 即 `workflow_id`；內部包含 title、status 和 steps 執行圖 |
| `docx` | Block 另帶 `docx_token`；正文由 `lark-doc` 處理 |
| `folder` | `id` 是目錄 Block ID，也可作為 `--parent-id`；只組織子 Block |

## Table Block（The Core）

Table 本身是 Base Block，也是 Base 的核心資料儲存層；Field、Record、View 和 Form 是 Table 內部物件，不是 Base Block。業務資料查詢、寫入、關聯、統計和分析都從 Table 開始。先用 `+table-list` 定位 Table；欄位名和目標已知的普通讀取可直接進入 Record 命令，只有寫入、篩選或關聯等依賴欄位型別/schema 的任務才補 `+field-list`。多表的 `+field-list` 可以併發執行。基礎的 Record / CellValue 讀寫直接按下方路徑；reference 只承載高階分析、完整協議和邊界細節。

**讀取 Table：** `+table-list` 定位表，`+table-get` 讀取詳情。Table 專屬複製使用 `+table-copy`，非同步狀態用 `+table-copy-status`；schema 和 records 由下方內部物件操作。

Table 下的大多數更新透過非同步鏈路生效，介面成功返回後立即讀取可能暫時看不到最新狀態。優先以寫入成功響應作為操作結果；任務必須確認最終狀態時，先完成本輪相關變更，再統一讀取驗收，避免逐項寫後立即讀回。

### Field

Field 定義列 schema。`field_id` 是穩定列標識，`name` 是可修改的展示名稱；Formula、Lookup、Link、Select 等屬於 Field 型別或能力。

**讀取 Field：** `+field-list` / `+field-get` / `+field-search-options`。**寫入 Field：** 已有 Table 中建立多個欄位時，優先向一次 `+field-create --json` 傳欄位物件陣列；單欄位更新和刪除用 `+field-update` / `+field-delete`。建立和更新分別讀取 [field-create](references/lark-base-field-create.md) / [field-update](references/lark-base-field-update.md)，由命令文件繼續路由 Field JSON、Formula 和 Lookup 協議。`欄位外掛` 用於擴充套件基礎欄位能力：按同一行其他欄位內容觸發 LLM 生成，並寫回已有目標欄位；當前已確認目標欄位支援文字、單選、數字，配置或觸發前先讀 [field-extension](references/lark-base-field-extension.md)。

### Record

Record 是 Table 中的一行資料，包含該記錄在各個 Field 下的 CellValue。系統 `record_id` 是表內穩定、非空且唯一的主鍵，Table 的主欄位只是展示欄位。

#### 1. 讀取記錄或單元格

- 已知若干個 `record_id`：`+record-get --record-id <id1> --record-id <id2>`
- 關鍵詞搜尋：`+record-search --keyword <text> --search-field <field>`；至少指定一個搜尋欄位。
- 其餘讀取：`+record-list`；結構化條件和排序分別用 `--filter-json` / `--sort-json`。

行數較大、需要服務端謂詞下推時，`--filter-json` 使用 tuple condition；最常用的篩選與完整日期範圍寫法：

{{CODE:2}}

完整運算子和各欄位取值結構讀取 [Filter 條件結構](references/lark-base-filter-condition.md)。

所有讀取都重複傳 `--field-id` 做最小欄位投影，並統一寫入 NDJSON artifact：`--format ndjson --output <path>.ndjson`。每行是一條 Record JSON，stdout 摘要包含 `records_count` 和 `has_more` 用於分頁判斷。

{{CODE:3}}

預計記錄數少於 500 行時，建議不做謂詞下推，直接拉取到本地用 jq 或 Python 處理；行數較大時可用 `--filter-json` 下推可表達的條件，正則、派生等無法下推的條件繼續在本地處理。

{{CODE:4}}

`--limit` 的預設值是 2000，最大值是 2000，通常無需手動指定 limit 引數；支援 `--offset` 引數；只有 `has_more=false` 且查詢範圍符合問題時，才能當作完整結果。大表完整讀取、View 範圍讀取、複雜 JOIN、集合/多值、時序、語義或專業統計分析時，讀取 [Record 查詢與分析 SOP](references/lark-base-record-query-and-analysis-sop.md)。

#### 2. 新增記錄或更新記錄單元格

一條 Record 是 `{欄位名或 field_id: CellValue}`，常見 CellValue：

{{CODE:5}}

附件使用專用 shortcut 上傳、下載或移除。created_at, updated_at, created_by, updated_by, auto_number, formula, lookup 型別欄位只讀，若誤寫入單元格會返回 `ignored_fields` 表示這些欄位被靜默過濾，其餘欄位正常寫入。

{{CODE:6}}

大 payload 可用指令碼生成 json 後用 `--json @file.json`。單批最多 200 條，超過後分批，同一 Table 序列寫入；並行可能觸發 `1254291` 併發衝突錯誤。

#### 3. 其他 Record 操作

- `+record-delete --base-token <base_token> --table-id <table_id> --record-id <id1> --record-id <id2>` 刪除若干個記錄
- `+record-share-link-create --base-token <base_token> --table-id <table_id> --record-id <id1> --record-id <id2>` 建立記錄分享連結
- `+record-history-list` 查詢單條記錄的變更事件，讀取 [歷史記錄協議](references/lark-base-record-history-list.md)
- 附件必須使用 `+record-upload-attachment` / `+record-download-attachment` / `+record-remove-attachment` 操作。

### View

View 共享 Table 的底層記錄；沒有特殊展示需求時優先使用 `grid`。讀取已有檢視用 `+view-list` / `+view-get`。

**所有 View 編輯前必讀 [View 型別與生命週期](references/lark-base-view.md)**，包括建立、改名、配置修改（篩選、排序、分組、欄位顯隱、時間條、卡片）和刪除。檢視選型、適用配置及完整操作示例統一在該 reference 中。

### Form

Form 依附於 Table，以 Field 作為題目，每次有效提交會建立一條 Record，適合資訊收集、外部填寫、條件題目和附件提交。

1. **讀取 Table 中的表單配置：** 使用 `+form-list` / `+form-get` 讀取表單，使用 `+form-questions-list` 讀取題目配置；這些命令使用表單所屬的 `base_token + table_id`。
2. **建立或修改 Table 中的表單配置：** 使用 `+form-create` / `+form-update` / `+form-delete` 管理表單；題目由 Table Field 承載，question ID 對應 `field_id`，建立和更新分別讀取 [questions create](references/lark-base-form-questions-create.md) / [questions update](references/lark-base-form-questions-update.md)，刪除使用 `+form-questions-delete`。
3. **調整表單題目顯隱和順序：** Form 在 `visible_fields` 介面中作為 View，`form_id` 傳給 `--view-id`。用 `+view-get-visible-fields` 讀取當前可見題目，再用 `+view-set-visible-fields` 提交最終需要展示的完整有序題目 ID 列表；省略當前可見題目會隱藏它，加入已有隱藏 Form 成員會重新展示，空列表會隱藏全部題目。目標只能包含已有 Form 成員；仍顯示題目的 `visible_rule` 只能引用位於它之前的可見題目。
4. **管理表單分享：** 使用 `+form-share-get` / `+form-share-update` 管理啟停、訪問範圍和匿名/登入要求；更新前先讀取現狀，每次只修改一個欄位，布林值顯式傳 `true` 或 `false`。
5. **填寫分享表單並提交：** 對錶單分享連結使用 `+url-resolve` 取得 `share_token`，按 [Form detail](references/lark-base-form-detail.md) 執行 `+form-detail` 讀取真實題目、必填項和顯示條件，再按 [Form submit](references/lark-base-form-submit.md) 構造欄位與附件並執行 `+form-submit`。

表單題目和欄位的關係：

- `+form-questions-create` 支援兩種形態：新建欄位題目需要 `title` + `type`；已有欄位題目需要 `use_existing_field:true` + `field_id`。已有欄位題目只是把該欄位加入表單，不建立新欄位，也不改變已有記錄資料；不要給該形態攜帶 `type`、`style`、`options` 等欄位定義屬性。
- 建立問題前先 `+form-questions-list`。若目標標題已經存在，除非使用者明確要求同名獨立問題，否則優先用 `+form-questions-update` 修改題目配置，不要先建立同名問題再刪除舊問題。
- `+form-questions-delete` 是高風險寫操作。預設會刪除承載問題的底層 Field 及該欄位所有記錄資料；只想把題目移出表單並保留欄位/資料時必須傳 `--keep-field`。保留欄位後可用 `+form-questions-create --questions '[{"use_existing_field":true,"field_id":"<field_id>"}]'` 加回表單。

## Dashboard Block

Dashboard Block 是 Base Block 樹中的儀表盤容器，負責承載頁面主題、佈局和內部元件集合，本身不表示某一項圖表資料。使用 `+dashboard-list` 定位容器，`+dashboard-get` 讀取容器資訊，`+dashboard-update` 修改主題，`+dashboard-arrange` 統一編排內部元件佈局。

**管理 Dashboard 分享：** 使用 `+dashboard-share-get` / `+dashboard-share-update` 管理啟停、訪問範圍和返回源 Base 入口；更新前先讀取現狀，每次只修改一個欄位，顯式 `false` 會被保留。

容器內部的圖表、指標卡和文字等元件在 Dashboard API 中也稱為 Block，但不屬於 Base Block 樹。內部 Block 分為三條操作路徑：

1. **讀取配置：** `+dashboard-block-list` / `+dashboard-block-get` 讀取元件型別、佈局和 `data_config`；文字元件的正文也屬於配置。
2. **寫入配置：** `+dashboard-block-create` / `+dashboard-block-update` / `+dashboard-block-delete` 管理元件，`data_config` 定義資料來源、維度、指標、聚合或文字內容。
3. **讀取內容：** `+dashboard-block-get-data` 讀取圖表、指標卡等資料元件的計算結果。

操作內部 Block 前先讀 [Dashboard](references/lark-base-dashboard.md)，由該入口繼續路由元件配置和結果協議。

## 應用模式與 Workspace 心智模型

Workspace 是組織 Base 和 BaseApp 的空間容器；BaseApp 建立時必須歸屬一個 Workspace。BaseApp 用 Page 組織介面，每個 Page 包含圖表、列表或富文字元件；元件透過 `data_config` 引用 Base 資料，但不會改變 Base、Table、Field 和 Record 的歸屬關係。Workspace 負責資源歸屬，App 負責頁面和元件，Base 負責資料。

1. **Workspace：** 使用 `+workspace-create`、`+workspace-entity-list` 和 `+workspace-move-in` 建立目錄、列出其中的 Base/BaseApp 或移入資源。
2. **應用：** 使用 `+app-create` / `+app-get`；應用查詢和建立依賴真實 `app_token` / `workspace_token`。
3. **頁面：** 使用 `+app-page-list/get/create/rename/delete` 管理 Page。
4. **元件：** 使用 `+app-block-list/get/create/update` 讀寫元件配置，使用 `+app-block-get-data` 讀取元件計算結果。

BaseApp、Workspace、Page 或元件任務開始前完整讀取 [應用模式與 Workspace](references/lark-base-app.md)；構造元件 `data_config` 時繼續讀取 [應用元件配置](references/lark-base-app-block-data-config.md)。BaseApp 不走 `lark-apps`。當前不支援 BaseApp 複製、Page 完整複製、頁面圖示以及從 Workspace 移出資源；遇到這些目標按 reference 的能力邊界處理，不以新建空物件或 Drive 移動冒充。

- BaseApp（應用模式）中的 Page 和元件使用 `app_token` / `page_id` / `block_id`，表、欄位和記錄仍使用元件所引用 Base 的 `base_token`；不要混用 token 或把 BaseApp 當作 Base 的別名。
- 複用現有 BaseApp block 的 `data_config` 只能作為結構模板，首次 Create/Update 前仍要逐項對齊使用者顯式要求；使用者要求排序時必須顯式寫 `group_by[].sort.order` 或頂層 `sort.order`，不能用舊配置省略的方向或當前 `get-data` 結果順序代替。
- 應用頁面的 block 與儀表盤 block 是同一套底層實體，但 ID 體系不通用；按當前模組 reference 選擇命令和配置協議。

## Workflow Block

Workflow 本身是 Base Block，其內部是一張由 `next` / `children` 連線的 steps 執行圖；觸發器、動作、條件分支和迴圈都是 step 型別。它適合定時執行、Record 新增或變更聯動、訊息通知、記錄讀寫和跨系統呼叫。Workflow 分為三條操作路徑：

1. **讀取配置：** `+workflow-list` 定位流程，`+workflow-get` 讀取 `title`、`status` 和完整 `steps` 執行圖。
2. **寫入配置：** `+workflow-create` 建立完整定義，`+workflow-update` 更新完整定義；構造或修改配置前讀取 [Workflow](references/lark-base-workflow.md)，由該入口繼續路由 step 型別和 schema。
3. **執行狀態控制：** `+workflow-enable` / `+workflow-disable` 啟用或停用已有 Workflow，不修改 steps 執行圖。

## Advanced Permission（AdvPerm）

AdvPerm 為 Base 開啟細粒度許可權模式；Role 在此基礎上配置 Base、Table、View、Field、Record、Dashboard 和 Docx 等資源的訪問能力，適合按團隊或職責限制可見範圍、編輯能力、複製下載和資料訪問規則。

**讀取 AdvPerm：** `+base-get` 檢視 `is_advanced`，`+role-list` / `+role-get` 檢視角色。**寫入 AdvPerm：** `+advperm-enable` / `+advperm-disable` 啟停高階許可權，`+role-create` / `+role-update` / `+role-delete` 管理角色。先讀 [許可權與角色](references/lark-base-advanced-permission-and-role.md)，由該入口繼續路由許可權 JSON 協議。

## Docx Block

Docx Block 是組織在 Base 目錄中的飛書文件資源，適合把說明、方案和報告與資料表、儀表盤及流程放在同一 Base 中；正文仍使用標準 Docx 資料模型。

從 Base Block 資源目錄按 `--type docx` 定位文件並取得 `docx_token`；正文讀取、建立與編輯使用 `lark-doc`。

## Folder Block

Folder Block 只承擔 Base 目錄分組和層級組織。用 `+base-block-list --parent-id <folder_block_id>` 讀取直接子項。

## 通用執行契約

- Update 先確認命令是完整替換還是 delta：完整替換使用可信當前配置做 read-modify-write，delta 只提交目標變更。
- 優先用寫入返回確認結果；返回不足以確認或任務明確要求核驗時再讀回目標。
- 命令具有 confirmation gate 時，確認目標和影響後使用 `--yes`。

## 不在本 Skill 範圍

- 認證、初始化、scope、身份切換和授權恢復 → `lark-shared`
- Excel、CSV、`.base` 等本地檔案與 Base 之間的匯入/匯出轉 `lark-drive`；線上複製走 `+base-copy`
- Base 內嵌 Docx 的正文編輯 → `lark-doc`；電子表格內容操作 → `lark-sheets`
