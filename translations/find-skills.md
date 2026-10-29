<!--meta
{"title":"技能搜尋器","category":"技能管理","tags":["技能搜尋","套件管理","skills CLI","入門必裝"],
"summary":"當你問「有沒有能做 X 的 skill」時，幫你在開放的 Agent Skills 生態系中搜尋、評估品質並安裝合適的 skill。是 skills.sh 上安裝數最多的 skill。",
"usage":"- 安裝：`npx skills add https://github.com/vercel-labs/skills --skill find-skills`\n- 直接用自然語言詢問代理：「有沒有幫我寫 changelog 的 skill？」\n- 代理會先查 skills.sh 排行榜，再執行 `npx skills find <關鍵字>`，依安裝數、來源信譽、GitHub 星數篩選後推薦\n- 你同意後，代理會執行 `npx skills add <owner/repo@skill> -g -y` 幫你安裝"}
-->
---
name: find-skills
description: 當使用者問「我要怎麼做 X」「幫我找一個做 X 的 skill」「有沒有能……的 skill」，或表示想擴充能力時，協助使用者探索並安裝代理技能（agent skills）。當使用者在尋找可能以可安裝 skill 形式存在的功能時，就應使用本技能。
---

# 尋找技能（Find Skills）

本技能協助你從開放的代理技能生態系中探索並安裝技能。

## 何時使用本技能

當使用者有以下情況時使用本技能：

- 問「我要怎麼做 X」，而 X 可能是已有現成 skill 的常見任務
- 說「幫我找一個做 X 的 skill」或「有沒有做 X 的 skill」
- 問「你能不能做 X」，而 X 是一項專門能力
- 表示有興趣擴充代理的能力
- 想搜尋工具、範本或工作流程
- 提到希望在某個特定領域（設計、測試、部署等）得到協助

## 什麼是 Skills CLI？

Skills CLI（`npx skills`）是開放代理技能生態系的套件管理器。Skill 是模組化的套件，透過專門知識、工作流程與工具來擴充代理的能力。

**主要指令：**

- `npx skills find [query] [--owner <owner>]` — 以互動方式或關鍵字搜尋技能，可選擇限定某個 GitHub 擁有者
- `npx skills add <package>` — 從 GitHub 或其他來源安裝技能
- `npx skills update` — 更新所有已安裝的技能

**瀏覽技能：** https://skills.sh/

## 如何協助使用者尋找技能

### 步驟 1：了解他們需要什麼

當使用者請求協助時，先辨識：

1. 領域（例如 React、測試、設計、部署）
2. 具體任務（例如撰寫測試、製作動畫、審查 PR）
3. 這是否是夠常見、很可能已有 skill 的任務

### 步驟 2：先看排行榜

在執行 CLI 搜尋之前，先查看 [skills.sh 排行榜](https://skills.sh/)，確認該領域是否已有知名的 skill。排行榜依總安裝數排序，會呈現最熱門、最經得起考驗的選項。

例如網頁開發的熱門技能包括：
- `vercel-labs/agent-skills` — React、Next.js、網頁設計（每個都超過 10 萬次安裝）
- `anthropics/skills` — 前端設計、文件處理（超過 10 萬次安裝）

### 步驟 3：搜尋技能

如果排行榜沒有涵蓋使用者的需求，就執行 find 指令：

{{CODE:1}}

例如：

- 使用者問「怎麼讓我的 React app 更快？」→ `npx skills find react performance`
- 使用者問「你能幫我做 PR 審查嗎？」→ `npx skills find pr review`
- 使用者問「我需要建立 changelog」→ `npx skills find changelog`

### 步驟 4：推薦前先驗證品質

**不要只根據搜尋結果就推薦技能。** 一定要驗證：

1. **安裝數** — 優先選擇安裝數 1K 以上的技能，低於 100 的要謹慎。
2. **來源信譽** — 官方來源（`vercel-labs`、`anthropics`、`microsoft`）比不知名作者更可信。
3. **GitHub 星數** — 查看來源儲存庫。星數低於 100 的 repo 所提供的技能應抱持懷疑。

### 步驟 5：向使用者呈現選項

找到相關技能時，向使用者呈現：

1. 技能名稱與功能
2. 安裝數與來源
3. 可以執行的安裝指令
4. 到 skills.sh 了解更多的連結

回覆範例：

{{CODE:2}}

### 步驟 6：主動提議安裝

如果使用者想繼續，你可以幫他們安裝：

{{CODE:3}}

`-g` 旗標代表全域（使用者層級）安裝，`-y` 則略過確認提示。

## 常見技能類別

搜尋時可參考以下常見類別：

| 類別       | 搜尋關鍵字範例                           |
| ---------- | ---------------------------------------- |
| 網頁開發   | react, nextjs, typescript, css, tailwind |
| 測試       | testing, jest, playwright, e2e           |
| DevOps     | deploy, docker, kubernetes, ci-cd        |
| 文件       | docs, readme, changelog, api-docs        |
| 程式碼品質 | review, lint, refactor, best-practices   |
| 設計       | ui, ux, design-system, accessibility     |
| 生產力     | workflow, automation, git                |

## 有效搜尋的技巧

1. **使用具體關鍵字**：「react testing」比單純「testing」好
2. **嘗試替代詞彙**：如果「deploy」找不到，試試「deployment」或「ci-cd」
3. **查看熱門來源**：許多技能來自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 找不到技能時

如果沒有相關技能：

1. 承認沒有找到現成的技能
2. 主動提議直接用你的通用能力協助完成任務
3. 建議使用者可以用 `npx skills init` 建立自己的技能

範例：

{{CODE:4}}
