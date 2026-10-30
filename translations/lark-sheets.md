<!--meta
{"title": "飛書電子表格", "category": "文件與辦公", "tags": ["飛書", "Lark", "電子表格", "lark-cli"], "summary": "原文為簡體中文，已轉為繁體。透過 lark-cli 建立與操作飛書電子表格：工作表與列欄結構、儲存格讀寫（值、公式、樣式、註解、圖片）、排序篩選、尋找取代、圖表、樞紐分析表、條件格式、下拉選單、公式驗證、版本回溯，以及本機 Excel／CSV 的匯入匯出；也適用於財務建模（DCF、三表、預算、敏感度分析）。", "usage": "- 需安裝 `lark-cli`，並先閱讀 `lark-shared` 技能完成認證\n- 說「在飛書建立一張預算表」「把這個 Excel 匯入飛書表格」「幫這張表加條件格式」\n- 多維表格（Base）請改用 lark-base；搜尋雲端檔案用 lark-drive\n- 給 doubao.com 的 /sheets/ 連結也適用"}
-->
---
name: lark-sheets
version: 3.5.2
description: "飛書電子表格：建立和操作電子表格。支援工作表與行列結構（增刪/合併/尺寸/隱藏/凍結/分組）、單元格讀寫（值/公式/樣式/批註/單元格圖片）、區域複製移動排序填充、查詢替換、批次更新，圖表、透視表、條件格式、篩選器與篩選檢視、下拉選單、迷你圖、浮動圖片等物件的建立與維護，以及公式校驗、歷史版本回滾、本地 Excel/CSV 與飛書表格的匯入匯出。當使用者需要建立或編輯表格、統計彙總與視覺化、表格美化、公式計算（含 Excel 公式遷移）、金融/財務建模（DCF、三張表、預算、Sensitivity 等）時使用。多維表格（Base/bitable）請改用 lark-base；若使用者是想按名稱或關鍵詞搜尋雲空間（雲盤/雲端儲存）裡的表格檔案，請改用 lark-drive 的 drive +search 先定位資源。當使用者給出 doubao.com 的 /sheets/ URL/token 時，也應直接使用本 skill，不要因為域名不是飛書而回退到 WebFetch；路由依據是 URL 路徑模式和 token，而不是域名。"
metadata:
  requires:
    bins: ["lark-cli"]
    siblings: ["lark-shared"]
  cliHelp: "lark-cli sheets --help"
---

# sheets

**CRITICAL — 開始前 MUST 先用 Read 工具讀取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含認證、許可權處理。**

## 場景 → 命令速查

> 按當前動作選行；下一步必須 Read 該行 reference，讀取完成前不得執行命令。只讀命中的文件；含公式 / 樣式等橫切動作時再讀對應規範，禁止用目錄列舉代替 Read。

