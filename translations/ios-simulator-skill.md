<!--meta
{"title":"iOS 模擬器自動化","category":"瀏覽器與測試自動化","tags":["iOS","Xcode","模擬器","UI 測試","無障礙"],
"summary":"用 30 支節省 token 的腳本在 iOS 模擬器中建置、測試與操作 App：建置 Xcode 專案並解析結果、以無障礙標籤點擊／輸入／滑動 UI（優先讀無障礙樹而不是截圖）、截圖與視覺比對、無障礙稽核、讀日誌與診斷卡頓（HangBuster）、在地化稽核，以及管理模擬器（開機、清除、權限、定位、推播、外觀、狀態列）。破壞性操作需加 `--yes` 並先詢問你。",
"usage":"- 僅限 macOS（Apple silicon）；需要 Xcode 26+、Python 3.12+ 與 `brew install facebook/fb/idb`\n- 先檢查環境：`bash scripts/sim_health_check.sh`\n- 說「建置並在模擬器跑這個專案的測試」「點登入按鈕並輸入帳號」「稽核這個畫面的無障礙」「找出捲動時卡頓的原因」\n- 所有腳本都支援 `--help`，多數支援 `--json`"}
-->
---
name: ios-simulator-skill
version: 1.7.0
description: 用 30 支節省 token 的腳本，在模擬器中建置、測試並操作 iOS App。在被要求建置或測試 Xcode 專案、在模擬器上啟動 App、依無障礙標籤在 UI 中點擊／輸入／滑動、擷取截圖或視覺差異、稽核無障礙、讀取日誌或診斷卡頓，或管理模擬器（開機、清除、權限、定位、推播、外觀）時使用。僅限 macOS；需要 Xcode、Python 3.12+ 與 idb。
---

# iOS 模擬器技能

使用以無障礙為驅動的導覽與結構化資料（而不是像素座標），建置、測試並自動化 iOS 應用程式。

## 快速開始

{{CODE:1}}

**路徑：** `scripts/` 是相對於包含這份 SKILL.md 的目錄，而不是使用者的專案。範例為了簡潔寫成 `scripts/...`；請從使用者的專案以絕對路徑執行（例如 `python3 <skill-dir>/scripts/navigator.py ...`），讓相對的 Xcode 專案路徑仍然能被解析。

所有腳本都支援 `--help` 查看詳細選項；大多數支援 `--json` 輸出機器可讀的格式。

## 導覽策略

**導覽時一律優先使用無障礙樹，而不是截圖。** 無障礙樹提供元素類型、標籤、框架與點擊目標——比圖片分析更便宜、更可靠的結構化資料。

使用這個優先順序：
1. `screen_mapper.py` → 結構化的元素清單（5–7 行，約 10 個 token）
2. `navigator.py --find-text/--find-type/--find-id` → 語意化的互動
3. 截圖 → 只用於視覺驗證、錯誤回報或視覺比對

截圖依大小需要 1,600–6,300 個 token。無障礙樹在預設模式下只需要 10–50 個 token。

## 30 支正式腳本

### 建置與開發（2 支）

1. **build_and_test.py** —— 建置 Xcode 專案、執行測試，以漸進式揭露解析結果
   - 以即時串流結果的方式建置
   - 從 xcresult 套件解析錯誤與警告
   - 需要時取得詳細的建置日誌
   - 選項：`--project`、`--scheme`、`--clean`、`--test`、`--verbose`、`--json`

2. **log_monitor.py** —— 以智慧過濾即時監控日誌
   - 串流日誌或依時間長度擷取
   - 依嚴重度過濾（error/warning/info/debug）
   - 去除重複的訊息
   - 選項：`--app`、`--severity`、`--follow`、`--duration`、`--output`、`--json`

### 裝置狀態（3 支）

3. **appearance.py** —— 控制模擬器外觀：深色模式、動態字級大小、對比與語系／地區
   - 透過 `xcrun simctl ui` 切換淺色／深色主題
   - 以友善的別名設定動態字級大小（XS 到 AX5）
   - `--contrast high|normal` 切換「增加對比」並讀回確認；`--reset` 也會恢復正常對比
   - 寫入語系與地區的預設值；可透過 `--bundle-id` 選擇重新啟動 App
   - 對 ar/he/fa/ur/yi 語系自動標記為由右到左（RTL）
   - 選項：`--theme`、`--text-size`、`--contrast`、`--locale`、`--region`、`--reset`、`--bundle-id`、`--udid`、`--json`、`--verbose`

