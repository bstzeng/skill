<!--meta
{"title":"MCP 伺服器建構（Composio 收錄版）","category":"AI 整合與開發工具","tags":["MCP","API 整合","Python","TypeScript","FastMCP"],
"summary":"ComposioHQ 收錄的 Anthropic mcp-builder 早期版本：引導你打造高品質的 MCP 伺服器，讓 LLM 透過設計良好的工具串接外部 API。分四階段：深入研究與規劃（以代理為中心的設計原則、研讀協定與 SDK 文件、規劃工具與共用函式）→ 實作（Python FastMCP 或 Node/TypeScript SDK）→ 審查與測試 → 建立 10 題可驗證的評估問題。",
"usage":"- 說「幫我做一個串接 XX API 的 MCP 伺服器」\n- 會先研讀 MCP 協定與目標 API 的完整文件，再規劃工具\n- 測試時不要直接執行伺服器（會卡住），改用評估工具、tmux 或 `timeout`\n- 新版請見 Anthropic 清單中的 mcp-builder"}
-->
---
name: mcp-builder
description: 建立高品質 MCP（Model Context Protocol）伺服器的指南，讓 LLM 能透過設計良好的工具與外部服務互動。在建構 MCP 伺服器以整合外部 API 或服務時使用，無論是 Python（FastMCP）或 Node/TypeScript（MCP SDK）。
license: 完整條款見 LICENSE.txt
---

# MCP 伺服器開發指南

## 概覽

要建立能讓 LLM 有效與外部服務互動的高品質 MCP（Model Context Protocol）伺服器，請使用本技能。MCP 伺服器提供讓 LLM 存取外部服務與 API 的工具。MCP 伺服器的品質，取決於它多能讓 LLM 使用所提供的工具完成真實世界的任務。

---

# 流程

## 🚀 高層工作流程

建立高品質的 MCP 伺服器包含四個主要階段：

### 階段 1：深入研究與規劃

#### 1.1 理解以代理為中心的設計原則

在進入實作之前，先檢視以下原則，理解如何為 AI 代理設計工具：

**為工作流程而建，而不只是 API 端點：**
- 不要只是包裝既有的 API 端點——要建立經過思考、高影響力的工作流程工具
- 合併相關的操作（例如同時檢查空檔並建立事件的 `schedule_event`）
- 聚焦於能完成整個任務的工具，而不只是個別的 API 呼叫
- 考慮代理實際需要完成哪些工作流程

**為有限的脈絡最佳化：**
- 代理的上下文視窗有限——讓每個 token 都有價值
- 回傳高訊號的資訊，而不是鉅細靡遺的資料傾印
- 提供「精簡」與「詳細」的回應格式選項
- 預設使用人類可讀的識別資訊，而不是技術代碼（用名稱而非 ID）
- 把代理的脈絡預算視為稀缺資源

**設計可據以行動的錯誤訊息：**
- 錯誤訊息應該引導代理走向正確的使用方式
- 建議具體的下一步：「試著使用 filter='active_only' 減少結果」
- 讓錯誤具有教育性，而不只是診斷性
- 透過清楚的回饋，幫助代理學會正確使用工具

**遵循自然的任務劃分：**
- 工具名稱應該反映人類如何思考任務
- 以一致的前綴把相關工具分組，方便探索
- 圍繞自然的工作流程設計工具，而不只是依 API 結構

**使用以評估驅動的開發：**
- 及早建立實際的評估情境
- 讓代理的回饋驅動工具的改善
- 快速做出原型，並依代理的實際表現迭代

#### 1.3 研讀 MCP 協定文件

**擷取最新的 MCP 協定文件：**

使用 WebFetch 載入：`https://modelcontextprotocol.io/llms-full.txt`

這份完整的文件包含完整的 MCP 規格與指引。

#### 1.4 研讀框架文件

**載入並閱讀以下參考檔案：**

- **MCP 最佳實務**：[📋 查看最佳實務](./reference/mcp_best_practices.md) —— 所有 MCP 伺服器的核心指引

**Python 實作，另外載入：**
- **Python SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 實作指南](./reference/python_mcp_server.md) —— Python 專屬的最佳實務與範例

**Node/TypeScript 實作，另外載入：**
- **TypeScript SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) —— Node/TypeScript 專屬的最佳實務與範例

#### 1.5 徹底研讀 API 文件

要整合一個服務，就讀完 **所有** 可取得的 API 文件：
- 官方 API 參考文件
- 認證與授權要求
- 速率限制與分頁模式
- 錯誤回應與狀態碼
- 可用的端點及其參數
- 資料模型與結構

