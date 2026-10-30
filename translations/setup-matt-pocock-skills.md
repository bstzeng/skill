<!--meta
{"title":"Matt Pocock 技能初始設定","category":"技能管理","tags":["初始設定","Issue Tracker","分類標籤","CLAUDE.md","Matt Pocock"],
"summary":"在使用 Matt Pocock 的工程類技能（to-spec、to-tickets、triage、code-review 等）之前執行一次：為這個 repo 設定 issue 追蹤系統（GitHub、GitLab、本機 Markdown 或其他）、分類標籤用語，以及 GLOSSARY.md／ADR 的存放方式，並寫入 CLAUDE.md 或 AGENTS.md。",
"usage":"- 安裝：`npx skills add https://github.com/mattpocock/skills --skill setup-matt-pocock-skills`\n- 在 repo 根目錄手動輸入 `/setup-matt-pocock-skills`\n- 代理會先探索 repo 現況，再一節一節問你（每題都附建議答案），確認草稿後才寫入 `docs/agents/*.md`\n- 之後要改設定可直接編輯 `docs/agents/*.md`"}
-->
---
name: setup-matt-pocock-skills
description: "為這個 repo 設定工程類技能：建立它的 issue 追蹤系統、分類標籤用語與領域文件配置。在第一次使用其他工程技能之前執行一次。"
disable-model-invocation: true
---

# 設定 Matt Pocock 的技能

建立工程類技能所預設的、每個 repo 專屬的設定骨架：

- **Issue 追蹤系統**：issue 存放在哪裡（預設為 GitHub；也內建支援本機 Markdown）
- **分類標籤**：五個標準分類角色所使用的字串
- **領域文件**：`GLOSSARY.md` 與 ADR 存放在哪裡，以及閱讀它們的使用規則

這是一個由提示驅動的技能，而不是決定性的腳本。先探索、呈現你的發現、與使用者確認，然後才寫入。

## 流程

### 1. 探索

檢視目前的 repo 以了解其起始狀態。讀取任何存在的東西；不要假設：

