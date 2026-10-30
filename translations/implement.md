<!--meta
{"title":"依規格實作","category":"程式品質與除錯","tags":["實作","TDD","Code Review","Issue","Matt Pocock"],
"summary":"依照規格書或一組工單實作工作：先抓取工單並說明標題，在事先約定的接縫上用 tdd 技能開發，定期跑型別檢查與單一測試，最後跑完整測試、用 code-review 技能自我審查並 commit。",
"usage":"- 安裝：`npx skills add https://github.com/mattpocock/skills --skill implement`（建議一起裝 tdd 與 code-review）\n- 手動輸入 `/implement #42` 或 `/implement docs/spec.md` 觸發\n- 常接在 to-spec 或 to-tickets 之後，形成「規格 → 工單 → 實作 → 審查」的完整流程"}
-->
---
name: implement
description: "依照規格書或一組工單實作一項工作。"
disable-model-invocation: true
---

實作使用者在規格書或工單中描述的工作。

如果使用者傳入工單參照，就從 issue 追蹤系統抓取它，並在開始前說明它的標題。如果參照模稜兩可，就詢問。

可能的話，在事先約定的接縫上，用「tdd」呼叫 Skill 工具。

定期執行型別檢查、定期執行單一測試檔，並在最後執行一次完整的測試套件。

完成後，用「code-review」呼叫 Skill 工具來審查這項工作。

把你的工作 commit 到目前的分支。