4. **location.py** —— 模擬 GPS 座標、具名的城市預設與 GPX 情境播放
   - 用 `--lat`/`--lng` 固定座標，或用 `--city` 選擇城市
   - 透過 `--gpx <scenario>` 播放內建情境（City Run、Freeway Drive 等）
   - 透過 `--waypoints` 與 `--speed` 以可設定的速度動畫呈現多個路徑點
   - 用 `--clear` 清除模擬位置；用 `--list-scenarios` 列出可用的情境
   - 選項：`--lat`、`--lng`、`--city`、`--gpx`、`--waypoints`、`--speed`、`--clear`、`--list-scenarios`、`--udid`、`--json`、`--verbose`

5. **media.py** —— 為照片選擇器測試填入或清空相簿
   - 透過 `xcrun simctl addmedia` 執行 `--add a.jpg b.png`
   - `--clear --yes` 透過 `idb photos clear`（idb 1.7+）清空相簿；`--clear --yes --add` 會只留下剛加入的檔案
   - 沒有 `--yes` 時，如果相簿中有照片，`--clear` 會拒絕執行（照片無法復原）：先詢問使用者
   - 遇到不存在的檔案會立即失敗
   - 選項：`--add`、`--clear`、`--yes`、`--udid`、`--json`

### 導覽與互動（5 支）

6. **screen_mapper.py** —— 分析目前畫面並列出可互動的元素
   - 元素類型統計
   - 可互動的按鈕清單
   - 文字欄位狀態
   - 如果有標籤的元素涵蓋不到畫面的 10%，會加上一行 `Coverage:` 建議使用 `--deep`
   - `--deep` 透過 idb 的 axbridge 後端（idb 1.7+）讀取：也能看到 Safari/WKWebView 的內容與預設讀取漏掉的 App 內警示，以及許多沒有標籤的容器視圖。它會開啟裝置的無障礙自動化模式（之後不會還原）。網頁內容的框架是相對於網頁視圖，所以用 `--deep` 來找元素，而不是取得點擊座標
   - 選項：`--verbose`、`--hints`、`--deep`、`--json`

7. **navigator.py** —— 以語意找出元素並與之互動
   - 依文字尋找（模糊比對，或用 `--find-exact` 精確比對）；共用同一個標籤時，可互動的葉節點元素排在容器之前
   - 依元素類型尋找
   - 依無障礙 ID 尋找
   - 輸入文字或點擊元素
   - 對有唯一無障礙 ID 或標籤的 Button/Link/Switch/CheckBox/Tab 使用 `--tap` 時，會改用無障礙按壓（idb 1.7+），所以像浮動搜尋列這類覆蓋層無法攔截；輸出會顯示 `(accessibility press)`。否則就點擊框架中心
   - `--set-value TEXT` 不透過鍵盤直接取代欄位的值（任何字元，idb 1.7+）。焦點不會移動，所以之後需要按 Return 送出時，改用 `--enter-text`。宣稱成功前會讀回數值（安全欄位除外）；不相符時以結束碼 1 結束
   - `--tap --expect VALUE` 只有在元素的值是 VALUE 時才點擊（切換開關：`1` 為開、`0` 為關），否則不點擊並以結束碼 1 結束，所以「把 X 關掉」可以安全地重複執行
   - iOS 27 把切換開關回報為 `CheckBox`。只有按壓能切換它（任何 HID 觸控都不行，即使點在開關本身上）；如果 ID 與標籤都不唯一，輸出會警告你檢查數值
   - 凍結的 App 會讓每一次讀取與點擊都停住，直到它的主執行緒回應
   - 失敗訊息會包含 idb 的 stderr（例如 companion 已經死掉）
   - 選項：`--find-text`、`--find-exact`、`--find-type`、`--find-id`、`--index`、`--tap`、`--expect`、`--tap-at`、`--enter-text`、`--set-value`、`--list`

