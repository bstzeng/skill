<!--meta
{"title":"HyperFrames 動畫","category":"影片與多媒體","tags":["影片製作","動畫","轉場","GSAP","HyperFrames"],
"summary":"HyperFrames 所有動態知識集中在一個技能：原子規則（單一動作做法）、藍圖（多階段場景模板）、場景轉場、動態設計技巧，以及各執行環境的 API 轉接。本頁內容取自 skills.sh 頁面的摘錄，該 skill 已從 GitHub 儲存庫的主分支移除。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-animation`\n- 在 HyperFrames 專案中說「標題進場改成打字機效果」「兩個場景之間加一個推移轉場」\n- 合成契約（data 屬性、子合成、決定性）請看 hyperframes-core"}
-->
**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-animation/../hyperframes/references/plugin-installation.md)。獨立安裝則維持下方的更新說明。

# HyperFrames 動畫

## 目錄

* [預設：組合原子規則](#default-compose-atomic-rules)
* [何時載入藍圖](#load-a-blueprint-when)
* [路由](#routing)
* [選擇執行環境](#picking-a-runtime)
* [關鍵限制](#critical-constraints)
* [腳本](#scripts)
* [另見](#see-also)
* [參考檔案](#reference-files)

所有動態知識都在一個技能裡：**規則**（原子做法）、**藍圖**（多階段場景模板）、**轉場**（場景到場景）、**技巧**（較廣泛的動態設計模式），以及**轉接器**（各執行環境的 API）。

合成契約（data 屬性、子合成、決定性）請見 `hyperframes-core`。
