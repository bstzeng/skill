<!--meta
{"title":"MCP 伺服器建構","category":"AI 整合與開發工具","tags":["MCP","API 整合","TypeScript","Python","Anthropic 官方"],
"summary":"Anthropic 官方技能：引導你打造高品質的 MCP（Model Context Protocol）伺服器，讓 LLM 透過設計良好的工具串接外部 API 或服務。分四階段：深入研究與規劃 → 實作（TypeScript SDK v2 或 Python FastMCP）→ 審查與測試 → 建立 10 題評估集。",
"usage":"- 安裝：`npx skills add https://github.com/anthropics/skills --skill mcp-builder`，或 Claude Code `/plugin marketplace add anthropics/skills`\n- 說「幫我做一個串接 Notion API 的 MCP server」\n- 推薦組合：TypeScript ＋ Streamable HTTP（遠端）/ stdio（本機）\n- 完成後用 `npx @modelcontextprotocol/inspector` 測試，並產出 XML 評估題組驗證 LLM 是否真的會用"}
-->
---
name: mcp-builder
description: 建立高品質 MCP（Model Context Protocol）伺服器的指南，讓 LLM 能透過設計良好的工具與外部服務互動。在建構 MCP 伺服器以整合外部 API 或服務時使用，無論是 Python（FastMCP）或 Node/TypeScript（MCP SDK）。
license: 完整條款見 LICENSE.txt
---

# MCP 伺服器開發指南

## 概述

建立 MCP（Model Context Protocol）伺服器，讓 LLM 能透過設計良好的工具與外部服務互動。MCP 伺服器的品質，取決於它能讓 LLM 多好地完成真實世界的任務。

---

# 流程

## 🚀 高層工作流程

建立高品質的 MCP 伺服器包含四個主要階段：

### 第一階段：深入研究與規劃

#### 1.1 了解現代 MCP 設計

**API 覆蓋 vs. 工作流程工具：**
在全面的 API 端點覆蓋與專門的工作流程工具之間取得平衡。工作流程工具對特定任務可能更方便，而全面覆蓋則讓代理有彈性組合操作。效能因客戶端而異——有些客戶端能從結合基本工具的程式碼執行中獲益，有些則與較高層的工作流程配合得更好。不確定時，優先考慮全面的 API 覆蓋。

**工具命名與可發現性：**
清楚、具描述性的工具名稱能幫助代理快速找到正確的工具。使用一致的前綴（例如 `github_create_issue`、`github_list_repos`）以及以動作為導向的命名。

**上下文管理：**
代理受益於精簡的工具描述，以及篩選/分頁結果的能力。設計能回傳聚焦、相關資料的工具。有些客戶端支援程式碼執行，能幫助代理有效率地篩選與處理資料。

**可執行的錯誤訊息：**
錯誤訊息應以具體的建議與下一步引導代理走向解決方案。

#### 1.2 研讀 MCP 協定文件

**瀏覽 MCP 規格：**

從網站地圖開始找到相關頁面：`https://modelcontextprotocol.io/sitemap.xml`

然後加上 `.md` 後綴抓取特定頁面以取得 markdown 格式（例如 `https://modelcontextprotocol.io/specification/draft.md`）。

要檢閱的關鍵頁面：
- 規格總覽與架構
- 傳輸機制（streamable HTTP、stdio）
- 工具、資源與提示詞的定義

#### 1.3 研讀框架文件

**推薦技術組合：**
- **語言**：TypeScript（高品質的 SDK 支援，在許多執行環境中相容性良好，例如 MCPB。而且 AI 模型擅長產生 TypeScript 程式碼，受益於其廣泛使用、靜態型別與良好的 lint 工具）
- **傳輸**：遠端伺服器使用 Streamable HTTP 搭配無狀態 JSON（相較於有狀態的 session 與串流回應，更容易擴展與維護）。本機伺服器使用 stdio。

**載入框架文件：**

- **MCP 最佳實踐**：[📋 查看最佳實踐](./reference/mcp_best_practices.md) - 核心準則

**TypeScript（推薦）：**

TypeScript SDK 有兩個主要版本。寫程式前先選一個：
- **v2**（`@modelcontextprotocol/server`）：目前的穩定版。新伺服器請用它。
- **v1**（`@modelcontextprotocol/sdk`）：只接收 bug 與安全性修正。只有在專案的 `package.json` 已經依賴 `@modelcontextprotocol/sdk` 時才使用，或用 `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` 遷移該專案。

如果專案已在使用 v1，用一兩句話告訴使用者一次：v2（`@modelcontextprotocol/server`）是目前的穩定版、v1 只接收 bug 與安全性修正，以及 `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` 可以遷移專案。然後除非使用者要求遷移，否則繼續使用 v1。

不要在同一個專案中混用兩者：v1 的程式碼範例（從 `@modelcontextprotocol/sdk/...` 匯入）不適用於 v2。