8. **gesture.py** —— 執行滑動、捲動、捏合與複雜手勢
   - 方向滑動（上／下／左／右）——`--swipe` 是手指移動的方向
   - 多次滑動的捲動——`--scroll` 是內容移動的方向（`down` 會顯示下方的內容）
   - 透過 `idb ui pinch` 捏合縮放（`--pinch out` 是放大；`--scale` 設定明確的倍率）
   - 透過 `idb ui tap --duration` 長按
   - 下拉重新整理
   - `--double-tap X,Y [--tap-count N]` —— 在某一點多次點擊（idb 1.7+）
   - `--drag SOURCE DEST` —— 按住、拖曳、放開；兩端各是 `x,y` 或無障礙標籤，例如 `--drag "Row 1" "Row 4"`（idb 1.7+）
   - `--rotate portrait|portrait-upside-down|landscape-left|landscape-right` —— 實體裝置旋轉（idb 1.7+）
   - `--shake` —— 搖晃裝置，用於除錯選單與復原（idb 1.7+）
   - 選項：`--swipe`、`--swipe-from/--swipe-to`、`--scroll`、`--scroll-amount`、`--pinch`、`--scale`、`--long-press`、`--duration`、`--refresh`、`--double-tap`、`--tap-count`、`--drag`、`--rotate`、`--shake`

9. **keyboard.py** —— 文字輸入與實體按鍵控制
   - 輸入文字（快速或緩慢；只限 ASCII）
   - 特殊按鍵（return、delete、tab、space、escape、方向鍵）、單一字母或原始 HID 代碼
   - 按鍵序列（`--key-sequence h,i,return`）
   - 組合鍵：`--key z --command --shift`（重做）；`--shift/--control/--option` 需要 idb 1.7+
   - 清除聚焦中的欄位（Cmd+A、delete）
   - 實體按鍵：home、鎖定／電源、側邊鍵、siri、apple-pay、音量加／減（音量需要 idb 1.6.3+）
   - 選項：`--type`、`--slow`、`--key`、`--shift`、`--control`、`--option`、`--command`、`--count`、`--key-sequence`、`--button`、`--clear`、`--dismiss`

10. **app_launcher.py** —— App 生命週期管理
   - 依 bundle ID 啟動 App
   - 終止 App
   - 從 .app 套件安裝／解除安裝（`--uninstall` 需要 `--yes`：App 的資料會被刪除）
   - 深層連結導覽
   - 列出已安裝的 App
   - 檢查 App 狀態
   - 在啟動／重新啟動時傳入啟動參數（`--args`）與環境變數（`--env KEY=VALUE`，以 `SIMCTL_CHILD_*` 注入）
   - 選項：`--launch`、`--terminate`、`--restart`、`--install`、`--uninstall`、`--yes`、`--open-url`、`--list`、`--state`、`--args`、`--env`、`--wait-for-debugger`

### 測試與分析（9 支）

11. **accessibility_audit.py** —— 檢查目前畫面的 WCAG 合規
    - 嚴重問題（缺少標籤、空按鈕、沒有替代文字）
    - 警告（缺少提示、觸控目標太小）
    - 資訊（缺少 ID、巢狀太深）
    - 選項：`--verbose`、`--output`、`--json`

12. **visual_diff.py** —— 比較兩張截圖的視覺變化
    - 逐像素比較
    - 以門檻判定通過／失敗
    - 產生差異圖
    - 選項：`--threshold`、`--output`、`--details`、`--json`

13. **test_recorder.py** —— 自動記錄測試執行過程
    - 每個步驟擷取截圖與無障礙樹
    - 產生附時間資料的 markdown 報告
    - 選項：`--test-name`、`--output`、`--verbose`、`--json`

14. **app_state_capture.py** —— 建立完整的除錯快照
    - 截圖、UI 階層、App 日誌、裝置資訊
    - 用於錯誤回報的 markdown 摘要
    - 選項：`--app-bundle-id`、`--output`、`--log-lines`、`--json`

15. **sim_health_check.sh** —— 確認環境設定正確
    - 檢查 macOS、Xcode、simctl、IDB、Python
    - 列出可用與已開機的模擬器
    - 確認 Python 套件（Pillow）

16. **model_inspector.py** —— 從專案檔檢視 Core Data 與 SwiftData 模型
    - 解析 .xcdatamodeld 套件（實體、屬性、關聯）
    - 偵測模型版本與目前使用中的版本
    - 盡力擷取 SwiftData 的 @Model 類別
    - 需要時傾印任何模型的原始內容（`--raw ModelName`）
    - 選項：`--project-path`、`--core-data-only`、`--swiftdata-only`、`--show-versions`、`--raw`、`--verbose`、`--json`