| 你要做的事 | ✅ 正確寫法 | 動手前讀（先 Read 再動手） |
| --- | --- | --- |
| 讀資料 | `+csv-get`（純值/CSV）、`+cells-get`（公式/樣式/批註） | 讀 `references/lark-sheets-read-data.md` |
| 寫入資料 | `+csv-put`（無型別歧義純文字）、`+table-put`（typed；量值/真日期；標籤/編號/前導零/文字數字用 object，禁裸 csv-put）、`+cells-set`（公式/富寫入）、`+cells-set-style`（樣式）、`+cells-set-image`（單元格圖片） | 讀 `references/lark-sheets-write-cells.md` |
| 格式繼承（新列/新行） | 物理插行 / 插列用 `+dim-insert --inherit-style before\|after`；往已有空白區域擴寫用 `+range-copy --paste-type formats` 先鋪樣式再寫值 | 讀 `references/lark-sheets-range-operations.md`；插行插列再讀 `references/lark-sheets-sheet-structure.md` |
| 工作簿操作 | `+workbook-create`、`+workbook-info`、`+workbook-import`、`+sheet-copy`、`+revision-get`、`+workbook-export` | 讀 `references/lark-sheets-workbook.md` |
| 行列操作 | 排序用 `+range-sort` 原子移動整行；合併 / 取消合併用 `+cells-merge` / `+cells-unmerge`；清空內容才用 `+cells-clear`；尺寸用 `+cols-resize` / `+rows-resize` | 讀 `references/lark-sheets-range-operations.md`；涉結構佈局再讀 `references/lark-sheets-sheet-structure.md` |
| 美化收尾 | `+styles-put` | 讀 `references/lark-sheets-styles-put.md` |
| 子表結構 | `+sheet-info`、`+dim-insert`；刪整行 / 列用 `+dim-delete`，不能用 clear 代替 | 讀 `references/lark-sheets-sheet-structure.md` |
| 畫圖表 / 視覺化 / 柱狀圖 / 折線圖 / 餅圖 / 趨勢 / 佔比 | 單圖用 `+chart-create-basic`，多圖用扁平輸入的 `+batch-chart-create`；改已有圖的資料來源用 `+chart-data-update`、配置用 `+chart-config-update`；只有語義 shortcut 表達不了的單系列 / 單資料點 / 高階欄位才用 `+chart-create` / `+chart-update`，且只提交必要的區域性 properties。動手前先斷言每張圖的型別、橫軸欄位、分組欄位和目標張數，畫完 `+chart-list` 逐項核；圖片遷移成真圖表後刪除並複查原浮動圖片 | 讀 `references/lark-sheets-chart.md`；含透視 / 分組彙總再讀 `references/lark-sheets-pivot-table.md` |
| 分組彙總 / 透視 | `+pivot-create` | 讀 `references/lark-sheets-pivot-table.md` |
| 篩選 / 只看符合條件的行 | `+filter-create` | 讀 `references/lark-sheets-filter.md` |
| 查詢 / 替換文字 | `+cells-search`、`+cells-replace` | 讀 `references/lark-sheets-search-replace.md` |
| 條件格式 / 條件高亮 / 資料條 / 色階 | 隨資料變化的標色用 `+cond-format-create`；固定刷色只用於使用者點名要靜態著色 | 讀 `references/lark-sheets-conditional-format.md` |
| 插圖：自由擺放的裝飾 | `+float-image-create` | 讀 `references/lark-sheets-float-image.md` |
| 迷你圖 / 單元格內趨勢線 | `+sparkline-create` | 讀 `references/lark-sheets-sparkline.md` |
| 批次清除多區域 | `+cells-batch-clear` | 讀 `references/lark-sheets-batch-update.md`（high-risk） |
| 複核編輯變更 / 取版本間差異 | `+changeset-get` | 讀 `references/lark-sheets-changeset.md` |
| 儲存多份篩選狀態 / 命名篩選檢視 | `+filter-view-create`；檢視與 `+filter-create` 相互獨立、可在同一子表共存 | 讀 `references/lark-sheets-filter-view.md` |
| 查編輯歷史 / 回滾到歷史版本 | `+history-list` 取版本，`+history-revert`（high-risk，非同步）回滾後用 `+history-revert-status` 輪詢 | 讀 `references/lark-sheets-history.md` |

> ⚠️ 金額 / 百分比 / 比率 / 計數及參與運算的真日期寫數字（百分比傳 `0.4` + `number_format`）；日期標籤、編號、前導零、身份證 / 單據號寫文字。`--range` 只寫 `A1:B2`，子表另傳 `--sheet-id` / `--sheet-name`。

## 飛書表格編輯準則

