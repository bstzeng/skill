<!--meta
{"title":"結構化程式碼搜尋（ast-grep）","category":"程式品質與除錯","tags":["ast-grep","程式搜尋","重構","AST","claude-mods"],
"summary":"用 ast-grep 依抽象語法樹（AST）結構搜尋程式碼，找出函式呼叫、import、類別定義等語意模式，而不是靠正規表示式比對文字。內附模式語法（$NAME、$_、$$$）、十個最常用的模式、指令速查（指定語言、預覽／套用取代、JSON 輸出、計數、YAML 規則），以及 JS/TS、Python、Go/Rust 與安全漏洞的模式參考。",
"usage":"- 先安裝：`brew install ast-grep` 或 `cargo install ast-grep`\n- 說「找出所有呼叫 fetchUser 的地方」「把這個 API 的用法全部改掉」\n- 基本用法：`sg -p 'console.log($_)'`；取代預覽：`sg -p '舊' -r '新'`\n- 正規表示式容易誤判、或要做大規模重構時特別好用"}
-->
---
name: structural-search
description: "使用 ast-grep 依 AST 結構搜尋程式碼。找出像函式呼叫、import、類別定義這類語意模式，而不是文字模式。觸發於：找出所有對 X 的呼叫、搜尋模式、重構用法、找出函式在哪裡被使用、結構化搜尋、ast-grep、sg。"
license: MIT
compatibility: "需要 ast-grep（sg）CLI 工具。安裝：brew install ast-grep（macOS）或 cargo install ast-grep（跨平台）。"
allowed-tools: "Bash"
metadata:
  author: claude-mods
---

# 結構化搜尋

依程式碼的抽象語法樹（AST）結構來搜尋。找出正規表示式無法可靠比對的語意模式。

## 工具

| 工具 | 指令 | 用途 |
|------|---------|---------|
| ast-grep | `sg -p 'pattern'` | 理解 AST 的程式碼搜尋 |

## 模式語法

| 模式 | 比對 | 範例 |
|---------|---------|---------|
| `$NAME` | 具名的識別字 | `function $NAME() {}` |
| `$_` | 任意單一節點 | `console.log($_)` |
| `$$$` | 零個或多個節點 | `function $_($$$) {}` |

## 十大必備模式

{{CODE:1}}

## 速查

| 任務 | 指令 |
|------|---------|
| 尋找模式 | `sg -p 'pattern'` |
| 指定語言 | `sg -p 'pattern' --lang python` |
| 取代（預覽） | `sg -p 'old' -r 'new'` |
| 取代（套用） | `sg -p 'old' -r 'new' --rewrite` |
| 顯示上下文 | `sg -p 'pattern' -A 3` |
| JSON 輸出 | `sg -p 'pattern' --json` |
| 只列檔案 | `sg -p 'pattern' -l` |
| 計算符合數 | `sg -p 'pattern' --count` |
| 執行 YAML 規則 | `sg scan` |

## 何時使用

- 找出某個函式／方法的所有用法
- 定位特定的程式碼模式（hooks、API 呼叫）
- 為大規模重構做準備
- 當正規表示式會比對到誤報時
- 偵測反模式與安全問題
- 建立自訂的 lint 規則

## 其他資源

完整的模式請載入：
- `./references/js-ts-patterns.md` —— JavaScript/TypeScript 模式
- `./references/python-patterns.md` —— Python 模式
- `./references/go-rust-patterns.md` —— Go 與 Rust 模式
- `./references/security-patterns.md` —— 安全漏洞偵測
- `./references/advanced-usage.md` —— YAML 規則與工具整合
- `./assets/rule-template.yaml` —— 自訂規則的起始範本