17. **container.py** —— 檢視 App 沙箱：檔案、UserDefaults 與 Core Data 儲存路徑
    - 透過 `--ls` 以可設定的深度列出資料容器的檔案
    - 透過 `--cat` 讀取檔案並自動偵測 plist 解碼（大型檔案會快取）
    - 透過 `--userdefaults` 以 key=value 或 JSON 傾印 UserDefaults
    - 透過 `--core-data-path` 找出 `.sqlite`／`.sqlite-wal`／`.sqlite-shm` 儲存檔
    - 透過 `--export` 匯出完整的容器快照
    - 選項：`--ls`、`--cat`、`--userdefaults`、`--core-data-path`、`--export`、`--udid`、`--json`、`--verbose`

18. **hang_watcher.py**（HangBuster）—— 以漸進式揭露記錄並摘要 os_log 的卡頓事件
    - **工作階段模式（HangBuster，代理原生）：** 啟動一個分離的記錄器、操作模擬器、停止以取得精簡的摘要
      - `--start` → 回傳工作階段 ID；分離的 worker 會即時正規化事件並套用門檻
      - `--stop SESSION_ID` → 輸出約 80–120 token 的 L1 摘要（標頭 + 前 N 個群集 + 深入提示）
      - `--get-details SESSION_ID [--cluster N | --raw]` → L2 完整群集或 L3 逐事件細節
      - `--list-sessions`／`--clear-sessions [--older-than 24h]`／`--diff A B`（跨工作階段的回歸報告）
      - 過濾流水線：解析 → 正規化 → 門檻 → 分桶 → 分群 → 彙總 → 排序 → 格式化（在 `common/hang_pipeline.py`）
      - `--budget-tokens N` 選擇放得下的最密集層級（L0/L1/L2）；`--terse` 強制 L0
      - `--auto-sample` 在每個群集的第一個事件時擷取主執行緒堆疊（軟相依：`main_thread_sampler.py` #62；不存在時優雅地不做事）
    - **原始擷取模式（供 `jq` 探索的完整保真度）：** 跳過分群流水線，把每一行符合的日誌原樣傾印到 `raw.ndjson`
      - `--start --raw-capture [--max-size-mb 10] [--no-gzip]` —— 產生 `log stream --style ndjson`
      - 每個工作階段的大小上限（`--max-size-mb`，預設 10）—— 達到上限時 worker 乾淨地停止；`extras.truncated=true`
      - `--stop` 把 `raw.ndjson` 壓縮成 `raw.ndjson.gz`（約 15–19 倍壓縮；`--no-gzip` 可關閉）
      - 對原始工作階段執行 `--get-details SESSION_ID` 會印出路徑，並附上 `zcat | jq ...` 的提示
    - **韌性（串流死掉時自動重啟）：** EOF 或子程序死掉會觸發 `stream_died` 事件，接著以 2 秒退避進行有界的重啟。超過 `IOS_SIM_HANG_MAX_RESTARTS`（預設 3）次後，工作階段會被標記為 `crashed`，絕不會停留在過時的 `running` 狀態。`--list-sessions` 會顯示 `capture=Xs` 與 `restarts=N`。
    - **清理是自動的：** TTL 修剪（`IOS_SIM_HANG_SESSION_TTL_HOURS`，預設 24 小時）+ 總量上限（`IOS_SIM_HANG_TOTAL_CAP_MB`，預設 100 MB，先移除最舊的）都會在每次 `--start` 時執行。
    - **舊模式（為向後相容而不變）：** `--watch [--duration N]`（即時串流）與 `--since 5m`（歷史）
    - 過濾：`--bundle-id`（解析後才套用——卡頓擷取維持在模擬器全域，以保留 RunningBoard/SpringBoard 的事件）、`--predicate`（也可透過 `IOS_SIM_HANG_PREDICATE`）
    - 所有輸出都支援 `--json`；工作階段儲存在 `~/.ios-simulator-skill/sessions/<id>/{meta.json,events.jsonl,summary.json,raw.ndjson.gz}`

    **快速開始（摘要模式）：**
    ```bash
    SID=$(python3 scripts/hang_watcher.py --start --min-hang-ms 200)
    # ... interact with the simulator (open sheets, scroll, navigate) ...
    python3 scripts/hang_watcher.py --stop $SID                  # token-tight L1 summary
    python3 scripts/hang_watcher.py --get-details $SID --cluster 1  # drill into cluster 1
    python3 scripts/hang_watcher.py --diff $SID_BASELINE $SID    # cross-session regression
    ```

    **快速開始（原始擷取 + `jq` 探索）：**
    ```bash
    SID=$(python3 scripts/hang_watcher.py --start --raw-capture --max-size-mb 5)
    # ... interact with the simulator ...
    python3 scripts/hang_watcher.py --stop $SID
    # → "Session ...: raw mode, 737 lines, 0.96 MB → 0.05 MB gzipped"

    # Top processes by event count:
    zcat ~/.ios-simulator-skill/sessions/$SID/raw.ndjson.gz \
      | jq -s 'group_by(.processImagePath) | map({proc: (.[0].processImagePath | split("/") | last), n: length}) | sort_by(-.n) | .[:5]'

    # All RunningBoard assertion invalidations:
    zcat .../raw.ndjson.gz | jq -c 'select(.subsystem == "com.apple.runningboard" and (.eventMessage | startswith("Invalidating")))'

    # Hangs per minute:
    zcat .../raw.ndjson.gz | jq -r '.timestamp[:16]' | sort | uniq -c
    ```

