<!--meta
{"title":"HyperFrames 混音","category":"影片與多媒體","tags":["影片製作","混音","音效","Web Audio","HyperFrames"],
"summary":"HyperFrames 影片的音訊混音：把混音看成音軌之間的「關係」而不是一疊效果器——找出兩條音軌在爭什麼，交給需要的那一方。效果以 `data-fx-chain` 寫在元素上，預覽與渲染跑同一套 Web Audio 圖，聽到的就是輸出的。本頁內容取自 skills.sh 頁面的摘錄，該 skill 已從 GitHub 儲存庫的主分支移除。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-audio`\n- 說「旁白出現時背景音樂自動壓低」「這兩段音樂的銜接加淡入淡出」\n- 取得音樂、音效、旁白素材請用 media-use"}
-->
**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-audio/../hyperframes/references/plugin-installation.md)。獨立安裝則維持下方的更新說明。

# HyperFrames 音訊

混音是一組關係，而不是一疊處理器。兩條各自聽起來都對的音軌，放在一起可能令人無法聆聽，而修正方法幾乎從來不是「把其中一條調小聲」——而是找出它們在爭奪什麼，然後把它交給需要它的那一方。這裡的每個工具，都是為了表達其中一種關係而存在。

效果以 `data-fx-chain` 存在元素上，預覽與渲染執行同一個 Web Audio 圖——Studio 在即時的脈絡中、引擎則在它本來就在驅動的瀏覽器內以離線方式執行。每種效果只有一份實作，所以你拖曳預覽時聽到的，就是會被寫出的。你永遠不需要調兩次。