1. **最小改動**：使用者沒點名要刪 / 改名 / 隱藏時，已有 Sheet 一張不動；補齊只寫空格，未要求調整的值 / 結構 / 格式不動。
2. **目標子表與回讀斷言**：先確認真實末行與目標區域；未點名子表時只從 `resource_type=sheet && is_hidden=false` 的可見網格候選裡選，唯一才自動使用，多張不得按 index 猜。涉及"所有 / 每個 sheet"（跨表彙總、批次清洗、合併多張子表）時先 `+workbook-info` 列全再逐個處理，別隻做前幾張。寫後用 `+csv-get` / `+cells-get` / `+<物件>-list` 驗首、中、末及使用者點名項——返回 `ok` 只表示請求成功。純 CSV 回寫前去掉 `annotated_csv` 的 `[row=N] ` 字首，`cells-get` 的樣式欄位與值分開處理，公式必須回讀 `formula`。**樣式同樣要回讀**：寫過邊框 / 底色 / 字型色 / 數字格式 / 行高列寬 / 凍結的，收尾用 `+cells-get --include style` 或 `+sheet-info` 抽查目標區域首、中、末格確認屬性真的在——寫入返回 `ok` 不代表樣式落上了；缺的整份重發（樣式是冪等蓋章，重發無副作用）。
3. **公式閉環**：可推導值寫落格公式，不用靜態值代替——用 Python 算好數值再寫進單元格，交付的是改輸入不重算的死表；Python 只用於推導和驗證，落進單元格的必須是引用其他格的公式。寫前確認欄位語義、閾值邊界（以上/至少=`>=`，超過/大於=`>`）、單位/時區和完整源範圍，選首中末、空值、邊界及一條可手算記錄作哨兵；寫後逐段 `+formula-verify --exit-on-error`，各段 `status='success'` 且哨兵值正確才算完成（AI 公式例外：非同步計算，改用 `+formula-verify --ai-only` 對整個寫入區間做一次非同步狀態檢查，不用 `+cells-get` 輪詢結果，`failed` 清零後即使仍有 pending 也可交付並說明）；試錯 3 次仍失敗可降級靜態值，交付說明寫明「靜態值 + 失敗原因 + 不隨源資料更新」。
4. **完整繼承樣式**：新增行列時禁止只讀值只寫值——原表字型、對齊、底色（含奇偶行交替）、四邊框都延續到新區域。**物理插入行 / 列**用 `+dim-insert --inherit-style before|after`（原生繼承，比補刷可靠）；**往已有空白區域擴寫**（如在資料右側加新列）用 `+range-copy --paste-type formats` 先鋪樣式再寫值；兩者都表達不了的非規則樣式，才用 `+cells-get --include style` 讀源區樣式隨值寫回。無論走哪條路徑，插入後都另查行高列寬（行高不隨樣式繼承，插行填長文字前補 `+rows-resize`）、合併與跨列標題並補齊。詳見 `references/lark-sheets-write-cells.md`。
5. **原子操作**：排序用 `+range-sort`，`--range` 覆蓋完整記錄寬度，排序列只寫進 `--sort-keys`；刪除記錄用 `+dim-delete`，清空內容 / 格式才用 `+cells-clear`；禁止讀值後用 `+csv-put` 覆蓋來模擬排序 / 刪除。僅跨型別且有順序依賴時才用 high-risk `+batch-update`。
6. **標色分流**：資料變化後應自動重算的高亮 / 標紅用條件格式，已確定結果的固定標註用靜態樣式，裝飾性美化按視覺規範。兩條路徑取色欄位用同一判據：使用者中文語境下的"標紅 / 染色 / 標記"指**單元格背景色**，"文字紅 / 字型紅 / 把字變紅"才用字型色，預設無說明時選背景色。條件格式建完先 `+cond-format-list` 驗規則與範圍，再 `+cond-format-result-get` 抽查哨兵格命中樣式。
7. **產物可核對**：使用者點名的 sheet 名與數量、表頭、標題、圖例、檔名、口徑逐字保留；回覆中每項“已完成”都能定位到產物，缺口逐項宣告。
8. **替換與新增**：批次替換 / 刪除後搜尋確認無殘留；新增列要有表頭，單位 / 口徑另置，不佔原表頭或資料格。
9. **不編造**：表外資料須有可核驗來源，不用常識或名稱推斷偽造公司、標準值、行情或法規引數；**沒有來源就留空**——憑記憶填的數值大機率與真實值對不上，比留空更糟。留空的格在交付說明裡逐項列出格址與缺的來源，不要只寫一句"部分資料缺失"。

