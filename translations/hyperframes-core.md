<!--meta
{"title":"HyperFrames 核心契約","category":"影片與多媒體","tags":["影片製作","HTML 轉影片","技術規範","GSAP","HyperFrames"],
"summary":"HyperFrames 專案的技術契約：如何用 data 屬性在 HTML 中宣告時間、讓動畫可逐格定位、由框架掌控媒體播放，並列出代理最常踩的坑（置中方式、場景結束不要手動隱藏、timeline id 必須對應等）。本頁內容取自 skills.sh 頁面的摘錄，該 skill 已從 GitHub 儲存庫的主分支移除。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-core`\n- 開始任何 HyperFrames 影片前先載入，作為建構規範\n- 渲染後看摘要第二行：`screenshot` + `software gpu` 代表在 Linux 上走慢速路徑"}
-->
**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-core/../hyperframes/references/plugin-installation.md)。獨立安裝則維持下方的更新說明。

# HyperFrames 核心

**代理常見陷阱（先讀）：**

* 用 flex/`inset` 置中，不要在之後要用 GSAP 調整 `x`/`y` 的節點上使用 CSS `transform: translate(-50%,-50%)`。Lint：`gsap_css_transform_conflict`。改用 `fromTo` 或 `xPercent`/`yPercent`。
* 不要加入場景結束時的 `tl.set(..., {visibility:"hidden"})`。執行環境已經會隱藏有時間的片段。對內部節點做不透明度淡出（或對 `.clip` 設定 `opacity`）就夠了。字幕的強制隱藏是另一條規則。
* `window.__timelines["id"]` 必須與根層級的 `data-composition-id` 相符。
* `render` 之後，閱讀摘要的第二行：`beginframe` 還是 `screenshot`、GPU 模式、各階段耗時。在 Linux 上 `screenshot` + `software gpu` 是慢速路徑。

HyperFrames 從 HTML 渲染影片。一個合成是一個 HTML 檔，其 DOM 以 `data-*` 屬性宣告時間，其動畫執行環境可以定位，而其媒體播放由框架掌控。

本技能是**技術契約**——如何建構一個 hyperframes 專案。下方內文是建構指南；各主題的細節放在 `references/`（索引在下一節），需要時再讀。流程文件（需求簡報、分鏡、審查、製作、派工、影格 worker）位於 `/hyperframes` → `references/`。其他面向則在同層的領域技能中——`hyperframes-animation`、`hyperframes-creative`、`media-use`、`hyperframes-cli`、`hyperframes-registry`。`/hyperframes` 中的能力地圖說明每一個涵蓋什麼。

## 參考資料
