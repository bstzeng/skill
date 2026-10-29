<!--meta
{"title":"HyperFrames 指令工具","category":"影片與多媒體","tags":["影片製作","CLI","渲染","時間軸編輯","HeyGen","HyperFrames"],
"summary":"HeyGen 開源的 HyperFrames（用 HTML 渲染影片）CLI 使用指南，依工作分類：建立專案、檢查、看影格、編輯時間軸、預覽、本機或雲端渲染、發布、專案歷史，以及建置/渲染失敗時的排除方法。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-cli`（建議與 hyperframes 一起裝）\n- 需要 Node.js 22+ 與 FFmpeg\n- 工作循環：`lint` → `check --json` 修完所有錯誤 → `snapshot` 看截圖 → `preview --background` 給你預覽 → 你核准後 `render --quality delivery`\n- 時間軸修改可先加 `--plan` 預覽，每次修改都能 `history undo`"}
-->
---
name: hyperframes-cli
description: 依工作分類的 HyperFrames CLI——建立骨架、檢查、查看影格、編輯時間軸、預覽、本機或雲端渲染、發布、專案歷史——以及讀取其 JSON 輸出與從建置或渲染失敗中恢復。
---

**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](../hyperframes/references/plugin-installation.md)。

# HyperFrames CLI

執行 `npx hyperframes <command>`，除非專案提供了包裝指令；那就用包裝指令。需要 Node.js 22+ 與 FFmpeg。每個指令都有 `--help`；大多數接受 `--json`，失敗時會印出 `✗ …` 與一行 `Fix:`，並以非零狀態碼結束。

## 依工作分類的指令

| 工作 | 指令 |
| --- | --- |
| 開始 | `init <dir>`（空白專案；只有被要求時才用 `--example <name>`）、`capture <url>` |
| 讀取專案 | `info`、`compositions`、`timeline --json`、`docs <topic>` |
| 檢查 | 撰寫時用 `lint`；以 `check --json` 作為關卡（lint、執行期、版面、對比） |
| 查看 | `snapshot`（`--at <t,…>`、`--range START,END`、`--composition <id>`、`--zoom`、`--angle`、`--against <video>`）、`keyframes`、`compare`、`audio` |
| 編輯時間軸 | `timeline` 搭配 `move`、`trim`、`split`、`set`、`duplicate`、`delete`、`apply`、`undo`、`ids` |
| 重用 | `catalog`、`add`（`/hyperframes-registry`） |
| 媒體與聲音 | `media-treatment`、`grade-compare`、`remove-background`、`tts`、`transcribe`、`beats`、`normalize-audio`（`/media-use`） |
| 展示與交付 | `preview`、`present`（`/slideshow`）、`render`、`publish`、`cloud`、`lambda`、`cloudrun` |
| 桌面應用程式 | `open`、`catch-up` |
| 維護 | `doctor`、`browser`、`upgrade`、`skills`、`usage`、`clean`、`feedback` |

`validate`、`inspect` 與 `layout` 是 `check` 已棄用的別名；`events` 是給技能自身腳本用的遙測。不要執行它們。

## 工作循環

1. 撰寫，然後在第一輪之後與結構變更之後執行 `npx hyperframes lint`。
2. 執行 `npx hyperframes check --json` 並修正每一個錯誤。只要還有 lint 錯誤，版面與對比稽核就不會執行；「0 samples」代表什麼都沒檢查到。對比失敗會附帶 `suggestedColor`。只出現在單一取樣點的發現（進場動畫進行中）屬於資訊；3 秒以上卻沒有可見變化的影片會讓 `sweep_static` 失敗。
3. 執行 `npx hyperframes snapshot` 並閱讀 PNG（在 `.hyperframes/artifacts/snapshots/` 下）：這就是你「看」影片的方式。有子合成時，為每個場景的中點拍快照；極小又沒有樣式的內容或缺少主視覺，代表掛載有缺陷（`../hyperframes/references/format.md`）。
4. 執行 `npx hyperframes preview --background`，確認該 URL 回應 200，把專案 URL 交給使用者並等待，除非他們要求直接給檔案或不要中途停下。光是檢查通過並不是渲染的理由。
5. 到了要渲染的時候（步驟 4）：`npx hyperframes render --quality looks --output out.mp4`（反覆修改時用 `draft`，最終版用 `delivery`）。確認檔案不是空的、其 `ffprobe` 長度與根層級的 `data-duration` 相符，然後查看解碼後的影格。

「這個元素」或目前的選取：`npx hyperframes preview --context --json --context-fields selection`；`no-selection` 代表要請他們點選它。

## 編輯時間軸

