<!--meta
{"title":"React 效能最佳實踐","category":"前端與設計","tags":["React","Next.js","效能優化","Vercel"],
"summary":"Vercel 工程團隊維護的 React / Next.js 效能優化指南：8 大類共 70 條規則，依影響程度排序（消除請求瀑布、縮小 bundle、伺服器端效能、重新渲染優化等），撰寫、審查或重構 React 程式時自動套用。",
"usage":"- 安裝：`npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices`\n- 撰寫或審查 React 元件、Next.js 頁面、資料抓取時自動觸發；也可直接說「用 Vercel 最佳實踐檢查這個頁面的效能」\n- 每條規則在 `rules/<規則名>.md` 有錯誤/正確範例；完整版見 `AGENTS.md`"}
-->
---
name: vercel-react-best-practices
description: 來自 Vercel 工程團隊的 React 與 Next.js 效能優化指南。撰寫、審查或重構 React/Next.js 程式碼時應使用本技能，以確保採用最佳效能模式。涉及 React 元件、Next.js 頁面、資料抓取、bundle 優化或效能改進的任務會觸發。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳實踐

由 Vercel 維護、針對 React 與 Next.js 應用程式的完整效能優化指南。包含 8 個類別共 70 條規則，依影響程度排定優先順序，用於引導自動化重構與程式碼生成。

## 何時套用

在以下情況參考這些指南：
- 撰寫新的 React 元件或 Next.js 頁面
- 實作資料抓取（客戶端或伺服器端）
- 審查程式碼的效能問題
- 重構既有的 React/Next.js 程式碼
- 優化 bundle 大小或載入時間

## 依優先順序排列的規則類別

| 優先序 | 類別 | 影響 | 前綴 |
|--------|------|------|------|
| 1 | 消除瀑布式請求 | 關鍵 | `async-` |
| 2 | Bundle 大小優化 | 關鍵 | `bundle-` |
| 3 | 伺服器端效能 | 高 | `server-` |
| 4 | 客戶端資料抓取 | 中高 | `client-` |
| 5 | 重新渲染優化 | 中 | `rerender-` |
| 6 | 渲染效能 | 中 | `rendering-` |
| 7 | JavaScript 效能 | 中低 | `js-` |
| 8 | 進階模式 | 低 | `advanced-` |

## 快速參考

### 1. 消除瀑布式請求（關鍵）

- `async-cheap-condition-before-await` - 在 await 旗標或遠端值之前，先檢查便宜的同步條件
- `async-defer-await` - 把 await 移到真正用到它的分支中
- `async-parallel` - 對彼此獨立的操作使用 Promise.all()
- `async-dependencies` - 對部分相依的情況使用 better-all
- `async-api-routes` - 在 API 路由中提早啟動 promise、延後 await
- `async-suspense-boundaries` - 使用 Suspense 串流內容

### 2. Bundle 大小優化（關鍵）

- `bundle-barrel-imports` - 直接匯入，避免 barrel 檔案
- `bundle-analyzable-paths` - 優先使用可靜態分析的 import 與檔案系統路徑，避免過大的 bundle 與追蹤
- `bundle-dynamic-imports` - 對笨重的元件使用 next/dynamic
- `bundle-defer-third-party` - 在 hydration 之後才載入分析/日誌工具
- `bundle-conditional` - 只在功能啟用時才載入模組
- `bundle-preload` - 在 hover/focus 時預先載入，提升感知速度

### 3. 伺服器端效能（高）

- `server-auth-actions` - 像 API 路由一樣驗證 server action
- `server-cache-react` - 使用 React.cache() 做單次請求內的去重
- `server-cache-lru` - 使用 LRU 快取做跨請求快取
- `server-dedup-props` - 避免 RSC props 中的重複序列化
- `server-hoist-static-io` - 把靜態 I/O（字型、Logo）提升到模組層級
- `server-no-shared-module-state` - 避免在 RSC/SSR 中使用模組層級的可變請求狀態
- `server-serialization` - 盡量減少傳給客戶端元件的資料
- `server-parallel-fetching` - 重組元件以平行化資料抓取
- `server-parallel-nested-fetching` - 在 Promise.all 中為每個項目串接巢狀抓取
- `server-after-nonblocking` - 使用 after() 執行非阻塞操作

### 4. 客戶端資料抓取（中高）

