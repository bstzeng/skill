<!--meta
{"title":"Microsoft Foundry AI 代理平台","category":"雲端與 DevOps","tags":["Azure","AI Foundry","AI 代理","模型部署","微調","Microsoft"],
"summary":"Microsoft 官方技能：端到端建構、部署、評估、優化、微調與管理 Microsoft Foundry 上的 AI 代理、模型與資源。涵蓋 Prompt / Hosted / 託管 Copilot / 語音代理的完整開發生命週期、批次與持續評估、Agent Optimizer、模型部署與配額、RBAC 權限、VNet 網路隔離，以及 SFT/DPO/RFT 模型微調。",
"usage":"- 安裝：`npx skills add https://github.com/microsoft/azure-skills --skill microsoft-foundry`（需 Azure CLI、azd 與 Azure MCP Server）\n- 說「在 Foundry 建一個新的 hosted agent 並部署測試」「幫我評估並優化這個代理的提示詞」「部署 gpt 模型時配額不足怎麼辦」\n- 載入後會先執行相依檢查腳本，並依任務讀取對應子技能（deploy、invoke、observe、finetuning、quota、rbac…）\n- 一般 Azure Functions / App Service 部署請改用 azure-deploy"}
-->
---
name: microsoft-foundry
description: "端到端建構、部署、評估、優化、微調與管理 Microsoft Foundry 的代理、模型與資源。用於：foundry、azd ai agent、azd provision/deploy、hosted agent 建立骨架/開發/執行/部署/疑難排解、prompt agent、託管 harness 代理、Copilot harness、語音代理、建立/更新/呼叫/評估代理、為代理加入工具、代理洞察、批次/持續評估、持續監控、代理 CI/CD、優化/改進提示詞、優化代理指示、Agent Optimizer、從追蹤整理資料集、部署模型、模型微調（SFT/DPO/RFT）、Foundry 專案、RBAC、角色指派、權限、配額、容量、區域、部署失敗、AI Services、建立 Foundry 資源、知識索引、自訂部署、導入、可用性、訓練資料、評分器、蒸餾、大型檔案上傳。不要用於：Azure Functions、App Service、一般的 Azure 部署（使用 azure-deploy）、一般的 Azure 準備（使用 azure-prepare）。"
license: MIT
metadata:
  author: Microsoft
  version: "1.2.32"
---

# Microsoft Foundry 技能

本技能協助開發者使用 Microsoft Foundry 資源，涵蓋模型探索與部署、AI 代理的完整開發生命週期、評估工作流程，以及疑難排解。

## 執行前要求

在開始對應的動作或工作流程之前，遵循下方每個適用的小節。

### 相依檢查與設定

**強制：** 本技能載入後的第一步，從本技能的根目錄執行下方的相依檢查與設定腳本，並等待它完成後再繼續。腳本會先檢查，只安裝缺少的相依項目；不會重新安裝已可用的相依項目。

**在閱讀或進入任何子技能、工作流程或工作流程專屬參考之前，你「必須」完成這項檢查。**

{{CODE:1}}

後續動作請嚴格遵循腳本的輸出。

### 工作流程指引

**強制：** 在執行「任何」工作流程專屬步驟之前，你「必須」閱讀對應的子技能文件。沒有閱讀其技能文件，就不要為某個工作流程呼叫該工作流程專屬的 MCP 工具。即使你已經知道 MCP 工具的參數也適用——技能文件包含必須遵循的必要工作流程步驟、預先檢查與驗證邏輯。每當新的使用者訊息觸發不同的工作流程時，即使技能已經載入，這條規則也適用。

### Foundry MCP

**強制：** 在使用 Foundry MCP 操作之前，呼叫 Azure MCP 的 `foundry` 工具，檢查可用的 Foundry MCP 工具與相關參數。把這當作以 MCP 為基礎之工作流程的探索/說明步驟。

### azd

**強制：** 在執行「任何」azd 指令之前，你「必須」閱讀 [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md)，並嚴格遵循其中定義的共用規則，特別是 `AZURE_DEV_USER_AGENT` 的設定規則。

