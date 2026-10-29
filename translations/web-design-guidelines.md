<!--meta
{"title":"網頁介面規範審查","category":"前端與設計","tags":["UI 審查","無障礙","UX","Vercel"],
"summary":"依照 Vercel 維護的《Web Interface Guidelines》審查你的 UI 程式碼，以 `檔案:行號` 格式列出不符合規範之處（無障礙、互動、排版等）。",
"usage":"- 安裝：`npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`\n- 對代理說「review my UI」「幫我檢查無障礙」或 `/web-design-guidelines src/components/**/*.tsx`\n- 每次審查前會即時抓取最新版規範，所以規則永遠是最新的"}
-->
---
name: web-design-guidelines
description: 審查 UI 程式碼是否符合 Web Interface Guidelines（網頁介面規範）。當被要求「review my UI」「檢查無障礙」「稽核設計」「審查 UX」或「依最佳實踐檢查我的網站」時使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <檔案或樣式>
---

# 網頁介面規範（Web Interface Guidelines）

審查檔案是否符合網頁介面規範。

## 運作方式

1. 從下方來源 URL 抓取最新的規範
2. 讀取指定的檔案（或請使用者提供檔案/樣式）
3. 依抓取到的規範中所有規則進行檢查
4. 以精簡的 `file:line` 格式輸出發現

## 規範來源

每次審查前都要抓取最新規範：

{{CODE:1}}

使用 WebFetch 取得最新規則。抓取到的內容包含所有規則與輸出格式說明。

## 用法

當使用者提供檔案或樣式參數時：
1. 從上方來源 URL 抓取規範
2. 讀取指定的檔案
3. 套用抓取到的規範中所有規則
4. 依規範中指定的格式輸出發現

如果沒有指定檔案，就詢問使用者要審查哪些檔案。
