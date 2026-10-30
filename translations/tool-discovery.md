<!--meta
{"title":"工具探索：選對代理與技能","category":"技能管理","tags":["技能推薦","子代理","claude-mods","Claude Code"],
"summary":"claude-mods 套件中的導覽技能：依任務推薦該用哪個重量級代理（Agent 工具）或輕量技能（Skill tool）。內附決策流程圖、40 多個 `-ops` 技能的觸發關鍵字速查表、代理速查表、依任務類型對照的建議，以及「技能用於查詢模式、代理用於決策」的原則，每個任務最多推薦 2–3 個工具。",
"usage":"- 說「這個任務該用哪個 agent？」「哪個 skill 適合做 X？」「幫我選工具」\n- 需要搭配 claude-mods 的其他 `-ops` 技能才有對應的實際內容\n- 完整目錄見 `references/agents-catalog.md` 與 `references/skills-catalog.md`"}
-->
---
name: tool-discovery
description: "為任何任務推薦合適的代理與技能。涵蓋重量級的代理（Agent 工具）與輕量的技能（Skill 工具）。觸發於：哪個代理、哪個技能、我該用什麼工具、幫我選、推薦代理、找到合適的工具。"
license: MIT
allowed-tools: "Read Glob"
metadata:
  author: claude-mods
  related-skills: claude-code-ops
---

# 工具探索

為任何任務推薦合適的代理與技能。

## 決策流程圖

{{CODE:1}}

**規則：** 技能 = 模式／參考。代理 = 決策／專業。

## 技能速查

| 技能 | 觸發關鍵字 |
|-------|----------|
| **file-search** | fd、rg、fzf、找檔案 |
| **find-replace** | sd、批次取代 |
| **code-stats** | tokei、difft、行數統計 |
| **data-processing** | jq、yq、json、yaml |
| **structural-search** | ast-grep、sg、AST 模式 |
| **git-ops** | git、gh、lazygit、delta、commit、PR、release、rebase |
| **python-env** | uv、venv、pyproject |
| **go-ops** | golang、go、goroutine、channel、context、errgroup、go test |
| **rust-ops** | rust、cargo、ownership、tokio、serde、trait、Result、Option |
| **typescript-ops** | typescript、型別系統、泛型、utility types、Zod |
| **docker-ops** | docker、Dockerfile、docker-compose、多階段建置 |
| **ci-cd-ops** | github actions、CI、CD、pipeline、release、workflow |
| **api-design-ops** | API 設計、gRPC、GraphQL、進階 REST、protobuf |
| **rest-ops** | HTTP 方法、狀態碼 |
| **sql-ops** | CTE、視窗函式 |
| **postgres-ops** | postgresql、postgres、EXPLAIN ANALYZE、vacuum、pgbouncer、JSONB、RLS、replication |
| **sqlite-ops** | sqlite、EXPLAIN QUERY PLAN、覆蓋索引、rows_read、D1、wrangler d1、node:sqlite、better-sqlite3、bun:sqlite、aiosqlite、libsql、fts5 |
| **tailwind-ops** | tailwind、tw classes、深色模式、響應式 |
| **mcp-ops** | MCP 伺服器、fastmcp、tool handler、transport |
| **react-ops** | react、hooks、useState、next.js、RSC、zustand |
| **vue-ops** | vue、composition api、pinia、nuxt、script setup |
| **javascript-ops** | javascript、node、esm、async/await、event loop |
| **astro-ops** | astro、islands、content collections、部分水合 |
| **laravel-ops** | laravel、eloquent、artisan、sanctum、pest |
| **payloadcms-ops** | payload、payload cms、headless cms、collections |
| **craftcms-ops** | craft、craftcms、twig、matrix fields |
| **asus-router-ops** | 華碩路由器、asuswrt、merlin、網路強化 |
| **nginx-ops** | nginx、反向代理、ssl、負載平衡、proxy_pass |
| **cloudflare-ops** | cloudflare、workers、KV、D1、R2、pages、wrangler、edge |
| **cypress-ops** | cypress、e2e、元件測試、custom commands、stubbing |
| **bash-ops** | bash、shell 腳本、traps、CI 腳本、防禦性腳本 |
| **claude-code-ops** | Claude Code 擴充、skills、agents、hooks、MCP、plugins |
| **auth-ops** | jwt、oauth2、session、rbac、passkey、mfa、登入 |
| **monitoring-ops** | prometheus、grafana、opentelemetry、SLO、告警 |
| **debug-ops** | 除錯、當機、記憶體洩漏、競態條件、bisect |
| **perf-ops** | 效能、profiling、火焰圖、bundle 大小、負載測試、基準測試 |
| **migrate-ops** | 遷移、升級、破壞性變更、codemod、版本升級 |
| **refactor-ops** | 重構、抽取、程式碼異味、死碼、重新命名、重組 |
| **scaffold** | 骨架、樣板、專案範本、初始化專案、新專案 |
| **log-ops** | JSONL、日誌分析、解析日誌、lnav、日誌搜尋、時間軸 |

## 代理速查

| 代理 | 觸發關鍵字 |
|-------|----------|
| **firecrawl-expert** | 網頁爬取、爬蟲、反機器人 |
| **project-organizer** | 重組、整理、清理 |
| **git-agent** | commit、push、PR（由 git-ops 派發） |
| **Explore** | 「在哪裡」「找」 |
| **Plan** | 設計、架構 |

對於 Cloudflare／Workers、Cypress／E2E、shell 腳本、Claude Code 擴充工作，以及 CMS／裝置領域（Payload、Craft、華碩路由器），使用對應的 `-ops` 技能（`cloudflare-ops`、`cypress-ops`、`bash-ops`、`claude-code-ops`、`payloadcms-ops`、`craftcms-ops`、`asus-router-ops`）。對於語言／框架工作（Python、TypeScript、React、Postgres 等），使用對應的 `-ops` 技能——或派發 `general-purpose`，並指示它先讀該技能的 SKILL.md。

## 如何啟動

**技能：**
{{CODE:2}}

**代理**（在 Claude Code 2.1.63 之前，Agent 工具的名稱是 Task；`Task(...)` 仍可作為別名使用）：
{{CODE:3}}

## 依任務類型對照

| 任務 | 先用技能 | 必要時用代理 |
|------|-------------|-----------------|
| 「CTE 怎麼寫？」 | sql-ops | — |
| 「最佳化這個查詢」 | postgres-ops | — |
| 「找名為 X 的檔案」 | file-search | Explore |
| 「建立 Python 專案」 | python-env | — |
| 「X 該用哪個 HTTP 狀態碼？」 | rest-ops | — |
| 「React Server Components？」 | react-ops | — |
| 「Vue 3 composable 模式」 | vue-ops | — |
| 「設定 nginx SSL」 | nginx-ops | — |
| 「JWT 還是 session 認證」 | auth-ops | — |
| 「設定 Prometheus」 | monitoring-ops | — |
| 「除錯記憶體洩漏」 | debug-ops | — |
| 「爬一個被封鎖的網站」 | jina-ops | firecrawl-expert |

## 小技巧

- **技能比較便宜**——用於查詢、模式
- **代理比較強大**——用於決策、最佳化
- **不要過度推薦**——每個任務最多 2–3 個工具

## 其他資源

完整目錄請載入：
- `./references/agents-catalog.md` —— 所有代理及其能力
- `./references/skills-catalog.md` —— 部分技能的詳細說明，加上選擇指南（不是完整清單）
