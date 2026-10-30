<!--meta
{"title":"網頁 Artifact 建構器","category":"前端與設計","tags":["React","Tailwind","shadcn/ui","Artifact","Anthropic 官方"],
"summary":"Anthropic 官方技能：用 React 18 + TypeScript + Vite + Tailwind + shadcn/ui 建構複雜、多元件的 claude.ai HTML artifact，最後用 Parcel 打包成單一 HTML 檔。適合需要狀態管理、路由或 shadcn 元件的作品，簡單的單檔 HTML 不需要用它。",
"usage":"- 安裝：`npx skills add https://github.com/anthropics/skills --skill web-artifacts-builder`\n- 說「做一個有分頁、篩選和圖表的專案管理儀表板 artifact」\n- 流程：`scripts/init-artifact.sh` 建專案 → 編輯程式 → `scripts/bundle-artifact.sh` 打包成 `bundle.html`\n- 明確要求避免「AI 味」：不要過多置中、紫色漸層、統一圓角與 Inter 字型"}
-->
---
name: web-artifacts-builder
description: 一套使用現代前端網頁技術（React、Tailwind CSS、shadcn/ui）建立精緻、多元件 claude.ai HTML artifact 的工具。用於需要狀態管理、路由或 shadcn/ui 元件的複雜 artifact——不適用於簡單的單檔 HTML/JSX artifact。
license: 完整條款見 LICENSE.txt
---

# 網頁 Artifact 建構器

要建立強大的前端 claude.ai artifact，請依照以下步驟：
1. 使用 `scripts/init-artifact.sh` 初始化前端 repo
2. 編輯產生的程式碼來開發你的 artifact
3. 使用 `scripts/bundle-artifact.sh` 把所有程式碼打包成單一 HTML 檔
4. 把 artifact 呈現給使用者
5. （選用）測試 artifact

**技術棧**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 設計與樣式準則

非常重要：為了避免常被稱為「AI slop」的東西，避免使用過多的置中版面、紫色漸層、統一的圓角，以及 Inter 字型。

## 快速開始

### 步驟 1：初始化專案

執行初始化腳本來建立新的 React 專案：
{{CODE:1}}

這會建立一個完整設定好的專案，包含：
- ✅ React + TypeScript（透過 Vite）
- ✅ Tailwind CSS 3.4.1 搭配 shadcn/ui 主題系統
- ✅ 已設定路徑別名（`@/`）
- ✅ 預先安裝 40 多個 shadcn/ui 元件
- ✅ 包含所有 Radix UI 相依套件
- ✅ 已設定 Parcel 打包（透過 .parcelrc）
- ✅ 相容 Node 18+（自動偵測並固定 Vite 版本）

### 步驟 2：開發你的 Artifact

要建構 artifact，請編輯產生的檔案。指引請見下方的**常見開發任務**。

### 步驟 3：打包成單一 HTML 檔

要把 React 應用程式打包成單一 HTML artifact：
{{CODE:2}}

這會建立 `bundle.html` ——一個自成一體的 artifact，所有 JavaScript、CSS 與相依套件都已內嵌。這個檔案可以直接在 Claude 對話中以 artifact 的形式分享。

**需求**：你的專案根目錄必須有一個 `index.html`。

**腳本做了什麼**：
- 安裝打包相依套件（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 建立支援路徑別名的 `.parcelrc` 設定
- 用 Parcel 建置（不產生 source map）
- 用 html-inline 把所有素材內嵌到單一 HTML 中

### 步驟 4：與使用者分享 Artifact

最後，在對話中把打包好的 HTML 檔分享給使用者，讓他們能以 artifact 的形式檢視。

### 步驟 5：測試/視覺化 Artifact（選用）

注意：這是完全選用的步驟。只在必要或被要求時執行。

要測試/視覺化 artifact，使用可用的工具（包括其他技能，或像 Playwright、Puppeteer 這類內建工具）。一般來說，避免事先測試 artifact，因為這會在請求與看到完成的 artifact 之間增加延遲。在呈現 artifact 之後，如果有人要求或出現問題，再進行測試。

## 參考

- **shadcn/ui 元件**：https://ui.shadcn.com/docs/components