> 🤖 **文字類 NLP 任務首選 AI 公式，別預設退回手工 / Python**：只要對文字列做**翻譯 / 情感 / 分類打標籤 / 資訊提取 / 總結 / 潤色**等 NLP，飛書線上表格上優先用原生 `=AI(prompt, range)` 逐列鋪開（寫法與普通公式一致，見 `references/lark-sheets-formula-translation.md`），一次落表隨行自動計算，比逐條讀 → 手工判斷 → 回寫 / Python 調模型再寫靜態值都更省事。**判定標準是「逐行獨立」**：每個目標單元格只依賴同一行輸入即為逐行獨立，**資料量（哪怕 1 萬 +）、分批、判斷複雜度都不改變該判定**——大資料量下 AI 公式仍是首選，分批只改公式鋪設的批次大小（行數很多時按批序列，量級參考每批幾百到一千行），不得改為「用 Python 或規則指令碼生成語義結果後靜態寫回」；Python 只能做清洗 / 行號對映 / 構造公式批次，不得讀源文字生成目標語義值。只有單個結果依賴多行輸入的跨行任務才走非公式路線。AI 公式非同步計算，寫完先對種子格 / 首格做**一次** `+cells-get --include formula` 核對文字，隨後**第一校驗入口必須是** `+formula-verify --ai-only --range <整個寫入區間>`，禁止用 `+cells-get` 輪詢計算結果；判據為 `ai_formula_failed_count == 0`（`--range` 只透傳給後端、不保證收窄彙總口徑，按返回的單元格定位核對本次區間，別拿總數對預期條數），滿足後即使仍有 pending 也可交付，並告知使用者"AI 公式仍在後臺執行"。

> 流程：瞭解結構 →（未點名時先按 visible_grid selection 定位）→ 讀資料 → 原生工具寫入 → 按使用者點名項回讀驗證 → 線上交付。整理 / 美化 / 加彙總行這類會改變表長或版式的任務，收尾把表頭行凍住（原表已有凍結設定的不動）。xlsx 驗收只在處理本地 xlsx、或使用者點名要本地 xlsx / 下載 / 列印時跑。
## References

reference 分兩組：先讀**通用方法與規範**（橫切所有任務的樣式 / 公式規則），再按操作物件進入**工具參考**查具體 shortcut。編輯類任務務必先過通用方法與規範，連同上方「飛書表格編輯準則」對所有工具參考一律生效。

### 通用方法與規範（先讀，橫切所有任務，不含具體 shortcut）

| Reference | 描述 |
| --- | --- |
| [飛書表格樣式與配色規範](references/lark-sheets-visual-standards.md) | 飛書表格樣式與配色規範：表頭/資料區/彙總行的顏色、字號、對齊、邊框、數字格式等取值標準，以及從零新建表格的版式美化、新增彙總行、追加行列繼承原表風格、已有區域美化等典型場景的決策流程與樣式要點。工具呼叫引數細節請參考對應的 lark-sheets-write-cells / lark-sheets-range-operations / lark-sheets-batch-update。條件格式（高亮、標紅、資料條、色階）請使用 lark-sheets-conditional-format。 |
| [飛書表格公式生成規則](references/lark-sheets-formula-translation.md) | Excel 公式到飛書表格公式的遷移與生成規則。核心目標不是保留 Excel 原語法，而是按飛書表格可執行規則重寫公式，並在結果上儘量對齊 Excel。當使用者要求把 Excel 公式改寫成飛書表格公式，或需要生成飛書公式（尤其涉及 ARRAYFORMULA、陣列語義與逐行填充、原生陣列函式、INDEX/OFFSET、MAP/LAMBDA、日期差、多層範圍結果與二次展開）時使用。本文負責把公式寫對；落表後必須用 `references/lark-sheets-formula-verify.md` 對本次公式範圍逐段診斷。 |

