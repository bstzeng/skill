<!--meta
{"title": "飛書 OKR", "category": "文件與辦公", "tags": ["飛書", "Lark", "OKR", "目標管理", "lark-cli"], "summary": "飛書（Lark）官方 CLI 技能：查看與編輯 OKR 週期、目標、關鍵結果、對齊關係、量化指標與進展紀錄。待辦任務、行程與績效評估不在範圍內。原文為簡體中文，以 OpenCC 轉為台灣繁體。", "usage": "- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-okr`（需 `lark-cli` 與 lark-shared）\n- 說「列出我這一季的 OKR」「在目標 2 下新增一個關鍵結果」「我的目標對齊到誰？」\n- 預設以 `--as user` 查看自己或上下級的 OKR；以 `--as bot` 查看他人需要相應權限"}
-->
---
name: lark-okr
version: 1.0.0
description: "飛書 OKR：管理目標與關鍵結果。檢視和編輯 OKR 週期、目標、關鍵結果、對齊關係、量化指標和進展記錄。當使用者需要檢視或建立 OKR、管理目標和關鍵結果、檢視對齊關係時使用。不負責：待辦任務管理（lark-task）、日程/會議安排（lark-calendar）、績效評估"
metadata:
  requires:
    bins: [ "lark-cli" ]
  cliHelp: "lark-cli okr --help"
---

# okr (v2)

**CRITICAL — 開始前 MUST 先用 Read 工具讀取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含認證、許可權處理**

**身份**：OKR 操作預設使用 `--as user`（檢視當前使用者/上下級的 OKR 時）。也支援 `--as bot` 檢視他人 OKR（需相應許可權）。

## 快速決策

| 使用者需求                     | 操作路徑                                                                                                                | 參考文件                                                                                                                                                                                                             |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 檢視自己/他人的 OKR          | 獲取使用者 ID -> `+cycle-list` -> `+cycle-detail` -> 按需查指標/進展記錄                                                  | [`cycle-list`](references/lark-okr-cycle-list.md), [`cycle-detail`](references/lark-okr-cycle-detail.md), [`indicators`](references/lark-okr-indicators.md), [`progress-list`](references/lark-okr-progress-list.md) |
| 為自己寫一組 OKR             | 優先用 `+batch-create` 建立 Objective/KR 骨架                                                                           | [`batch-create`](references/lark-okr-batch-create.md), [`contentblock`](references/lark-okr-contentblock.md)                                                                                                         |
| 只新增一條 O 或單條 KR       | 用 `+create`                                                                                                            | [`create`](references/lark-okr-create.md)                                                                                                                                                                            |
| 編輯內容/備註/截止時間       | 用 `+patch`                                                                                                             | [`patch`](references/lark-okr-patch.md)                                                                                                                                                                              |
| 修改 OKR 分數                | 只有使用者明確說“分數”“評分”“打分”“score”時才用 `+patch --score`；分數不是進度/完成度                                     | [`patch`](references/lark-okr-patch.md)                                                                                                                                                                              |
| 調整順序或權重               | 用 `+reorder` / `+weight`                                                                                               | [`reorder`](references/lark-okr-reorder.md), [`weight`](references/lark-okr-weight.md)                                                                                                                               |
| 更新數字進度/完成度          | 百分比或不帶單位數字用 `+indicator-update`；需要改單位/目標值時查指標後用 `indicators patch`                            | [`indicator-update`](references/lark-okr-indicator-update.md), [`indicators`](references/lark-okr-indicators.md)                                                                                                     |
| 寫文字進展                   | 用 `+progress-create`；如果文字和數字都有，百分比或預設單位可使用 `--progress-percent` 統一改，非百分比單位更新量化指標 | [`progress-create`](references/lark-okr-progress-create.md), [`progress-list`](references/lark-okr-progress-list.md), [`progress-update`](references/lark-okr-progress-update.md)                                    |
| 對齊目標                     | 直接按對齊關係工作流處理                                                                                                | [`alignments`](references/lark-okr-alignments.md)                                                                                                                                                                    |
| 查詢/建立/修改/解決 OKR 評論 | 獲取週期下全部評論聚合用 `+comment-detail`，查詢單個 O/KR/進展或僅查詢週期全域性評論用 `+comment-list`；                | [`comment`](references/lark-okr-comment-list.md), [`comment-create`](references/lark-okr-comment-create.md), [`comment-solve-reopen`](references/lark-okr-comment-solve-reopen.md)                                   |

