<!--meta
{"title":"HyperFrames 元件庫","category":"影片與多媒體","tags":["影片製作","元件庫","轉場","字幕樣式","HyperFrames"],
"summary":"約 450 個現成的 HyperFrames 區塊與元件，安裝後是可直接修改的原始碼：轉場、疊加圖層、標題卡、動態文字、字幕樣式、圖表、地圖、3D 與運鏡。在手刻任何有名稱的視覺效果（CRT 掃描線、故障效果、底片顆粒、圖表）之前先來這裡找。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-registry`\n- 搜尋：`npx hyperframes catalog --query \"film grain\"`（請用英文查）；安裝：`npx hyperframes add <名稱>`\n- 區塊裝到 `compositions/<name>.html` 用 `data-composition-src` 掛載；元件則把標記、樣式與腳本複製進你的場景\n- 找不到合適的就用 `npx hyperframes feedback --search-miss ...` 回報缺口"}
-->
---
name: hyperframes-registry
description: 約 450 個現成的 HyperFrames 區塊與元件，以可編輯的原始碼形式安裝——轉場、疊加圖層、標題、動態文字、字幕、圖表、地圖疊加、3D、運鏡。在手工製作任何有名稱的視覺效果（CRT 掃描線、故障效果、底片顆粒、一張圖表）之前使用；也用於 hyperframes add 與 catalog。
---

**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](../hyperframes/references/plugin-installation.md)。

# HyperFrames 元件庫（registry）

從一個現成項目開始，比自己寫效果更快，通常也更好；而且安裝後的項目就是你專案中普通的原始碼：修改它、刪減它、重新設計它的樣式。

## 尋找與安裝

沒有 `hyperframes registry` 這個指令；搜尋是 `catalog`，安裝是 `add`。

{{CODE:1}}

- 即使影片不是英文的，也用英文查詢：目錄是以英文建立索引的，其他文字會回傳 `No searchable words in query`，這並不代表缺少項目。
- 搜尋在本機進行，不會送出任何東西。預設的 `words` 等級只會找到重用你所用字詞的項目；`--on-device` 在一次性下載約 33 MB 後，會依語意排序。提議這個下載並讓使用者決定；絕不默默啟用。`--json` 外層結構會標明是哪個等級回答的。
- 用 `--type block|component` 與 `--tag <tag>` 縮小範圍。`add <tag>` 會安裝帶有該標籤的每個區塊；相依項目會先安裝。即使是先前安裝過的項目，`add` 也需要網路；搜尋則能用快取的清單離線運作。
- 沒有合適的：在手工製作之前先回報，無論是哪個等級。`catalog --query` 會印出預先填好的那一行（`--json` 中為 `report_gap`）：`npx hyperframes feedback --search-miss "<query>" --wanted "<你需要的動作>" --tier <tier>`。描述效果本身，而不是你想像出來的項目名稱。

等級、`dropped` 與 `unindexed`、過期的索引、離線行為：見 `references/search.md`。

## 裡面有什麼

| 區塊：擁有自己時間軸的場景 | 範例 |
| --- | --- |
| 轉場 | `beat-freeze-cut`、`chromatic-radial-split`、`cinematic-zoom` |
| 疊加圖層與下方字卡 | `camcorder-hud`、`editorial-flash-overlay`、`lt-clean-bar` |
| 標題卡與動態文字 | `canopy-part-title`、`code-slice-hero` |
| 社群、聊天與 UI 卡片 | `ai-chat-reveal`、`chatgpt-exchange` |
| 程式碼、圖表、資料與地圖 | `code-diff`、`bar-chart-race`、`data-chart` |
| 3D、著色器與背景 | `app-showcase`、`aurora`、`blob` |

| 元件：合併進你場景的片段 | 範例 |
| --- | --- |
| 動態基本元素與文字效果 | `agent-cursor`、`blur-in`、`bottom-up-letters` |
| 字幕樣式 | `caption-clip-wipe`、`caption-editorial-emphasis` |
| 運鏡 | `camera-shake`、`camera-scan-gate` |
| 產品示範與 UI 道具 | `before-after-wipe`、`browser-device-stage` |
| 材質、粒子與效果 | `ascii-render-pass`、`grain-overlay` |

## 接線

- **區塊**：安裝到 `compositions/<name>.html`。用 `data-composition-src`、與區塊自身 id 相符的 `data-composition-id`、`data-start` 以及你需要的 `data-duration` 掛載它；`add` 印出的片段就是起點。見 `references/wiring-blocks.md`。
- **元件**：安裝到 `compositions/components/<name>.html`。把它的標記、`<style>` 與腳本複製進你的場景，如果它會掛進你的時間軸，就照它的註解區塊操作。見 `references/wiring-components.md`。
- 採用能符合需求的最大單位，然後編輯它。保留已安裝項目的 id 前綴不變，讓兩個項目不會衝突。
- 每個項目保有自己的變數；在它的容器上用 `data-variable-values` 為單次掛載設定（`add --vars '{"title":"…"}'` 會寫入這個），並把它的色彩與字型變數指向你的品牌值。
- 與節拍同步的區塊從 `npx hyperframes beats --json` 取得擊點時間：節拍時間減去該掛載的 `data-start`。
- 安裝路徑來自 `hyperframes.json`（`references/install-locations.md`）。

## 貢獻

為上游 PR 撰寫新的區塊或元件：見 `references/contributing.md`，入門模板在 `references/templates.md`，品質標準在 `references/component-quality-bar.md`。
