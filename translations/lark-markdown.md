<!--meta
{"title": "飛書 Markdown 檔案", "category": "文件與辦公", "tags": ["飛書", "Lark", "Markdown", "雲端空間", "lark-cli"], "summary": "飛書（Lark）官方 CLI 技能：查看、建立、上傳、編輯與比較存在飛書雲端空間中的原生 `.md` 檔，也能把遠端版本與本機草稿做 diff。不負責匯入成線上文件或搬移、權限等雲端空間管理。原文為簡體中文，以 OpenCC 轉為台灣繁體。", "usage": "- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-markdown`（需 `lark-cli` 與 lark-shared）\n- 說「把 notes.md 上傳到飛書雲端」「比較雲端這份 README.md 和我本機的草稿有什麼不同」\n- 通常以 `--as user` 執行；第一次使用前先 `lark-cli auth login`"}
-->
---
name: lark-markdown
version: 1.2.2
description: "飛書 Markdown：檢視、建立、上傳、編輯和比較飛書中的原生 Markdown 檔案。當使用者要操作飛書 Markdown 檔案，或比較其遠端版本及本地草稿時使用。純本地 Markdown 檔案操作不觸發本 skill。不負責將 Markdown 匯入為飛書線上文件，也不負責檔案搜尋、許可權、評論、移動、刪除等雲空間管理操作。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli markdown --help"
---

# markdown (v1)

**CRITICAL — 開始前 MUST 先用 Read 工具讀取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含認證、許可權處理**

## 快速決策

- 身份：Markdown 檔案通常屬於使用者雲空間資源，優先使用 `--as user`。如為自動化場景，或應用已建立並持有目標檔案許可權，可按場景使用 `--as bot`。首次以 `user` 身份訪問前執行 `lark-cli auth login`
- `markdown +create` / `+overwrite` 失敗時，先判斷是不是身份和許可權問題：`bot` 更常見的是 app scope 或目標目錄 ACL，`user` 更常見的是使用者授權或使用者 ACL；不要不加判斷地來回切身份重試。

- 使用者要**上傳、建立一個原生 `.md` 檔案**，使用 `lark-cli markdown +create`
- 使用者要**比較原生 `.md` 檔案的歷史版本差異**，或比較遠端 Markdown 與本地草稿，使用 `lark-cli markdown +diff`
- 使用者要**讀取 Drive 裡某個 `.md` 檔案內容**，使用 `lark-cli markdown +fetch`
- 使用者要對 Markdown 檔案做**區域性文字替換 / 正則替換**，優先使用 `lark-cli markdown +patch`
- 使用者要**覆蓋更新 Drive 裡某個 `.md` 檔案內容**，使用 `lark-cli markdown +overwrite`
- 使用者要先拿 Markdown 檔案的歷史版本號，再做比較/下載/回滾，先用 [`lark-drive`](../lark-drive/SKILL.md) 的 `lark-cli drive +version-history`
- 使用者要把本地 Markdown **匯入成線上新版文件（docx）**，不要用本 skill，改用 [`lark-drive`](../lark-drive/SKILL.md) 的 `lark-cli drive +import --type docx`
- 使用者要對 Markdown 檔案做**rename / move / delete / 搜尋 / 許可權 / 評論**等雲空間（雲盤/雲端儲存）操作，不要留在本 skill，切到 [`lark-drive`](../lark-drive/SKILL.md)
- `markdown +create` / `+overwrite` 命中 `missing scope`、`permission denied`、`not found`、`quota_exceeded`、`version limit` 時，預設停止重試並按報錯 hint 處理；只有 `rate_limit`、`server_error` 或臨時網路錯誤才做有限退避重試。
- `markdown +create` 的目標引數不要猜：Drive 資料夾用 `--folder-token`，Wiki 節點用 `--wiki-token`。如果使用者給的是 URL，可以直接傳完整 URL；CLI 會歸一成 token。不要把 doc/sheet/wiki URL 放進 `--folder-token` 試錯。

## 核心邊界

- 本 skill 處理的是 **Drive 中作為普通檔案儲存的 Markdown**，不是 docx 文件
- `--name` 和本地 `--file` 檔名都必須顯式帶 `.md` 字尾；不滿足時 shortcut 會直接報錯
- `--content` 支援：
  - 直接傳字串
  - `@file` 從本地檔案讀取內容
  - `-` 從 stdin 讀取內容
- `markdown +patch` 的內部語義是：**先完整下載 Markdown，再本地替換，再整檔案覆蓋上傳**
- `markdown +patch` 不是服務端原子 patch；它是 CLI 側編排出來的區域性更新能力
- `markdown +patch` 當前只支援**單組** `--pattern` / `--content`
- `markdown +patch` 替換後的最終內容**不能為空**；CLI 會拒絕上傳空檔案，因為 Drive 不支援零位元組 Markdown，且空檔案通常是誤操作
- `--file` 只接受本地 `.md` 檔案路徑

正則替換時要特別注意 `--pattern` 的轉義：

{{CODE:1}}

## Shortcuts（推薦優先使用）

Shortcut 是對常用操作的高階封裝（`lark-cli markdown +<verb> [flags]`）。有 Shortcut 的操作優先使用。

| Shortcut | 說明 |
|----------|------|
| [`+create`](references/lark-markdown-create.md) | Create a Markdown file in Drive |
| [`+diff`](references/lark-markdown-diff.md) | Compare two remote Markdown versions, or compare remote Markdown against a local file |
| [`+fetch`](references/lark-markdown-fetch.md) | Fetch a Markdown file from Drive |
| [`+patch`](references/lark-markdown-patch.md) | Patch a Markdown file in Drive via fetch-local-replace-overwrite |
| [`+overwrite`](references/lark-markdown-overwrite.md) | Overwrite an existing Markdown file in Drive |

## 參考

- [lark-shared](../lark-shared/SKILL.md) — 認證和全域性引數
- [lark-drive](../lark-drive/SKILL.md) — Drive 檔案管理、匯入 docx、move/delete/search 等