## 子技能

本技能包含針對特定工作流程的專門子技能。**當某個子技能符合任務時，嚴格遵循其工作流程：**

| 子技能 | 何時使用 | 參考 |
|--------|----------|------|
| **deploy** | 把 hosted 代理部署到 Foundry、對部署做冒煙測試、建立或更新 prompt 代理，以及管理代理版本與多環境部署。 | [deploy](foundry-agent/deploy/deploy.md) |
| **cicd** | 為 Foundry 代理建立 CI/CD 部署管線。 | [cicd](foundry-agent/cicd/cicd.md) |
| **invoke** | 傳送訊息給代理，單輪或多輪對話 | [invoke](foundry-agent/invoke/invoke.md) |
| **routine** | 用 routine 排程或以事件觸發 Foundry 代理；使用 `azd` 進行 CRUD、啟用/停用、手動派發與檢視過往執行，或在 `azure.yaml` 中定義 routine。 | [routine](foundry-agent/routine/routine.md) |
| **invocations-ws** | 建構、部署並連線到使用開發者定義、透過 `invocations_ws` 的雙工即時或媒體串流之自訂 Hosted 代理。 | [invocations-ws](foundry-agent/invocations-ws/invocations-ws.md) |
| **observe** | 評估代理品質、執行批次評估、分析失敗、優化提示詞、改進代理指示、比較版本、建立 CI/CD 監控，以及啟用持續的正式環境評估 | [observe](foundry-agent/observe/observe.md) |
| **insights** | 從既有的監控中拉取已產生的代理洞察、證據與建議；唯讀擷取，而不是新的分析執行 | [insights](foundry-agent/insights/insights.md) |
| **trace** | 查詢追蹤、分析延遲/失敗，透過 App Insights 的 `customEvents` 把評估結果關聯到特定回應 | [trace](foundry-agent/trace/trace.md) |
| **troubleshoot** | 檢視 hosted 代理日誌、查詢遙測、診斷失敗 | [troubleshoot](foundry-agent/troubleshoot/troubleshoot.md) |
| **validate** | 只有在使用者明確要求使用這個驗證子技能，或要求依最佳實踐驗證 Microsoft Foundry hosted 代理程式碼時才使用。絕不主動呼叫它，也不要把它加入其他工作流程。 | [validate](foundry-agent/validate/validate.md) |
| **create（快速入門）** | 從零端到端建立新的 hosted Foundry 代理——建立骨架、佈建或使用既有的 Foundry 專案、部署並做冒煙測試。不要用於任何既有程式碼的工作。快速入門未涵蓋的任何事，使用 **create**。 | [create/quick-start-hosted.md](foundry-agent/create/quick-start-hosted.md) |
| **create** | 當標準的端到端順利路徑（快速入門）不適用時使用。建立新的 Foundry 代理、更新既有代理的程式碼、繼續開發既有代理、在建立骨架時接好連線、使用進階設定或 A2A（Agent2Agent），或從失敗的快速入門執行中恢復。 | [create](foundry-agent/create/create-hosted.md) |
| **create managed harness** | 建立或繼續開發明確使用 Foundry 託管 Copilot harness 的 Prompt 代理。使用 `azd` 與 `azure.yaml`，而不是一般的 Prompt 代理 MCP 工作流程。 | [create-managed-harness](foundry-agent/create/create-managed-harness.md) |
| **create voice** | 建立、設定或擴充 Foundry 語音代理，一般請求預設為託管的 Prompt Voice，也支援自行部署的 Prompt Voice 或雙代理的 Hosted Voice。 | [create-voice](foundry-agent/create/create-voice.md) |
| **agent-optimizer** | 讓既有的 Python hosted 代理程式碼可供優化、設定 eval.yaml、執行 Agent Optimizer 工作、在本機套用候選版本，並在審查後透過 azd 部署。 | [agent-optimizer](foundry-agent/agent-optimizer/agent-optimizer.md) |
| **eval-datasets** | 把正式環境追蹤收集成評估資料集、管理資料集版本與分割、追蹤評估指標隨時間的變化、偵測退化，並維護從追蹤到部署的完整譜系。用於：從追蹤建立資料集、資料集版本控制、評估趨勢、退化偵測、資料集比較、評估譜系。 | [eval-datasets](foundry-agent/eval-datasets/eval-datasets.md) |
| **project/create** | 建立新的 Microsoft Foundry 專案以託管代理與模型。在導入 Foundry 或建立新的基礎設施時使用。 | [project/create/create-foundry-project.md](project/create/create-foundry-project.md) |
| **resource/create** | 使用 Azure CLI 建立 Azure AI Services 多服務資源（Foundry 資源）。在以細部控制手動佈建 AI Services 資源時使用。 | [resource/create/create-foundry-resource.md](resource/create/create-foundry-resource.md) |
| **private-network** | 回答關於 Foundry 網路隔離的問題，**並**以 VNet 隔離部署 Foundry（自帶 VNet、託管 VNet、混合）。涵蓋架構概念、範本選擇、部署與部署後驗證。 | [resource/private-network/private-network.md](resource/private-network/private-network.md) |
| **models/deploy-model** | 具智慧路由的統一模型部署。處理快速的預設部署、完全自訂的部署（版本/SKU/容量/RAI），以及跨區域的容量探索。路由到子技能：`preset`（快速部署）、`customize`（完全控制）、`capacity`（尋找可用容量）。 | [models/deploy-model/SKILL.md](models/deploy-model/SKILL.md) |
| **quota** | 管理 Microsoft Foundry 資源的配額與容量。在檢查配額使用量、排除因配額不足導致的部署失敗、申請提高配額或規劃容量時使用。 | [quota/quota.md](quota/quota.md) |
| **rbac** | 管理 Microsoft Foundry 資源的 RBAC 權限、角色指派、受控識別與服務主體。用於存取控制、稽核權限與 CI/CD 設定。 | [rbac/rbac.md](rbac/rbac.md) |
| **finetuning** | 在 Microsoft Foundry 上微調模型——SFT 蒸餾、DPO 偏好優化、搭配評分器與工具呼叫的 RFT。資料集準備、評分器校準、訓練、檢查點選擇、部署、評估。用於：微調、SFT、DPO、RFT、訓練資料、評分器、蒸餾、微調後的模型、大型檔案上傳。 | [finetuning/SKILL.md](finetuning/SKILL.md) |
| **azd-guidance** | 提供管理 Foundry 代理的共用 azd 知識與指引。任何與 azd 相關的工作流程都先讀這份。 | [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) |

