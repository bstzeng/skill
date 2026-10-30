<!--meta
{"title":"Playwright 測試專家","category":"瀏覽器與測試自動化","tags":["Playwright","E2E 測試","Page Object","無障礙測試","視覺回歸"],
"summary":"處理 Playwright 測試時自動啟用的專家技能：涵蓋設定（專案、瀏覽器、報告器）、以角色為主的定位器與串接、Page Object 模式、自動等待斷言、fixture、以 storageState 重用登入狀態、網路 mock、@axe-core 無障礙稽核、截圖視覺回歸，以及 trace／截圖除錯與常見問題（不穩定測試、找不到元素、測試太慢）。附各功能的最低版本對照。",
"usage":"- 編輯 `*.spec.ts`、`playwright.config` 或提到定位器、Page Object 時自動觸發\n- 說「幫我把這個登入流程寫成 Playwright 測試」「這個測試為什麼不穩定」\n- 檢查環境：`{baseDir}/scripts/check-playwright-setup.sh`\n- 速查表：`references/playwright-cheatsheet.md`；Page Object 範本：`assets/page-object.template.ts`"}
-->
---
name: playwright-testing
description: 當使用者處理 Playwright 測試、提到 Playwright 設定、詢問選擇器／定位器／page object，或有位於 e2e 或 tests 目錄中符合 *.spec.ts 的檔案時自動啟用。提供 E2E 與整合測試的 Playwright 專業知識。
version: 1.1.0
allowed-tools: Read, Grep, Glob, Bash
capabilities:
  - playwright-configuration
  - locator-selection
  - page-object-patterns
  - fixture-creation
  - network-mocking
  - accessibility-testing
  - debugging-traces
  - api-testing
  - cross-browser-testing
---

# Playwright 測試專業

你是 Playwright 測試框架的專家，對瀏覽器自動化、選擇器、page object 以及端到端測試的最佳實務有深入的了解。

## 你的能力

1. **Playwright 設定**：專案、瀏覽器、報告器與 fixture
2. **定位器與選擇器**：以角色、文字、CSS 為基礎的定位器，以及串接的定位器
3. **Page Object 模型**：用 page object 組織測試
4. **斷言**：內建斷言、自訂 matcher、自動等待
5. **測試 Fixture**：內建與自訂的 fixture、測試隔離
6. **除錯**：trace、截圖、影片與 Playwright Inspector
7. **API 測試**：request fixture 與 API 測試能力

## 何時使用本技能

在以下情況，Claude 應自動呼叫本技能：
- 使用者提到 Playwright、playwright.config 或 Playwright 功能
- 遇到位於 e2e、tests 或 playwright 目錄中、符合 `*.spec.ts` 的檔案
- 使用者詢問定位器、page object 或瀏覽器自動化
- 討論到 E2E 或整合測試
- 需要瀏覽器測試的設定

## 如何使用本技能

### 存取資源

使用 `{baseDir}` 參照本技能目錄中的檔案：
- 腳本：`{baseDir}/scripts/`
- 文件：`{baseDir}/references/`
- 範本：`{baseDir}/assets/`

## 可用資源

本技能在 `{baseDir}` 中包含現成可用的資源：

- **references/playwright-cheatsheet.md** —— 定位器、斷言、動作與 CLI 指令的速查表
- **assets/page-object.template.ts** —— 完整的 Page Object 模型範本，含基底類別與範例
- **scripts/check-playwright-setup.sh** —— 驗證 Playwright 設定與瀏覽器安裝

## Playwright 最佳實務

### 測試結構
{{CODE:1}}

### 定位器最佳實務

#### 偏好的定位器（最有彈性）
{{CODE:2}}

#### 串接定位器
{{CODE:3}}

#### 測試 ID（最後手段）
{{CODE:4}}

### Page Object 模式
{{CODE:5}}

### 自動等待與斷言
{{CODE:6}}

### Fixture
{{CODE:7}}

### 以 Storage State 認證

不必每次都透過 UI 登入的高效認證方式：

{{CODE:8}}

### 網路 Mock 與攔截

Mock API 回應，讓測試可靠又快速：

{{CODE:9}}

### 無障礙測試

整合 @axe-core/playwright 進行無障礙稽核：

{{CODE:10}}

### 視覺回歸測試

比較截圖以偵測視覺變化：

{{CODE:11}}

## Playwright 設定

### 基本設定
{{CODE:12}}

## 除錯與疑難排解

### 除錯模式
{{CODE:13}}

### Trace
{{CODE:14}}

### 截圖
{{CODE:15}}

## 常見問題與解法

### 問題：不穩定的測試
- 使用自動等待的斷言，而不是固定的等待
- 等待特定的元素，而不是 `networkidle`（遇到 WebSocket、長輪詢、分析服務時會失效）：
  ```typescript
  // Bad: networkidle is unreliable
  await page.waitForLoadState('networkidle');

  // Good: wait for specific content
  await expect(page.getByRole('main')).toBeVisible();
  await expect(page.getByTestId('data-loaded')).toBeAttached();
  ```
- 確保適當的測試隔離

### 問題：找不到元素
- 使用 Playwright Inspector 找出更好的定位器
- 偏好以角色為基礎的選擇器
- 檢查是否有 iframe 或 shadow DOM

### 問題：測試太慢
- 重用認證狀態
- 使用 `test.describe.parallel()`
- Mock 緩慢的 API 呼叫

## 範例

### 範例 1：表單測試
測試表單時：
1. 輸入欄位使用 getByLabel
2. 為了速度使用 fill() 而不是 type()
3. 以按鈕定位器送出
4. 斷言成功訊息或頁面導覽

### 範例 2：表格測試
測試表格／清單時：
1. 表格列使用 getByRole('row')
2. 用 `.filter()` 依內容篩選
3. 串接以找出列中的動作
4. 斷言列數或內容

## 版本相容性

本技能中的模式需要以下最低版本：

| 功能 | 最低版本 | 備註 |
|---------|----------------|-------|
| getByRole 搭配 name | 1.27+ | 帶可存取名稱的角色定位器 |
| toHaveScreenshot | 1.22+ | 視覺回歸測試 |
| storageState | 1.13+ | 認證狀態持久化 |
| @axe-core/playwright | 4.7+ | 無障礙測試整合 |
| route.fulfill | 1.0+ | 網路 mock（穩定） |
| test.describe.configure | 1.24+ | 平行／循序測試設定 |

### 功能偵測

檢查你的 Playwright 版本：
{{CODE:16}}

### 升級

{{CODE:17}}

## 重要注意事項

- 相關時會自動呼叫 Playwright 技能
- 一律檢查 playwright.config.ts 中的專案設定
- 偏好以角色為基礎的定位器，讓測試更有彈性
- 使用自動等待的斷言，而不是明確的等待
- 在 CI 中考慮行動裝置與跨瀏覽器測試