這些就是 Studio 本身會做的編輯，所以結果會維持 Studio 的格式。

- `timeline --json` 列出各片段的絕對 `absStart`/`absEnd`、所屬的 `file`，以及編輯指令接受的 `#id` 參照（`timeline ids` 會補上缺少的 id）。
- `timeline move|trim|split|set|duplicate|delete <ref> … --plan --json` 預覽一次編輯；再去掉 `--plan` 執行一次。`--start`、`--end`、`--duration` 設定某一邊或長度。
- 如果片段會與相鄰片段重疊（使用 `--overwrite`，或先移動相鄰片段），或結束時間超過其合成，編輯會被拒絕：先調高根層級的 `data-duration`。沒有任何指令會更改 `data-duration`。
- 一次多項編輯：寫一個 JSON 檔，例如 `[{"verb": "move", "ref": "#outro", "time": "9"}]`，然後執行 `timeline apply plan.json --json`。每次執行都會印出一份 `receipt`；保存它，用 `timeline undo receipt.json` 即可還原。

<!-- history (trial): remove this block together with the command -->

## 專案歷史

每次寫入都會被保留並可復原。在每一輪開始時執行 `npx hyperframes history begin --who <you> --label "<plan>"`，然後用 `history --since mine --who <you>` 查看使用者改了什麼；在他們的修改之上繼續。檢查失敗或他們說變差了：執行 `history undo --who <you>`，絕不手動改回去。以 `history end` 結束這一輪。

<!-- /history (trial) -->

## 在哪裡渲染

| 需求 | 指令 |
| --- | --- |
| 本機 | `render --quality looks --output out.mp4`（`draft`、`delivery`） |
| 可重現的容器 | `render --docker --strict --output out.mp4` |
| 依變數批次渲染 | `render --batch rows.json --output "renders/{name}.mp4"` |
| 雲端託管，本機不需 Chrome 或 FFmpeg | `cloud render`（`references/cloud.md`） |
| 你自己的 AWS 或 GCP | `lambda render`、`cloudrun render`（`references/lambda.md`、`references/cloudrun.md`） |

30 秒的影片一兩分鐘就能渲染完：在前景執行。只有渲染時間超過你工具的逾時限制時才分離執行（`HYPERFRAMES_RENDER_DETACHED=1`、獨立的程序群組、輸出到日誌），並用 `until grep -qE 'Render (complete|failed)' render.log; do sleep 5; done` 等待；絕不用 `pgrep -f`，它會匹配到自己的迴圈，一直等到工具逾時。

渲染驗證完成後，送出一次 `feedback --rating`，並針對使用者要求但 HyperFrames 做不到的事送出回報，除非遙測已關閉：`references/feedback.md`。

## 指令失敗時

| 症狀 | 修正 |
| --- | --- |
| 找不到 Chrome 或無法啟動 | `npx hyperframes browser ensure`；`doctor --json` 一律以 0 結束，請以 `.ok` 判斷 |
| 很重的頁面來不及準備好 | 調高 `check` 或 `snapshot` 的 `--timeout` |
| 少見的編碼看起來一片空白 | 保持 `--proxy` 開啟（預設值） |
| 在 Linux 上渲染很慢 | 摘要第二行顯示 `screenshot` + `software gpu`：那是慢速路徑 |
| `capture` 失敗或寫出 `BLOCKED.md` | 不要採用它的任何部分檔案；改用新的 `-o` 資料夾重試 |
| 磁碟空間緊張 | 先 `clean --dry-run`，再 `clean`；絕不刪除 `.hyperframes`（裡面存有歷史） |

## 參考資料

執行某指令前先閱讀該列對應的文件。

| 指令 | 閱讀 |
| --- | --- |
| `init`、`capture`、`skills` | `references/init-and-scaffold.md` |
| `lint`、`check`、motion sidecar、`snapshot` | `references/lint-validate-inspect.md` |
| `compare`、`grade-compare`、`render --batch` | `references/compare-and-batch.md` |
| `beats` | `references/beats.md` |
| `preview`、`play`、`render`、`publish`、Studio 脈絡 | `references/preview-render.md` |
| `doctor`、`browser` | `references/doctor-browser.md` |
| `auth`、`cloud`、模板變數 | `references/cloud.md` |
| `lambda`、`cloudrun` | `references/lambda.md`、`references/cloudrun.md` |
| `info`、`upgrade`、`compositions`、`timeline`、`docs`、`usage`、遙測 | `references/upgrade-info-misc.md` |
| `--strict` 旗標、run id、`clean`、shader lint、JSON 路徑 | `references/conventions.md` |
| `keyframes` | `../hyperframes/references/motion.md`（觀察動態） |