### 按物件的工具參考（含 shortcut）

| Reference | 描述 |
| --- | --- |
| [Lark Sheet Formula Verify](references/lark-sheets-formula-verify.md) | 公式寫入 / 批次填充 / `--copy-to-range` 擴充套件 / 匯入含公式工作簿後的完成檢查。普通公式按本次新增或修改範圍逐段掃描，合併編譯失敗與 7 類執行錯誤；`partial` 繼續拆分，全部 `status='success'` 後完成。AI 公式用 `--ai-only` 對整個寫入區間做一次非同步狀態檢查，pending 可說明後交付。 |
| [Lark Sheet Workbook](references/lark-sheets-workbook.md) | 管理飛書表格的工作簿結構（子表列表及後設資料）。當使用者提到"看看這個表格有什麼"、"表格結構"、"有哪些 sheet"、"新建一個 sheet"、"刪除這個工作表"、"重新命名"、"複製一份"、"移動到前面"時使用。 |
| [Lark Sheet Sheet Structure](references/lark-sheets-sheet-structure.md) | 管理飛書表格的子表結構與佈局：檢視行高列寬、隱藏、合併、凍結與分組，並執行插入/刪除/移動行列等物理結構操作。資料分組統計走 lark-sheets-pivot-table。普通表尾追加優先用 lark-sheets-write-cells 的 `+table-put --mode append` 自動定位末行；只有使用者明確要求物理插入行列、繼承模板結構或擴容佈局時才先用本 reference。 |
| [Lark Sheet Read Data](references/lark-sheets-read-data.md) | 讀取飛書表格中的單元格資料。當使用者需要"看看資料"、"分析資料"、"統計/彙總"時使用；也適用於需要檢視公式、樣式、批註等詳細資訊的場景。 |
| [Lark Sheet Search & Replace](references/lark-sheets-search-replace.md) | 在飛書表格中搜尋和替換文字，支援限定範圍、大小寫匹配、精確匹配、正規表示式。當使用者需要"查詢"、"搜尋"、"定位"某個值，或"替換"、"批次修改文字"、"把 A 改成 B"時使用。不要用於理解表格結構（應讀取資料）、不要用於資料分析（應讀取資料後計算）、不要把使用者操作動作中的關鍵詞（如"彙總金額""統計數量"）當作搜尋詞。 |
| [Lark Sheet Write Cells](references/lark-sheets-write-cells.md) | 向飛書表格指定區域批次寫入值、公式、樣式、批註或單元格圖片。純文字可用 `+csv-put`；金額、百分比、日期、布林、計數和後續參與聚合的列用 `+table-put` 並顯式宣告 dtypes/formats；公式或富欄位用 `+cells-set`。追加資料可直接使用 `+table-put --mode append`；只有明確需要物理插行/列時才先走 lark-sheets-sheet-structure。公式落表後必須執行 lark-sheets-formula-verify。 |
| [Lark Sheet Range Operations](references/lark-sheets-range-operations.md) | 對飛書表格中指定區域執行結構性操作（不涉及寫入單元格資料值）。適用場景：清除內容或格式（"清空"、"刪除內容"、"去掉格式"）、合併/取消合併單元格、調整行高列寬（"加寬列"、"自適應列寬"）、移動/複製/填充/排序資料（"移動資料"、"複製到"、"自動填充"、"按某列排序"）。寫入單元格資料請使用 lark-sheets-write-cells。 |
| [Lark Sheet Styles Put](references/lark-sheets-styles-put.md) | 把一份宣告式視覺規格（樣式/邊框/合併/行高列寬/凍結）一次性應用到已有飛書表格的多個子表，整份規格一次提交。當任務是對存量表做美化收尾、批次刷樣式、統一版式時使用。樣式取值標準見 lark-sheets-visual-standards；建新錶帶樣式走 lark-sheets-workbook（+workbook-create --styles）、寫資料同步帶樣式走 lark-sheets-write-cells（+table-put --styles），三者共用同一份 --styles 詞彙。僅針對飛書表格。 |
| [Lark Sheet Batch Update](references/lark-sheets-batch-update.md) | 將多個飛書表格寫入操作合併為一次批次執行，按順序依次完成。適合需要連續執行多個寫入操作的場景（如先修改結構再寫入資料）。 |
| [Lark Sheet Chart](references/lark-sheets-chart.md) | 管理飛書表格中的圖表（柱形圖、折線圖、餅圖、條形圖、面積圖、散點圖、組合圖、雷達圖等）。當使用者需要建立圖表、修改圖表樣式或資料來源、檢視已有圖表配置、刪除圖表時使用。也適用於使用者提到"資料視覺化"、"畫個圖"、"趨勢分析"、"對比圖"、"佔比分析"、"做個圖表"等資料視覺化相關場景。 |
| [Lark Sheet Pivot Table](references/lark-sheets-pivot-table.md) | 管理飛書表格中的資料透視表。當使用者需要建立透視表、修改透視表的行列欄位/聚合方式/篩選條件、檢視已有透視表配置、刪除透視表時使用。也適用於使用者提到"分組彙總"、"交叉分析"、"按XXX統計"、"按欄位分組"、"再分下組"、"多維分析"、"資料透視"等場景。 |
| [Lark Sheet Conditional Format](references/lark-sheets-conditional-format.md) | 管理飛書表格中的條件格式規則（重複值高亮、單元格值比較、資料條、色階、排名、自定義公式等）。當使用者需要建立條件格式、修改已有規則的範圍或樣式、檢視當前條件格式配置、刪除規則時使用。也適用於使用者提到"高亮"、"標紅"、"顏色標記"、"資料條"、"色階"、"條件樣式"等場景。 |
| [Lark Sheet Filter](references/lark-sheets-filter.md) | 管理飛書表格中的篩選器（filter）。當使用者需要篩選資料（按文字/數值/顏色/日期條件過濾行）、檢視已有篩選配置、修改或刪除篩選器時使用。也適用於"只看"、"篩選出"、"僅保留符合條件的"等場景。 |
| [Lark Sheet Filter View](references/lark-sheets-filter-view.md) | 管理飛書表格中的篩選檢視（filter view）。當使用者需要"建一個 XX 檢視"、"儲存這個篩選狀態"、"切換不同篩選"、維護一個 sheet 上多份獨立篩選配置時使用。檢視與篩選器（filter）相互獨立，可在同一 sheet 共存；檢視的隱藏行僅在使用者進入該檢視時本地生效，不影響其他協作者。 |
| [Lark Sheet Sparkline](references/lark-sheets-sparkline.md) | 管理飛書表格中的迷你圖（折線迷你圖、柱形迷你圖、勝負迷你圖）。當使用者需要在單元格內嵌入小型圖表來展示資料趨勢時使用。也適用於"趨勢線"、"單元格內圖表"、"迷你圖"等場景。注意：不等同於被禁用的 SPARKLINE() 公式函式。 |
| [Lark Sheet Float Image](references/lark-sheets-float-image.md) | 管理飛書表格中的浮動圖片。當使用者需要在表格中插入浮動圖片、調整圖片位置和大小、檢視已有浮動圖片、刪除圖片時使用。也適用於"插入圖片"、"新增 logo"、"放一張圖"等場景。注意：如果使用者需要將圖片嵌入到某個單元格內部（單元格圖片），請閱讀 lark-sheets-write-cells。 |
| [Lark Sheet History](references/lark-sheets-history.md) | 查詢飛書表格的歷史版本並回滾到指定版本。當使用者需要檢視一張表的編輯歷史版本列表、回滾到某個歷史版本、或查詢回滾的非同步狀態（進行中/成功/失敗）時使用。回滾為非同步操作，發起後透過狀態查詢輪詢結果。僅針對飛書表格。 |
| [Lark Sheet Changeset](references/lark-sheets-changeset.md) | 讀取兩個版本（CS revision）之間的 changeset（原始變更操作清單），用於複核某次編輯——尤其是 AI 編輯——是否真實滿足使用者訴求。傳入起始版本（編輯前基線），可選結束版本（省略取最新），版本差上限 20；返回裡最外層帶當前表格最新版本號。當使用者需要"看看這次改了什麼"、"核對 AI 改動"、"對比兩個版本的變更"時使用。 |

