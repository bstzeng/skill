<!--meta
{"title":"飛書雲文件操作","category":"文件與辦公","tags":["飛書","Lark","雲文件","Wiki","lark-cli"],
"summary":"飛書（Lark）官方 CLI 技能：讀取、建立、編輯飛書雲文件（Docx / Wiki），插入或下載圖片附件、操作畫板與思維筆記。原文為簡體中文，此處轉為繁體。",
"usage":"- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-doc`（需同時安裝 lark-shared 與 `lark-cli`）\n- 貼上飛書文件 URL 並說「幫我摘要這份文件」「在這份文件末尾補一段」\n- 建議所有文件操作加上 `--as user` 以使用者身分執行\n- 搜尋文件、匯入匯出、權限管理請改用 lark-drive"}
-->
---
name: lark-doc
description: "飛書雲文件（Docx / Wiki）內容操作：讀取、建立、編輯文件，插入或下載圖片附件，以及操作思維筆記。使用者提供文件 URL/token（包括 doubao.com 的 /docx/、/wiki/）時使用；依 URL 路徑/token 而非網域來路由；`/page/<token>` 是妙搭應用，不是飛書雲文件。文件內嵌資源依讀取參考中的統一規則分流。獨立的評論操作走 lark-drive；隨正文讀取評論使用 docs +fetch。表格或 Base 內部的資料操作不在本 skill 範圍。"
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-shared"]
  cliHelp: "lark-cli docs --help;lark-cli mindnotes --help"
---

# docs

## 情境與 Shortcut 路由

**CRITICAL：先判斷情境，再讀取該情境的參考檔案；不要在任務一開始就一次讀取全部參考檔案。每個檔案只在第一次進入對應階段時讀取一次。**

**身分：文件操作建議明確指定 `--as user`。**

**本機檔案引用一律遵循檔案存取權限：CWD 內優先使用 `@./相對路徑`，其他目錄使用 `@絕對路徑`。XML 內的相對資源路徑先查 CWD；只有檔案不存在時才查來源 XML 檔所在目錄，同名檔案以 CWD 為準。內嵌內容、stdin、線上文件沒有來源檔目錄，不執行回退。**

### 文件內容

- **讀取 / 摘要 — [`+fetch`](references/lark-doc-fetch.md)**：先讀參考再取得文件。
- **從零創作 — [`建立工作流`](references/lark-doc-create-workflow.md)**：先完整執行建立工作流，**簡單任務不是跳過的理由**；
- **匯入 / 空白文件 — [`+create`](references/lark-doc-create.md)**：只有在建立空白文件或原樣匯入使用者提供的完整內容時，才跳過建立工作流。
- **編輯 / block 直達連結 — [`+update`](references/lark-doc-update.md)**：語意改寫、潤飾、重組、補寫或排版都依 update 參考完成。

### 輔助能力

- **草稿初始化、解析與統計 — [`+script`](references/lark-doc-script.md)**：支援解析文件 URL / token 與本機 XML，統計字數並回傳字元診斷；不支援 Markdown 輸入。
- **歷史版本 — [`+history-list` / `+history-revert` / `+history-revert-status`](references/lark-doc-history.md)**：查詢、回復文件歷史版本，或檢查回復任務狀態。

### 資源、畫板與思維筆記

- **插入本機素材 — [`+media-insert`](references/lark-doc-media-insert.md)**：在文末插入本機圖片或檔案。
- **預覽素材 — [`+media-preview`](references/lark-doc-media-preview.md)**：預覽文件或評論中的圖片、附件或素材。
- **下載素材 — [`+media-download`](references/lark-doc-media-download.md)**：下載文件中的圖片、附件、素材或畫板縮圖。
- **Docx 封面 — [`+resource-download` / `+resource-update` / `+resource-delete`](references/lark-doc-resource-cover.md)**：下載、更新或刪除 Docx 封面。
- **畫板 — [`畫板工作流`](references/lark-doc-whiteboard.md)**：建立或更新畫板時先讀取工作流；更新既有畫板必須重用現有 token，禁止新建空白畫板；使用 [`whiteboard +update`](../lark-whiteboard/references/lark-whiteboard-update.md) 寫入。
- **思維筆記 — `mindnotes`**：既有思維筆記走 [`思維筆記流程`](references/lark-doc-mindnote.md)；新建思維筆記走 [`lark-doc-whiteboard`](references/lark-doc-whiteboard.md)。

### 認證與 Scope

執行 Shortcut 時，不預先讀取 [`lark-shared`](../lark-shared/SKILL.md) 或預先執行 `auth status --verify`；只有遇到未認證、token / 身分或 scope 錯誤時才讀取該 Skill，修復後重試。認證、身分或 scope 管理的請求則直接使用該 Skill。

## 不在本 Skill 範圍

- **Drive 檔案層級操作**：找文件、匯入匯出、雲端空間檔案上傳 / 下載 / 權限管理 → [`lark-drive`](../lark-drive/SKILL.md)。複製文件、建立副本或另存為副本時，依其指引使用 `lark-cli drive files copy`；不要用 `docs +fetch` + `docs +create` 重建正文。
- **獨立評論操作**：新增、分頁檢視、回覆評論或增刪 reaction → [`lark-drive`](../lark-drive/SKILL.md)；只需要精簡的評論脈絡時，直接使用預設 JSON 回應的 `docs +fetch`。
