<!--meta
{"title":"Issue 分類整理","category":"程式品質與除錯","tags":["Issue","PR","專案管理","開源維護","Matt Pocock"],
"summary":"把 issue 與外部 PR 送進一套分類狀態機（bug/enhancement × needs-triage/needs-info/ready-for-agent/ready-for-human/wontfix）：先驗證、必要時拷問釐清，最後寫出可直接交給 AI 代理執行的任務簡報。",
"usage":"- 安裝：`npx skills add https://github.com/mattpocock/skills --skill triage`，並先執行 `/setup-matt-pocock-skills` 設定標籤對應\n- 手動輸入 `/triage` 後用自然語言下指令：「有哪些需要我處理？」「看一下 #42」「把 #42 移到 ready-for-agent」\n- 每則貼到 issue 的留言都會加上 AI 產生的免責聲明"}
-->
---
name: triage
description: 讓 issue 與外部 PR 通過一套分類角色的狀態機：歸類、驗證、必要時拷問釐清，並撰寫可交給代理執行的簡報。
disable-model-invocation: true
---

# 分類整理（Triage）

讓專案 issue 追蹤系統上的 issue 通過一個由分類角色組成的小型狀態機。

如果這個 repo 把外部 pull request 視為一種請求管道（見 issue-tracker 設定），分類也涵蓋它們：**PR 就是附帶程式碼的 issue**，使用相同的角色、相同的狀態與相同的狀態機，只有少數差異會在下方以「對於 PR」標示。依照追蹤系統設定，把單純的 `#42` 解析為 issue 或 PR。

分類期間貼到 issue 追蹤系統的每則留言或 issue，都**必須**以這段免責聲明開頭：

{{CODE:1}}

## 參考文件

- [AGENT-BRIEF.md](AGENT-BRIEF.md)：如何撰寫耐用的代理簡報
- [OUT-OF-SCOPE.md](OUT-OF-SCOPE.md)：`.out-of-scope/` 知識庫如何運作

## 角色

兩個**類別**角色：

- `bug`：有東西壞了
- `enhancement`：新功能或改進

五個**狀態**角色：

- `needs-triage`：維護者需要評估
- `needs-info`：等待回報者提供更多資訊
- `ready-for-agent`：已完整規格化，可交給無人值守（AFK）的代理
- `ready-for-human`：需要人類實作
- `wontfix`：不會處理

對於 PR，相同的狀態是針對附帶的程式碼來解讀：`ready-for-agent` 代表已附上簡報，代理應對 diff 採取下一步；`ready-for-human` 代表已可由人類合併。

每個分類過的 issue 應該剛好帶有一個類別角色與一個狀態角色。如果狀態角色有衝突，先標記出來並詢問維護者，再做其他事。

這些是標準的角色名稱。issue 追蹤系統中實際使用的標籤字串可能不同。對應關係應該已經提供給你。如果沒有，請使用者執行 `/setup-matt-pocock-skills`。

狀態轉換：未加標籤的 issue 通常先進入 `needs-triage`；從那裡移到 `needs-info`、`ready-for-agent`、`ready-for-human` 或 `wontfix`。回報者回覆後，`needs-info` 回到 `needs-triage`。維護者隨時可以覆寫；看起來不尋常的轉換要標記出來並在進行前詢問。

## 呼叫方式

維護者呼叫 `/triage`，並用自然語言描述他們想要什麼。解讀請求並採取行動。範例：

- 「給我看所有需要我注意的東西」
- 「我們來看 #42」（issue 或 PR）
- 「把 #42 移到 ready-for-agent」
- 「有哪些已經可以讓代理接手？」

## 顯示需要注意的項目

查詢 issue 追蹤系統，並以最舊的優先呈現三個分組：

1. **未加標籤**：從未分類過。
2. **`needs-triage`**：評估進行中。
3. **自上次分類筆記後回報者有新動態的 `needs-info`**：需要重新評估。

當 PR 在範圍內時，把外部 PR 也納入這些分組，並在每一行標上 `[PR]` 或 `[issue]`。探索只會呈現*外部* PR（追蹤系統設定定義誰算外部），所以協作者進行中的 PR 不是分類工作。這個篩選只用於探索；被明確指名的 PR 無論作者是誰一律會分類。

顯示數量以及每個項目的一行摘要。讓維護者挑選。

## 分類特定的 issue 或 PR

1. **收集脈絡。** 讀完整個 issue 或 PR（內文、留言、標籤、作者、日期；對於 PR 還要看 diff）。解析任何先前的分類筆記，避免重問已解決的問題。使用專案的領域詞彙表探索程式碼庫，並尊重該區域的 ADR。針對程式碼庫做兩項檢查：(a) **重複性**：依領域概念（而不只是請求的字面用語）搜尋所請求行為是否已有實作，並回報你找過哪些地方。如果找到，就是「已實作」的 `wontfix`（步驟 5）。(b) **先前是否被拒絕**：閱讀 `.out-of-scope/*.md`，並提出任何與此請求相似的項目。

2. **提出建議。** 告訴維護者你建議的類別與狀態及理由，並附上與該請求相關的程式碼庫簡要摘要（包括是否已經實作）。等待指示。

3. **驗證主張。** 在任何拷問之前，先確認主張站得住腳。對於 bug，依照回報者的步驟重現它。對於 PR，確認 diff 確實做到它宣稱的事：checkout 下來、執行相關測試或指令。回報結果：已確認（附程式路徑）、失敗，或細節不足（強烈的 `needs-info` 訊號）。經確認的驗證能讓代理簡報強得多。

4. **拷問（如有需要）。** 如果請求需要補充細節，就呼叫 Skill 工具兩次，分別用「grilling」與「domain-modeling」，一次一輪問題地把它拷問成形，磨利領域用語，並在決策成形時即時更新 `GLOSSARY.md`/ADR。

5. **套用結果：**
   - `ready-for-agent`：貼上一則代理簡報留言（[AGENT-BRIEF.md](AGENT-BRIEF.md)）。
   - `ready-for-human`：結構與代理簡報相同，但註明為什麼不能委派（需要判斷、需要外部存取、設計決策、手動測試）。
   - `needs-info`：貼上分類筆記（模板見下方）。
   - 對於 `wontfix`，關閉 issue，留言內容依*原因*而定：
     - **已實作**：程式碼庫中已有這項變更。指出它在哪裡；**不要**寫入 `.out-of-scope/`（那個知識庫是給*被拒絕*的請求，不是已完成的）。
     - **拒絕（bug）**：給出禮貌的說明，然後關閉。
     - **拒絕（enhancement）**：寫入 `.out-of-scope/`，在留言中連結它，然後關閉（[OUT-OF-SCOPE.md](OUT-OF-SCOPE.md)）。
   - `needs-triage`：套用該角色。若有部分進展可選擇留言。

## 快速覆寫狀態

如果維護者說「把 #42 移到 ready-for-agent」，就信任他們並直接套用角色。確認你即將做的事（角色變更、留言、關閉），然後執行。略過拷問。如果沒有經過拷問就移到 `ready-for-agent`，詢問他們是否要撰寫代理簡報。

## Needs-info 模板

{{CODE:2}}

把拷問中所有已解決的事項記錄在「目前已確立」之下，避免成果流失。問題必須具體且可執行，而不是「請提供更多資訊」。

## 接續先前的 session

如果 issue 或 PR 上已有先前的分類筆記，先閱讀它們，檢查回報者是否回答了任何未解決的問題，並在繼續之前呈現更新後的全貌。不要重問已解決的問題。