## 公共 flag 速查

各 reference 的 shortcut 標題下用一行徽章標註支援的公共 / 系統 flag（如 `_公共四件套 · 系統：--dry-run_`）。type / 必填 / 描述在本段統一宣告：

### 公共 flag（定位資源）

**公共四件套** = `--url` / `--spreadsheet-token` / `--sheet-id` / `--sheet-name`，分成兩組 XOR，**每組都必須給且只能給一個**（XOR = 二選一必填，不是"可選"）——`spreadsheet` 指工作簿、`sheet` 指子表；條件格式 / 圖表 / 篩選檢視 / 透視表 / 迷你圖 / 浮動圖片這類物件在四件套之外另用各自的 `--*-id` 定位：

1. **spreadsheet 定位（必填）**：`--url`（解析 `/sheets/`、`/spreadsheets/`、`/wiki/` 三種連結；wiki 連結自動定位背後的電子表格）與 `--spreadsheet-token`（裸 token）二選一。**例外**：`+workbook-create` / `+workbook-import` 產出**還不存在**的表，不接受任何定位 flag。
2. **sheet 定位（公共四件套 shortcut 必填）**：`--sheet-id` 與 `--sheet-name` 二選一。
   - ⚠️ **不確定 sheet 名時禁止猜 `Sheet1`**：除非對話或上下文已出現具體值，第一步先 `+workbook-info` 拿 `sheets[].sheet_id/title` 再選——中文表的子表常叫"資料"/"工作表 1"/業務名，猜名大機率撞 `sheet not found`。
   - ⚠️ **`--range` 裡的 `Sheet1!` 字首不能替代 sheet 定位**：仍必須傳 `--sheet-id` / `--sheet-name`。
   - ⚠️ **A1 引用含 `!` 時整段用單引號包裹**（`--range 'Sheet1!A1:B2'`，擋 bash history expansion；別用 `set +H`，sh/dash 下非法）。sheet 名要在 A1 裡內層再包單引號時用 `'\''` 轉義。
   - **例外**：徽章標 `_公共：URL/token（無 sheet 定位）…_` 的 shortcut 不接受 sheet 定位——工作簿級（`+workbook-info` / `+sheet-list` / `+sheet-create` / `+revision-get` / `+changeset-get` / `+history-list|revert|revert-status`）、批次與整表級（`+batch-update` / `+batch-chart-create|update` / `+cells-batch-clear` / `+styles-put` / `+dropdown-update|delete`），以及子表名寫在 payload 裡的 `+table-put`。`+workbook-export` 只接 `--sheet-id`（無 `--sheet-name`），`+pivot-create` 用 `--target-sheet-id/name`（XOR，可都不傳）。徽章是判據，本行只是速記。