- **TypeScript SDK（v2）**：用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`；完整文件索引在 `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt`
- [⚡ TypeScript 指南（v2）](./reference/node_mcp_server_v2.md) - TypeScript 模式與範例
- 僅限 v1 專案：`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` 以及 [TypeScript 指南（v1）](./reference/node_mcp_server.md)

**Python：**
- **Python SDK**：用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) - Python 模式與範例

#### 1.4 規劃你的實作

**了解 API：**
檢閱該服務的 API 文件，找出關鍵端點、驗證需求與資料模型。視需要使用網路搜尋與 WebFetch。

**工具選擇：**
優先考慮全面的 API 覆蓋。列出要實作的端點，從最常用的操作開始。

---

### 第二階段：實作

#### 2.1 設定專案結構

專案設定請見各語言指南：
- [⚡ TypeScript 指南（v2）](./reference/node_mcp_server_v2.md) - 專案結構、package.json、tsconfig.json（既有 v1 專案請見 [v1](./reference/node_mcp_server.md)）
- [🐍 Python 指南](./reference/python_mcp_server.md) - 模組組織、相依套件

#### 2.2 實作核心基礎設施

建立共用工具：
- 帶驗證的 API 客戶端
- 錯誤處理輔助函式
- 回應格式化（JSON/Markdown）
- 分頁支援

#### 2.3 實作工具

對每個工具：

**輸入 Schema：**
- 使用 Zod（TypeScript）或 Pydantic（Python）
- 包含限制條件與清楚的描述
- 在欄位描述中加入範例

**輸出 Schema：**
- 盡可能為結構化資料定義 `outputSchema`
- 在工具回應中使用 `structuredContent`（TypeScript SDK 功能）
- 幫助客戶端理解與處理工具輸出

**工具描述：**
- 功能的精簡摘要
- 參數描述
- 回傳型別 schema

**實作：**
- I/O 操作使用 async/await
- 適當的錯誤處理並提供可執行的訊息
- 適用時支援分頁
- 使用現代 SDK 時同時回傳文字內容與結構化資料

**註記（Annotations）：**
- `readOnlyHint`：true/false
- `destructiveHint`：true/false
- `idempotentHint`：true/false
- `openWorldHint`：true/false

---

### 第三階段：審查與測試

#### 3.1 程式碼品質

檢查：
- 沒有重複的程式碼（DRY 原則）
- 一致的錯誤處理
- 完整的型別覆蓋
- 清楚的工具描述

#### 3.2 建置與測試

**TypeScript：**
- 執行 `npm run build` 驗證編譯
- v2 專案：對建置好的伺服器執行 [v2 指南](./reference/node_mcp_server_v2.md#verify-your-server)中的自我檢查腳本
- 用 MCP Inspector 測試：`npx @modelcontextprotocol/inspector`

**Python：**
- 驗證語法：`python -m py_compile your_server.py`
- 用 MCP Inspector 測試

詳細的測試方法與品質檢查清單請見各語言指南。

---

### 第四階段：建立評估

實作完 MCP 伺服器後，建立完整的評估來測試其成效。

**載入 [✅ 評估指南](./reference/evaluation.md) 取得完整的評估準則。**

#### 4.1 了解評估的目的

用評估來測試 LLM 是否能有效使用你的 MCP 伺服器來回答真實、複雜的問題。

#### 4.2 建立 10 道評估題目

要建立有效的評估，請遵循評估指南中概述的流程：

1. **檢查工具**：列出可用的工具並了解其能力
2. **探索內容**：使用「唯讀」操作探索可用的資料
3. **產生題目**：建立 10 道複雜、真實的題目
4. **驗證答案**：自己解出每一題以驗證答案

#### 4.3 評估要求

確保每道題目：
- **獨立**：不依賴其他題目
- **唯讀**：只需要非破壞性的操作
- **複雜**：需要多次工具呼叫與深入探索
- **真實**：基於人類會在意的真實使用情境
- **可驗證**：單一、清楚、可用字串比對驗證的答案
- **穩定**：答案不會隨時間改變

#### 4.4 輸出格式

建立一個具有以下結構的 XML 檔：

{{CODE:1}}

---

# 參考檔案

## 📚 文件庫

在開發過程中視需要載入這些資源：

### 核心 MCP 文件（最先載入）
- **MCP 協定**：從 `https://modelcontextprotocol.io/sitemap.xml` 網站地圖開始，然後加上 `.md` 後綴抓取特定頁面
- [📋 MCP 最佳實踐](./reference/mcp_best_practices.md) - 通用 MCP 準則，包括：
  - 伺服器與工具的命名慣例
  - 回應格式準則（JSON vs Markdown）
  - 分頁最佳實踐
  - 傳輸選擇（streamable HTTP vs stdio）
  - 安全性與錯誤處理標準

### SDK 文件（在第一/二階段載入）
- **Python SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 抓取
- **TypeScript SDK（v2）**：從 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 抓取；完整文件索引在 `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt`
- **TypeScript SDK（v1，僅限既有 v1 專案）**：從 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` 抓取

### 各語言實作指南（在第二階段載入）
- [🐍 Python 實作指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包含：
  - 伺服器初始化模式
  - Pydantic 模型範例
  - 以 `@mcp.tool` 註冊工具
  - 完整可運作的範例
  - 品質檢查清單

- [⚡ TypeScript 實作指南（SDK v2）](./reference/node_mcp_server_v2.md) - 針對 `@modelcontextprotocol/server` 的完整 TypeScript 指南，包含：
  - 專案設定與伺服器工廠
  - 工具設計：Zod 4 schema、輸出格式、分頁、錯誤
  - 同時提供 stdio 與 Streamable HTTP 的完整範例，以及 bearer 驗證
  - 資源、提示詞與通知
  - 驗證建置後伺服器的自我檢查腳本
  - 進階功能的 SDK 範例連結
  - v1 → v2 對照表、遷移步驟與品質檢查清單

- [⚡ TypeScript 實作指南（SDK v1）](./reference/node_mcp_server.md) - 針對既有 `@modelcontextprotocol/sdk` 專案的對應指南

### 評估指南（在第四階段載入）
- [✅ 評估指南](./reference/evaluation.md) - 完整的評估建立指南，包含：
  - 題目建立準則
  - 答案驗證策略
  - XML 格式規格
  - 範例題目與答案
  - 使用提供的腳本執行評估
