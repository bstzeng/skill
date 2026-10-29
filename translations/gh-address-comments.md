<!--meta
{"title":"處理 PR 審查意見","category":"雲端與 DevOps","tags":["GitHub","Code Review","gh CLI","OpenAI Codex"],
"summary":"找出目前分支對應的 GitHub PR，列出所有審查意見與討論串並編號摘要，讓你挑選要處理哪幾則，再由代理動手修正。",
"usage":"- Codex：`$skill-installer gh-address-comments` 安裝；其他代理可直接複製 skill 資料夾\n- 先 `gh auth login` 完成登入\n- 在 PR 分支上對代理說「幫我處理這個 PR 的 review comments」\n- 代理會列出編號清單 → 你回覆要處理的編號 → 代理套用修正"}
-->
---
name: gh-address-comments
description: 使用 gh CLI 協助處理目前分支所對應的開啟中 GitHub PR 上的審查/issue 意見；先驗證 gh 是否已登入，若未登入則提示使用者進行驗證。
metadata:
  short-description: 處理 GitHub PR 審查中的意見
---

# PR 意見處理器

指引如何找到目前分支的開啟中 PR，並用 gh CLI 處理其中的意見。所有 `gh` 指令都要以提升的網路權限執行。

前置條件：確認 `gh` 已驗證（例如執行一次 `gh auth login`），然後以提升的權限執行 `gh auth status`（包含 workflow/repo 範圍），讓 `gh` 指令能成功執行。如果沙箱阻擋了 `gh auth status`，就以 `sandbox_permissions=require_escalated` 重新執行。

## 1) 檢查需要處理的意見
- 執行 scripts/fetch_comments.py，它會列出 PR 上所有的意見與審查討論串

## 2) 向使用者確認
- 為所有審查討論串與意見編號，並簡短摘要每一則需要做什麼修正
- 詢問使用者要處理哪幾個編號的意見

## 3) 如果使用者選了意見
- 對選定的意見套用修正

注意：
- 如果 gh 在執行途中遇到驗證或速率限制問題，提示使用者用 `gh auth login` 重新驗證，然後重試。