{{CODE:1}}

### 系統 flag

| Flag | Type | 必填 | 說明 |
| --- | --- | --- | --- |
| `--dry-run` | bool | 否 | 零副作用：僅列印請求路徑與引數模板，不發起呼叫 |
| `--yes` | bool | 是（僅 `high-risk-write`） | 二次確認；不帶時退出碼 10。詳見 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 高風險審批協議 |
| `--print-schema` | bool | 否 | 寫複合 JSON flag 前結構不確定就先跑它：本地列印 Schema 並退出（不發起呼叫、不需要其它 required flag），搭配 `--flag-name` 指定查哪個 flag，省略時列出該 shortcut 可查的 flag。只有含複合 JSON flag 的 shortcut 支援。 |
| `--flag-name` | string | 否 | 配合 `--print-schema`：flag 名不帶 `--` 字首（`cells` / `properties`）。**支援點分路徑切片**：`--flag-name properties.snapshot.plotArea.axes` 只列印該子樹，大 schema（chart 的 properties 約 1700 行）按需取，別整篇翻頁。 |

> **bool flag 語法**：開啟可用裸 `--flag`；顯式值只用 `--flag=true` 或 `--flag=false`，不得用空格分隔。

> ⚠️ **high-risk-write 命令清單（exit 10 強確認門禁）**：`+batch-update`、`+cells-clear`、`+cells-batch-clear`、`+sheet-delete`、`+dim-delete`、`+dropdown-delete`、`+history-revert`（整表回滾到歷史版本），以及各物件刪除 `+chart-delete` / `+pivot-delete` / `+cond-format-delete` / `+filter-delete` / `+filter-view-delete` / `+sparkline-delete` / `+float-image-delete`。
>
> **審批協議**：先 `--dry-run` 預覽、向使用者展示將執行的操作與影響範圍，**獲得使用者明確同意後**再在原命令追加 `--yes` 執行。未經使用者同意不得帶 `--yes`，也不得在 exit 10 後靜默補 `--yes` 重試——那等於禁用門禁。完整協議見 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)。