> 💡 **提示：** 完整的導入流程：`project/create`（公開）或 `private-network`（VNet 隔離）→ `models/deploy-model` → 代理工作流程（`create` → `deploy` → `invoke`）。

> 💡 **微調：** 所有模型客製化都使用 `finetuning`——SFT 蒸餾、DPO 偏好優化，以及搭配評分器的 RFT。包含快速入門、評分器校準與訓練曲線分析。

> 💡 **模型部署：** 所有部署情境都使用 `models/deploy-model`——它會在快速預設部署、完全控制的自訂部署與跨區域容量探索之間智慧路由。

> 💡 **提示詞優化：** 對於「優化我的提示詞」或「改進我的代理指示」這類請求，載入 [observe](foundry-agent/observe/observe.md)，並透過那個以評估驅動的工作流程使用 `prompt_optimize` MCP 工具。

## 基礎設施生命週期

把使用者意圖對應到正確的基礎設施工作流程。

| 使用者意圖 | 工作流程 |
|------------|----------|
| 「建立 Foundry」/「設定 Foundry」（模糊） | 使用 `AskUserQuestion`：(a) 只要一個 AI Services 資源，(b) 一個公開存取的專案，還是 (c) 一個有網路隔離的專案？路由：(a) → [resource/create](resource/create/create-foundry-resource.md)、(b) → [project/create](project/create/create-foundry-project.md)、(c) → [private-network](resource/private-network/private-network.md) |
| 以 VNet 隔離設定 Foundry | [private-network](resource/private-network/private-network.md) |
| 建立 Foundry 專案（公開） | [project/create](project/create/create-foundry-project.md) |
| 建立單純的 Foundry 資源 | [resource/create](resource/create/create-foundry-resource.md) |

