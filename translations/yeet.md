<!--meta
{"title":"一鍵提交並開 PR","category":"雲端與 DevOps","tags":["Git","GitHub","Pull Request","gh CLI","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：只在你明確要求時，用 gh CLI 一次完成 stage、commit、push 並開啟 GitHub PR。會自動找出 repo 的 PR 模板、預設開草稿 PR，PR 標題用 `<type>(<scope>): <subject>` 格式，內文先寫「為什麼」再寫「改了什麼」。",
"usage":"- Codex：`$skill-installer yeet`；需先安裝並登入 `gh`（`gh auth login`）\n- 說「yeet」「全部 commit、push 然後開 PR」\n- 在 main 上會先開新分支；分支已有 PR 時會更新它而不是另開，也不會改變它的草稿狀態\n- 不會刪除既有 PR 內文中的圖片"}
-->
---
name: "yeet"
description: "只在使用者明確要求使用 GitHub CLI（`gh`）在一個流程中完成 stage、commit、push 並開啟 GitHub pull request 時使用。"
---

## 前置條件

- 需要 GitHub CLI `gh`。檢查 `gh --version`。如果沒有，請使用者安裝 `gh` 並停止。
- 需要已驗證的 `gh` session。執行 `gh auth status`。如果未驗證，請使用者執行 `gh auth login`（並重新執行 `gh auth status`）後再繼續。

## 命名慣例

- 分支：從 main/master/預設分支開始時，使用 `{description}`。
- Commit：`{description}`（簡短）。
- PR 標題：摘要整個 diff 的 `{description}`。

## 尋找 PR 模板

在建立 PR 之前，解析 repo 根目錄，並從那裡尋找啟用中的 GitHub PR 模板：

{{CODE:1}}

模板候選，依序為：

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/pull_request_template/` 下的一個 `*.md` 檔
- `.github/PULL_REQUEST_TEMPLATE/` 下的一個 `*.md` 檔

使用從 repo 根目錄輸出的路徑，例如 `.github/pull_request_template.md`，而不是 `./.github/pull_request_template.md`。

如果恰好找到一個模板，在撰寫最終 PR 內文之前先閱讀它，並以 `--template "$template"` 傳給 `gh pr create`。

如果找到多個模板檔，在建立 PR 之前停下來，詢問要使用哪個模板。如果沒有模板，使用本技能中的備用內文形狀。

## 工作流程

- 如果在 main/master/預設分支上，建立一個分支：`git checkout -b "{description}"`
- 否則留在目前的分支。
- 確認狀態，然後 stage 所有東西：`git status -sb` 然後 `git add -A`。
- 以描述簡短地 commit：`git commit -m "{description}"`
- 如果還沒執行檢查，就執行。如果檢查因缺少相依套件/工具而失敗，就安裝相依套件並重新執行一次。
- 帶追蹤地 push：`git push -u origin $(git branch --show-current)`
- 如果 git push 因 workflow 驗證錯誤而失敗，就從 master pull，然後重試 push。
- 尋找並閱讀 repo 的 PR 模板（如果有）。
- 檢查目前的分支是否已經有 PR：`gh pr view "$(git branch --show-current)" --json number,isDraft,url`
- 如果已經有 PR，就原地更新那個 PR。不要建立另一個 PR，也不要改變既有 PR 是草稿還是可審查的狀態。
- 如果沒有 PR，就開啟一個新的草稿 PR：
  - 有一個模板時：`GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --template "$template" --head "$(git branch --show-current)"`
  - 沒有模板時：`GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head "$(git branch --show-current)"`
- 編輯 PR 標題與內文，讓它們反映 diff 中實際的淨變更。
- 把 PR 描述寫進一個有真正換行的暫存檔，並透過 `--body-file` 或 `gh pr edit --body-file` 傳入，以避免出現 `\n` 跳脫的 markdown。

## 確定 PR

在更新流程中稍早建立的 PR 時，盡可能從目前的分支推斷 PR：

{{CODE:2}}

如果這找到了一個既有的 PR，保留它目前的審查狀態。絕不在 `yeet` 中把一個既有的「可審查」PR 改回草稿；只有這個流程新建立的 PR 才應以草稿開始。

## PR 標題

格式：`<type>(<scope>): <subject>`

`<scope>` 是選填的。scope 是一個描述程式碼庫某個部分（元件、服務或子系統）的名詞。

### 範例

{{CODE:3}}

更多範例：

- `feat`：（給使用者的新功能，不是給建置腳本的新功能）
- `fix`：（給使用者的 bug 修正，不是對建置腳本的修正）
- `docs`：（文件的變更）
- `style`：（格式、缺少分號等；沒有正式程式碼的變更）
- `refactor`：（重構正式程式碼，例如重新命名變數）
- `test`：（加入缺少的測試、重構測試；沒有正式程式碼的變更）
- `chore`：（更新 grunt 任務等；沒有正式程式碼的變更）


## PR 內文內容

被呼叫時，使用 `gh` 編輯 pull request 的內文與標題，以反映指定 PR 的內容。務必檢查既有的 pull request 內文，看看是否有應該保留的關鍵資訊。例如，絕不要移除既有 pull request 內文中的圖片，因為如果你移除它，作者可能沒有辦法復原。

當 repo 有 PR 模板時，讓最終的 PR 內文配合那個模板。保留有意義的標題、必要的檢查清單與 repo 專屬的提示，但把占位文字替換成針對淨 diff 的內容，或在模板要求時填 `N/A`。不要只因為下方的備用形狀比較短，就丟掉模板的章節。

解釋這項變更*為什麼*要做，是非常重要的。如果呼叫本技能的目前對話中討論過動機，務必把它記錄在 pull request 內文中。

內文也應該解釋*改了什麼*，但這應該放在*為什麼*之後。

把討論限制在 commit 的*淨變更*上。一般不贊成討論在開發 pull request 的過程中嘗試過、後來又撤回的變更。改寫 pull request 內文時，當這類細節對未來的讀者不再合適/有意義時，你可能需要把它們刪除。

避免提及我本機磁碟上的絕對路徑。談到 repo 內的路徑時，直接使用相對於 repo 的路徑。

預設省略 `Verification`。只有在你有值得為審查者保留的行為證據時才加入：一個重現的 bug、一個前後對照的檢查、一個演練了變更行為的針對性測試，或一個有輸入與觀察結果的手動情境。不要用它來放一般性的指令或自動化結果，例如套件測試、型別檢查、linter、格式化工具、pre-commit/pre-push hook 或 CI 狀態。

如果 repo 的模板要求驗證章節，就保留那個章節並避免空泛的填充：包含有意義的指令/結果、一個針對性的手動情境，或註明 `Not run` 並附上原因。

使用專業的 Markdown：

- 把程式碼、路徑、指令、旗標與識別碼放在反引號中。
- shell 逐字紀錄或多行範例使用圍欄程式碼區塊。
- 引用與變更相關的既有程式碼時，使用 GitHub 永久連結。
- 引用相關的 issue 或相關的 PR，但不要在 PR 自己的內文中引用它自己。

### 建議的 PR 內文形狀

當 repo 沒有 PR 模板時，以此作為備案：

{{CODE:4}}
