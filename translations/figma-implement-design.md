<!--meta
{"title":"Figma 設計轉程式碼","category":"前端與設計","tags":["Figma","設計轉程式","Design Token","MCP","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：透過 Figma MCP 伺服器，把 Figma 設計以 1:1 視覺還原度轉成可上線的程式碼——取得設計脈絡與截圖、下載素材、轉換成專案慣例與設計系統 token，最後對照截圖逐項驗證。",
"usage":"- Codex：`$skill-installer figma-implement-design`；需先連接 Figma MCP Server（遠端或 figma-desktop）\n- 貼上 Figma 連結並說「實作這個元件」：`https://figma.com/design/<fileKey>/...?node-id=42-15`\n- 使用 figma-desktop MCP 時，直接在 Figma 桌面版選取節點即可，不必貼網址\n- 會優先重用專案既有元件與 token，而非照抄 Figma 輸出的 Tailwind"}
-->
---
name: figma-implement-design
description: 把 Figma 設計以 1:1 的視覺還原度轉換成可上線的應用程式碼。在從 Figma 檔案實作 UI 程式碼、使用者提到「implement design」「generate code」「implement component」、提供 Figma URL，或要求建立符合 Figma 規格的元件時使用。若要透過 `use_figma` 寫入 Figma 畫布，請使用 `figma-use`。
---

# 實作設計

## 概述

本技能提供一套結構化的工作流程，以像素級的精準度把 Figma 設計轉換成可上線的程式碼。它確保與 Figma MCP 伺服器的整合一致、正確使用設計 token，並與設計達到 1:1 的視覺一致。

## 技能邊界

- 當交付成果是使用者 repo 中的程式碼時，使用本技能。
- 如果使用者要求在 Figma 本身內部建立/編輯/刪除節點，改用 [figma-use](../figma-use/SKILL.md)。
- 如果使用者要求從程式碼或描述在 Figma 中建立或更新整頁畫面，改用 [figma-generate-design](../figma-generate-design/SKILL.md)。
- 如果使用者只要求 Code Connect 對應，改用 [figma-code-connect-components](../figma-code-connect-components/SKILL.md)。
- 如果使用者要求撰寫可重用的代理規則（`CLAUDE.md`/`AGENTS.md`），改用 [figma-create-design-system-rules](../figma-create-design-system-rules/SKILL.md)。

## 前置條件

- Figma MCP 伺服器必須已連線且可存取
- 使用者必須提供以下格式的 Figma URL：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - `:fileKey` 是檔案金鑰
  - `1-2` 是節點 ID（要實作的特定元件或框架）
- **或者**使用 `figma-desktop` MCP 時：使用者可以直接在 Figma 桌面應用程式中選取節點（不需要 URL）
- 專案應有既定的設計系統或元件庫（建議）

## 必要工作流程

**依序遵循這些步驟。不要略過步驟。**

### 步驟 1：取得節點 ID

#### 選項 A：從 Figma URL 解析

當使用者提供 Figma URL 時，擷取檔案金鑰與節點 ID，作為參數傳給 MCP 工具。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**擷取：**

- **檔案金鑰：** `:fileKey`（`/design/` 之後的那一段）
- **節點 ID：** `1-2`（`node-id` 查詢參數的值）

**注意：** 使用本機桌面版 MCP（`figma-desktop`）時，`fileKey` 不會作為參數傳給工具呼叫。伺服器會自動使用目前開啟的檔案，所以只需要 `nodeId`。

**範例：**

- URL：`https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- 檔案金鑰：`kL9xQn2VwM8pYrTb4ZcHjF`
- 節點 ID：`42-15`

#### 選項 B：使用 Figma 桌面應用程式的目前選取（僅限 figma-desktop MCP）

使用 `figma-desktop` MCP 且使用者「沒有」提供 URL 時，工具會自動使用桌面應用程式中已開啟的 Figma 檔案裡目前選取的節點。

**注意：** 以選取為基礎的提示只適用於 `figma-desktop` MCP 伺服器。遠端伺服器需要框架或圖層的連結才能擷取脈絡。使用者必須開著 Figma 桌面應用程式並選取一個節點。

### 步驟 2：取得設計脈絡

以擷取到的檔案金鑰與節點 ID 執行 `get_design_context`。

{{CODE:1}}

這會提供結構化資料，包括：

- 版面屬性（Auto Layout、約束、尺寸）
- 字體排印規格
- 色彩值與設計 token
- 元件結構與變體
- 間距與內距值

**如果回應太大或被截斷：**

1. 執行 `get_metadata(fileKey=":fileKey", nodeId="1-2")` 取得高層的節點地圖
2. 從中繼資料中找出需要的特定子節點
3. 以 `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")` 個別抓取子節點

### 步驟 3：擷取視覺參考

以相同的檔案金鑰與節點 ID 執行 `get_screenshot` 取得視覺參考。

{{CODE:2}}

這張截圖是視覺驗證的真實依據。在整個實作過程中都要保持可取用。

### 步驟 4：下載所需素材

下載 Figma MCP 伺服器回傳的所有素材（圖片、圖示、SVG）。

**重要：** 遵循以下素材規則：

- 如果 Figma MCP 伺服器為圖片或 SVG 回傳 `localhost` 來源，就直接使用該來源
- **不要**匯入或新增圖示套件——所有素材都應來自 Figma 的回傳內容
- 如果提供了 `localhost` 來源，**不要**使用或建立占位符
- 素材透過 Figma MCP 伺服器內建的素材端點提供

### 步驟 5：轉換成專案慣例

把 Figma 輸出轉換成此專案的框架、樣式與慣例。

**關鍵原則：**

- 把 Figma MCP 輸出（通常是 React + Tailwind）視為設計與行為的表示，而不是最終的程式碼風格
- 把 Tailwind 工具類別換成專案偏好的工具類別或設計系統 token
- 重用既有元件（按鈕、輸入框、文字、圖示包裝），而不是重複實作功能
- 一致地使用專案的色彩系統、字級階層與間距 token
- 尊重既有的路由、狀態管理與資料抓取模式

### 步驟 6：達到 1:1 視覺一致

力求與 Figma 設計達到像素級的視覺一致。

**準則：**

- 優先考慮 Figma 還原度，精確符合設計
- 避免寫死的值——盡可能使用 Figma 中的設計 token
- 當設計系統 token 與 Figma 規格衝突時，優先使用設計系統 token，但以最小幅度調整間距或尺寸以符合視覺
- 遵循 WCAG 無障礙要求
- 視需要加入元件文件

### 步驟 7：對照 Figma 驗證

在標記完成之前，對照 Figma 截圖驗證最終 UI。

**驗證清單：**

- [ ] 版面相符（間距、對齊、尺寸）
- [ ] 字體排印相符（字型、大小、字重、行高）
- [ ] 色彩完全相符
- [ ] 互動狀態依設計運作（hover、active、disabled）
- [ ] 響應式行為遵循 Figma 約束
- [ ] 素材正確渲染
- [ ] 符合無障礙標準

## 實作規則

### 元件組織

- 把 UI 元件放在專案指定的設計系統目錄中
- 遵循專案的元件命名慣例
- 除非動態值確實需要，否則避免內嵌樣式

### 設計系統整合

- 可能的話「一律」使用專案設計系統中的元件
- 把 Figma 設計 token 對應到專案設計 token
- 當已有相符的元件時，擴充它，而不是建立新的
- 記錄任何新加入設計系統的元件

### 程式碼品質

- 避免寫死的值——抽成常數或設計 token
- 讓元件保持可組合、可重用
- 為元件 props 加上 TypeScript 型別
- 為匯出的元件加上 JSDoc 註解

## 範例

### 範例 1：實作按鈕元件

使用者說：「實作這個 Figma 按鈕元件：https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15」

**動作：**

1. 解析 URL，擷取 fileKey=`kL9xQn2VwM8pYrTb4ZcHjF` 與 nodeId=`42-15`
2. 執行 `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")`
3. 執行 `get_screenshot(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")` 取得視覺參考
4. 從素材端點下載任何按鈕圖示
5. 檢查專案是否已有按鈕元件
6. 如果有，用新的變體擴充它；如果沒有，依專案慣例建立新元件
7. 把 Figma 色彩對應到專案設計 token（例如 `primary-500`、`primary-hover`）
8. 對照截圖驗證內距、圓角、字體排印

**結果：** 符合 Figma 設計、並整合進專案設計系統的按鈕元件。

### 範例 2：建立儀表板版面

使用者說：「做出這個儀表板：https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Dashboard?node-id=10-5」

**動作：**

1. 解析 URL，擷取 fileKey=`pR8mNv5KqXzGwY2JtCfL4D` 與 nodeId=`10-5`
2. 執行 `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 了解頁面結構
3. 從中繼資料中找出主要區塊（頁首、側邊欄、內容區、卡片）及其子節點 ID
4. 對每個主要區塊執行 `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId=":childNodeId")`
5. 對整頁執行 `get_screenshot(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")`
6. 下載所有素材（Logo、圖示、圖表）
7. 使用專案的版面基本元件建立版面
8. 盡可能使用既有元件實作每個區塊
9. 對照 Figma 約束驗證響應式行為

**結果：** 符合 Figma 設計、具響應式版面的完整儀表板。

## 最佳實踐

### 永遠從脈絡開始

絕不基於假設來實作。一律先抓取 `get_design_context` 與 `get_screenshot`。

### 漸進式驗證

在實作過程中頻繁驗證，而不只是在最後。這能及早發現問題。

### 記錄偏離之處

如果必須偏離 Figma 設計（例如因為無障礙或技術限制），在程式碼註解中說明原因。

### 重用優於重建

建立新元件之前，一律先檢查既有元件。整個程式碼庫的一致性，比精確複製 Figma 更重要。

### 設計系統優先

拿不定主意時，優先採用專案的設計系統模式，而不是逐字翻譯 Figma。

## 常見問題與解法

### 問題：Figma 輸出被截斷

**原因：** 設計太複雜，或巢狀圖層太多，無法在單一回應中回傳。
**解法：** 用 `get_metadata` 取得節點結構，再用 `get_design_context` 個別抓取特定節點。

### 問題：實作後設計不相符

**原因：** 實作的程式碼與原始 Figma 設計之間有視覺差異。
**解法：** 與步驟 3 的截圖並排比較。檢查設計脈絡資料中的間距、色彩與字體排印值。

### 問題：素材無法載入

**原因：** Figma MCP 伺服器的素材端點無法存取，或 URL 被修改了。
**解法：** 確認 Figma MCP 伺服器的素材端點可以存取。伺服器在 `localhost` URL 提供素材。直接使用，不要修改。

### 問題：設計 token 的值與 Figma 不同

**原因：** 專案設計系統 token 的值與 Figma 設計中指定的不同。
**解法：** 當專案 token 與 Figma 值不同時，為了一致性優先使用專案 token，但調整間距/尺寸以維持視覺還原度。

## 理解設計實作

Figma 實作工作流程建立了一套把設計轉換成程式碼的可靠流程：

**對設計師：** 有信心實作結果會以像素級的精準度符合他們的設計。
**對開發者：** 一種消除猜測、減少來回修改的結構化做法。
**對團隊：** 一致、高品質、能維持設計系統完整性的實作。

遵循這個工作流程，你就能確保每一份 Figma 設計都以同樣的用心與對細節的關注被實作出來。

## 其他資源

- [Figma MCP 伺服器文件](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP 伺服器工具與提示詞](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma 變數與設計 Token](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
