<!--meta
{"title":"交接文件","category":"需求與規劃","tags":["交接","上下文壓縮","多代理","Matt Pocock"],
"summary":"把目前的對話濃縮成一份交接文件，讓另一個全新的代理（或新的對話）能無縫接手工作。",
"usage":"- 安裝：`npx skills add https://github.com/mattpocock/skills --skill handoff`\n- 對話快塞滿或要換 session 時輸入 `/handoff 下一階段要做的事`\n- 文件會存到系統暫存目錄（不是專案資料夾），並附上「建議使用的 skills」；機密資訊會被遮蔽，已存在的規格/PR 只放連結不重複貼"}
-->
---
name: handoff
description: 把目前的對話壓縮成一份交接文件，供另一個代理接手。
argument-hint: "下一個 session 要用來做什麼？"
disable-model-invocation: true
---

撰寫一份交接文件，摘要目前的對話，讓一個全新的代理可以繼續這項工作。存到使用者作業系統的暫存目錄（`$TMPDIR`，否則 `/tmp`；Windows 上為 `%TEMP%`）——而不是目前的工作區。

在文件中加入「建議技能」一節，列出下一個代理應該用 Skill 工具呼叫哪些技能。

不要重複已經記錄在其他產出物中的內容（規格、計畫、ADR、issue、commit、diff），改用路徑或 URL 引用它們。

遮蔽任何敏感資訊，例如 API 金鑰、密碼或個人可識別資訊。

如果使用者有傳入參數，就把它視為下一個 session 要聚焦的內容描述，並據此調整文件。