**Schema 的邊界**：`--print-schema` 列印的是 flag 值的內部結構，flag 描述要求外層信封時（如 `--sheets` 的 `{"sheets":[…]}`）schema 裡看不到那層，按描述補上；reference 的 `## Schemas` 段也只給一層。圖表直接 `+chart-create --print-example <type>` 拿最小可用模板改參。

### flag 內容型別與輸出約定（術語速記）

- JSON 類入參分三類：**複合 JSON** = 深層巢狀物件（`--print-schema` 可查）；**簡單 JSON** = 一二維標量陣列；**非 JSON 文字** = 原樣文字（如 CSV）。
- **envelope**：所有 shortcut 返回統一外層 `{ok, identity, data, ...}`；寫操作不會自動回讀，校驗自行呼叫 `+*-list` / `+*-get` / `+cells-get`。
- **大 payload 走檔案 / stdin，不在命令列內聯**：Type 標 `File + Stdin` 的 flag 支援 `--flag "@./x.json"`（`@file` 只接受 cwd 下相對路徑，絕對路徑被拒）與 `--flag -`（stdin）；payload 含換行 / 引號或體量大時一律落檔案。**stdin 每次呼叫只能給一個 flag**——`+table-put` 的 `--sheets` 與 `--styles` 都是大 JSON 時，一個走 `-`、另一個走 `@./x.json`。臨時檔案不要落進使用者專案目錄。
- **非 POSIX shell（PowerShell / cmd.exe）適配**：本 skill 全部 `bash` 程式碼塊（heredoc `<<'JSON'`、單引號轉義 `'\''`）只適用於 bash / zsh，動手前先判斷當前 shell，非 POSIX 環境按下表改寫，**不要試錯式改引號**——`@file`（cwd 相對路徑）是全平臺無引號問題的兜底形態：

| 形態 | bash / zsh | PowerShell | cmd.exe |
| --- | --- | --- | --- |
| 大 / 多行 JSON | `--flag - <<'JSON' … JSON` | 先寫 UTF-8 無 BOM 檔案再 `--flag '@./x.json'`，或 `Get-Content -Raw ./x.json \| lark-cli … --flag -` | 先寫檔案再 `--flag @./x.json`（cmd 無 heredoc / 管道讀檔案不可靠） |
| 單行 inline JSON | `--flag '{"a":1}'` | `--flag '{"a":1}'`（PS 單引號同為字面量） | 不要 inline——cmd 會吃掉內層雙引號，一律走 `@file` |