## 代理開發生命週期

把使用者意圖對應到正確的代理工作流程。執行前依序閱讀每個子技能。

| 使用者意圖 | 工作流程（依序閱讀） |
|------------|----------------------|
| 建立或開發語音代理（Prompt Voice 或 Hosted Voice） | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → [create-voice](foundry-agent/create/create-voice.md) → [deploy](foundry-agent/deploy/deploy.md) → [invoke](foundry-agent/invoke/invoke.md) |
| 建立或開發明確要求的託管 Harness 代理 / Copilot harness 代理 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → [create-managed-harness](foundry-agent/create/create-managed-harness.md) → [deploy](foundry-agent/deploy/deploy.md) → [invoke](foundry-agent/invoke/invoke.md) |
| 端到端建立新的 hosted 代理（骨架 + 部署 + 測試） | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → [quick-start-hosted](foundry-agent/create/quick-start-hosted.md)（自成一體的端到端流程） |
| 超出標準快速入門的任何事（既有程式碼、遷移、重新託管、部署客製化、建立骨架時的連線、A2A（Agent2Agent）、恢復） | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → [create](foundry-agent/create/create-hosted.md) → [deploy](foundry-agent/deploy/deploy.md) → [invoke](foundry-agent/invoke/invoke.md) |
| 優化既有的 Python hosted 代理 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → [agent-optimizer](foundry-agent/agent-optimizer/agent-optimizer.md) → 建立骨架/審查 → eval.yaml → 優化 → 套用候選版本 → 部署 → 呼叫 |
| 部署代理（程式碼已存在） | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → deploy（含評估套件設定）→ invoke → observe（評估/優化） |
| 程式碼變更後更新/重新部署代理 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → deploy（含評估套件設定）→ invoke → observe（評估/優化） |
| 為 hosted 代理建立 CI/CD 部署管線 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → cicd |
| 呼叫/測試/與代理對話 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → invoke |
| 排程/以事件觸發代理，或對 routine 進行 CRUD/啟用/停用/派發 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → routine |
| 優化 / 改進代理提示詞或指示 | observe（步驟 4：優化） |
| 評估並優化代理（完整循環） | observe |
| 啟用持續評估監控 | observe（步驟 6：CI/CD 與監控） |
| 拉取代理洞察 / 列出已產生的問題與建議 | [相依檢查與設定](#dependency-check-and-setup) → [insights](foundry-agent/insights/insights.md)（所有頁面並展開證據；唯讀） |
| 排除代理問題 | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → invoke → troubleshoot |
| 修復壞掉的代理（疑難排解 + 重新部署） | [相依檢查與設定](#dependency-check-and-setup) → [azd-guidance](foundry-agent/azd-guidance/azd-guidance.md) → invoke → troubleshoot → 套用修正 → deploy → invoke |

## 代理：.foundry 工作區標準

每個代理原始碼資料夾都可以在 `.foundry/` 下保存 Foundry 專屬的快取與覆蓋層狀態：

{{CODE:2}}

- 在 azd 專案中，從 `azure.yaml` 加上 `azd env get-values` 推導部署脈絡（專案端點、代理名稱/版本、ACR、App Insights）；azd 已經提供這些值時，不要在中繼資料中重複它們。
- `agent-metadata.yaml` 是建議的本機/開發覆蓋層，用於非 azd 的值、遠端 Foundry 套件參照、本機快取路徑、結果摘要與明確的覆寫。選用的附屬檔案（例如 `agent-metadata.prod.yaml`）可以保存單一的正式環境或 CI 目標覆蓋層，而不必在一個檔案中混合多個環境。
- `suites/`、`datasets/` 與 `evaluators/` 是本機快取資料夾。它們是最新的時候就重用，在重新整理或覆寫之前先詢問。
- 標準 schema 與工作流程規則請見[代理中繼資料契約](references/agent-metadata-contract.md)。

## 代理：設定參考

- [標準代理設定](references/standard-agent-setup.md)——針對需要資料駐留控制之正式環境工作負載的進階設定（透過 Foundry capability host 自帶 Cosmos DB / Storage / AI Search）。預設的 `azd ai agent` 流程使用**基本代理設定**，**不會**佈建 `capabilityHosts/agents`——不要把它的缺少標記為 bug。預設的佈建後狀態，請見 [foundry-agent/create/create-hosted.md](foundry-agent/create/create-hosted.md) 中的「預期的環境變數特徵」一節。

## 代理：通用專案脈絡解析

代理技能應該**只在需要尚未取得的設定值時**才執行這個步驟。如果某個值（例如代理根目錄、環境、專案端點或代理名稱）已經從使用者的訊息或同一 session 中先前的技能得知，就略過該值的解析。

### 步驟 1：探索代理根目錄與 azd 脈絡

先檢查工作區是否有 `azure.yaml`，且其中有使用 `host: azure.ai.agent` 的服務。

- **一個 azd 代理服務** -> 依 `kind`、`harness`、`modelType` 與 `conversationEngine` 分類它，然後以該服務的 `project` 資料夾或 `azure.yaml` 所在目錄作為代理根目錄。
- **多個 azd 代理服務** -> 檢查是否有語音包裝器透過 `conversationEngine.name` 參照某個 `kind: hosted` 服務：
  - **選擇 Hosted Voice 包裝器**代表其指名的 `kind: hosted` 目標是上游相依（`uses: [<target>]`、`conversationEngine.name: <target>`）；部署與驗證必須分別回報兩個服務。
  - **只選擇 `kind: hosted` 目標**會把變更/除錯範圍限定在目標容器，不會自動修改包裝器。
  - **否則** -> 要求使用者選擇目標服務/資料夾。
- **沒有 azd 代理服務** -> 在工作區中搜尋含有 `agent-metadata.yaml` 或 `agent-metadata.<env>.yaml` 的 `.foundry/` 資料夾。
  - **一個符合** -> 使用該代理根目錄。
  - **多個符合** -> 要求使用者選擇目標代理資料夾。
  - **沒有符合** -> 對於 [insights](foundry-agent/insights/insights.md)，只詢問缺少的遠端輸入，不初始化本機檔案；對於 create/deploy 工作流程，在設定期間建立新的 `.foundry/` 資料夾；對於其他工作流程，停下來詢問使用者要初始化哪個代理原始碼資料夾。

選定代理根目錄後，所有本機 `.foundry` 快取檢查、原始碼檢查、評估器建議、資料集建議與提示詞優化脈絡，都只保留在該資料夾內。除非使用者明確切換根目錄，否則**不要**掃描相鄰的代理資料夾。

### 步驟 2：解析環境與部署脈絡

如果有 `azure.yaml`，先解析 azd 環境：

1. 使用者明確指名的環境
2. `azd env get-values` 中的 `AZURE_ENV_NAME`
3. `.azure/config.json` 中的 azd 預設環境
4. session 中先前已選定的環境

當專案/部署值尚未得知時，對選定的環境執行 `azd env get-values`。部署脈絡優先使用 azd 的值：

| azd 變數 | 解析為 |
|----------|--------|
| `AZURE_AI_PROJECT_ENDPOINT` 或 `AZURE_AIPROJECT_ENDPOINT` | 專案端點 |
| `AGENT_<SERVICE>_NAME` | 所選 azd 服務的代理名稱 |
| `AGENT_<SERVICE>_VERSION` | 所選 azd 服務的代理版本 |
| `AZURE_CONTAINER_REGISTRY_NAME` 或 `AZURE_CONTAINER_REGISTRY_ENDPOINT` | ACR 登錄名稱 / 映像 URL 前綴 |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | 追蹤工作流程用的 App Insights 連線字串 |
| `AZURE_SUBSCRIPTION_ID`、`AZURE_RESOURCE_GROUP`、`AZURE_AI_ACCOUNT_NAME`、`AZURE_AI_PROJECT_NAME` | Azure 資源查找與 Playground 連結 |

當 azd 提供這些值時，以它們作為真實來源，並且在寫入中繼資料時不要把它們複製到 `.foundry/agent-metadata*.yaml`。

### 步驟 3：選擇中繼資料覆蓋層並解析環境

在選定的代理根目錄內，依此順序選擇中繼資料檔：
1. 使用者或工作流程明確提供的中繼資料檔名或路徑
2. 如果已知明確的環境，且 `.foundry/agent-metadata.<env>.yaml` 存在，就使用該檔案
3. `.foundry/agent-metadata.yaml`
4. 如果仍有多個中繼資料檔，且上述規則都無法選出一個，就請使用者選擇

讀取選定的中繼資料檔，並依此順序解析任何剩下的環境選擇：
1. 使用者明確指名的環境
2. 如果選定的中繼資料檔只定義了一個環境，就使用它
3. session 中先前已選定的環境
4. 中繼資料中的 `defaultEnvironment`

如果選定的中繼資料檔仍包含多個環境，且上述規則都無法選出一個，就請使用者選擇。在每份工作流程摘要中，都要讓選定的代理根目錄、中繼資料檔、環境，以及脈絡來自 azd 還是中繼資料保持可見。

如果選定的環境公開的是較舊的 `testSuites[]` 中繼資料而非 `evaluationSuites[]`，就把 `testSuites[]` 當作此 session 的來源，並在繼續之前於記憶體中把每個項目正規化為 `evaluationSuites[]` 的形狀。如果中繼資料更舊，只公開舊版的 `testCases[]`，就以同樣方式正規化該清單。保留資料集與評估器欄位、保留任何既有的 `tags`，並且只在 `tags.tier` 缺少時把舊版的 `priority` 對應到 `tags.tier`：`P0` -> `smoke`、`P1` -> `regression`、`P2` -> `coverage`。

### 步驟 4：解析 eval.yaml 的本機評估意圖

如果選定的代理根目錄中有 `eval.yaml`，在產生新套件之前先解析它：

- `agent.name` -> 目標代理候選；使用前先確認它與選定的 azd/中繼資料代理相符。
- `dataset.local_uri` -> 本機種子資料集候選；舊版的 `dataset_file` 可以在記憶體中正規化。
- `dataset.name` / `dataset.version` -> 已註冊的資料集候選。
- `validation_dataset` -> 選用的驗證資料集候選。
- `evaluators[]` -> 候選的 Foundry 評估器名稱；在把它們當作遠端評估器之前，先用 `evaluator_catalog_get` 確認。
- `name` -> 本機評估/套件候選；在以 `suiteName` 保存之前先遠端確認。
- `options.eval_model`、`options.optimization_model`、`options.max_candidates`、`options.optimization_config.model_search_space`、`options.pass_threshold`、`max_samples`、`trace_days` 與 `generation_instruction` -> 設定預設值。

把 `eval.yaml` 視為本機的評估意圖，而不是 Foundry 套件存在的證明。只有在遠端查找或註冊成功之後，才把已同步的套件/資料集/評估器參照保存到 `.foundry`。

### 步驟 5：解析共用設定

依此順序疊加來源：

1. 使用者明確的輸入，以及 session 中已選定的值
2. 部署脈絡的 azd 環境值
3. `.foundry/agent-metadata*.yaml` 的覆蓋層值與遠端套件/快取參照
4. `azure.yaml` 與 `eval.yaml` 的本機來源設定
5. 對仍缺少的任何值詢問使用者

如果 azd 與中繼資料都提供了同一個值且兩者不同，就停下來詢問哪個來源才是權威。如果相同，就使用 azd 的值，並避免在未來寫入中繼資料時重寫重複的值。

| 有效值 | 優先來源 | 使用者 |
|--------|----------|--------|
| 專案端點 | azd env | deploy、invoke、observe、trace、troubleshoot |
| 代理名稱/版本 | azd 代理變數，其次是 `azure.yaml` | invoke、observe、trace、troubleshoot |
| ACR | azd env | deploy |
| 評估套件與快取路徑 | `.foundry/agent-metadata*.yaml` | observe、eval-datasets |
| 本機種子資料集/評估器意圖 | `eval.yaml` | observe、eval-datasets |

### 步驟 6：寫入中繼資料覆蓋層（僅限 Create/Deploy/Observe）

在任何中繼資料寫入時（部署、自動設定、資料集重新整理，或從追蹤到資料集的更新），只在選定的中繼資料檔中保存無法推導的覆蓋層/快取狀態：

- 對未來解析有用時，保存 azd 綁定（`azd.environmentName`、`azd.service`）
- 帶有遠端套件/資料集/評估器參照與本機快取路徑的 `evaluationSuites[]`
- `lastEval`、結果檔、比較摘要，或明確的非 azd 覆寫

azd 已經提供時，不要把 azd 擁有的部署值複製到中繼資料中。如果選定的檔案是建議的單一環境檔，只重寫那一個環境區塊。如果選定的檔案是舊版的多環境檔，只重寫選定的環境區塊。絕不自動在相鄰的中繼資料檔之間複製或合併環境。如果選定的環境仍使用較舊的 `testSuites[]` 或舊版的 `testCases[]`，就把它重寫為 `evaluationSuites[]`，並從重寫後的項目中移除已遷移的 `priority` 欄位。

### 步驟 7：蒐集缺少的值

**只對**無法從使用者訊息、session 脈絡、中繼資料或 azd 啟動解析出的值，使用 `ask_user` 或 `askQuestions` 工具。技能可能需要的常見值：
- **代理根目錄**——目標 azd 服務的專案資料夾，或含有 `.foundry/agent-metadata*.yaml` 的資料夾
- **中繼資料檔**——本機/開發用的 `agent-metadata.yaml`，或明確的附屬檔，例如 `agent-metadata.prod.yaml`
- **環境**——azd 環境、`dev`、`prod`，或中繼資料中的其他環境鍵
- **專案端點**——Microsoft Foundry 專案端點 URL
- **代理名稱**——目標代理的名稱

> 💡 **提示：** 如果使用者已經提供代理路徑、環境、專案端點或代理名稱，就直接擷取——不要再問一次。

## 代理：代理類型

代理工作流程區分四種一級代理類型：

| 類型 | Kind | 說明 |
|------|------|------|
| **Prompt** | `"prompt"` | 以模型部署為後端、基於 LLM 的代理；透過 Foundry MCP 或 SDK 管理 |
| **Hosted** | `"hosted"` | 執行自訂程式碼、基於容器的代理；透過 `azd` 開發與部署 |
| **託管 Harness 代理** | 新撰寫時為 `"prompt"` 搭配 `harness.type: "microsoft_copilot_preview"` | 在 Foundry 託管的 Copilot harness 上執行的 Prompt 代理；透過 `azd` 開發與部署 |
| **Voice** | `"voice"` | 託管的即時語音代理——**Prompt Voice**（1 個代理，`modelType: managed` 或 `self_deployed`）或 **Hosted Voice**（2 個代理：帶有 `conversationEngine.type: hosted_agent` 的 `kind: voice` 包裝器 + 透過 `invocations_ws` `1.0.0` 與 Voice Live Bridge `1.0` 的 `kind: hosted` 目標）；透過 `azd` 開發與部署，並透過 `voice` WebSocket 端點驗證 |

依照以下確切順序、根據 `azure.yaml` 服務的定義來分類它，而不是只看 `host`：

1. `kind: voice` -> **Voice**。為了相容性，把既有的 `kind: prompt-voice` 服務默默分類為 Voice，然後在編輯其 YAML 時正規化。分類子類型：
   - `conversationEngine.type: hosted_agent` -> **Hosted Voice 包裝器**（與一個指名的 `kind: hosted` 目標服務配對）。
   - `modelType: managed` 或 `modelType: self_deployed` -> **Prompt Voice**（Foundry 會從 `model.id` 推斷是原生語音轉語音，還是串接的 STT -> LLM -> TTS）。
   - **同時**有 `modelType`/`model` 與 `conversationEngine` 是無效的（停下來修正 `azure.yaml`）；**兩者都沒有**則是不完整的（不要猜）。絕不使用已淘汰的 `modelType: hosted_agent`、`targetAgent` 或巢狀的 `config:` 區塊。
2. `kind: hosted` -> **Hosted**。當它宣告 `protocols: [{ protocol: invocations_ws, version: 1.0.0 }]` 與 `metadata.voiceLiveCompatible: "true"`，並搭配一個 `kind: voice` 包裝器時，它是 **Hosted Voice 目標**；否則把獨立的 `invocations_ws` 服務視為**自訂的 Hosted 即時/音訊代理**。
3. `kind: prompt` 加上 `harness.type: microsoft_copilot_preview` 或舊版的 `github_copilot_preview` -> **託管 Harness 代理**。
4. 沒有該 harness 的 `kind: prompt` -> 一般的 **Prompt 代理**。

只有在無法從專案脈絡解析類型時才使用 `agent_get`。保留既有託管 Harness 代理上已撰寫的 harness 判別值；不要在一般的編輯或重新部署中遷移它。不要把既有的代理在 Prompt、Hosted、託管 Harness 代理與 Voice 類型之間轉換；改為建立新的代理。在建立任何**語音代理**之前，先依 [create-voice](foundry-agent/create/create-voice.md) 決定模型策略。

## 工具使用慣例

- 每當向使用者蒐集資訊時，使用 `ask_user` 或 `askQuestions` 工具
- 使用 `task` 或 `runSubagent` 工具委派長時間執行或獨立的子任務（例如環境變數掃描、狀態輪詢、Dockerfile 產生）
- Hosted 代理、託管 Harness 代理與語音代理優先使用 azd；一般的 Prompt 代理優先使用 Foundry MCP。
- 引用官方 Microsoft 文件 URL，而不是內嵌 CLI 指令語法

## Azure 驗證

- [Azure 驗證最佳實踐](references/auth-best-practices.md)

## 其他資源

- [Foundry Hosted 代理](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry)
- [Foundry 代理執行期元件](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/runtime-components?view=foundry)

## 網路隔離錯誤

適用於對 Foundry 專案或其上層 Foundry 帳戶的**任何**呼叫——Foundry MCP 工具、`azd`、`az` CLI、`curl`、REST 或 SDK。

如果錯誤符合 `Public access is disabled` / `PublicNetworkAccessDisabled` / 來自私人端點的 `403 Forbidden` / 連線逾時 / 專案端點 FQDN 解析為公用 IP，這通常代表上層 Foundry 帳戶的 `publicNetworkAccess=Disabled` 或 `Enabled from selected IP addresses`，而目前的 shell 在其 VNet 之外。

只有在錯誤模稜兩可時，才用管理平面呼叫對 Foundry 帳戶進行確認（只要有讀者權限，從任何地方都可以執行）：

{{CODE:3}}

`publicNetworkAccess: "Disabled"`——或 `"Enabled"` 搭配非空的 `networkAcls.ipRules` / `virtualNetworkRules`——即確認有隔離。如果 `publicNetworkAccess: "Enabled"` 且 `networkAcls` 為空，則失敗是呼叫端的網路問題（例如在有私人端點的 VNet 內，私人 DNS 把 FQDN 解析成公用 IP），而不是帳戶設定問題。

如果確實是網路隔離問題，支援的連線選項記載於[選擇連線到 Foundry 的安全方式](https://learn.microsoft.com/azure/foundry/how-to/configure-private-link#choose-a-secure-connection-method-to-foundry)。

> ℹ️ Foundry MCP 工具即使在 VNet 內部也無法連到 VNet 隔離的專案。
