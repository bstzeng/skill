<!--meta
{"title":"打造 Next.js + Sanity 部落格","category":"前端與設計","tags":["Next.js","Sanity","部落格","SEO","i18n"],
"summary":"為 Next.js 網站加入以 Sanity CMS 為後台的企業部落格的通用工作流程：先掃描專案（Next.js 版本、next-intl、Tailwind、既有路由與慣例），再查最新官方文件，接著用 30 多題的需求問卷建立專案設定檔，產出一頁的高層計畫並等你核准，最後依 20 節規格實作（SEO 優先、多語系、效能預算、無障礙），並可用 Gemini 生成主視覺圖。",
"usage":"- 說「幫這個 Next.js 網站加一個部落格」「用 Sanity 建部落格」「規劃部落格架構」\n- 規格在 `blog-technical-requirements.md`，主視覺圖風格在 `blog-image-style-guide.md`\n- 會先等你核准計畫才開始寫程式\n- 不適用於純 MDX 部落格、新聞媒體或文件網站"}
-->
---
name: building-blog
description: 在為 Next.js + Sanity 網站加入部落格、從零建立部落格區塊、整合 Sanity CMS 管理編輯內容，或建立 SEO 最佳化的文章頁面時使用。觸發於像「加一個部落格」「建立部落格」「建立部落格區塊」「用 Sanity 設定部落格」「整合 Sanity CMS」「部落格架構」這類用語，或任何 Next.js 專案上的新部落格範圍討論。
---

# 打造部落格（Next.js + Sanity）

## 概覽

為以 Sanity CMS 為後台的 Next.js 網站加入部落格的通用工作流程。目標是企業部落格：SEO 優先、支援多語系、有效能預算、符合無障礙規範。

**SKILL.md 是協調者。規格放在兩份參考檔案中。**

## 檔案

- `blog-technical-requirements.md` —— §0 需求問卷（30 多題）→ §1 專案設定檔 → §2–§20 通用規格 → 檢查表。每個專案只編輯 §0 的答案與 §1。
- `blog-image-style-guide.md` —— 透過 Gemini 3 Pro Image（Nano Banana Pro）以 AI 生成主視覺圖的通用範本。上方是需求問題，中間是美學骨架，底部是三個範例欄位。

## 工作流程

### 步驟 1 —— 掃描主專案（在問任何問題之前）

先讀已經存在的東西。從偵測到的數值預填答案，遠比問使用者好。尋找：

- `package.json` —— Next.js 版本、`next-intl`、Sanity 套件、Tailwind、`framer-motion`
- `next.config.{ts,js,mjs}` —— 既有的 `images.formats`、i18n 設定
- `src/messages/**`、`src/i18n/**`、`messages/**` —— 目前的語系組合
- `src/app/[locale]/**` 或 `app/[locale]/**` —— 路由模式
- `tailwind.config.*`、`globals.css`、設計系統檔案 —— token、字型
- `CLAUDE.md`、`AGENTS.md`、`GEMINI.md` —— 專案慣例與核准的覆寫
- 既有的 `sanity-studio/` 或 `studio/` 資料夾
- `app/layout.{tsx,jsx}` —— 字型、分析工具、動態設定
- `public/brand/**`、`public/logo*` —— 發布者標誌
- `sitemap.ts`、`robots.ts` —— 既有的路由
- `.env*` 檔案 —— 已設定的環境變數名稱（不要記錄密鑰的值）

在問卷之前，把發現記錄成一份簡短的「已偵測」清單。

### 步驟 1.5 —— 擷取你會用到之技術堆疊的最新文件

規格的觀點可能與上游的實際情況脫節。實作之前，先取得這個專案實際會用到之函式庫的最新文件。不要跳過——規格是在某個固定時間點稽核的，而 Next.js／Sanity／next-intl 發布破壞性變更的頻率，比本技能更新的頻率還高。

如果環境中有 [`context7`](https://context7.com)，就使用它（它是閱讀最新函式庫文件最快的方式）；否則透過 `WebFetch` 改用函式庫的官方文件網站。到達對應的章節時，與規格交叉比對。

任何部落格建置都至少要讀的文件：

- **Next.js** —— App Router、`generateStaticParams`、`generateMetadata`、動態 `params`（15/16 中是同步還是 Promise）、圖片設定、`revalidateTag`、`unstable_cache` 的棄用狀態
- **Sanity v3**（`@sanity/client`、`next-sanity`）—— `client.fetch` 選項、草稿模式 + `stega` 規則、`defineQuery`、GROQ 投影模式、圖片 URL 產生器
- **next-intl**（只在多語系時）—— App Router 設定、`getTranslations`、`getMessages`、`setRequestLocale`、hreflang 模式
- **@portabletext/react** —— 目前的元件覆寫 API、外掛套件
- **@sanity/image-url** —— 參數、熱點／裁切行為、`auto=format`

到達對應的規格章節時，也要即時檢查：

- **主視覺圖產生器** —— Gemini 3 Pro Image（Nano Banana Pro）—— 目前的模型名稱、圖片生成端點、支援的尺寸／長寬比、`responseModalities` 的 JSON 結構
- **JSON-LD** —— Google 的 [Article 結構化資料](https://developers.google.com/search/docs/appearance/structured-data/article) 頁面，確認目前的必要欄位
- **CWV 門檻** —— `web.dev` 的 Core Web Vitals 頁面，確認目前 LCP/INP/CLS 的「良好」門檻

如果文件與規格矛盾，以文件為準。在專案設定檔（§1）中記下這個矛盾，並依文件進行。

### 步驟 2 —— 進行需求問卷

開啟 `blog-technical-requirements.md` 並逐一走過 §0。

- **Claude Code：** 使用 `AskUserQuestion`。把相關的問題合併成一次呼叫（每次最多 4 題）。從掃描結果預填建議的答案。
- **Codex／沒有互動式選擇器的 CLI：** 以純文字編號列出問題，請使用者以每批 5–10 題回答。顯示從掃描得到的建議答案。
- **無介面／非互動式：** 對提示中沒有明確涵蓋的部分套用通用預設值；列出每一項假設。

把答案寫進 §1「專案設定檔」（寫在 `docs/blog/` 下的專案本地副本，而不是通用的原始檔）。

### 步驟 3 —— 產出高層計畫

使用 §0 結尾的計畫範本。一頁。包含階段、鎖定的範圍、範圍外的項目、待決事項。**等待使用者明確核准。不要開始寫程式。**

### 步驟 4 —— 依規格實作

依序遵循 §2–§20。§19（通過／失敗檢查表）就是完成的定義。如果範圍包含 AI 生成的主視覺圖，就由圖片風格指南驅動 §20。

## 何時「不」使用本技能

- 靜態／只用 MDX 的部落格（沒有 CMS）—— 不同的技術堆疊、不同的模式
- 高頻率發稿的新聞媒體 —— sitemap 分塊與編輯工具會成為主要考量
- 文件網站 —— 改用文件框架
- 其實不算部落格的行銷到達頁

## 建議搭配的技能

- `frontend-design` —— 如果視覺識別不明確或網站還在從零開始，先發想方向
- `superpowers:brainstorming` —— 用於超出 §0 所涵蓋的範圍討論
- `superpowers:writing-plans` —— 在寫程式之前，把高層計畫展開成各階段的實作計畫
