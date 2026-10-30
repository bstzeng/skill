<!--meta
{"title":"遷移到 Codex","category":"技能管理","tags":["Codex","Claude Code","遷移","MCP","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：把 Claude Code 的指示檔（CLAUDE.md）、slash 指令、技能、子代理、hooks 與 MCP 設定，遷移成 Codex 的 AGENTS.md、`.agents/skills/`、`.codex/agents/`、`.codex/hooks.json` 與 `.codex/config.toml`。先掃描與試跑，再實際寫入、驗證並自我修復，最後以表格回報哪些已加入、哪些需要檢查。",
"usage":"- Codex：`$skill-installer migrate-to-codex`\n- 在專案中說「把我的 Claude Code 設定遷移到 Codex」，可選全域（`~/.claude` → `~/.codex`）或專案（`.claude` → `.codex`）\n- 指令：`--scan-only` / `--plan` / `--doctor` 先檢視 → `--dry-run` → 實際執行 → `--validate-target`\n- 不會修改原本的 Claude Code 檔案；外掛需要手動設定"}
-->
---
name: migrate-to-codex
description: 把支援的指示檔、技能、代理與 MCP 設定遷移到 Codex 的專案與全域檔案中。
---

# 遷移到 Codex

## 自主性

持續進行，直到選定的遷移完全完成：執行遷移器、檢查報告、修正遷移後的 Codex 指示/技能/代理/MCP 設定，並重新執行檢查，不要停下來請求確認下一步。如果使用者已經選定目標，在該目標（`AGENTS.md`、`.codex/`、`.agents/` 或 `~/.codex/`）中建立、編輯、取代或刪除產生的 Codex 產出物之前，不要詢問。保留 `.codex/config.toml` 或 `~/.codex/config.toml` 中不相關的既有 Codex 設定條目，例如 `notify`、`projects`、`marketplaces` 或不相關的 MCP 伺服器；除非它們驗證失敗或與遷移直接衝突，否則不要詢問。不要編輯來源的 Claude Code 檔案（`.claude/`、`~/.claude/`、`.mcp.json` 或 `.claude.json`）、不相關的專案程式碼、機密或其他 repo。

## 遷移順序

對每個選定的全域或專案來源，依此順序執行遷移：

1. 一開始先使用 Codex 內建的 TODO/任務清單工具。除非使用者明確要求，否則不要建立 `MIGRATION_TODOS.md` 或任何 TODO 檔。TODO 清單的輸入有一個 `plan` 陣列，其中每個項目都有 `step` 與 `status`；狀態使用 `pending`、`in_progress` 與 `completed`。讓 TODO 針對所選的產出物具體化。結束之前，更新 TODO 清單，讓每個完成的步驟都標記為 `completed`，且沒有任何步驟仍是 `in_progress`。使用字面上的「來源 → Codex 目標」標籤，例如：
   - 檢查 `.claude/commands` → Codex 技能/提示
   - 檢查 `.claude/agents` → `.codex/agents`
   - 檢查 `.mcp.json` → `.codex/config.toml` MCP 伺服器
   - 檢查 `.claude/settings.json` hooks → `.codex/hooks.json`
   - 遷移安全的所選產出物 → Codex 檔案
   - 驗證產生的 `.codex/config.toml`
   - 驗證產生的 `.codex/agents`
   - 回報已遷移的產出物與需人工審查的項目

2. 閱讀 `references/differences.md`（如果它的「Docs last checked」日期很舊，就重新整理 Codex 文件）。

3. 寫入之前先掃描與檢查：
   - `--scan-only` 列出啟用與未啟用的來源介面。
   - `--plan` 印出準備產生的 Codex 產出物路徑與報告列。
   - `--doctor` 摘要準備程度、需人工審查的工作與驗證風險。

4. 依 CLI 使用的相同順序轉換各介面：
   - 指示：`CLAUDE.md` / `AGENTS.md` 轉成 `AGENTS.md`
   - 外掛：把 Claude 外掛樹與 marketplace 回報為需手動遷移的工作
   - hooks：把支援的 Claude hooks 改寫進 `.codex/hooks.json`，並啟用 `[features].codex_hooks = true`
   - 技能與指令：在 `.agents/skills/` 下寫入 Codex 技能
   - 設定：從 Claude 的模型/沙箱設定與 MCP 伺服器寫出 `.codex/config.toml`，產生設定時包含 `personality = "friendly"`
   - 子代理：在 `.codex/agents/` 下寫入 Codex 自訂代理

5. 先試跑，再寫入所選的目標。只有在應該刪除孤立的已產生技能或代理時，才使用 `--replace`。

6. 實際執行之後，檢查終端機輸出與 `.codex/migrate-to-codex-report.txt`。

7. 依此順序審查產生的產出物：`AGENTS.md`、`.agents/skills/`、`.codex/config.toml`、`.codex/hooks.json`、`.codex/agents/`，然後是只列在報告中的外掛項目。

8. 編輯之後，對每個目標執行 `--validate-target`。

9. 編輯之後，重新執行檢查與 `--dry-run`。

10. 以每個有資料列的範圍一張 Markdown 表格，回傳最終的遷移報告。表格只涵蓋你所執行的非原生後續遷移工作，例如從 slash 指令建立的技能、子代理、MCP 伺服器、hooks、不支援/本機外掛的註記，以及需人工審查的但書。只有在你在這次後續執行中親自遷移了設定、指示、技能或支援的外掛時，才包含它們的程式化原生匯入列。

    如果只有一個範圍有資料列，就只渲染那張表格，不加標題。如果有多個範圍有資料列，在每張表格前渲染一個標題。使用者範圍的資料列使用 `**User Config**`。專案範圍的資料列，使用實際的專案資料夾名稱作為標題，例如 `**northstar-support-portal**`；不要用「Current Project」作為標題。不要在表格輸出前後加任何文字。

    確切使用以下欄位：

    **northstar-support-portal**

    | Status | Item | Notes |
    | --- | --- | --- |
    | `Added` | `Slash command` pr-review | Converted into a Codex skill |
    | `Added` | `Subagent` release-lead | Added as a Codex subagent |
    | `Check before using` | `Hook` PreToolUse | Converted, but some Claude hook behavior differs in Codex |
    | `Not Added` | `Hook` Notification | Codex does not have an equivalent notification hook |
    | `Not Added` | `Plugin` team-macros | Plugin needs manual setup |

    `Status` 必須是 `Added`、`Check before using` 或 `Not Added`。當建立或變更了一個面向 Codex 的產出物、且不需要特別審查時，使用 `Added`。當建立或變更了一個面向 Codex 的產出物，但遷移改變了語意、推斷了行為、把工具規則保留為指引，或丟掉了不支援的行為時，使用 `Check before using`。當偵測到來源產出物、但沒有建立任何面向 Codex 的產出物時，使用 `Not Added`。`Item` 在一個儲存格中結合產出物類型與具體的項目名稱。產出物類型必須是單數：`Skill`、`Slash command`、`Subagent`、`MCP`、`Hook` 或 `Plugin`。把產出物類型包在行內程式碼中；在其後以純文字寫出項目名稱。`Notes` 一律必填；絕不留空。讓註記保持簡短、平實、照字面。避免像 runtime expansion 這類內部實作術語。優先使用像 `Converted into a Codex skill`、`Added as a Codex subagent`、`Added to Codex config`、`Converted into a Codex hook`、`Converted, but some Claude hook behavior differs in Codex`、`Codex does not have an equivalent notification hook`、`Plugin needs manual setup` 或 `Plugin marketplace needs manual setup` 這樣的用語。

## 自我修復循環

持續循環，直到選定的遷移完成：

1. 執行 `--plan` 或 `--doctor`。
2. 以 `--dry-run` 執行遷移。
3. 實際執行遷移。
4. 修正每一個產生的 `## MANUAL MIGRATION REQUIRED` 區塊，以及每一個能在 Codex 產出物內解決的 `manual_fix_required` 或 `skipped` 報告列。
5. 執行 `--validate-target`。
6. 重新執行遷移器與驗證器，直到報告與驗證器都沒有剩下可處理的產生產出物修正為止。

在這個循環中，不要編輯來源的 Claude Code 檔案、不相關的專案程式碼、機密或其他 repo。如果某個報告列需要修改來源供應商的檔案或需要產品判斷，就在產生的 Codex 產出物中留下清楚的人工指引，而不是修改來源。

## 指令

選擇遷移器指令。

   ```bash
   MIGRATE_TO_CODEX='python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py'
   ```

寫入之前先檢查遷移。

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --scan-only
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --plan
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --doctor
   ```

對全域與專案，先試跑，再不帶 `--dry-run` 執行。

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/
   ```

編輯之後，對每個目標執行遷移後的驗證器。

   ```bash
   $MIGRATE_TO_CODEX --validate-target ~/.codex/
   $MIGRATE_TO_CODEX --validate-target ./.codex/
   ```

執行 `$MIGRATE_TO_CODEX --help` 查看旗標（`--scan-only`、`--plan`、`--doctor`、`--validate-target`、預設值等）。更深入的表格與更多連結在 `references/differences.md`。
