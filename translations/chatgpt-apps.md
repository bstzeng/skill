<!--meta
{"title":"ChatGPT App 開發","category":"AI 整合與開發工具","tags":["ChatGPT Apps SDK","MCP","Widget","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：建立、搭骨架、重構與除錯結合 MCP 伺服器與 widget UI 的 ChatGPT Apps SDK 應用。一律先查官方文件，先判斷應用類型與規劃工具，再優先從官方範例改起；涵蓋 MCP Apps bridge、`window.openai` 擴充、CSP 與網域設定、本機以 ngrok 在 ChatGPT 開發者模式測試，到正式部署與上架送審。",
"usage":"- Codex：`$skill-installer chatgpt-apps`（建議同時用 `$openai-docs`）\n- 說「Use $chatgpt-apps with $openai-docs to scaffold a ChatGPT app for 訂餐廳 with a TS MCP server and React widget」\n- 測試：本機跑 `/mcp` → `ngrok http <port>` → ChatGPT「設定 → Apps & Connectors → 進階設定」開啟開發者模式並新增 app\n- 只有要公開上架時才會進入送審流程"}
-->
---
name: chatgpt-apps
description: 建構、搭建骨架、重構與疑難排解結合 MCP 伺服器與 widget UI 的 ChatGPT Apps SDK 應用程式。當 Codex 需要設計工具、註冊 UI 資源、接上 MCP Apps bridge 或 ChatGPT 相容 API、套用 Apps SDK 中繼資料或 CSP 或網域設定，或產出與文件一致的專案骨架時使用。優先採用文件優先的工作流程，在產生程式碼之前先呼叫 openai-docs 技能或 OpenAI 開發者文件 MCP 工具。
---

# ChatGPT 應用程式

## 概述

以文件優先、範例優先的工作流程，搭建 ChatGPT Apps SDK 實作的骨架，然後產生遵循目前 Apps SDK 與 MCP Apps bridge 模式的程式碼。

使用本技能產出：

- 主要的應用程式原型分類，以及 repo 形狀的決策
- 一份工具計畫（名稱、schema、註記、輸出）
- 一個上游起點的建議（官方範例、ext-apps 範例，或本機備用骨架）
- 一個 MCP 伺服器骨架（資源註冊、工具處理器、中繼資料）
- 一個 widget 骨架（以 MCP Apps bridge 為主，`window.openai` 相容/擴充為輔）
- 一個可重用的 Node + `@modelcontextprotocol/ext-apps` 入門骨架，作為低相依的備案
- 一份對照最低可運作 repo 契約的驗證報告
- 本機開發與連接器的設定步驟
- 一段簡短的、給利害關係人看的應用程式功能摘要（被要求時）

## 強制的文件優先工作流程

每當建構或變更 ChatGPT Apps SDK 應用程式時，一律先使用 `$openai-docs`。

1. 呼叫 `$openai-docs`（優先）或直接呼叫 OpenAI 文件 MCP 伺服器。
2. 在寫程式碼之前，抓取目前的 Apps SDK 文件，特別是（基準頁面）：
   - `apps-sdk/build/mcp-server`
   - `apps-sdk/build/chatgpt-ui`
   - `apps-sdk/build/examples`
   - `apps-sdk/plan/tools`
   - `apps-sdk/reference`
3. 在搭建新應用程式的骨架或產生第一版實作時，抓取 `apps-sdk/quickstart`，並在從零發明骨架之前，先查看官方範例 repo/頁面。
4. 當任務包含在本機以 ChatGPT 測試、託管或公開上線時，抓取部署/送審文件：
   - `apps-sdk/deploy`
   - `apps-sdk/deploy/submission`
   - `apps-sdk/app-submission-guidelines`
5. 解釋設計選擇或產生的骨架時，引用你使用的文件 URL。
6. 當目前的文件指引與較舊的 repo 模式不同時，優先採用目前的文件，並明確指出相容的別名。
7. 如果文件搜尋逾時或回傳的相符結果很差，就直接以 URL 抓取標準的 Apps SDK 頁面並繼續；不要讓搜尋失敗阻擋骨架的建立。

如果無法使用 `$openai-docs`，就使用：

- `mcp__openaiDeveloperDocs__search_openai_docs`
- `mcp__openaiDeveloperDocs__fetch_openai_doc`

閱讀 `references/apps-sdk-docs-workflow.md` 取得建議的文件查詢與一份精簡的檢查清單。
在選擇範例或骨架之前，閱讀 `references/app-archetypes.md`，把請求歸類到少數幾種支援的應用程式形狀之一。
在產生或審查 repo 時閱讀 `references/repo-contract-and-validation.md`，讓輸出保持在穩定的「可運作應用程式」契約之內。
當應用程式類似連接器、只有資料、以同步為主，或要與公司知識或深度研究配合良好時，閱讀 `references/search-fetch-standard.md`。
在開始一個全新的應用程式，或決定要改編上游範例還是使用本機備用骨架時，閱讀 `references/upstream-example-workflow.md`。
當任務需要 ChatGPT 專屬的 widget 行為，或要轉換使用包裝器專屬 `app.*` 輔助方法的 repo 範例時，閱讀 `references/window-openai-patterns.md`。

## 提示詞指引

使用明確把本技能與 `$openai-docs` 搭配的提示詞，讓產生的骨架以目前的文件為依據。

建議的提示詞模式：

- `Use $chatgpt-apps with $openai-docs to scaffold a ChatGPT app for <use case> with a <TS/Python> MCP server and <React/vanilla> widget.`
- `Use $chatgpt-apps with $openai-docs to adapt the closest official Apps SDK example into a ChatGPT app for <use case>.`
- `Use $chatgpt-apps and $openai-docs to refactor this Apps SDK demo into a production-ready structure with tool annotations, CSP, and URI versioning.`
- `Use $chatgpt-apps with $openai-docs to plan tools first, then generate the MCP server and widget code.`

回應時，在寫程式碼之前，詢問或推斷以下輸入：

- 使用情境與主要的使用者流程
- 唯讀 vs 會變更資料的工具
- 示範 vs 正式環境的目標
- 私人/內部使用 vs 公開目錄送審
- 後端語言與 UI 技術棧
- 驗證需求
- 要加入 CSP 允許清單的外部 API 網域
- 託管目標與本機開發方式
- 組織擁有權/驗證的準備程度（對於送審任務）

## 選擇程式碼之前先為應用程式分類

在選擇範例、repo 形狀或骨架之前，把請求歸類到一個主要原型並說明。

- `tool-only`
- `vanilla-widget`
- `react-widget`
- `interactive-decoupled`
- `submission-ready`

除非缺少的細節真的會造成阻礙，否則就推斷原型。用原型來選擇：

- 到底需不需要 UI
- 是否保留分開的 `server/` + `web/` 配置
- 優先採用官方 OpenAI 範例、ext-apps 範例，還是本機備用骨架
- 哪些驗證檢查最重要
- `search` 與 `fetch` 是否應該作為預設的唯讀工具介面

決策評分標準見 `references/app-archetypes.md`。

## 預設的起點順序

對於全新的應用程式，依此順序優先選擇起點：

1. **官方 OpenAI 範例**：當已經有一個相近的範例符合所要求的技術棧或互動模式時。
2. **版本相符的 `@modelcontextprotocol/ext-apps` 範例**：當使用者需要一個較底層或更可攜的 MCP Apps 基準時。
3. **`scripts/scaffold_node_ext_apps.mjs`**：只有在沒有相近的範例適合、使用者想要一個極小的 Node + vanilla 入門，或不希望使用網路存取/取得範例時。

如果已經有相近的上游範例，就不要從零產生一個大型的自訂骨架。
複製最小的相符範例，移除不相關的示範程式碼，然後依目前的文件與使用者的請求修補它。

## 建構工作流程

### 0. 為應用程式原型分類

在規劃工具或選擇起點之前，挑選一個主要原型。

- 優先選擇單一主要原型，而不是混合好幾種。
- 如果請求很廣泛，就推斷仍能滿足需求的最小原型。
- 只有在使用者要求公開上線、目錄送審或可供審查的部署時，才升級到 `submission-ready`。
- 在回應中說明所選的原型，讓使用者在需要時能及早更正。

### 1. 寫程式碼之前先規劃工具

從使用者的意圖定義工具介面。

- 一個工具一項工作。
- 撰寫以「Use this when...」行為提示開頭的工具描述。
- 讓輸入明確且對機器友善（列舉、必要欄位、範圍）。
- 決定每個工具是只有資料、只負責渲染，還是兩者皆是。
- 準確設定註記（`readOnlyHint`、`destructiveHint`、`openWorldHint`；成立時加上 `idempotentHint`）。
- 如果應用程式類似連接器、只有資料、以同步為主，或用於公司知識或深度研究，預設使用標準的 `search` 與 `fetch` 工具，而不是發明自訂的唯讀替代品。
- 對於教育/示範型的應用程式，優先一個工具一個概念，讓模型能乾淨地挑選正確的範例。
- 依學習目標為示範工具分組：資料進入 widget、widget 動作回到對話或工具、主機/版面的環境訊號，以及生命週期/串流行為。

當 `search` 與 `fetch` 可能相關時，閱讀 `references/search-fetch-standard.md`。

### 2. 選擇應用程式架構

選擇符合目標的最簡單結構。

- 快速原型、工作坊或概念驗證，使用**最小示範模式**。
- 正式環境的 UX 使用**資料/渲染解耦模式**，讓 widget 不會在每次工具呼叫時都重新渲染。

對於不簡單的應用程式，優先使用解耦模式：

- 資料工具回傳可重用的 `structuredContent`。
- 渲染工具附加 `_meta.ui.resourceUri` 與選用的 `_meta["openai/outputTemplate"]`。
- 渲染工具的描述說明前置條件（例如「先呼叫 `search`」）。

### 2a. 當有適合的上游範例時從它開始

對於全新的工作，當上游範例與所要求的應用程式相近時，預設從上游範例開始。

- 對於面向 ChatGPT 的應用程式、精緻的 UI 模式、React 元件、檔案上傳流程、彈出視窗流程，或類似文件範例的應用程式，先查看官方 OpenAI 範例。
- 當請求更接近原始的 MCP Apps bridge/伺服器接線，或版本相符的套件模式比 ChatGPT 專屬的精緻度更重要時，使用 `@modelcontextprotocol/ext-apps` 範例。
- 挑選最小的相符範例，只複製相關的檔案；不要原封不動地移植整個展示應用程式。
- 複製之後，讓範例與你抓取的目前文件一致：工具名稱/描述、註記、`_meta.ui.*`、CSP、URI 版本控制與本機執行說明。
- 用一句話說明你選了哪個範例以及原因。

選擇與改編的評分標準見 `references/upstream-example-workflow.md`。

### 2b. 當低相依的備案有幫助時使用入門腳本

只有在使用者想要一個快速、全新的 Node 入門、可以接受 vanilla HTML widget，而且沒有更好的上游範例作為起點時，才使用 `scripts/scaffold_node_ext_apps.mjs`。

- 只在抓取目前的文件之後執行它，然後讓產生的檔案與你抓取的文件一致。
- 如果你選擇腳本而不是上游範例，說明為什麼這個備案對該請求更好。
- 當有相近的官方範例、使用者已經有既有的應用程式結構、需要非 Node 的技術棧、明確想要先用 React，或只想要計畫/審查而不是程式碼時，略過它。
- 這個腳本會產生一個最小的 `@modelcontextprotocol/ext-apps` 伺服器，加上一個預設使用 MCP Apps bridge 的 vanilla HTML widget。
- 產生的 widget 把後續訊息保留在標準的 `ui/message` bridge 上，只有在選用的主機訊號/擴充時才使用 `window.openai`。
- 執行之後，修補產生的輸出以符合目前的文件與使用者的請求：調整工具名稱/描述、註記、資源中繼資料、URI 版本控制與 README/執行說明。

### 3. 搭建 MCP 伺服器的骨架

產生一個符合以下條件的伺服器：

- 以 MCP Apps UI 的 MIME 類型（`text/html;profile=mcp-app`），或在使用 `@modelcontextprotocol/ext-apps/server` 時以 SDK 常數（`RESOURCE_MIME_TYPE`），註冊 widget 資源/模板
- 以清楚的名稱、schema、標題與描述註冊工具
- 有意識地回傳 `structuredContent`（給模型 + widget）、`content`（給模型的敘述）與 `_meta`（只給 widget 的資料）
- 讓處理器保持冪等，或明確記載非冪等的行為
- 在 ChatGPT 中有幫助時，包含工具狀態字串（`openai/toolInvocation/*`）

讓 `structuredContent` 保持精簡。把大型或敏感、只給 widget 的承載移到 `_meta`。

### 4. 搭建 Widget UI 的骨架

為了可攜性先使用 MCP Apps bridge，然後在能實質改善 UX 時，再加入 ChatGPT 專屬的 `window.openai` API。

- 監聽 `ui/notifications/tool-result`（透過 `postMessage` 的 JSON-RPC）
- 從 `structuredContent` 渲染
- 元件發起的工具呼叫使用 `tools/call`
- 只有在 UI 狀態應該改變模型所看到的內容時，才使用 `ui/update-model-context`

把 `window.openai` 用於相容與擴充（檔案上傳、彈出視窗、顯示模式等），而不是新應用程式唯一的整合路徑。

#### API 介面的防護規則

- 有些範例用一個 `app` 物件包裝 bridge（例如 `@modelcontextprotocol/ext-apps/react`），並提供像 `app.sendMessage()`、`app.callServerTool()`、`app.openLink()` 這樣的輔助方法名稱，或主機的 getter 方法。
- 把那些包裝器視為實作細節或便利層，而不是預設要教的標準公開 API。
- 對於面向 ChatGPT 的指引，優先使用目前文件記載的介面：`window.openai.callTool(...)`、`window.openai.sendFollowUpMessage(...)`、`window.openai.openExternal(...)`、`window.openai.requestDisplayMode(...)`，以及像 `window.openai.theme`、`window.openai.locale`、`window.openai.displayMode`、`window.openai.toolInput`、`window.openai.toolOutput`、`window.openai.toolResponseMetadata` 與 `window.openai.widgetState` 這樣的直接全域變數。
- 如果你引用 repo 範例中的包裝輔助方法，就把它們對應回文件記載的 `window.openai` 或 MCP Apps bridge 基本元件，並指出包裝器不是規範性的 API 介面。
- 包裝器到標準 API 的對應，以及 React 輔助方法的抽取模式，使用 `references/window-openai-patterns.md`。

### 5. 加入資源中繼資料與安全性

在 widget 資源/模板上有意識地設定資源中繼資料：

- 帶有確切 `connectDomains` 與 `resourceDomains` 的 `_meta.ui.csp`
- 可供送審的部署使用 `_meta.ui.domain`
- `_meta.ui.prefersBorder`（或需要時使用 OpenAI 的相容別名）
- 選用的 `openai/widgetDescription`，以減少多餘的敘述

除非 iframe 嵌入是產品的核心，否則避免使用 `frameDomains`。

### 5a. 強制執行最低可運作 repo 契約

每個產生的 repo 在你認為完成之前，都應該滿足一份小而穩定的契約。

- repo 的形狀符合所選的原型。
- MCP 伺服器與工具接到一個可連線的 `/mcp` 端點。
- 工具有清楚的描述、準確的註記，並在需要時有 UI 中繼資料。
- 類似連接器、只有資料、以同步為主，以及公司知識類型的應用程式，在相關時使用標準的 `search` 與 `fetch` 工具形狀。
- 有 UI 時，widget 正確使用 MCP Apps bridge。
- repo 包含足夠的腳本或指令，讓使用者能在本機執行與檢查。
- 回應明確說明執行了哪些驗證、哪些沒有執行。

詳細的檢查清單與驗證階梯見 `references/repo-contract-and-validation.md`。

### 6. 驗證本機循環

對照最低可運作 repo 契約進行驗證，而不只是「檔案有沒有被建立」。

- 先執行成本最低的檢查：
  - 靜態的契約審查
  - 可行時的語法或編譯檢查
  - 可行時的本機 `/mcp` 健康檢查
- 然後往上進行執行期檢查：
  - 在 MCP Inspector 中驗證工具描述與 widget 渲染
  - 透過 HTTPS 通道在 ChatGPT 開發者模式中測試應用程式
  - 演練重試與重複的工具呼叫，以確認冪等行為
  - 檢查在主機事件與後續工具呼叫之後 widget 的更新
- 如果你只交付骨架、沒有安裝相依套件，仍然要執行低成本的檢查，並確切說明你沒有執行什麼。

驗證階梯見 `references/repo-contract-and-validation.md`。

### 7. 在 ChatGPT（開發者模式）中連線與測試

對於本機開發，包含明確的 ChatGPT 設定步驟（而不只是程式碼/執行指令）。

- 在本機的 `http://localhost:<port>/mcp` 上執行 MCP 伺服器
- 以公開的 HTTPS 通道公開本機伺服器（例如 `ngrok http <port>`）
- 從 ChatGPT 連線時，使用通道的 HTTPS URL 加上 `/mcp` 路徑
- 在 ChatGPT 中，於**設定 → Apps & Connectors → 進階設定**下啟用開發者模式
- 在 ChatGPT 的應用程式設定中，為遠端 MCP 伺服器建立一個新應用程式，並貼上公開的 MCP URL
- 告訴使用者在 MCP 工具/中繼資料變更後重新整理應用程式，讓 ChatGPT 重新載入最新的描述

注意：有些文件/截圖仍使用較舊的「connector」用語。給出逐步說明時，優先使用目前的產品用語（「app」），同時承認兩種標籤。

### 8. 規劃正式環境的託管與部署

當使用者要求部署或準備上線時，為 MCP 伺服器（以及若另外託管時的 widget 資產）產生託管指引。

- 託管在穩定的公開 HTTPS 端點之後（不是通道），並有可靠的 TLS
- 在 `/mcp` 上保留低延遲的串流行為
- 在 repo 之外設定機密（環境變數 / 機密管理器）
- 為工具呼叫加入日誌、請求延遲追蹤與錯誤可見性
- 加入基本的可觀測性（CPU、記憶體、請求量）與疑難排解路徑
- 送審之前，在 ChatGPT 開發者模式中重新測試託管的端點

### 9. 準備送審與發布（僅限公開應用程式）

只有在使用者打算公開列入目錄時，才包含這些步驟。

- 送審流程使用 `apps-sdk/deploy/submission`，審查要求使用 `apps-sdk/app-submission-guidelines`
- 私人/內部應用程式保留在開發者模式中，而不是送審
- 在進行送審工作之前，確認組織驗證與 Owner 角色的前置條件
- 確保 MCP 伺服器使用公開的正式環境端點（沒有 localhost/測試 URL），並設定好可供送審的 CSP
- 準備送審產出物：應用程式中繼資料、Logo/截圖、隱私權政策 URL、客服聯絡方式、測試提示/回應、在地化資訊
- 如果需要驗證，包含可供審查使用的示範帳號，並端到端測試登入路徑
- 在 Platform 後台送出審查、監控審查狀態，並且只在核准之後發布

## 互動狀態指引

當應用程式有長時間存在的 widget 狀態、重複的互動，或元件發起的工具呼叫時（例如遊戲、看板、地圖、儀表板、編輯器），閱讀 `references/interactive-state-sync-patterns.md`。

用它來選擇以下的模式：

- 狀態快照加上單調遞增的事件 token（`stateVersion`、`resetCount` 等）
- 冪等、重試安全的處理器
- `structuredContent` vs `_meta` 的劃分
- 以 MCP Apps bridge 為主的更新流程，搭配選用的 `window.openai` 相容
- 對於更複雜的互動式應用程式，資料/渲染解耦的工具架構

## 輸出預期

使用本技能搭建程式碼骨架時，除非使用者另有要求，否則依此順序產出：

- 對於直接要求骨架的請求，不要停在計畫：給出簡短的計畫，然後立即建立檔案。

1. 選擇的主要應用程式原型及原因
2. 工具計畫與架構選擇（最小 vs 解耦）
3. 選擇的上游起點（官方範例、ext-apps 範例或本機備用骨架）及原因
4. 從 `$openai-docs` 使用的文件頁面/URL
5. 要建立或修改的檔案樹
6. 實作（伺服器 + widget）
7. 對照最低可運作 repo 契約所執行的驗證
8. 本機執行/測試說明（包括通道 + ChatGPT 開發者模式的應用程式設定）
9. 部署/託管指引（如果被要求或有所暗示）
10. 送審準備檢查清單（對於公開上線的請求）
11. 風險、缺口與後續改進

## 參考

- `references/app-archetypes.md`：把請求歸類到少數幾種支援的應用程式形狀
- `references/apps-sdk-docs-workflow.md`：文件查詢、目標頁面與程式碼產生檢查清單
- `references/interactive-state-sync-patterns.md`：有狀態或高度互動的 widget 應用程式的可重用模式
- `references/repo-contract-and-validation.md`：最低可運作 repo 契約與輕量的驗證階梯
- `references/search-fetch-standard.md`：何時以及如何預設使用標準的 `search` 與 `fetch` 工具
- `references/upstream-example-workflow.md`：在官方範例、ext-apps 範例與本機備用骨架之間做選擇
- `references/window-openai-patterns.md`：ChatGPT 專屬的擴充、包裝器 API 轉換與 React 輔助方法模式
- `scripts/scaffold_node_ext_apps.mjs`：一個最小的 Node + `@modelcontextprotocol/ext-apps` 備用入門骨架