- `client-swr-dedup` - 使用 SWR 自動去除重複請求
- `client-event-listeners` - 去除重複的全域事件監聽器
- `client-passive-event-listeners` - 捲動事件使用 passive 監聽器
- `client-localstorage-schema` - 為 localStorage 資料加上版本並精簡內容

### 5. 重新渲染優化（中）

- `rerender-defer-reads` - 不要訂閱只在回呼中使用的狀態
- `rerender-memo` - 把昂貴的工作抽到 memo 化的元件中
- `rerender-memo-with-default-value` - 把非基本型別的預設 props 提升到外部
- `rerender-dependencies` - 在 effect 中使用基本型別的相依
- `rerender-derived-state` - 訂閱衍生出的布林值，而不是原始值
- `rerender-derived-state-no-effect` - 在渲染期間推導狀態，而不是在 effect 中
- `rerender-functional-setstate` - 使用函式形式的 setState 以取得穩定的回呼
- `rerender-lazy-state-init` - 對昂貴的值傳函式給 useState
- `rerender-simple-expression-in-memo` - 簡單的基本型別不要用 memo
- `rerender-split-combined-hooks` - 拆分相依彼此獨立的 hook
- `rerender-move-effect-to-event` - 把互動邏輯放在事件處理器中
- `rerender-transitions` - 對不緊急的更新使用 startTransition
- `rerender-use-deferred-value` - 延後昂貴的渲染，讓輸入保持即時回應
- `rerender-use-ref-transient-values` - 對短暫且頻繁變動的值使用 ref
- `rerender-no-inline-components` - 不要在元件內部定義元件

### 6. 渲染效能（中）

- `rendering-animate-svg-wrapper` - 動畫外層 div，而不是 SVG 元素
- `rendering-content-visibility` - 長清單使用 content-visibility
- `rendering-hoist-jsx` - 把靜態 JSX 抽到元件外部
- `rendering-svg-precision` - 降低 SVG 座標精度
- `rendering-hydration-no-flicker` - 對僅限客戶端的資料使用內嵌腳本
- `rendering-hydration-suppress-warning` - 壓下預期中的不一致警告
- `rendering-activity` - 使用 Activity 元件處理顯示/隱藏
- `rendering-conditional-render` - 條件渲染用三元運算子，而不是 &&
- `rendering-usetransition-loading` - 載入狀態優先使用 useTransition
- `rendering-resource-hints` - 使用 React DOM 資源提示進行預先載入
- `rendering-script-defer-async` - 在 script 標籤上使用 defer 或 async

### 7. JavaScript 效能（中低）

- `js-batch-dom-css` - 透過 class 或 cssText 批次變更 CSS
- `js-index-maps` - 為重複查找建立 Map
- `js-cache-property-access` - 在迴圈中快取物件屬性
- `js-cache-function-results` - 在模組層級的 Map 中快取函式結果
- `js-cache-storage` - 快取 localStorage/sessionStorage 的讀取
- `js-combine-iterations` - 把多個 filter/map 合併成一個迴圈
- `js-length-check-first` - 在昂貴的比較之前先檢查陣列長度
- `js-early-exit` - 提早從函式返回
- `js-hoist-regexp` - 把 RegExp 的建立提升到迴圈外
- `js-min-max-loop` - 用迴圈找最小/最大值，而不是排序
- `js-set-map-lookups` - 使用 Set/Map 進行 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可變性
- `js-flatmap-filter` - 使用 flatMap 一次完成 map 與 filter
- `js-request-idle-callback` - 把非關鍵工作延到瀏覽器閒置時間

### 8. 進階模式（低）

- `advanced-effect-event-deps` - 不要把 `useEffectEvent` 的結果放進 effect 相依
- `advanced-event-handler-refs` - 把事件處理器存在 ref 中
- `advanced-init-once` - 每次應用程式載入只初始化一次
- `advanced-use-latest` - 用 useLatest 取得穩定的回呼參照

## 如何使用

閱讀個別的規則檔以取得詳細說明與程式碼範例：

{{CODE:1}}

每個規則檔包含：
- 簡短說明為什麼它重要
- 錯誤的程式碼範例及說明
- 正確的程式碼範例及說明
- 額外的脈絡與參考資料

## 完整彙編文件

所有規則完整展開的指南：`AGENTS.md`