分類只在使用者明確要求分類，或建立 Objective 返回 `invalid parameters` 且懷疑租戶強制開啟分類時處理：用 `lark-cli okr categories list --params '{"owner_type":"user","page_size":100}' --as user` 查可用分類，選擇語義合適且`enabled=true` 的分類 ID；分類可後續調整，不必停下等待使用者確認。

獲取當前使用者用 `contact +get-user`；按姓名/郵箱查他人用 `contact +search-user`，拿到 `open_id` 後再查 OKR。

{{CODE:1}}

最常用 OKR 命令示例：

{{CODE:2}}

分數和進度不要混用：使用者說“進度”“完成度”“當前做到 75%”時，通常是在改量化指標或寫進展記錄，不是在改 `score`。只有明確要求修改 OKR 分數/評分/打分時，才使用 [`+patch --score`](references/lark-okr-patch.md)；`score` 取值是 0-1，最多一位小數。

進度判斷規則：使用者說“進度”“完成度”時，先判斷是否是量化數字。數字進度通常對應量化指標；不可量化文字對應進展記錄。需要修改指標單位時看 [`lark-okr-indicators.md`](references/lark-okr-indicators.md)

## Shortcuts（推薦優先使用）

Shortcut 是對常用操作的高階封裝（`lark-cli okr +<verb> [flags]`）。有 Shortcut 的操作優先使用。

| Shortcut                                                         | 說明                                                                                                          |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| [`+cycle-list`](references/lark-okr-cycle-list.md)               | 分頁獲取特定使用者的 OKR 週期列表，可以用 `--time-range` 對當前頁後置篩選                                       |
| [`+cycle-detail`](references/lark-okr-cycle-detail.md)           | 獲取特定 OKR 中所有目標和關鍵結果的內容                                                                       |
| [`+create`](references/lark-okr-create.md)                       | 建立單個 Objective（可帶備註），或向已有 Objective 新增 KR                                                    |
| [`+progress-list`](references/lark-okr-progress-list.md)         | 分頁獲取目標或關鍵結果的進展記錄列表                                                                          |
| [`+progress-get`](references/lark-okr-progress-get.md)           | 根據 ID 獲取單條 OKR 進展記錄                                                                                 |
| [`+progress-create`](references/lark-okr-progress-create.md)     | 為目標或關鍵結果建立進展記錄                                                                                  |
| [`+progress-update`](references/lark-okr-progress-update.md)     | 更新指定 ID 的進展記錄內容                                                                                    |
| [`+progress-delete`](references/lark-okr-progress-delete.md)     | 刪除指定 ID 的進展記錄（不可恢復）                                                                            |
| [`+upload-image`](references/lark-okr-image-upload.md)           | 上傳圖片用於 OKR 進展記錄的富文字內容                                                                         |
| [`+batch-create`](references/lark-okr-batch-create.md)           | 批次建立 Objective（可帶備註）和 KR                                                                           |
| [`+reorder`](references/lark-okr-reorder.md)                     | 調整 Objective 或 KR 的順位                                                                                   |
| [`+weight`](references/lark-okr-weight.md)                       | 調整 Objective 或 KR 的權重                                                                                   |
| [`+indicator-update`](references/lark-okr-indicator-update.md)   | 更新 Objective 或 KR 的當前進度指標。更復雜的量化指標操作見 [量化指標管理](references/lark-okr-indicators.md) |
| [`+patch`](references/lark-okr-patch.md)                         | 部分更新 Objective 或 KR（content、notes、score、deadline）                                                   |
| [`+comment-detail`](references/lark-okr-comment-detail.md)       | 獲取週期下 Cycle/Objective/KeyResult/Progress 的全部評論                                                      |
| [`+comment-list`](references/lark-okr-comment-list.md)           | 分頁獲取單個 OKR 實體下的評論                                                                                 |
| [`+comment-get`](references/lark-okr-comment-get.md)             | 獲取單條評論詳情                                                                                              |
| [`+comment-create`](references/lark-okr-comment-create.md)       | 建立新評論或回覆已有評論(僅支援 --as user)                                                                    |
| [`+comment-patch`](references/lark-okr-comment-patch.md)         | 修改評論內容(僅支援 --as user)                                                                                |
| [`+comment-delete`](references/lark-okr-comment-delete.md)       | 永久刪除單條評論(僅支援 --as user)                                                                            |
| [`+comment-solve`](references/lark-okr-comment-solve-reopen.md)  | 解決評論或劃詞評論串(僅支援 --as user)                                                                        |
| [`+comment-reopen`](references/lark-okr-comment-solve-reopen.md) | 重新開啟評論或劃詞評論串(僅支援 --as user)                                                                    |

