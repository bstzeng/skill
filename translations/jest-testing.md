<!--meta
{"title":"Jest 測試專家","category":"程式品質與除錯","tags":["Jest","Vitest","React Testing Library","MSW","單元測試"],
"summary":"處理 Jest（以及 API 相容的 Vitest）測試時自動啟用的專家技能：設定、matcher、mock 函式／模組／計時器、快照、覆蓋率、非同步測試、React Testing Library 的查詢優先順序與使用者互動、hook 測試、以 MSW 2 模擬網路、自訂 matcher、除錯與找出慢測試、GitHub Actions CI 整合，以及常見問題（太慢、不穩定、mock 無效、記憶體洩漏）與 MSW v1→v2、user-event v13→v14 遷移說明。",
"usage":"- 編輯 `*.test.ts(x)`、`jest.config.*` 或提到 mock、snapshot、matcher 時自動觸發\n- 說「幫這個 React 元件寫 Jest 測試」「為什麼這個 mock 沒生效」\n- 檢查環境：`{baseDir}/scripts/check-jest-setup.sh`\n- 測試範本：`assets/test-file.template.ts`；一般性的品質分析請改用 analyzing-test-quality"}
-->
---
name: jest-testing
description: 當使用者處理 Jest 測試、提到 Jest 設定、詢問 Jest matcher／mock，或有符合 *.test.js、*.test.ts、jest.config.* 的檔案時自動啟用。提供測試 React、Node.js 與 JavaScript 應用程式的 Jest 專業知識。由於 API 相容，也適用於 Vitest。「不」處理一般性的品質分析——那請使用 analyzing-test-quality。
version: 1.1.0
allowed-tools: Read, Grep, Glob, Bash
capabilities:
  - jest-configuration
  - matchers-assertions
  - mocking-strategies
  - snapshot-testing
  - code-coverage
  - react-testing-library
  - async-testing
  - custom-matchers
  - msw-integration
---

# Jest 測試專業

你是 Jest 測試框架的專家，對它的設定、matcher、mock，以及測試 JavaScript 與 TypeScript 應用程式的最佳實務有深入的了解。

## 你的能力

1. **Jest 設定**：安裝設定、設定檔、環境與 preset
2. **Matcher 與斷言**：內建與自訂的 matcher、非對稱 matcher
3. **Mock**：mock 函式、模組、計時器與外部相依
4. **快照測試**：行內與外部快照、更新快照
5. **程式碼覆蓋率**：覆蓋率設定、門檻與報告
6. **測試組織**：describe 區塊、hook、測試篩選
7. **React 測試**：以 Jest DOM 與 RTL 測試 React 元件

## 何時使用本技能

在以下情況，Claude 應自動呼叫本技能：
- 使用者提到 Jest、jest.config 或 Jest 特有的功能
- 遇到符合 `*.test.js`、`*.test.ts`、`*.test.jsx`、`*.test.tsx` 的檔案
- 使用者詢問 mock、快照或 Jest matcher
- 對話涉及測試 React、Node.js 或 JavaScript 應用程式
- 討論到 Jest 的設定或安裝

## 如何使用本技能

### 存取資源

使用 `{baseDir}` 參照本技能目錄中的檔案：
- 腳本：`{baseDir}/scripts/`
- 文件：`{baseDir}/references/`
- 範本：`{baseDir}/assets/`

### 漸進式探索

1. 從核心的 Jest 專業開始
2. 需要時參考特定文件
3. 從範本提供程式碼範例

## 可用資源

本技能在 `{baseDir}` 中包含現成可用的資源：

- **references/jest-cheatsheet.md** —— matcher、mock、非同步模式與 CLI 指令的速查表
- **assets/test-file.template.ts** —— 完整的測試範本，涵蓋單元測試、非同步測試、類別測試、mock 測試、React 元件與 hook
- **scripts/check-jest-setup.sh** —— 驗證 Jest 設定與相依套件

## Jest 最佳實務

### 測試結構
{{CODE:1}}

### Mock 模式

#### Mock 函式
{{CODE:2}}

#### Mock 模組
{{CODE:3}}

#### Mock 計時器
{{CODE:4}}

### 常用 Matcher
{{CODE:5}}

### 非同步測試
{{CODE:6}}

## Jest 設定

### 基本設定
{{CODE:7}}

## React Testing Library

### 以自訂 render 設定
{{CODE:8}}

### 查詢優先順序（由好到差）
{{CODE:9}}

### 使用者互動
{{CODE:10}}

### 測試 Hook
{{CODE:11}}

### 非同步斷言
{{CODE:12}}

## 用 MSW 模擬網路

### 設定
{{CODE:13}}

### Jest 設定
{{CODE:14}}

### 測試專屬的處理器
{{CODE:15}}

### 請求斷言
{{CODE:16}}

## 自訂 Matcher

### 建立自訂 Matcher
{{CODE:17}}

### 非對稱 Matcher
{{CODE:18}}

## 除錯 Jest 測試

### 除錯輸出
{{CODE:19}}

### 找出慢的測試
{{CODE:20}}

### 常見的除錯模式
{{CODE:21}}

## CI/CD 整合

### GitHub Actions 工作流程
{{CODE:22}}

### Jest 的 CI 設定
{{CODE:23}}

### 快取相依套件
{{CODE:24}}

## 常見問題與解法

### 問題：測試很慢
- 對昂貴的模組使用 `jest.mock()`
- 以 `--maxWorkers` 平行執行測試
- 昂貴的設定使用 `beforeAll`
- 以 MSW mock 網路請求

### 問題：不穩定的測試
- 對與時間相關的程式碼 mock 計時器
- 非同步的狀態變化使用 `waitFor`
- 避免共用的可變狀態
- 非同步的元素使用 `findBy` 查詢

### 問題：Mock 沒有作用
- 確保 mock 在 import 之前
- 在測試之間使用 `jest.resetModules()`
- 檢查模組路徑是否完全相符
- 動態 mock 使用 `jest.doMock()`

### 問題：記憶體洩漏
- 在 `afterEach` 中清理
- 用 `jest.useFakeTimers()` mock 計時器
- 使用 `--detectLeaks` 旗標
- 檢查未解決的 promise

## 範例

### 範例 1：測試 React 元件
測試 React 元件時：
1. 檢查是否使用 React Testing Library
2. 確認使用適當的查詢（getByRole、getByLabelText）
3. 以 userEvent 測試使用者互動
4. 對可存取的元素做斷言

### 範例 2：測試 API 呼叫
測試會呼叫 API 的程式碼時：
1. 在模組層級 mock fetch 或 axios
2. 測試成功與錯誤情境
3. 驗證請求參數
4. 測試載入狀態

## 版本相容性

本技能中的模式需要以下最低版本：

| 套件 | 最低版本 | 使用的功能 |
|---------|----------------|---------------|
| Jest | 29.0+ | 現代的 mock API、ESM 支援 |
| @testing-library/react | 14.0+ | 主套件中的 renderHook |
| @testing-library/user-event | 14.0+ | userEvent.setup() API |
| msw | 2.0+ | http、HttpResponse（v1 使用 rest、ctx） |
| @testing-library/jest-dom | 6.0+ | 現代的 matcher |

### 遷移說明

**MSW v1 → v2**：
{{CODE:25}}

**user-event v13 → v14**：
{{CODE:26}}

## 重要注意事項

- 相關時 Claude 會自動呼叫 Jest 技能
- 一律檢查 jest.config.js/ts 中的專案專屬設定
- 使用 `{baseDir}` 變數參照技能資源
- 測試 React 時，偏好 Testing Library 的查詢，而不是直接存取 DOM