19. **localization_audit.py** —— 偵測字串目錄的缺口、缺少的鍵與佔位符不一致
    - 回報 `.xcstrings` 目錄中各語系缺少的鍵，以及 `needs_review`／`new` 的鍵
    - 透過 `--source` 把目錄的鍵與 Swift 原始碼（`String(localized:)`／`NSLocalizedString`）交叉比對
    - 標記各語系之間佔位符數量不一致（`%d`、`%@`、`%s`、`%lld`）
    - 透過 `plistlib` 支援舊式的 `.strings` 與 `.stringsdict`
    - 適合 CI 的 `--strict`，只要有任何發現就以結束碼 2 結束
    - 選項：`--catalog`、`--source`、`--locale`、`--strict`、`--json`、`--verbose`

### 進階測試與權限（4 支）

20. **clipboard.py** —— 管理模擬器的剪貼簿以測試貼上
    - 把文字複製到剪貼簿
    - 不需手動輸入就能測試貼上流程
    - 選項：`--copy`、`--test-name`、`--expected`、`--json`

21. **status_bar.py** —— 覆寫模擬器狀態列的外觀
    - 預設組合：clean（9:41、100% 電量）、testing（11:11、50%）、low-battery（20%）、airplane（離線）
    - 自訂時間、網路、電量、WiFi 設定
    - 選項：`--preset`、`--time`、`--data-network`、`--battery-level`、`--clear`、`--json`

22. **push_notification.py** —— 傳送模擬的推播通知
    - 簡單模式（標題 + 內文 + 徽章）
    - 自訂 JSON 酬載
    - 測試通知處理與深層連結
    - `--list` 顯示已送達的通知；`--clear` 全部撤回（兩者都需要 idb 1.7+；傳送仍使用 simctl）
    - App 在前景時傳送的推播不會送到通知中心，所以 `--list` 不會顯示它
    - 選項：`--bundle-id`、`--title`、`--body`、`--badge`、`--payload`、`--list`、`--clear`、`--json`

23. **privacy_manager.py** —— 授予、撤銷與重設 App 權限
    - 支援 13 種服務（相機、麥克風、定位、聯絡人、照片、行事曆、健康等）
    - 批次操作（以逗號分隔的服務）
    - 附測試情境追蹤的稽核軌跡
    - 選項：`--bundle-id`、`--grant`、`--revoke`、`--reset`、`--list`、`--json`

### 探索模擬器（2 支）

24. **sim_list.py** —— 以漸進式揭露列出模擬器
    - 預設為精簡摘要（總數／可用／已開機）
    - 需要時透過快取 ID 取得完整細節
    - 依裝置類型過濾
    - 用 `--suggest` 建議推薦的模擬器
    - 比原始的 `simctl list` 減少 96% 的 token（57k → 2k）
    - 選項：`--get-details`、`--suggest`、`--device-type`、`--json`

25. **simulator_selector.py** —— 建議最適合這項工作的模擬器
    - 依最近的使用（來自 `config.json`）、最新的 iOS、常見的測試機型與開機狀態為候選排序
    - 用 `--list` 列出所有可用的模擬器
    - 用 `--boot` 直接開機選定的模擬器
    - 供程式使用的 JSON 輸出
    - 選項：`--suggest`、`--list`、`--boot`、`--json`

### 裝置生命週期管理（5 支）

