<!--meta
{"title":"資安程式碼所有權地圖","category":"資訊安全","tags":["資安","Bus Factor","git 歷史","CODEOWNERS","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：分析 git 歷史，建立「人 ↔ 檔案」的資安所有權拓撲，計算 bus factor 與敏感程式碼（驗證、加密、機密）的所有權風險，找出無人維護的敏感程式碼與熱點，並匯出 CSV/JSON 供 Neo4j、Gephi 等圖形資料庫視覺化。",
"usage":"- Codex：`$skill-installer security-ownership-map`；需要 Python 3 與 `networkx`\n- 只在明確要求資安導向的所有權分析時觸發：「哪些敏感程式碼只有一個人懂？」「拿 CODEOWNERS 跟實際提交紀錄比對」\n- 主要腳本：`scripts/run_ownership_map.py`，查詢用 `scripts/query_ownership.py`\n- 輸出在 `ownership-map-out/`（people.csv、files.csv、edges.csv、summary.json 等）"}
-->
---
name: "security-ownership-map"
description: "分析 git repo 以建立資安所有權拓撲（人對檔案），計算 bus factor 與敏感程式碼的所有權，並匯出 CSV/JSON 供圖形資料庫與視覺化使用。只有在使用者明確想要以 git 歷史為依據、資安導向的所有權或 bus factor 分析時才觸發（例如：無人維護的敏感程式碼、資安維護者、針對風險的 CODEOWNERS 實況檢查、敏感熱點或所有權群集）。一般的維護者清單或非資安的所有權問題不要觸發。"
---

# 資安所有權地圖

## 概述

從 git 歷史建立人與檔案的二部圖，然後計算所有權風險，並匯出供 Neo4j/Gephi 使用的圖形產出物。也建立一張檔案共同變更圖（以共享 commit 計算 Jaccard 相似度），依檔案一起變動的方式為它們分群，同時忽略大型、雜訊多的 commit。

## 需求

- Python 3
- `networkx`（必要；預設啟用社群偵測）

安裝：

{{CODE:1}}

## 工作流程

1. 界定 repo 與時間範圍（選用 `--since/--until`）。
2. 決定敏感度規則（使用預設值或提供 CSV 設定）。
3. 用 `scripts/run_ownership_map.py` 建立所有權地圖（共同變更圖預設開啟；使用 `--cochange-max-files` 忽略超級節點 commit）。
4. 預設會計算社群；graphml 輸出為選用（`--graphml`）。
5. 用 `scripts/query_ownership.py` 查詢輸出，取得有界的 JSON 片段。
6. 保存並視覺化（見 `references/neo4j-import.md`）。

預設情況下，共同變更圖會忽略常見的「黏著」檔案（lockfile、`.github/*`、編輯器設定），讓群集反映實際的程式碼變動，而不是共享的基礎設施修改。用 `--cochange-exclude` 或 `--no-default-cochange-excludes` 覆寫。Dependabot 的 commit 預設被排除；用 `--no-default-author-excludes` 覆寫，或透過 `--author-exclude-regex` 加入模式。

如果你想從共同變更分群中排除像 `Kbuild` 這樣的 Linux 建置黏著檔，傳入：

{{CODE:2}}

## 快速開始

從 repo 根目錄執行：

{{CODE:3}}

預設值：使用作者身分、作者日期，並排除 merge commit。需要時使用 `--identity committer`、`--date-field committer` 或 `--include-merges`。

範例（覆寫共同變更的排除）：

{{CODE:4}}

預設會計算社群。要停用：

{{CODE:5}}

## 敏感度規則

預設情況下，腳本會標記常見的驗證/加密/機密路徑。提供 CSV 檔來覆寫：

{{CODE:6}}

以 `--sensitive-config path/to/sensitive.csv` 使用它。

## 輸出產出物

`ownership-map-out/` 包含：

- `people.csv`（節點：人）
- `files.csv`（節點：檔案）
- `edges.csv`（邊：接觸）
- `cochange_edges.csv`（檔案對檔案的共同變更邊，附 Jaccard 權重；使用 `--no-cochange` 時省略）
- `summary.json`（資安所有權發現）
- `commits.jsonl`（選用，若有 `--emit-commits`）
- `communities.json`（有共同變更邊時預設從中計算；包含每個社群的 `maintainers`；用 `--no-communities` 停用）
- `cochange.graph.json`（含 `community_id` + `community_maintainers` 的 NetworkX node-link JSON；沒有共同變更邊時退回 `ownership.graph.json`）
- `ownership.graphml` / `cochange.graphml`（選用，若有 `--graphml`）

`people.csv` 包含根據作者 commit 時差偵測的時區：`primary_tz_offset`、`primary_tz_minutes` 與 `timezone_offsets`。

## LLM 查詢輔助工具

使用 `scripts/query_ownership.py` 回傳小型、以 JSON 為界的片段，而不必把整張圖載入上下文。

範例：

{{CODE:7}}

使用 `--community-top-owners 5`（預設）控制每個社群儲存多少位維護者。

## 基本資安查詢

執行這些查詢，以有界的輸出回答常見的資安所有權問題：

{{CODE:8}}

注意：
- 接觸預設以一次撰寫的 commit 計（而不是每個檔案）。使用 `--touch-mode file` 以每個檔案計算接觸。
- 使用 `--window-days 90` 或 `--weight recency --half-life-days 180` 來平滑變動量。
- 用 `--ignore-author-regex '(bot|dependabot)'` 過濾機器人。
- 使用 `--min-share 0.1` 只顯示穩定的維護者。
- 使用 `--bucket quarter` 依日曆季度分組。
- 使用 `--identity committer` 或 `--date-field committer` 從作者歸屬改為提交者歸屬。
- 使用 `--include-merges` 納入 merge commit（預設排除）。

### 摘要格式（預設）

使用這個結構，需要時可加欄位：

{{CODE:9}}

## 圖形保存

需要把 CSV 載入 Neo4j 時，使用 `references/neo4j-import.md`。它包含約束條件、匯入的 Cypher 與視覺化訣竅。

## 注意事項

- `summary.json` 中的 `bus_factor_hotspots` 列出 bus factor 低的敏感檔案；`orphaned_sensitive_code` 是其中已無人更新的子集。
- 如果 `git log` 太大，用 `--since` 或 `--until` 縮小範圍。
- 拿 `summary.json` 與 CODEOWNERS 比對，突顯所有權的偏移。