- `git remote -v` 與 `.git/config`：這是 GitHub repo 嗎？是哪一個？
- repo 根目錄的 `AGENTS.md` 與 `CLAUDE.md`：有沒有其中一個？其中是否已經有 `## Agent skills` 一節？
- repo 根目錄的 `GLOSSARY.md` 與 `GLOSSARY-MAP.md`，以及舊版的 `CONTEXT.md` / `CONTEXT-MAP.md`。如果有舊版檔案，提議用 `git mv` 把它改成 `GLOSSARY` 名稱，並在 `docs/agents/domain.md` 中改寫這些名稱。
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目錄
- `docs/agents/`：本技能先前的輸出是否已經存在？
- `.scratch/`：這是已在使用本機 Markdown issue 追蹤慣例的跡象
- 是否已安裝 `triage` 技能？（與本技能並列的 `triage` 技能資料夾，或你的可用技能中有 `triage`。）這決定 B 節是否要執行。
- Monorepo 的訊號：`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 欄位，或已有內容且各自有 `src/` 的 `packages/*`。只有在真正大型的多套件 repo 中才會出現這些；沒有它們代表單一脈絡，幾乎所有 repo 都是如此。

### 2. 呈現發現並詢問

摘要有什麼、缺什麼。然後依序處理各節。一節一個答案，然後下一節。

每一節都以建議答案開頭，讓使用者一個字就能接受。只有在選擇確實會分岔時才給一行說明；探索已經解決的節就完全略過（`triage` 未安裝時略過 B 節，沒有 monorepo 時略過 C 節）。

**A 節：Issue 追蹤系統。**

> 說明：「issue 追蹤系統」是這個 repo 的 issue 存放之處。`to-tickets`、`triage` 與 `to-spec` 等技能會讀取並寫入它。它們需要知道要呼叫 `gh issue create`、在 `.scratch/` 下寫一個 Markdown 檔，還是遵循你描述的其他流程。選擇你實際追蹤這個 repo 工作的地方。

預設立場：這些技能是為 GitHub 設計的。如果 `git remote` 指向 GitHub，就提議用它。如果 `git remote` 指向 GitLab（`gitlab.com` 或自架主機），就提議 GitLab。否則（或使用者偏好時），提供：

- **GitHub**：issue 存在 repo 的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**：issue 存在 repo 的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本機 Markdown**：issue 以檔案形式存在這個 repo 的 `.scratch/<feature>/` 下（適合個人專案或沒有遠端的 repo）
- **其他**（Jira、Linear 等）：請使用者用一段話描述流程；技能會把它記錄成自由形式的文字

把選擇記錄在 `docs/agents/issue-tracker.md`。GitHub 與 GitLab 模板帶有一個「把 PR 當作請求管道」的旗標，預設**關閉**。保持關閉，也不要提起它：想把外部 PR 納入分類佇列的使用者，之後可以在檔案中切換這個旗標。

GitHub 或 GitLab 追蹤系統需要一個可連線的 repo。當使用者選了其中一個、但沒有 `git remote` 指向該主機時，向他們取得 repo URL 並接好（需要時 `git init`、`git remote add origin <url>`），再繼續。當 `gh repo view` / `glab repo view` 在此目錄中能印出該專案時就完成了；如果不能，停下來告訴使用者缺少什麼。

**B 節：分類標籤用語。** 如果沒有安裝 `triage` 技能（探索已告訴你），就完全略過本節，因為未安裝的技能不需要標籤。

如果已安裝，只問一個問題：

> 你要保留預設的分類標籤嗎？（建議：**是**）

預設值是五個標準角色，每個標籤字串都等於其名稱：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。回答**是**時，原樣寫入。只有在使用者說不時（通常是因為他們的追蹤系統已經在用其他名稱，例如用 `bug:triage` 代表 `needs-triage`），才蒐集覆寫值，讓 `triage` 套用既有的標籤，而不是建立重複的標籤。

**C 節：領域文件。** 預設為**單一脈絡**（repo 根目錄一個 `GLOSSARY.md` + `docs/adr/`）。這適合幾乎所有 repo；不必詢問就寫入。

只有在探索發現 monorepo 訊號時，才提供**多脈絡**（根目錄的 `GLOSSARY-MAP.md` 指向各脈絡的 `GLOSSARY.md` 檔）。然後確認他們要哪種配置。

### 3. 確認並編輯

讓使用者看以下內容的草稿：

- 要加到正在編輯的 `CLAUDE.md` / `AGENTS.md`（選擇規則見步驟 4）中的 `## Agent skills` 區塊
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 與 `docs/agents/triage-labels.md` 的內容（最後一個只在安裝了 `triage` 時才有）

讓他們在寫入前先編輯。

### 4. 寫入

**選擇要編輯的檔案：**

- 如果 `CLAUDE.md` 存在，就編輯它。
- 否則如果 `AGENTS.md` 存在，就編輯它。
- 如果兩者都不存在，詢問使用者要建立哪一個；不要替他們選。

當 `CLAUDE.md` 已經存在時，絕不建立 `AGENTS.md`（反之亦然）；一律編輯已經存在的那個。

如果所選檔案中已經有 `## Agent skills` 區塊，就原地更新其內容，而不是再附加一個重複的區塊。不要覆寫使用者對周圍各節的修改。

區塊內容：

{{CODE:1}}

只有在安裝了 `triage` 且執行了 B 節時，才包含 `### Triage labels` 子區塊並寫入 `docs/agents/triage-labels.md`。若沒有，兩者都省略。

當 B 節是在 GitHub 或 GitLab 上執行時，建立追蹤系統所缺少的每個已設定標籤（`gh label create` / `glab label create`）。

然後以本技能資料夾中的種子模板為起點寫入文件檔：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue 追蹤系統
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue 追蹤系統
- [issue-tracker-local.md](./issue-tracker-local.md)：本機 Markdown issue 追蹤系統
- [triage-labels.md](./triage-labels.md)：標籤對應（只在安裝了 `triage` 時）
- [domain.md](./domain.md)：領域文件的使用規則 + 配置

對於「其他」issue 追蹤系統，根據使用者的描述從零撰寫 `docs/agents/issue-tracker.md`。

### 5. 完成

告訴使用者設定已完成，以及哪些工程技能現在會讀取這些檔案。提到他們之後可以直接編輯 `docs/agents/*.md`；只有在想切換 issue 追蹤系統或從頭開始時，才需要重新執行本技能。