26. **simctl_boot.py** —— 開機模擬器，可選擇確認就緒
    - 依 UDID 或裝置名稱開機
    - 以逾時等待裝置就緒
    - 批次開機操作（--all、--type）
    - 效能計時
    - 選項：`--udid`、`--name`、`--wait-ready`、`--timeout`、`--all`、`--type`、`--json`

27. **simctl_shutdown.py** —— 優雅地關閉模擬器
    - 依 UDID 或裝置名稱關閉
    - 可選擇確認關閉完成
    - 批次關閉操作
    - 選項：`--udid`、`--name`、`--verify`、`--timeout`、`--all`、`--type`、`--json`

28. **simctl_create.py** —— 動態建立模擬器
    - 依裝置類型與 iOS 版本建立
    - 列出可用的裝置類型與執行環境
    - 自訂裝置名稱
    - 回傳 UDID 以整合 CI/CD
    - 選項：`--device`、`--runtime`、`--name`、`--list-devices`、`--list-runtimes`、`--json`

29. **simctl_delete.py** —— 永久刪除模擬器
    - 依 UDID 或裝置名稱刪除
    - 沒有 `--yes` 時會拒絕（不會提示；模擬器及其資料無法復原）：先詢問使用者
    - 批次刪除操作
    - 智慧刪除（--old N 會為每種裝置類型保留 N 個）
    - 選項：`--udid`、`--name`、`--yes`、`--all`、`--type`、`--old`、`--json`

30. **simctl_erase.py** —— 不刪除而把模擬器恢復原廠設定
    - 保留裝置 UUID（比刪除再建立更快）
    - 清除全部、依類型或已開機的模擬器
    - 可選擇確認
    - 沒有 `--yes` 時會拒絕（App、資料與設定都無法復原）：先詢問使用者
    - 選項：`--udid`、`--name`、`--yes`、`--verify`、`--timeout`、`--all`、`--type`、`--booted`、`--json`

## 常見模式

**自動偵測 UDID**：如果沒有提供 --udid，大多數腳本會自動偵測已開機的模擬器。

**解析裝置名稱**：使用裝置名稱（例如「iPhone 16 Pro」）而不是 UDID——腳本會自動解析。

**批次操作**：許多腳本支援以 `--all` 指定所有模擬器，或以 `--type iPhone` 依裝置類型過濾。

**輸出格式**：預設是精簡、人類可讀的輸出。在 CI/CD 中使用 `--json` 取得機器可讀的輸出。

**說明**：所有腳本都支援 `--help` 查看詳細的選項與範例。

**截圖尺寸**：截圖會縮小以節省 token。預設組合：`full`（3–4 個圖塊，約 5K token）、`half`（1 個圖塊，約 1.6K token，預設）、`quarter`（1 個圖塊，約 800 token，細節較少）。快速視覺檢查用 `quarter`，可讀的 UI 用 `half`，只有在需要像素層級的細節時才用 `full`。會擷取截圖的腳本（`app_state_capture.py`、`test_recorder.py`）預設為 `half`。

## 典型的工作流程

1. 確認環境：`bash scripts/sim_health_check.sh`
2. 啟動 App：`python3 scripts/app_launcher.py --launch com.example.app`
3. 分析畫面：`python3 scripts/screen_mapper.py`
4. 互動：`python3 scripts/navigator.py --find-text "Button" --tap`
5. 驗證：`python3 scripts/accessibility_audit.py`
6. 需要時除錯：`python3 scripts/app_state_capture.py --app-bundle-id com.example.app`

## 設定

大多數的操作限制都可以透過環境變數調整。預設值適用於一般的本機開發；對於較慢的 CI 執行器、大型 monorepo 建置或複雜畫面的無障礙稽核，可以調高。

