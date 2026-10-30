<!--meta
{"title":"Playwright 網頁應用測試","category":"瀏覽器與測試自動化","tags":["Playwright","E2E 測試","行動裝置模擬","API Mock","視覺回歸"],
"summary":"用 Playwright 做專業的網頁應用測試與自動化：跨 Chromium／Firefox／WebKit 測試、元素互動（點擊、輸入、拖放、上傳下載）、斷言、截圖與錄影、網路攔截與 API mock、100 多種行動裝置模擬。內含基本測試、表單、API mock、行動裝置、視覺回歸的工作流程範例，以及可靠選擇器、自動等待、測試隔離與 Page Object 模式。",
"usage":"- 說「幫這個登入頁寫 E2E 測試」「測試手機版的排版」「mock 這個 API 再測結帳流程」\n- 安裝與 pytest／playwright.config 設定見 `references/setup-configuration.md`\n- 除錯：`PWDEBUG=1 pytest test.py`；CI 平行：`pytest -n auto`\n- 範例在 `examples/`（登入、表單、電商、API mock、行動裝置、POM）"}
-->
---
name: webapp-testing
description: "使用 Playwright 進行專業的網頁應用測試與自動化，支援多種瀏覽器、行動裝置模擬、截圖擷取、網路攔截與全面的測試斷言。用於：(1) 跨瀏覽器 E2E 測試，(2) UI 自動化，(3) 表單測試與驗證，(4) 視覺回歸測試，(5) API mock 與攔截，(6) 行動響應式測試"
---

# 用 Playwright 測試網頁應用

## 概覽

Playwright 是一個強大的網頁測試與自動化框架，支援所有現代瀏覽器（Chromium、Firefox、WebKit）。它提供可靠、快速且能力完整的自動化，具備自動等待、網路控制與全面的測試能力。

在以下需要時使用本技能：
- 為網頁應用建立端到端測試
- 自動化瀏覽器互動與工作流程
- 跨多種瀏覽器與裝置測試
- 驗證 UI/UX 功能與無障礙
- Mock API 並攔截網路請求
- 擷取截圖與影片以便除錯

## 核心能力

### 多瀏覽器測試
- Chromium（Chrome、Edge、Brave）
- Firefox（Mozilla Firefox）
- WebKit（Safari 引擎）
- 跨瀏覽器相容性測試
- 跨瀏覽器平行執行

### 元素互動
- 點擊、雙擊、右鍵點擊
- 以擬真的鍵盤模擬輸入文字
- 選擇下拉選單與核取方塊
- 滑鼠懸停與焦點互動
- 拖放操作
- 檔案上傳與下載

### 斷言與驗證
- 元素可見性與狀態檢查
- 文字內容驗證
- 屬性驗證
- URL 與導覽斷言
- 自訂 expect matcher
- 用於多項檢查的軟斷言

### 截圖與影片擷取
- 整頁截圖
- 針對特定元素的擷取
- 錄製測試過程的影片
- 視覺比對測試
- 用於除錯的 trace 檔案

### 網路攔截
- Mock API 回應
- 攔截並修改請求
- 監控網路流量
- 測試離線情境
- 效能監控

### 行動裝置模擬
- 100 多種裝置預設（iPhone、Pixel、iPad 等）
- 自訂 viewport 設定
- 觸控事件模擬
- 地理位置測試
- 方向變更

## 核心測試工作流程

### 1. 基本測試設定

建立一個利用 Playwright 自動等待的簡單測試：

{{CODE:1}}

### 2. 表單互動

測試表單填寫、驗證與送出：

{{CODE:2}}

### 3. API Mock

Mock API 回應以進行受控的測試：

{{CODE:3}}

### 4. 行動裝置模擬

在行動裝置上測試響應式設計：

{{CODE:4}}

### 5. 視覺回歸

擷取截圖以進行視覺比對：

{{CODE:5}}

## 關鍵測試原則

### 使用可靠的選擇器

{{CODE:6}}

### 善用自動等待

{{CODE:7}}

### 確保測試隔離

{{CODE:8}}

### 處理不穩定的測試

{{CODE:9}}

## Page Object 模型

使用 Page Object 模式組織測試，以提高可維護性：

{{CODE:10}}

## 常見測試模式

### 認證

{{CODE:11}}

### 檔案操作

{{CODE:12}}

### 網路監控

{{CODE:13}}

## 執行測試

### 基本指令

{{CODE:14}}

### 設定

參見 `references/setup-configuration.md`，內容包括：
- 完整的安裝說明
- 專案結構設定
- pytest.ini 設定
- TypeScript 的 playwright.config.ts
- CI/CD 整合範例

## 品質標準

確保測試符合以下條件：
- 測試彼此獨立，可以任意順序執行
- 選擇器可靠（測試 ID、語意化選擇器）
- 適當的錯誤處理與斷言
- 失敗時擷取截圖／影片
- 沒有寫死的等待（使用自動等待）
- 測試之間乾淨的狀態管理

## 其他資源

### 詳細文件
- [設定與組態](./references/setup-configuration.md) —— 安裝、專案結構與設定
- [最佳實務](./references/best-practices.md) —— 選擇器策略、等待模式、防止不穩定的測試
- [常見陷阱](./references/common-pitfalls.md) —— 競態條件、脆弱的選擇器、清理問題
- [CI/CD 整合](./references/ci-cd-integration.md) —— GitHub Actions、Docker、部署流水線

### 程式碼範例
- [登入測試](./examples/login-testing.md) —— 認證流程與工作階段管理
- [表單測試](./examples/form-testing.md) —— 表單驗證、檔案上傳、下拉選單
- [電商測試](./examples/ecommerce-testing.md) —— 購物車、結帳流程、優惠券
- [API Mock](./examples/api-mocking.md) —— 網路攔截、mock、監控
- [行動裝置測試](./examples/mobile-testing.md) —— 裝置模擬、觸控事件、響應式設計
- [Page Object 模型](./examples/page-object-model.md) —— POM 模式實作

### 輔助腳本
- [Playwright 輔助工具](./scripts/playwright_helper.py) —— 常見 Playwright 操作的工具函式
- [測試範例](./scripts/test_examples.py) —— 完整的測試組範例

### 外部資源
- 官方文件：https://playwright.dev
- Python API：https://playwright.dev/python/docs/intro
- TypeScript API：https://playwright.dev/docs/intro
- 最佳實務：https://playwright.dev/docs/best-practices
- 社群 Discord：https://aka.ms/playwright/discord

## 疑難排解

**測試不穩定：**
- 使用 Playwright 的自動等待，而不是手動 sleep
- 確保適當的等待條件（`wait_for_selector`、`wait_for_url`）
- 使用會自動重試的 `expect()` 斷言

**選擇器找不到元素：**
- 用瀏覽器 DevTools 確認元素存在
- 使用 Playwright Inspector：`PWDEBUG=1 pytest test.py`
- 嘗試多種選擇器策略（文字、角色、test-id）

**CI 中測試很慢：**
- 啟用平行執行：`pytest -n auto`
- 只在除錯時使用有頭模式
- 對相關的測試考慮重用瀏覽器 context

更多疑難排解提示，請見 [常見陷阱](./references/common-pitfalls.md)。
