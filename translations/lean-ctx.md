<!--meta
{"title":"LeanCTX 脈絡閘道","category":"AI 整合與開發工具","tags":["MCP","脈絡管理","Token 節省","程式搜尋"],
"summary":"使用 LeanCTX 脈絡閘道的 MCP 工具（ctx_*）為任務挑選相關的程式脈絡：一次取得排序後的相關檔案與原始碼、依符號或語意搜尋、呼叫圖、快取讀取、壓縮過的 shell 輸出、跨工作階段的記憶，以及從截斷輸出精確取回需要的片段。兩條核心規則：減少往返次數比縮小輸出更重要，以及絕不用輪詢方式等待。",
"usage":"- 需先安裝並設定 lean-ctx（見 leanctx.com/docs），之後 `ctx_*` 工具才會出現\n- 想了解某個東西怎麼運作時先用 `ctx_compose(task)`，不要逐一搜尋再讀檔\n- 讀要編輯的檔案用 `ctx_read(path, mode=\"anchored\")`；只看脈絡用 `signatures` 或 `map` 模式\n- 不要透過 `ctx_shell` 執行 cat／grep，請改用 `ctx_read`／`ctx_search`"}
-->
---
name: lean-ctx
description: 使用 LeanCTX 脈絡閘道工具，挑選與任務相關的程式脈絡、套用支援的控制、重用本機知識並檢視記錄下來的證據。當有 lean-ctx MCP 工具（ctx_*）可用，或檔案、搜尋或指令輸出需要一個聚焦的檢視時使用。
---

# LeanCTX —— AI 系統的脈絡閘道

控制你的 AI 能看到什麼。LeanCTX Engine 為既有的代理提供本機脈絡選擇、支援的存取與內容控制，以及觀察到之脈絡操作的證據：選擇 → 控制 → 學習 → 證明。「學習」指的是本機任務與知識的延續性，不是模型訓練。能否復原取決於來源或封存檔是否可用，以及存取權限。LeanCTX SDK 則是給應用程式使用的另一個整合介面。

lean-ctx 會在脈絡到達你之前先塑形：快取的讀取、壓縮過的 shell 輸出、聚焦的搜尋、復原到確切的原始內容。兩條規則勝過所有細節：

1. **減少往返勝過縮小輸出。** 一次就能回答問題的呼叫，比三次小呼叫更便宜。絕不為了省幾百個 token 而多加一次呼叫。
2. **絕不以輪詢的方式等待。** 不要用 `sleep` + 狀態檢查的迴圈（見下方）。

## 意圖 → 工具

| 你想要…… | 呼叫 |
|---|---|
| 理解某個東西如何運作（不知道在哪裡） | `ctx_compose(task)` —— 一次呼叫取得排序後的檔案 + 原始碼；「先」用它，而不是搜尋→讀取→讀取 |
| 找出某個符號的確切定義 | `ctx_search(action="symbol", name=…)` |
| 依意義找程式碼 | `ctx_search(action="semantic", query=…)` |
| 找文字／正規表示式模式 | `ctx_search(pattern=…, path=…)` |
| 誰呼叫了 X／X 呼叫了什麼 | `ctx_callgraph(action="callers"|"callees", symbol=…)` |
| 讀取你要編輯的檔案 | `ctx_read(path, mode="anchored")` → 用宿主原生的編輯工具編輯，或 `ctx_call(name="ctx_patch", arguments={…})` |
| 只為了脈絡讀取檔案 | `ctx_read(path, mode="signatures"|"map")`；某個範圍：`mode="lines:N-M"` |
| 編輯後重新檢查檔案 | `ctx_read(path, mode="diff")` |
| 執行指令（建置、測試、git……） | `ctx_shell(command)` —— 輸出會被壓縮 |
| 列出檔案／目錄結構 | `ctx_glob(pattern)`／`ctx_tree(path, depth)` |
| 跨工作階段記住 | `ctx_session(action="finding"|"decision"|"task", value=…)`；持久的專案事實：`ctx_call(name="ctx_knowledge", arguments={"action": "remember", …})` |

不要透過 `ctx_shell` 讀取或搜尋（`cat`、`sed -n`、`grep`、`rg`）：那會繞過讀取快取與符號索引。使用 `ctx_read`／`ctx_search`。

## 延遲載入的工具（ToolSearch）

如果宿主只列出 lean-ctx 工具的名稱（Claude Code 的 ToolSearch），用「一次」呼叫載入任務所需的工具，例如 `select:mcp__lean-ctx__ctx_compose,mcp__lean-ctx__ctx_search,mcp__lean-ctx__ctx_read`。不要只因為 `ctx_shell` 剛好已載入，就什麼都退回用它。這裡提到、但你的工具清單中沒有的工具（預設設定檔只顯示一個小核心）仍然可以呼叫：`ctx_call(name="ctx_knowledge", arguments={…})`。`ctx_call(name="ctx_discover_tools", arguments={"query": "…"})` 會列出全部工具。

## 長時間執行的指令

- 偏好使用宿主自己、完成時會通知的背景執行（Claude Code：帶 `run_in_background` 的 `Bash`，或 `Monitor`）。啟動它，然後繼續其他工作或結束這一輪——完成時你會被告知。
- `ctx_shell(run_in_background=true)` 的工作不會自己通知。只在你真正需要結果時檢查一次；絕不在迴圈中 `sleep`。

## 被截斷的輸出

壓縮或封存的輸出結尾會有一個復原代號。只擷取你需要的片段：`ctx_expand(id, search=… | head=N | json_path=…)`，或用 `ctx_read(path, raw=true)` 取得確切的位元組。不要重新執行指令。

## 沒有 MCP 時（CLI）

{{CODE:1}}

## 設定

{{CODE:2}}

文件：https://leanctx.com/docs
