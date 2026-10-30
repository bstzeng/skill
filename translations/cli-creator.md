<!--meta
{"title":"CLI 工具建立器","category":"AI 整合與開發工具","tags":["CLI","API 包裝","Rust","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：從 API 文件、OpenAPI、curl 範例、SDK、網頁應用、管理工具或本機腳本，建立一個可長期使用、從任何 repo 都能以指令名稱呼叫的組合式 CLI——有 doctor、探索、解析 ID、讀取、單一動作寫入與原始逃生口指令，回傳穩定 JSON、管理驗證，並附一個搭配的 skill。",
"usage":"- Codex：`$skill-installer cli-creator`\n- 說「用這份 OpenAPI 幫我做一個 ci-logs CLI，可以下載失敗 job 的日誌」\n- 預設用 Rust（clap + reqwest + serde），有官方 SDK 時改用 TypeScript，資料處理類用 Python\n- 完成後會安裝到 PATH、從 /tmp 做冒煙測試，並建立 `$CODEX_HOME/skills/<tool>/SKILL.md`"}
-->
---
name: cli-creator
description: 從 API 文件、OpenAPI 規格、既有的 curl 範例、SDK、網頁應用程式、管理工具或本機腳本，為 Codex 建立一個可組合的 CLI。當使用者希望 Codex 建立一個能從任何 repo 執行、提供可組合的讀取/寫入指令、回傳穩定 JSON、管理驗證，並搭配一個附屬技能的命令列工具時使用。
---

# CLI 建立器

建立一個真正的 CLI，讓未來的 Codex 執行緒可以從任何工作目錄以指令名稱執行它。

本技能是給長期使用的工具，而不是一次性的腳本。如果目前 repo 中的一支短腳本就能解決任務，就把腳本寫在那裡。

## 開始

為目標工具、它的來源，以及它應該做的第一批實際工作命名：

- 來源：API 文件、OpenAPI JSON、SDK 文件、curl 範例、瀏覽器應用程式、既有的內部腳本、文章，或可運作的 shell 歷史。
- 工作：字面上的讀取/寫入，例如 `list drafts`、`download failed job logs`、`search messages`、`upload media`、`read queue schedule`。
- 安裝名稱：一個簡短的執行檔名稱，例如 `ci-logs`、`slack-cli`、`sentry-cli` 或 `buildkite-logs`。

當使用者想要一個個人工具、且沒有指名 repo 時，優先在 `~/code/clis/<tool-name>` 下建立新資料夾。

建立骨架之前，檢查提議的指令是否已經存在：

{{CODE:1}}

如果已經存在，就選一個更清楚的安裝名稱，或詢問使用者。

## 選擇執行環境

選擇之前，檢查使用者的機器與來源材料：

{{CODE:2}}

然後選擇最不令人意外的工具鏈：

- 對於 Codex 應能從任何 repo 執行的長期 CLI，預設使用 **Rust**：一個快速的執行檔、強大的參數解析、良好的 JSON 處理，容易複製/安裝到 `~/.local/bin`。
- 當官方 SDK、驗證輔助工具、瀏覽器自動化函式庫或既有的 repo 工具，是讓 CLI 能做得更好的原因時，使用 **TypeScript/Node**。
- 當來源是資料科學、本機檔案轉換、notebook、SQLite/CSV/JSON 分析，或以 Python 為主、仍可安裝成長期指令的管理工具時，使用 **Python**。

除非能實質改善 CLI，否則不要選擇會增加設定摩擦的語言。如果最佳的語言沒有安裝，就在使用者核准下安裝缺少的工具鏈，或選擇次佳的已安裝選項。

在建立骨架之前，用一句話說明你的選擇，包括原因以及你找到的已安裝工具鏈。

## 指令契約

在寫程式碼之前，先在對話中勾勒指令介面。包括執行檔名稱、探索指令、解析或 ID 查找指令、讀取指令、寫入指令、原始逃生口、驗證/設定的選擇，以及 PATH/安裝指令。

設計指令介面時，閱讀 [references/agent-cli-patterns.md](references/agent-cli-patterns.md) 了解預期的可組合 CLI 形狀。

朝這個介面建構：

- `tool-name --help` 顯示每一項主要能力。
- `tool-name --json doctor` 驗證設定、驗證、版本、端點可達性，以及缺少的設定。
- 當只用環境變數驗證很麻煩時，`tool-name init ...` 儲存本機設定。
- 探索指令找出帳戶、專案、工作區、團隊、佇列、頻道、repo、儀表板或其他頂層容器。
- 解析指令把名稱、URL、代稱、永久連結、客戶輸入或建置連結轉成穩定的 ID，讓之後的指令不必重複廣泛的搜尋。
- 讀取指令抓取確切的物件，並列出/搜尋集合。分頁清單支援有界的 `--limit`、cursor、offset，或清楚記載的預設值。
- 寫入指令每個只做一個有名稱的動作：建立、更新、刪除、上傳、排程、重試、留言、草稿。它們接受最窄的穩定資源 ID，在服務允許時優先支援 `--dry-run`、`draft` 或 `preview`，並且不把寫入藏在像 `fix`、`debug` 或 `auto` 這樣的寬泛指令裡。
- `--json` 回傳穩定、機器可讀的輸出。
- 存在一個原始逃生口：`request`、`tool-call`、`api`，或最貼切的名稱。

不要只提供一個通用的 `request` 指令。為重複的工作給 Codex 高層的動詞。

在 CLI 的 README 或同等文件中記載 JSON 政策：API 直通 vs CLI 外層結構、成功的形狀、錯誤的形狀，以及每個指令家族的一個範例。在 `--json` 下，錯誤必須是機器可讀的，而且不得包含憑證。

## 驗證與設定

先支援無聊的路徑，依此優先順序：

1. 使用該服務標準名稱的環境變數，例如 `GITHUB_TOKEN`。
2. `~/.<tool-name>/config.toml` 或其他簡單、有記載路徑下的使用者設定。
3. `--api-key` 或工具專屬的 token 旗標，只用於明確的一次性測試。一般使用優先用環境變數/設定，因為旗標可能洩漏到 shell 歷史或程序清單中。

絕不印出完整的 token。`doctor --json` 應說明是否有可用的 token、驗證來源類別（`flag`、`env`、`config`、供應商預設或缺少），以及缺少哪個設定步驟。

如果 CLI 能在沒有網路或驗證的情況下執行，就在 `doctor --json` 中明確說明：回報測試資料/離線模式、是否找到測試資料，以及該模式是否不需要驗證。

對於來源是 DevTools curl 的內部網頁應用程式，在實作之前先建立經過清理的端點筆記：資源名稱、方法/路徑、必要的標頭、驗證機制、CSRF 行為、請求主體、回應的 ID 欄位、分頁、錯誤，以及一份遮蔽過的範例回應。絕不 commit 複製來的 cookie、bearer token、客戶機密或完整的正式環境承載。

用截圖推斷工作流程、UI 用語、欄位與確認點。除非截圖搭配了網路請求、匯出、文件頁或測試資料，否則不要把截圖當成 API 證據。

## 建構流程

1. 只讀到足以盤點資源、驗證、分頁、ID、媒體/檔案流程、速率限制與危險寫入動作的程度。如果文件提供了 OpenAPI，在為指令命名之前先下載或檢查它。
2. 在對話中勾勒指令清單。保持名稱簡短、適合 shell。
3. 建立 CLI 骨架，附上 README 或同等的、面向 repo 的說明。
4. 實作 `doctor`、探索、解析、讀取指令、被要求時的一個窄範圍草稿或試跑寫入路徑，以及原始逃生口。
5. 把 CLI 安裝到 PATH，讓 `tool-name ...` 在來源資料夾之外也能運作。
6. 從另一個 repo 或 `/tmp` 做冒煙測試，而不只是用 `cargo run` 或套件管理器的包裝。執行 `command -v <tool-name>`、`<tool-name> --help` 與 `<tool-name> --json doctor`。
7. 執行格式化、型別檢查/建置、請求建構器的單元測試、分頁/請求主體建構器、不需驗證的 `doctor`、說明輸出，以及至少一次測試資料、試跑或即時唯讀的 API 呼叫。

如果需要一次即時寫入才能有信心，先詢問，並讓它可逆或只做草稿。

當來源是既有的腳本或 shell 歷史時，把可運作的呼叫拆成真正的階段：設定、探索、下載/匯出、轉換/索引、草稿、上傳、輪詢、即時寫入。保留使用者已經依賴的旗標、路徑與環境變數，然後用穩定的 ID、有界的 JSON 與檔案輸出包裝可重複的階段。

對於原始逃生口，先支援唯讀呼叫。除非使用者要求了那個特定的寫入，否則不要對即時服務執行原始的非 GET/HEAD 請求。

對於媒體、產出物或預簽署上傳流程，分別測試每個階段：建立上傳、傳輸位元組、輪詢/讀取處理狀態，然後附加或參照產生的 ID。

對於以測試資料為後盾的原型，把測試資料放在可預期的專案路徑中，並讓 CLI 在安裝後能找到它們。從 `/tmp` 做冒煙測試，以抓出只能在來源資料夾內運作的執行檔。

對於以日誌為主的 CLI，把決定性的片段擷取與模型的解讀分開。優先提供一個輸出檔名、行號或位元組範圍、匹配的規則與簡短摘錄的指令。

## Rust 預設值

以 Rust 建構時，使用成熟的 crate，而不是自訂的解析器：

- `clap` 處理指令與說明
- `reqwest` 處理 HTTP
- `serde` / `serde_json` 處理承載
- `toml` 處理小型設定檔
- `anyhow` 提供 CLI 形式的錯誤脈絡

加入一個 `Makefile` 目標，例如 `make install-local`，建置 release 並把執行檔安裝到 `~/.local/bin`。

## TypeScript/Node 預設值

以 TypeScript/Node 建構時，讓 CLI 保持可以作為一般指令安裝：

- `commander` 或 `cac` 處理指令與說明
- 原生的 `fetch`、官方 SDK，或使用者既有的 HTTP 輔助工具進行 API 呼叫
- 只在外部承載驗證能防止真正的損壞時才用 `zod`
- `package.json` 的 `bin` 條目作為安裝後的指令
- 依 repo 既有的慣例使用 `tsup`、`tsx` 或 `tsc`

加入安裝路徑，例如 `pnpm install`、`pnpm build` 與 `pnpm link --global`，或一個把小型包裝安裝到 `~/.local/bin` 的 `Makefile` 目標。

## Python 預設值

以 Python 建構時，除非工作流程需要更多，否則優先使用無聊的標準函式庫元件：

- `argparse` 處理指令與說明，或在子指令會變得混亂時用 `typer`
- 依已安裝或附近已在使用的，選擇 `urllib.request` / `urllib.parse`、`requests` 或 `httpx` 處理 HTTP
- `json`、`csv`、`sqlite3`、`pathlib` 與 `subprocess` 處理本機檔案、匯出、資料庫與既有腳本
- `pyproject.toml` 的 console script，或一個小型可執行包裝作為安裝後的指令
- 只在真的需要相依套件時才用 `uv` 或 virtualenv

加入一個 `Makefile` 目標，例如 `make install-local`，把指令安裝到 PATH，並記載它是否依賴 `uv`、virtualenv，或只需要系統 Python。

## 附屬技能

CLI 能運作之後，為它建立或更新一個小型技能。可用時使用 `$skill-creator`。個人附屬技能使用 `$CODEX_HOME/skills/<tool-name>/SKILL.md`，除非使用者指名了 repo 本機的 `.codex/skills/...` 路徑或其他技能 repo。

依未來 Codex 執行緒應使用 CLI 的順序撰寫附屬技能，而不是每個功能的導覽。說明：

- 如何驗證已安裝的指令存在。
- 先執行哪個指令。
- 驗證如何設定。
- 哪個探索指令能找到常用的 ID。
- 安全的讀取路徑。
- 預期的草稿/寫入路徑。
- 原始逃生口。
- 沒有使用者明確核准時不要做什麼。
- 三個可直接複製貼上的指令範例。

把 API 參考細節放在 CLI 文件或技能的參考檔中。讓技能聚焦在順序、安全，以及未來 Codex 執行緒實際應執行的範例。
