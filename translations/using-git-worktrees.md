<!--meta
{"title":"Git Worktree 隔離工作區","category":"雲端與 DevOps","tags":["Git","worktree","隔離環境","Superpowers"],
"summary":"開始新功能或執行實作計畫前，確保工作在隔離的工作區進行：先偵測是否已在 worktree 中，優先使用平台原生的 worktree 工具，沒有才退回手動 `git worktree add`，並確認目錄已被 gitignore、依賴已安裝、基準測試全綠。",
"usage":"- Claude Code：`/plugin marketplace add obra/superpowers-marketplace` 安裝 superpowers\n- 或 `npx skills add https://github.com/obra/superpowers --skill using-git-worktrees`\n- 說「開一個隔離的工作區來做這個功能」；代理會先徵求你同意，預設建立在 `.worktrees/`\n- 常與 writing-plans、executing-plans 搭配使用"}
-->
---
name: using-git-worktrees
description: 在開始需要與目前工作區隔離的功能開發時，或在執行實作計畫之前使用——透過原生工具或以 git worktree 作為備案，確保存在一個隔離的工作區
---

# 使用 Git Worktree

## 概述

確保工作在隔離的工作區中進行。優先使用你所在平台的原生 worktree 工具。只有在沒有原生工具時，才退回手動的 git worktree。

**核心原則：** 先偵測既有的隔離。然後使用原生工具。再退回 git。絕不和主控程式（harness）對著幹。

**開始時宣告：**「我正在使用 using-git-worktrees 技能來建立隔離的工作區。」

## 步驟 0：偵測既有的隔離

**在建立任何東西之前，先檢查你是否已經在隔離的工作區中。**

{{CODE:1}}

**子模組防護：** 在 git 子模組內，`GIT_DIR != GIT_COMMON` 也會成立。在下結論「已經在 worktree 中」之前，先確認你不在子模組裡：

{{CODE:2}}

**如果 `GIT_DIR != GIT_COMMON`（且不是子模組）：** 你已經在一個連結的 worktree 中。直接跳到步驟 2（專案設定）。**不要**再建立另一個 worktree。

連同分支狀態一起回報：
- 在某個分支上：「已在 `<path>` 的隔離工作區中，分支為 `<name>`。」
- 分離的 HEAD：「已在 `<path>` 的隔離工作區中（分離的 HEAD，由外部管理）。完成時需要建立分支。」

**如果 `GIT_DIR == GIT_COMMON`（或在子模組中）：** 你在一般的 repo checkout 中。

使用者是否已在你的指示中表明他們對 worktree 的偏好？如果沒有，在建立 worktree 之前先徵求同意：

> 「要不要我建立一個隔離的 worktree？它能保護你目前的分支不受變更影響。」

尊重任何已宣告的偏好，不必再問。如果使用者不同意，就在原地工作並跳到步驟 2。

## 步驟 1：建立隔離的工作區

**你有兩種機制。依此順序嘗試。**

### 1a. 原生 Worktree 工具（優先）

使用者已要求隔離的工作區（步驟 0 的同意）。你是否已經有建立 worktree 的方法？可能是名為 `EnterWorktree`、`WorktreeCreate` 的工具、`/worktree` 指令，或 `--worktree` 旗標。如果有，就使用它並跳到步驟 2。

原生工具會自動處理目錄位置、分支建立與清理。在有原生工具的情況下使用 `git worktree add`，會產生你的主控程式看不到也無法管理的幽靈狀態。

只有在沒有原生 worktree 工具可用時，才進行步驟 1b。

### 1b. Git Worktree 備案

**只有在步驟 1a 不適用時才使用**——也就是你沒有可用的原生 worktree 工具。用 git 手動建立 worktree。

#### 選擇目錄

依此優先順序。使用者明確的偏好永遠勝過觀察到的檔案系統狀態。

1. **檢查你的指示中是否有已宣告的 worktree 目錄偏好。** 如果使用者已經指定，就直接使用，不必詢問。

2. **檢查是否已有專案本地的 worktree 目錄：**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   如果找到就使用。如果兩者都存在，`.worktrees` 優先。

3. **如果沒有其他指引可用**，預設使用專案根目錄的 `.worktrees/`。

#### 安全驗證（僅限專案本地目錄）

**建立 worktree 之前「必須」確認目錄已被忽略：**

{{CODE:3}}

**如果「沒有」被忽略：** 加入 .gitignore、commit 這項變更，然後再繼續。

**為什麼這很關鍵：** 防止不小心把 worktree 的內容 commit 進 repo。

#### 建立 Worktree

{{CODE:4}}

**沙箱備案：** 如果 `git worktree add` 因權限錯誤（沙箱拒絕）而失敗，告訴使用者沙箱阻擋了 worktree 的建立，你改在目前目錄中工作。然後在原地執行設定與基準測試。

## 步驟 2：專案設定

自動偵測並執行適當的設定：

{{CODE:5}}

## 步驟 3：驗證乾淨的基準

執行測試以確保工作區一開始是乾淨的：

{{CODE:6}}

**如果測試失敗：** 回報失敗，並詢問要繼續還是先調查。

**如果測試通過：** 回報已就緒。

### 回報

{{CODE:7}}

## 快速參考

| 情況 | 動作 |
|------|------|
| 已在連結的 worktree 中 | 略過建立（步驟 0） |
| 在子模組中 | 視為一般 repo（步驟 0 防護） |
| 有原生 worktree 工具 | 使用它（步驟 1a） |
| 沒有原生工具 | Git worktree 備案（步驟 1b） |
| `.worktrees/` 存在 | 使用它（確認已忽略） |
| `worktrees/` 存在 | 使用它（確認已忽略） |
| 兩者都存在 | 使用 `.worktrees/` |
| 兩者都不存在 | 檢查指示檔，然後預設 `.worktrees/` |
| 目錄未被忽略 | 加入 .gitignore + commit |
| 建立時權限錯誤 | 沙箱備案，在原地工作 |
| 基準測試失敗 | 回報失敗 + 詢問 |
| 沒有 package.json/Cargo.toml | 略過相依安裝 |

## 常見的合理化藉口

| 藉口 | 現實 |
|------|------|
| 「我顯然不在 worktree 裡——不需要檢查」 | 執行步驟 0。主控程式建立的隔離與子模組都會騙過肉眼；偵測指令才能定論。 |
| 「`git worktree add` 比找原生工具快」 | 原生工具（例如 `EnterWorktree`）負責位置、分支與清理。繞過它是頭號錯誤——它會產生你的主控程式看不到也無法管理的幽靈狀態。 |
| 「worktree 目錄應該早就被忽略了」 | 執行 `git check-ignore`。沒被忽略的 worktree 目錄會把整棵樹 commit 進 repo。 |
| 「任何目錄名稱都行」 | 明確的指示勝過既有的專案本地目錄，後者又勝過 `.worktrees/` 預設值。 |
| 「工作區是新的——基準測試可以晚點再跑」 | 不乾淨的基準會讓之後的每個失敗都變得模稜兩可。現在就跑測試；是否在失敗的情況下繼續，由你的人類夥伴決定。 |