**需要時使用網路搜尋與 WebFetch 工具蒐集完整的資訊。**

#### 1.6 建立完整的實作計畫

依你的研究，建立包含以下內容的詳細計畫：

**工具選擇：**
- 列出最有價值、要實作的端點／操作
- 優先處理能支援最常見、最重要使用情境的工具
- 考慮哪些工具能一起運作以支援複雜的工作流程

**共用的工具函式與輔助函式：**
- 找出常見的 API 請求模式
- 規劃分頁輔助函式
- 設計篩選與格式化工具
- 規劃錯誤處理策略

**輸入／輸出設計：**
- 定義輸入驗證模型（Python 用 Pydantic、TypeScript 用 Zod）
- 設計一致的回應格式（例如 JSON 或 Markdown），以及可設定的詳細程度（例如詳細或精簡）
- 為大規模使用規劃（數千個使用者／資源）
- 實作字元上限與截斷策略（例如 25,000 個 token）

**錯誤處理策略：**
- 規劃優雅的失敗模式
- 設計清楚、可據以行動、對 LLM 友善、能促使進一步行動的自然語言錯誤訊息
- 考慮速率限制與逾時情境
- 處理認證與授權錯誤

---

### 階段 2：實作

有了完整的計畫之後，依各語言的最佳實務開始實作。

#### 2.1 建立專案結構

**Python：**
- 建立單一 `.py` 檔，複雜時再組織成模組（見 [🐍 Python 指南](./reference/python_mcp_server.md)）
- 使用 MCP Python SDK 註冊工具
- 定義 Pydantic 模型做輸入驗證

**Node/TypeScript：**
- 建立適當的專案結構（見 [⚡ TypeScript 指南](./reference/node_mcp_server.md)）
- 設定 `package.json` 與 `tsconfig.json`
- 使用 MCP TypeScript SDK
- 定義 Zod 結構做輸入驗證

#### 2.2 先實作核心基礎設施

**開始實作時，先建立共用的工具函式，再實作工具：**
- API 請求輔助函式
- 錯誤處理工具函式
- 回應格式化函式（JSON 與 Markdown）
- 分頁輔助函式
- 認證／token 管理

#### 2.3 有系統地實作工具

對計畫中的每個工具：

**定義輸入結構：**
- 使用 Pydantic（Python）或 Zod（TypeScript）做驗證
- 包含適當的限制（最小／最大長度、正規表示式、最小／最大值、範圍）
- 提供清楚、具描述性的欄位說明
- 在欄位說明中附上多樣的範例

**撰寫完整的 docstring／描述：**
- 一行摘要說明工具做什麼
- 詳細說明目的與功能
- 明確的參數型別與範例
- 完整的回傳型別結構
- 使用範例（何時使用、何時不要使用）
- 錯誤處理說明，概述遇到特定錯誤時該如何進行

**實作工具邏輯：**
- 使用共用的工具函式避免程式碼重複
- 所有 I/O 都遵循 async/await 模式
- 實作適當的錯誤處理
- 支援多種回應格式（JSON 與 Markdown）
- 遵守分頁參數
- 檢查字元上限並適當截斷

**加入工具註記：**
- `readOnlyHint`：true（唯讀操作）
- `destructiveHint`：false（非破壞性操作）
- `idempotentHint`：true（重複呼叫效果相同時）
- `openWorldHint`：true（與外部系統互動時）

#### 2.4 遵循各語言的最佳實務

**此時，載入對應的語言指南：**

**Python：載入 [🐍 Python 實作指南](./reference/python_mcp_server.md) 並確保：**
- 使用 MCP Python SDK 並正確註冊工具
- 使用帶 `model_config` 的 Pydantic v2 模型
- 全面使用型別提示
- 所有 I/O 操作都使用 async/await
- 適當地組織 import
- 模組層級的常數（CHARACTER_LIMIT、API_BASE_URL）

**Node/TypeScript：載入 [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) 並確保：**
- 正確使用 `server.registerTool`
- Zod 結構使用 `.strict()`
- 啟用 TypeScript 嚴格模式
- 不使用 `any` 型別——使用適當的型別
- 明確的 Promise<T> 回傳型別
- 已設定建置流程（`npm run build`）

---

### 階段 3：審查與修正

初步實作之後：

#### 3.1 程式碼品質審查

