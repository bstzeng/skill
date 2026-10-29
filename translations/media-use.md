<!--meta
{"title":"HyperFrames 媒體素材","category":"影片與多媒體","tags":["影片製作","配音","音樂","調色","HeyGen","HyperFrames"],
"summary":"為 HyperFrames 影片取得或產生各種媒體素材——配樂、音效、圖片、圖示、Logo、旁白、虛擬主播影片、逐字稿、去背、調色風格——可用 HeyGen（付費高品質）或免費本機工具，並混音已放置的音軌。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill media-use`\n- 在 HyperFrames 專案中說「幫這段加背景音樂和旁白」「這段畫面太暗，調亮一點」\n- 核心指令：`npx hyperframes media-use resolve ...`，素材一律落地到 `assets/`\n- 用 `--doctor` 檢查設定、`--local-only` 只用免費本機工具；付費呼叫前會先確認"}
-->
---
name: media-use
description: 為 HyperFrames 影片取得或製作任何媒體——音樂、音效、圖片、圖示、Logo、旁白、虛擬人像與生成影片、逐字稿、去背、調色與風格——使用 HeyGen 或免費的本機工具，並混音已放置的音訊。也適用於看起來太暗、太平、太灰，或應該風格化或遮蔽的影片素材。
---

**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](../hyperframes/references/plugin-installation.md)。

# HyperFrames 中的媒體

媒體會以本機檔案落地在專案的 `assets/` 中，並附帶一筆帳本紀錄；渲染時絕不從網路抓取。一個動詞就能找到或製作它：

{{CODE:1}}

它會印出一行：`resolved <id> → <path> (<type>, <metadata>)`。先用 `--candidates` 列出可重用的素材，自行判斷是否合適；重用、匯入（`--from`）與採用的說明在 `references/resolve.md`。

## 兩種取得方式

| 需求 | HeyGen（最佳品質） | 免費、不需帳號 |
| --- | --- | --- |
| 音樂（`bgm`） | 一萬首以上的曲庫 | 本機 MusicGen（`audio/references/bgm.md`） |
| 音效（`sfx`） | | Openverse；內附 21 個離線音效 |
| 圖片、圖示 | 素材搜尋，七萬五千筆以上 | 本機 FLUX（mflux），若已安裝 |
| Logo（`logo`） | | theSVG、GitHub 頭像、favicon；絕不重新繪製 |
| 旁白（`voice`） | HeyGen 語音、聲音複製 | `npx hyperframes tts`（裝置上的 Kokoro；需 Python 3.10+ 並 `pip install kokoro-onnx soundfile`） |
| 主持人說話畫面 | 虛擬人像影片（`--type video`） | 本機 LTX 產生通用片段，若已安裝 |
| 逐字稿 | | `npx hyperframes transcribe`（Parakeet 或 whisper） |
| 去背 | `heygen background-removal` | `npx hyperframes remove-background` |
| 調色、LUT、風格 | | `npx hyperframes media-treatment` |

**宿主應用程式。** 在提供自有媒體工具的應用程式中，優先使用那些工具。當設定了 `HEYGEN_API_BASE` 時，由宿主支付 HeyGen 費用：不要要求 `heygen` CLI 或登入；呼叫被拒絕時，照原文轉述宿主的訊息並停止。

**HeyGen。** 安裝 [`heygen` CLI](https://developers.heygen.com/cli)，然後用 `npx hyperframes auth login` 登入。HyperFrames 會把自己的憑證提供給輔助程式；它不會讀取另外的 HeyGen CLI 登入。明確提供的 API 金鑰會計費 API 點數，OAuth 是否適用與收費由伺服器決定。用 `npx hyperframes media-use resolve --doctor` 檢查設定。如果缺少必要的供應商或已登出，提供安裝連結與 HyperFrames 登入指令，然後提議改走免費路徑或等待。

**直接使用 HeyGen 的配方。** `references/operations.md` 中的 `heygen video-agent create`、`heygen video create`、`heygen voice clone create`、`heygen lipsync`、`heygen video-translate` 與 `heygen ai-clipping` 等指令，使用的是 HeyGen CLI 自己的憑證與 HeyGen/API 計費。它們不會繼承 HyperFrames 的 OAuth 或訂閱。只有在選定了那個獨立的付款方時才使用。

**免費。** 免費欄中的每個工具都不需要帳號；本機模型是選擇性安裝（`references/setup-providers.md`）。沒有 `heygen` 時，針對音樂、圖片與圖示的 `resolve` 會失敗並說明原因；使用 CC BY 音效時要註明出處（`audio/references/sfx.md`）。`--local-only` 會略過所有網路供應商。

**費用。** 你自己決定要發出的付費呼叫，執行前先確認（虛擬人像影片也算）；使用者明確要求的則直接執行。當使用者指名某個產生器時，用 `--provider <name>` 鎖定它。

## 真實影片素材的風格

如果回饋是素材太暗、太平、太灰，應該有復古或印刷感、需要遮住臉，或需要揭示效果，這都屬於媒體意圖：請閱讀 `references/media-treatments.md`。檢查實際的 `<img>`/`<video>`，選定一個意圖，從 `npx hyperframes media-treatment --capabilities --json` 開始，然後用 `--capability <id>`；絕不使用 `--all`。用 `npx hyperframes media-treatment` 保存最終處理；已支援的效果不要用 CSS 或 SVG 替代，也不要只為了編碼曝光或色溫就產生 `.cube` 檔。

## 只提議一次，絕不默默加入

建立或審查作品時，掃描一次具體的缺口（畫面上有文字卻沒有旁白、用 emoji 代替圖示、占位圖片、無聲的剪接、10 秒以上沒有音樂、偏色），然後一次提出具體的修正建議。沒有訊號就不建議；尊重「保持原樣」。

## 去哪裡找

| 任務 | 閱讀 |
| --- | --- |
| 解析、重用、採用、匯入、旗標 | `references/resolve.md` |
| 調色、LUT、`grade-compare` | `references/grading.md` |
| 旁白、音樂、音效、字幕、轉錄 | `references/audio.md` |
| 剪輯、重新構圖或轉換媒體；HeyGen 配方 | `references/operations.md` |
| 處理效果、即時特效、疊加、揭示 | `references/media-treatments.md` |
| 安裝、登入、供應商、RAM 階梯 | `references/setup-providers.md` |
| 已放置音軌的淡入淡出、增益、閃避（ducking）、自動化、效果、匯流排 | `references/mixing.md` |
| 本機指令：調色、去背、響度、節拍 | `references/local.md` |
| 記住的偏好 | `references/memory.md` |
