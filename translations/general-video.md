<!--meta
{"title":"HyperFrames 通用影片流程","category":"影片與多媒體","tags":["影片製作","工作流程","HeyGen","HyperFrames"],
"summary":"用 HyperFrames 製作一般影片的總流程：開始前查用量、確認技能為最新版，再套用跨領域的來源轉接——媒體一律走 media-use、Figma 連結先交給 /figma 處理，並依登入狀態決定協作或自主模式。本頁內容取自 skills.sh 頁面的摘錄，該 skill 已從 GitHub 儲存庫的主分支移除。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill general-video`\n- 說「幫我做一支介紹我們服務的影片」這類沒有指定類型的影片請求\n- 會在草稿完成後、渲染前再次執行 `npx hyperframes usage --json` 檢查剩餘用量"}
-->
**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/general-video/../hyperframes/references/plugin-installation.md)。獨立安裝則維持下方的更新說明。

# 通用影片

在開始時執行 `npx hyperframes usage --json`（除非工作流程剛讀過它），並在里程碑時再檢查一次，例如草稿完成後與渲染前。閱讀可用的時間窗與重置時間。如果用量未知，就直說，不要猜測額度；範圍與工作流程的選擇交由使用者決定。

在依賴這個工作流程之前，執行：

{{CODE:1}}

成功的空操作代表技能是最新的。如果更新失敗，要提出來，而不是憑記憶繼續。

## 1. 套用跨領域的來源轉接

* **媒體：** 任何音訊、圖片、圖示、Logo、語音、調色、LUT、處理/效果、字幕或媒體操作的需求，載入 `/media-use`，並遵循 `../media-use/references/resolve.md`（解析、採用、重用）與 `../media-use/references/setup-providers.md`（供應商、驗證）。對影片素材含糊的回饋與指名的風格，在編輯前先用 `../media-use/references/media-treatments.md`；不要用 CSS/SVG/不透明度即興製作已支援的媒體效果。在第一個需要驗證的供應商動作之前，執行 `npx hyperframes auth status` 並逐字轉述其輸出。如果尚未登入，套用 `../hyperframes/references/brief-contract.md` 中的關卡：協作模式等待登入或明確選擇離線；自主模式說明狀態並透過可用的離線供應商繼續。當沒有任何離線供應商能滿足必要的能力時，提出阻礙。單純在本機採用素材不需要驗證關卡。
* **Figma：** 如果任何輸入是 `figma.com` URL，先執行 `/figma`。以它匯出的素材、token、元件或分鏡框架來建構。不要使用原始的 Figma 連接器呼叫，因為它們會略過 SVG 清理、媒體來源追溯與品牌 token 綁定。