### 建立場景選擇

- **單條建立優先用 [`+create`](references/lark-okr-create.md)**：適合建立一個 Objective，或給已有 Objective 增加一個 KR。
- **批次建立用 [`+batch-create`](references/lark-okr-batch-create.md)**：適合一次建立多個 Objective，並可同時附帶多個 KR。
- 如果你只需要修改已有 Objective / KR 的內容、備註、分數或截止時間，使用 [`+patch`](references/lark-okr-patch.md)。

## 格式說明

- [`OKR 業務實體`](references/lark-okr-entities.md) 獲取 OKR 實體結構，定義和關係，幫助你更好的使用 OKR 功能
- [`ContentBlock 富文字格式`](references/lark-okr-contentblock.md) — Objective/KeyResult/Progress 中 Content/Note
  欄位使用的富文字格式說明，以及簡化的半純文字（SemiPlainContent）格式的進一步說明。
- **強烈建議** 在操作 OKR 前，閱讀[`OKR 業務實體`](references/lark-okr-entities.md)以瞭解基礎概念

## API Resources

### alignments

- `delete` — 刪除對齊關係
- `get` — 獲取對齊關係

> **操作指南：** [OKR 對齊關係管理](references/lark-okr-alignments.md) 包含 list/create/delete 完整工作流

### categories

- `list` — 批次獲取分類

### cycles

- `list` — 批次獲取使用者週期

### cycle.objectives

- `list` — 批次獲取使用者週期下的目標

### indicators

- `patch` — 更新量化指標

> **操作指南：** [OKR 量化指標管理](references/lark-okr-indicators.md) 包含目標/KR 指標查詢和 patch 更新完整工作流

### key_results

- `delete` — 刪除關鍵結果
- `get` — 獲取關鍵結果
- `patch` — 更新關鍵結果

### key_result.indicators

- `list` — 獲取關鍵結果的量化指標

> **操作指南：** [OKR 量化指標管理](references/lark-okr-indicators.md)

### objectives

- `delete` — 刪除目標
- `get` — 獲取目標
- `key_results_position` — 更新全部關鍵結果的位置
    - 請求中必須攜帶對應週期下全部關鍵結果的 ID，否則會引數校驗失敗。以傳入的關鍵結果ID順序重新排列關鍵結果。
- `key_results_weight` — 更新全部關鍵結果的權重
    - 類似 `objectives_weight`, 請求中必須同時修改對應目標下全部關鍵結果的權重，且所有權重值的和必須等於 1 ，否則會引數校驗失敗。
- `patch` — 更新目標

### objective.alignments

- `create` — 建立對齊關係
    - 對齊不允許對齊自己的目標，且發起對齊的目標和被對齊的目標所在週期時間上必須有重疊，否則會引數校驗失敗。
- `list` — 批次獲取目標下的對齊關係

### objective.indicators

- `list` — 獲取目標的量化指標

### objective.key_results

- `list` — 批次獲取目標下的關鍵結果

## 不在本 skill 範圍

- 待辦任務管理 → 使用 [`lark-task`](../lark-task/SKILL.md)
- 日程安排 → 使用 [`lark-calendar`](../lark-calendar/SKILL.md)
- 績效評估 → 使用 [`lark-openapi-explorer`](../lark-openapi-explorer/SKILL.md) 查詢原生介面