| 變數 | 預設 | 控制 |
|---|---|---|
| `IOS_SIM_A11Y_LABEL_MAX` | `80` | 無障礙稽核輸出中保留的 `AXLabel` 最大字元數 |
| `IOS_SIM_A11Y_TOP_ISSUES` | `10` | 每次稽核呈現的前幾個無障礙問題 |
| `IOS_SIM_APPS_PREVIEW` | `30` | `app_launcher.py` 截斷前列出的 App 數 |
| `IOS_SIM_BOOT_SUBPROCESS_TIMEOUT` | `60` | `simctl boot` 子程序本身的逾時（秒） |
| `IOS_SIM_BOOT_TIMEOUT` | `300` | 開機後等待就緒的逾時（秒） |
| `IOS_SIM_BUILD_JSON_CAP` | `50` | JSON 輸出中建置錯誤／失敗測試的最大數量 |
| `IOS_SIM_BUILD_LOG_PREVIEW` | `4000` | 預設輸出中建置日誌預覽的字元數 |
| `IOS_SIM_BUILD_TIMEOUT` | `1800` | `xcodebuild build` 被終止前的最大秒數 |
| `IOS_SIM_INTROSPECT_TIMEOUT` | `60` | `xcodebuild -list` 與 `simctl list` 查詢的逾時（秒） |
| `IOS_SIM_TEST_TIMEOUT` | `2700` | `xcodebuild test` 被終止前的最大秒數 |
| `IOS_SIM_BUILD_SUMMARY_CAP` | `15` | 預設建置摘要中的錯誤／失敗數 |
| `IOS_SIM_BUILD_VERBOSE_CAP` | `100` | 詳細建置輸出中的錯誤／警告數 |
| `IOS_SIM_CACHE_MAX_ENTRIES` | `500` | 漸進式揭露快取的最大條目數（LRU 淘汰） |
| `IOS_SIM_CACHE_TTL_HOURS` | `1` | 快取條目的過期時間 |
| `IOS_SIM_ERASE_TIMEOUT` | `90` | 等待清除的逾時（秒） |
| `IOS_SIM_HANG_PREDICATE` | _（預設）_ | 覆寫 `hang_watcher.py` 使用的 `os_log` 述詞（預設會抓 RunningBoard 終止 +「Hang detected」+ 主執行緒卡頓）。卡頓事件來自系統常駐程式（RunningBoard、SpringBoard），所以述詞維持在模擬器全域——`--bundle-id` 是在解析後套用，而不是以 AND 合併進去。 |
| `IOS_SIM_HANG_MIN_MS` | `250` | HangBuster 門檻——低於這個時長的事件不會寫入磁碟（越小越敏感、摘要越大） |
| `IOS_SIM_HANG_SESSION_TTL_HOURS` | `24` | HangBuster 工作階段的修剪年齡；每次 `--start` 都會執行修剪 |
| `IOS_SIM_HANG_DEFAULT_TOP_N` | `3` | `--stop` L1 輸出中預設的前 N 個群集 |
| `IOS_SIM_HANG_BUDGET_TOKENS` | _（未設定）_ | `--stop` 預設的 token 預算（選擇放得下的 L0/L1/L2） |
| `IOS_SIM_HANG_MAX_RESTARTS` | `3` | HangBuster worker：在 EOF／子程序死掉時，`log stream` 重新產生的最大嘗試次數，超過後工作階段標記為 `crashed` |
| `IOS_SIM_HANG_TOTAL_CAP_MB` | `100` | HangBuster 的總磁碟上限。`--start` 時若工作階段狀態總量超過此值，先移除最舊的工作階段。設為 `0` 停用。 |
| `IOS_SIM_LOG_JSON_CAP` | `100` | `log_monitor.py` JSON 輸出中錯誤／警告的最大數量 |
| `IOS_SIM_LOG_LINE_MAX` | `300` | 日誌摘要中每行的截斷長度 |
| `IOS_SIM_LOG_TAIL` | `200` | 詳細／範例輸出中日誌尾端的行數 |
| `IOS_SIM_LOG_TEXT_SUMMARY` | `15` | 文字模式日誌摘要中顯示的錯誤／警告數 |
| `IOS_SIM_MAX_ELEMENTS` | `25` | `navigator.py --list` 與 `push_notification.py --list` 列出的項目數 |
| `IOS_SIM_POLL_INTERVAL` | `0.5` | 開機／清除狀態的輪詢間隔（秒） |
| `IOS_SIM_RELAUNCH_DELAY_MS` | `1000` | `app_launcher.py` 中終止與重新啟動之間的延遲 |
| `IOS_SIM_SCREEN_BUTTONS_PREVIEW` | `15` | `screen_mapper.py` 列出的按鈕名稱數 |
| `IOS_SIM_SCREEN_SECTION_ITEMS` | `10` | `screen_mapper.py` 每個區塊顯示的項目數 |
| `IOS_SIM_STATE_SUBPROCESS_TIMEOUT` | `15` | `app_state_capture.py` 中的子程序逾時（秒） |
| `IOS_SIM_TAP_SETTLE_MS` | `500` | `navigator.py` 中點擊後的穩定延遲 |

範例：

{{CODE:2}}

