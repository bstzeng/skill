<!--meta
{"title":"Web 應用測試","category":"瀏覽器與測試自動化","tags":["Playwright","E2E 測試","Python","截圖","Anthropic 官方"],
"summary":"Anthropic 官方技能：用 Python Playwright 腳本測試本機網頁應用，內附可同時啟動前後端伺服器的輔助腳本，支援驗證前端功能、除錯 UI、截圖與讀取瀏覽器 console 日誌。",
"usage":"- Claude Code：`/plugin marketplace add anthropics/skills` 後安裝 example-skills\n- 或 `npx skills add https://github.com/anthropics/skills --skill webapp-testing`\n- 說「幫我測試 localhost:5173 的登入流程並截圖」\n- 代理會先用 `with_server.py --help` 了解用法，以「先偵察 DOM、再執行動作」的模式撰寫腳本"}
-->
---
name: webapp-testing
description: 使用 Playwright 與本機網頁應用程式互動並進行測試的工具組。支援驗證前端功能、除錯 UI 行為、擷取瀏覽器截圖，以及檢視瀏覽器日誌。
license: 完整條款見 LICENSE.txt
---

# 網頁應用程式測試

要測試本機網頁應用程式，請撰寫原生的 Python Playwright 腳本。

**可用的輔助腳本**：
- `scripts/with_server.py` — 管理伺服器生命週期（支援多個伺服器）

**一律先以 `--help` 執行腳本**查看用法。在你先試著執行腳本、並發現確實絕對需要客製化方案之前，**不要**閱讀原始碼。這些腳本可能非常大，會汙染你的上下文視窗。它們的存在是為了被當成黑盒腳本直接呼叫，而不是被讀進你的上下文視窗。

## 決策樹：選擇你的做法

{{CODE:1}}

## 範例：使用 with_server.py

要啟動伺服器，先執行 `--help`，再使用輔助腳本：

**單一伺服器：**
{{CODE:2}}

**多個伺服器（例如後端＋前端）：**
{{CODE:3}}

建立自動化腳本時，只需包含 Playwright 邏輯（伺服器會自動管理）：
{{CODE:4}}

## 先偵察、再行動的模式

1. **檢查渲染後的 DOM**：
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. 從檢查結果中**找出選擇器**

3. 使用找到的選擇器**執行動作**

## 常見陷阱

❌ **不要**在動態應用程式上，還沒等到 `networkidle` 就檢查 DOM
✅ **要**先等待 `page.wait_for_load_state('networkidle')` 再檢查

## 最佳實踐

- **把內附腳本當黑盒使用** — 要完成任務時，先考慮 `scripts/` 中是否有腳本可以幫忙。這些腳本能可靠地處理常見的複雜流程，又不會塞滿上下文視窗。用 `--help` 查看用法，然後直接呼叫。
- 同步腳本使用 `sync_playwright()`
- 完成後一律關閉瀏覽器
- 使用具描述性的選擇器：`text=`、`role=`、CSS 選擇器或 ID
- 加入適當的等待：`page.wait_for_selector()` 或 `page.wait_for_timeout()`

## 參考檔案

- **examples/** — 展示常見模式的範例：
  - `element_discovery.py` — 找出頁面上的按鈕、連結與輸入框
  - `static_html_automation.py` — 對本機 HTML 使用 file:// URL
  - `console_logging.py` — 在自動化過程中擷取 console 日誌
