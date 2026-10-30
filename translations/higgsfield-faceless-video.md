<!--meta
{"title":"Higgsfield 無露臉影片","category":"影片與多媒體","tags":["Higgsfield","無露臉影片","解說影片","兒歌影片","AI 影片"],
"summary":"用 Higgsfield CLI 製作完整的無露臉影片：插畫解說、紀錄片、繪本故事或兒童音樂影片，或編修先前做好的影片。依需求選擇製作模式（插畫解說、快剪動態、靜態繪本、兒歌、說話角色、主持人疊加、編修），在花費點數前先確認時長、比例、語言、風格、配音、音樂與字幕，並預估生成成本；以 ffmpeg 組裝影音片段而不改變語速。",
"usage":"- 需安裝並登入 `higgsfield` CLI，以及 ffmpeg、ffprobe、python3、curl、awk\n- 說「做一支 3 分鐘、16:9、中文的黑洞解說影片」「做一支兒歌影片」「修改這支無露臉影片的第二段」\n- 風格與配音用 `higgsfield preset list video-explainer --json`、`higgsfield voices list --json` 查詢，不會自己捏造 ID\n- 不適用於單一無聲片段、廣告／UGC 或只要腳本的需求"}
-->
---
version: 0.14.0
name: higgsfield-faceless-video
description: |
  建立一支完成的無露臉解說片、紀錄片、插畫故事或兒童音樂影片，或編修先前建立的無露臉影片。使用時機：「做一支無露臉影片」「建立有旁白的解說片」「做一支兒歌影片」「編修這支無露臉影片」。不適用於：單一無聲片段、廣告或 UGC、無關的素材剪輯，或只要腳本的請求。
argument-hint: "[topic or source] [duration] [language] [aspect ratio]"
allowed-tools: Bash
---

# 無露臉影片

建立一支視覺風格與旁白一致的完成影片。插畫解說片使用經過設計、以圖表為主的場景；故事或紀錄片則依需求調整節奏與畫面。不要把解說片當成要求快速剪接。保留使用者提供的選擇與素材。

在生成之前選擇所要求的模式：插畫解說片使用 `references/production.md`；快剪的頻道式動態使用 `references/channel-motion.md`；靜態圖片與繪本故事使用 `references/picture-story.md`；有歌唱的兒童音樂影片使用 `references/song.md`；明確要求的說話角色使用 `references/talking-characters.md`；要求的主持人疊加在動態工作流程之外搭配使用 `references/presenter.md`；編修先前生成的影片使用 `references/editing.md`。只要求背景音樂不算是歌曲請求。絕不要從偶然出現的照片推斷要加主持人。

當需求中提供了 `animation_mode`，把 `fully_animated` 視為動態、`scene_based` 視為靜態圖片，不再重複詢問。從完整的需求（包括主題與腳本）判斷是否為歌曲意圖；明確要唱歌的兒童影片即使提供了配音，也使用歌曲模式。延續或編修既有影片時，保留原本的製作模式。

## 花費點數之前

確認缺少的主題、大約時長、畫面比例、語言、視覺風格、配音、音樂與字幕選擇。絕不捏造 preset 或配音 ID。使用 `higgsfield preset list video-explainer --json` 與 `higgsfield voices list --json` 取得目前的選項，並用 `higgsfield preset resolve video-explainer <id> --json` 解析選定的 preset。使用參考圖片之前，先確認每張照片的角色。遵守要求的時長；絕不默默地把它進位加長。

找出本技能的安裝目錄，並保留其絕對路徑作為 `SKILL_DIR`。所有工作都放在一個持久的工作階段目錄中，而不是技能目錄。生成之前確認 `higgsfield account status`、`ffmpeg`、`ffprobe`、`python3`、`curl` 與 `awk`，並對每個計畫使用的模型用 `higgsfield model get` 檢查即時的結構定義。在支援的情況下用 `higgsfield generate cost` 預估生成成本；如果無法預估，在生成之前揭露這一點。如果任何必要的階段、模型、相依項目或要求的功能無法使用，在進行付費工作之前說明並停止。不要呼叫 `explainer_video` 或 `video_explainer`。

閱讀 `references/production.md` 了解生成、組裝、品管、復原與交付的程序。若需要字幕，閱讀 `references/captions.md`，並在付費生成之前檢查其相依項目。風格、素材、長篇規劃與審閱請閱讀 `references/creative.md`，風格指引請閱讀 `references/styles.md`，撰寫場景計畫時閱讀 `references/prompts.md`。可執行的輔助腳本 `scripts/assemble_blocks.sh` 會在不改變語速的情況下組裝依序排列的影音配對；執行前先閱讀它的用法。既有的安裝仍支援先前的技能名稱。