## 需求

- macOS 15（Sequoia）+
- Xcode 26+（完整的 App；只有命令列工具不足以使用 idb）
- Apple silicon Mac（Homebrew 的 idb 版本只支援 arm64）
- Python 3.12+
- `idb` **1.5.1+**（建議 1.6.3+）——每一支互動式腳本（點擊、滑動、輸入）都需要：
  `brew install facebook/fb/idb`（同時安裝 idb-cli 與 idb-companion）
- Pillow，只有視覺比對需要：`pip3 install pillow`

用 `bash scripts/sim_health_check.sh` 確認（加上 `--json` 取得結構化輸出）。

## 疑難排解

**點擊、滑動與輸入都沒有作用，但讀取正常。** `idb` 回報成功，但畫面從來沒有改變。在 Xcode 27 上，這代表 `idb-companion` 舊於 1.5.1：它在 Xcode 26 使用的路徑尋找 `SimulatorKit.framework`。一起升級兩者，然後重啟執行中的 companion：`brew upgrade facebook/fb/idb-cli facebook/fb/idb-companion && idb kill`。

**`SimulatorKit is required for HID interactions`。** 同樣的原因，同樣的修正。

**健康檢查警告「idb companions started before idb-companion was last installed」。** 那些 companion 仍在執行升級前的二進位檔。執行 `idb kill`；下一次 idb 呼叫會啟動新的 companion。

**每次 idb 呼叫都出現 `Connection refused` 或 `No such file`。** 一個已死的 companion 仍留在 idb 位於 `/tmp/idb/state` 的登錄中，所以 idb 會撥打一個沒人在聽的 socket，而不是啟動新的 companion。修正：`idb disconnect <udid>`。

**`open -a Simulator` 失敗。** Xcode 27 沒有 `Simulator.app`；它被 `Xcode.app/Contents/Applications/` 中的 `DeviceHub.app` 取代。改用無介面方式開機：`xcrun simctl boot <udid>`。注意，結束 DeviceHub 會關閉它所承載的模擬器。

**`idb: command not found`。** companion 與 CLI 是不同的套件；`brew install facebook/fb/idb` 會兩者都安裝。如果 `which -a idb` 顯示不只一個，`PATH` 上的第一個優先。如果那是舊的 pip `fb-idb`，需要 `pip uninstall fb-idb`。

**已知的上游 idb 問題**（截至 idb 1.7.6 仍未解決）：
- [facebook/idb#964](https://github.com/facebook/idb/issues/964)：在某些 iOS 26+ 的畫面上，`describe-all` 只回傳應用程式節點，而且 SpringBoard 的警示無法點擊。預設的 `ax` 後端無法跨越程序邊界；試試 `idb ui describe-all --json --api axbridge`。點擊座標是點（point），不是截圖的像素。App 重新啟動後，預設的讀取也可能卡在單一個大小為零的 Application 節點；執行一次 `screen_mapper.py --deep` 讀取（它本身可能會逾時一次）就能恢復。
- [facebook/idb#978](https://github.com/facebook/idb/issues/978)：`describe-all` 會列出無障礙自訂動作，但無法執行。
- [facebook/idb#954](https://github.com/facebook/idb/issues/954)：Homebrew 版本只支援 arm64，所以不支援 Intel Mac。

## 文件

- **SKILL.md**（本檔案）—— 腳本參考、需求、疑難排解
- **[README.md](https://github.com/conorluddy/ios-simulator-skill/blob/main/README.md)** —— 安裝、更新 idb、Xcode 27 說明
- **[AGENTS.md](https://github.com/conorluddy/ios-simulator-skill/blob/main/AGENTS.md)** —— 架構與實作細節

## 關鍵設計原則

**語意導覽**：依意義（文字、類型、ID）而不是像素座標找元素。能撐過 UI 的變更。

**Token 效率**：精簡的預設輸出（3–5 行），需要詳細結果時可選擇詳細與 JSON 模式。

**無障礙優先**：建立在標準的無障礙 API 上，以求可靠與相容。

**零設定**：在任何裝有 Xcode 的 macOS 上立即可用。不需要設定。

**結構化資料**：腳本輸出 JSON 或格式化的文字，而不是原始日誌。容易解析與整合。

**自動學習**：建置系統會記住你的裝置偏好。設定依專案儲存。

---

直接使用這些腳本，或在你的請求符合技能描述時，讓 Claude Code 自動呼叫它們。