為確保品質，審查程式碼：
- **DRY 原則**：工具之間沒有重複的程式碼
- **可組合性**：共用的邏輯抽成函式
- **一致性**：相似的操作回傳相似的格式
- **錯誤處理**：所有外部呼叫都有錯誤處理
- **型別安全**：完整的型別涵蓋（Python 型別提示、TypeScript 型別）
- **文件**：每個工具都有完整的 docstring／描述

#### 3.2 測試與建置

**重要：** MCP 伺服器是透過 stdio/stdin 或 sse/http 等待請求的長時間執行程序。直接在你的主程序中執行它們（例如 `python server.py` 或 `node dist/index.js`）會讓你的程序無限期卡住。

**測試伺服器的安全方式：**
- 使用評估工具（見階段 4）——建議的做法
- 在 tmux 中執行伺服器，讓它在你的主程序之外
- 測試時使用逾時：`timeout 5s python server.py`

**Python：**
- 驗證 Python 語法：`python -m py_compile your_server.py`
- 檢視檔案確認 import 正常
- 手動測試：在 tmux 中執行伺服器，然後在主程序中用評估工具測試
- 或直接使用評估工具（它會為 stdio 傳輸管理伺服器）

**Node/TypeScript：**
- 執行 `npm run build` 並確保沒有錯誤地完成
- 確認已建立 dist/index.js
- 手動測試：在 tmux 中執行伺服器，然後在主程序中用評估工具測試
- 或直接使用評估工具（它會為 stdio 傳輸管理伺服器）

#### 3.3 使用品質檢查表

為驗證實作品質，從各語言的指南載入對應的檢查表：
- Python：見 [🐍 Python 指南](./reference/python_mcp_server.md) 中的「Quality Checklist」
- Node/TypeScript：見 [⚡ TypeScript 指南](./reference/node_mcp_server.md) 中的「Quality Checklist」

---

### 階段 4：建立評估

實作 MCP 伺服器之後，建立完整的評估來測試它的有效性。

**載入 [✅ 評估指南](./reference/evaluation.md) 取得完整的評估指引。**

#### 4.1 理解評估的目的

評估測試 LLM 是否能有效使用你的 MCP 伺服器，回答實際、複雜的問題。

#### 4.2 建立 10 個評估問題

要建立有效的評估，遵循評估指南中概述的流程：

1. **檢視工具**：列出可用的工具並理解它們的能力
2. **探索內容**：使用「唯讀」操作探索可用的資料
3. **產生問題**：建立 10 個複雜、實際的問題
4. **驗證答案**：自己解每一題以驗證答案

#### 4.3 評估要求

每個問題都必須：
- **獨立**：不依賴其他問題
- **唯讀**：只需要非破壞性的操作
- **複雜**：需要多次工具呼叫與深入探索
- **實際**：以人類會在意的真實使用情境為基礎
- **可驗證**：單一、清楚、可以用字串比對驗證的答案
- **穩定**：答案不會隨時間改變

#### 4.4 輸出格式

建立具有以下結構的 XML 檔：

{{CODE:1}}

---

# 參考檔案

## 📚 文件庫

開發期間視需要載入這些資源：

### 核心 MCP 文件（先載入）
- **MCP 協定**：從 `https://modelcontextprotocol.io/llms-full.txt` 擷取——完整的 MCP 規格
- [📋 MCP 最佳實務](./reference/mcp_best_practices.md) —— 通用的 MCP 指引，包括：
  - 伺服器與工具的命名慣例
  - 回應格式指引（JSON vs Markdown）
  - 分頁最佳實務
  - 字元上限與截斷策略
  - 工具開發指引
  - 安全與錯誤處理標準

### SDK 文件（在階段 1/2 載入）
- **Python SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 擷取
- **TypeScript SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 擷取

### 各語言實作指南（在階段 2 載入）
- [🐍 Python 實作指南](./reference/python_mcp_server.md) —— 完整的 Python/FastMCP 指南，包含：
  - 伺服器初始化模式
  - Pydantic 模型範例
  - 以 `@mcp.tool` 註冊工具
  - 完整可運作的範例
  - 品質檢查表

- [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) —— 完整的 TypeScript 指南，包含：
  - 專案結構
  - Zod 結構模式
  - 以 `server.registerTool` 註冊工具
  - 完整可運作的範例
  - 品質檢查表

### 評估指南（在階段 4 載入）
- [✅ 評估指南](./reference/evaluation.md) —— 完整的評估建立指南，包含：
  - 問題建立指引
  - 答案驗證策略
  - XML 格式規格
  - 範例問題與答案
  - 使用提供的腳本執行評估
