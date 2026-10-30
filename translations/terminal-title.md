<!--meta
{"title":"終端機視窗標題","category":"AI 整合與開發工具","tags":["終端機","Claude Code","Codex","多工"],
"summary":"自動把終端機視窗標題改成目前的高層任務（例如「my-project | Fix: Login Bug」），讓同時開好幾個 Claude Code 或 Codex 終端機的人一眼看出每個視窗在做什麼。只在新工作階段開始或切換到明顯不同的任務時更新；提供 macOS／Linux 的 shell 腳本與 Windows 的 PowerShell 腳本，也可改用 UserPromptSubmit hook 以確定性方式設定。",
"usage":"- 安裝後會在每個新工作階段的第一個提示時自動設定標題，不需要你做什麼\n- 標題最多 40 字元，會自動加上目前資料夾名稱作前綴\n- 想加自訂前綴可設定環境變數 `CLAUDE_TITLE_PREFIX`（或 `CODEX_TITLE_PREFIX`）\n- Windows 原生環境要用 `set_title.ps1`，不能用 `.sh`"}
-->
---
name: terminal-title
description: 自動更新終端機視窗標題，以反映目前的高層任務。在每個 Claude Code 或 Codex 工作階段開始、使用者提供第一個提示時使用，以及每當使用者切換到明顯不同的新高層任務時使用。透過清楚、一目了然地標示每個終端機正在做什麼，幫助開發者管理多個 Claude Code 或 Codex 終端機。
metadata:
  version: "1.4.0"
---

# 終端機標題

## 概覽

依 Claude 正在處理的任務，設定具描述性的終端機視窗標題。對同時執行多個 Claude Code 實例、需要辨識哪個終端機在處理哪個任務的開發者來說不可或缺。

## 何時使用

**一律觸發本技能：**
- 在每個新的 Claude Code 或 Codex 工作階段開始時（收到使用者的第一個提示之後）
- 切換到實質上不同的任務時（例如從「API 整合」到「資料庫遷移」）

**在像這樣的任務切換時觸發：**
- 從前端工作切換到後端工作
- 從除錯轉到開發新功能
- 從一個模組或元件換到完全不同的另一個
- 開始處理系統的不同部分（例如從認證到金流）

**以下情況「不要」觸發：**
- 關於同一個任務的後續問題（「可以幫那個函式加個註解嗎？」）
- 對目前工作的小幅修正（「改成藍色，不要紅色」）
- 除錯你剛建好的同一個功能
- 釐清問題（「你說的 X 是什麼意思？」）
- 在同一個元件或模組上反覆修改
- 任務中途的狀態更新或進度確認

## 運作方式

1. **擷取任務摘要**：從使用者的提示辨識高層任務
2. **產生標題**：建立簡潔、具描述性的標題（最多 40 個字元）
3. **設定標題**：以產生的標題執行 `set_title.sh`（macOS／Linux）或 `set_title.ps1`（原生 Windows）
4. **不需要確認**：這會在背景默默進行

## 標題格式指引

**好的標題：**
- 「API Integration: Auth Flow」
- 「Fix: Login Bug」
- 「DB Migration: Users Table」
- 「Build: Dashboard UI」
- 「Refactor: Payment Module」

**顯示為（腳本會加上資料夾前綴）：**
- `my-project | API Integration: Auth Flow`
- `my-project | Fix: Login Bug`

**不好的標題：**
- 太長：「Implementing the new authentication system with OAuth2.0 support」
- 太籠統：「Working」或「Coding」
- 太囉嗦：「The user wants me to help them with...」
- 包含系統資訊：「/Users/john/project: Build feature」
- 完整的句子：「I am working on the dashboard component」

**格式模式：**
{{CODE:1}}

讓標題簡潔、以行動為導向，並且一看就認得出來。

## 實作

依主機作業系統選擇腳本。如果不確定，工作目錄的路徑樣式是可靠的線索：`/home/...` 或 `/Users/...` 代表 macOS／Linux（包括 WSL），而 `C:\...` 或 `D:\...` 代表原生 Windows。

### macOS／Linux／WSL

從安裝的技能目錄執行腳本。這裡顯示的是個人安裝路徑；專案安裝時，使用相對於專案根目錄的 `.claude/skills/terminal-title/scripts/set_title.sh`。

{{CODE:2}}

**工作流程範例：**
{{CODE:3}}

### 原生 Windows

在原生 Windows 上「不要」使用 `set_title.sh`：Bash 工具會在跳脫序列到達終端機之前把它去掉，所以什麼都不會改變。改用 PowerShell 腳本。從 Bash 工具（Git Bash）使用這個指令；`-ExecutionPolicy Bypass` 只對這一次呼叫生效，所以在預設的 `Restricted` 政策下也能運作：

{{CODE:4}}

從 PowerShell 工具，等效的寫法是（如果執行政策擋住了，就改用搭配 `$env:USERPROFILE` 的 `powershell.exe -ExecutionPolicy Bypass -File` 形式）：

{{CODE:5}}

專案安裝時，使用相對於專案根目錄的 `.claude/skills/terminal-title/scripts/set_title.ps1`。Codex 會把技能安裝在 `~/.agents/skills` 或 `~/.codex/skills`；用那個根目錄取代 `~/.claude/skills`。

## 腳本細節

`scripts/set_title.sh` 把 OSC 0 跳脫序列寫到控制終端機（`/dev/tty`），沒有連接終端機時退回 stdout。它也會把標題存到 `~/.claude/terminal_title`，讓 shell hook 可以在每次提示後重新套用。它相容於 macOS Terminal.app、iTerm2、Alacritty、Kitty，以及大多數相容 xterm 的終端模擬器（包括 tmux 與 screen）。

`scripts/set_title.ps1` 是 Windows 的對應版本。它透過 `[Console]::Title`（Win32 的 `SetConsoleTitle` API）在繼承的主控台上設定標題，所以不需要讓跳脫序列經過 stdout。它可在 Windows Terminal 與傳統主控台主機中運作，支援 Windows PowerShell 5.1 或 PowerShell 7，並寫入同一個 `~/.claude/terminal_title` 檔案。

兩個腳本都接受一個參數（標題），沒有提供時就默默結束。

## 自動加上目錄前綴

每個標題都會以目前的目錄名稱（通常是 repo 名稱）作為前綴：

{{CODE:6}}

## 選用的自訂前綴

使用者可以透過 `CLAUDE_TITLE_PREFIX` 環境變數加上自訂前綴（或 `CODEX_TITLE_PREFIX`，兩者都設定時以它為準）：

{{CODE:7}}

{{CODE:8}}

這會產生像 `Claude | my-project | Build: Dashboard UI` 這樣的標題。

**注意：** 你不需要檢查這些變數或改變你的行為。腳本會處理。

## 確定性的替代做法

本技能目錄中的 `hooks/set-title-hook.sh`（或原生 Windows 上的 `scripts/set_title.ps1`，在不帶參數呼叫時會從 stdin 讀取 hook 的 JSON）可以接成 Claude Code 的 `UserPromptSubmit` hook。它會從每個提示的第一行設定標題，而不依賴本技能被呼叫。設定片段請見專案的 README。
