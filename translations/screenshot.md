<!--meta
{"title":"系統截圖","category":"瀏覽器與測試自動化","tags":["截圖","桌面應用","macOS","Windows","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：在你明確要求桌面或系統截圖（全螢幕、特定應用程式或視窗、指定像素區域），或工具本身沒有截圖能力時，用作業系統層級的方式截圖。內附 macOS／Linux 的 Python 輔助腳本與 Windows 的 PowerShell 腳本，並處理 macOS 螢幕錄製權限與多螢幕情況。",
"usage":"- Codex：`$skill-installer screenshot`\n- 說「幫我截一張螢幕」「截 Safari 的視窗看看現在長怎樣」「截取左上角 800×600 的區域」\n- 存檔位置：你指定的路徑 → 系統預設截圖位置 → Codex 自己檢查用時存到暫存目錄\n- 瀏覽器或 Figma 有專屬工具時會優先用那些工具"}
-->
---
name: "screenshot"
description: "當使用者明確要求桌面或系統截圖（全螢幕、特定應用程式或視窗，或一個像素區域），或當工具專屬的擷取能力無法使用、需要作業系統層級的擷取時使用。"
---


# 螢幕截圖

每次都遵循這些存檔位置規則：

1) 如果使用者指定了路徑，就存到那裡。
2) 如果使用者要求截圖但沒有指定路徑，就存到作業系統預設的截圖位置。
3) 如果是 Codex 自己需要截圖來檢查，就存到暫存目錄。

## 工具優先順序

- 有工具專屬的截圖能力時優先使用（例如：Figma 檔案用 Figma MCP/技能，瀏覽器與 Electron 應用程式用 Playwright/agent-browser 工具）。
- 在被明確要求、需要整個系統的桌面擷取，或工具專屬的擷取無法取得你需要的東西時，使用本技能。
- 除此之外，對於沒有更整合之擷取工具的桌面應用程式，把本技能視為預設。

## macOS 權限預檢（減少重複的提示）

在 macOS 上，於擷取視窗/應用程式之前先執行一次預檢輔助工具。它會檢查螢幕錄製權限、說明為什麼需要它，並在同一處請求權限。

輔助工具會把 Swift 的模組快取導向 `$TMPDIR/codex-swift-module-cache`，以避免額外的沙箱模組快取提示。

{{CODE:1}}

為了避免多次沙箱核准提示，可能的話把預檢 + 擷取合併成一個指令：

{{CODE:2}}

對於 Codex 的檢查執行，把輸出保留在暫存目錄：

{{CODE:3}}

使用內附的腳本，避免重新推導各作業系統專屬的指令。

## macOS 與 Linux（Python 輔助工具）

從 repo 根目錄執行輔助工具：

{{CODE:4}}

常見模式：

- 預設位置（使用者要求「一張截圖」）：

{{CODE:5}}

- 暫存位置（Codex 視覺檢查）：

{{CODE:6}}

- 明確的位置（使用者提供了路徑或檔名）：

{{CODE:7}}

- 依應用程式名稱擷取應用程式/視窗（僅限 macOS；子字串比對即可；會擷取所有符合的視窗）：

{{CODE:8}}

- 應用程式內特定的視窗標題（僅限 macOS）：

{{CODE:9}}

- 擷取前先列出符合的視窗 id（僅限 macOS）：

{{CODE:10}}

- 像素區域（x,y,w,h）：

{{CODE:11}}

- 焦點/作用中的視窗（只擷取最前面的視窗；使用 `--app` 擷取所有視窗）：

{{CODE:12}}

- 特定的視窗 id（在 macOS 上使用 --list-windows 找出 id）：

{{CODE:13}}

腳本每次擷取會印出一個路徑。當有多個視窗或螢幕符合時，它會印出多個路徑（每行一個），並加上像 `-w<windowId>` 或 `-d<display>` 這樣的後綴。用圖片檢視工具依序檢視每個路徑，只有在需要或被要求時才處理圖片。

### 工作流程範例

- 「看一下 <App> 然後告訴我你看到什麼」：擷取到暫存目錄，然後依序檢視每個印出的路徑。

{{CODE:14}}

- 「Figma 上的設計和實作的不一樣」：先用 Figma MCP/技能擷取設計，然後用本技能擷取執行中的應用程式（通常存到暫存目錄），並在做任何處理之前比較原始截圖。

### 多螢幕行為

- 在 macOS 上，接了多台顯示器時，全螢幕擷取會為每個螢幕各存一個檔案。
- 在 Linux 與 Windows 上，全螢幕擷取使用虛擬桌面（所有顯示器在同一張圖中）；需要時用 `--region` 單獨擷取一個螢幕。

### Linux 的前置條件與選擇邏輯

輔助工具會自動選擇第一個可用的工具：

1) `scrot`
2) `gnome-screenshot`
3) ImageMagick `import`

如果都沒有，請使用者安裝其中之一再重試。

座標區域需要 `scrot` 或 ImageMagick `import`。

`--app`、`--window-name` 與 `--list-windows` 僅限 macOS。在 Linux 上，使用 `--active-window`，或在可用時提供 `--window-id`。

## Windows（PowerShell 輔助工具）

執行 PowerShell 輔助工具：

{{CODE:15}}

常見模式：

- 預設位置：

{{CODE:16}}

- 暫存位置（Codex 視覺檢查）：

{{CODE:17}}

- 明確的路徑：

{{CODE:18}}

- 像素區域（x,y,w,h）：

{{CODE:19}}

- 作用中的視窗（先請使用者讓它取得焦點）：

{{CODE:20}}

- 特定的視窗控制代碼（只在有提供時）：

{{CODE:21}}

## 直接的作業系統指令（備案）

當你無法執行輔助工具時使用這些。

### macOS

- 全螢幕存到特定路徑：

{{CODE:22}}

- 像素區域：

{{CODE:23}}

- 特定的視窗 id：

{{CODE:24}}

- 互動式選取或挑選視窗：

{{CODE:25}}

### Linux

- 全螢幕：

{{CODE:26}}

{{CODE:27}}

{{CODE:28}}

- 像素區域：

{{CODE:29}}

{{CODE:30}}

- 作用中的視窗：

{{CODE:31}}

{{CODE:32}}

## 錯誤處理

- 在 macOS 上，先執行 `bash <path-to-skill>/scripts/ensure_macos_permissions.sh`，在同一處請求螢幕錄製權限。
- 如果在沙箱執行中看到「screen capture checks are blocked in the sandbox」「could not create image from display」或 Swift `ModuleCache` 權限錯誤，就以提升的權限重新執行指令。
- 如果 macOS 的應用程式/視窗擷取沒有符合的結果，執行 `--list-windows --app "AppName"` 並以 `--window-id` 重試，並確認應用程式在螢幕上是可見的。
- 如果 Linux 的區域/視窗擷取失敗，用 `command -v scrot`、`command -v gnome-screenshot` 與 `command -v import` 檢查工具是否可用。
- 如果在沙箱中存到作業系統預設位置時因權限錯誤而失敗，就以提升的權限重新執行指令。
- 一律在回應中回報存檔的路徑。
