<!--meta
{"title":"HyperFrames 關鍵影格","category":"影片與多媒體","tags":["影片製作","關鍵影格","動畫","HyperFrames"],
"summary":"HyperFrames 的關鍵影格是一份「姿態契約」：可見的狀態、連續的主體識別、可安全定位的執行環境、經過驗證的像素。只負責視覺動態，剪接、修剪、重排等片段組裝交給 hyperframes-core。本頁內容取自 skills.sh 頁面的摘錄，該 skill 已從 GitHub 儲存庫的主分支移除。",
"usage":"- 安裝：`npx skills add https://github.com/heygen-com/hyperframes --skill hyperframes-keyframes`\n- 說「讓這個 Logo 從左下飛到中央並放大」等需要精準姿態控制的動作\n- 交叉淡化要用不同軌道上重疊的片段加上不透明度關鍵影格；聲音淡入淡出請用 hyperframes-audio"}
-->
**外掛安裝：** 當本技能位於 HyperFrames 外掛中時，在執行設定或更新指令之前，請遵循[外掛執行規則](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-keyframes/../hyperframes/references/plugin-installation.md)。獨立安裝則維持下方的更新說明。

# HyperFrames 關鍵影格

關鍵影格是一份姿態契約：可見的狀態、連續的主體識別、可安全定位的執行環境、經過驗證的像素。

廣泛的場景做法請用 `hyperframes-animation`。完整指令文件請用 `hyperframes-cli`。只有在選擇實作機制（而非視覺風格）時，才使用 `references/keyframe-patterns.md`。

## 創作者的編輯邊界

關鍵影格負責視覺動態，而不是片段組裝。來源區段的硬切、修剪、接合與重新排序屬於 `/hyperframes-core`：為每個保留的區段撰寫一個媒體元素，用 `data-start` 與 `data-duration` 擺放它，並用 `data-media-start` 選擇其來源偏移。相鄰的區段構成硬切。交叉淡化使用不同軌道上重疊的片段，加上視覺不透明度關鍵影格；聲音淡入淡出使用 `/hyperframes-audio`。
