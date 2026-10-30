<!--meta
{"title":"Codex 外掛建立器","category":"技能管理","tags":["Codex","外掛","plugin.json","Marketplace","OpenAI Codex"],
"summary":"OpenAI Codex 官方系統技能：為 Codex 建立外掛目錄骨架——必要的 `.codex-plugin/plugin.json`、選用的 skills／hooks／scripts／assets／.mcp.json／.app.json，以及可在發布前編輯的占位值；也能產生或更新 repo 根目錄的 `.agents/plugins/marketplace.json` 條目，控制外掛在 Codex UI 的排序與可用性。",
"usage":"- Codex 內建，不需安裝；說「幫我建立一個新的 Codex 外掛」「把這個外掛加到 marketplace」\n- 尚未說明位置時，代理會先問要建在 repo 內還是家目錄\n- 外掛名稱會自動正規化（`My Plugin` → `my-plugin`）；新條目預設 `AVAILABLE` + `ON_INSTALL`"}
-->
---
name: plugin-creator
description: 為 Codex 建立外掛目錄骨架，包含必要的 `.codex-plugin/plugin.json`、選用的外掛資料夾/檔案，以及可在發布或測試前編輯的基本占位值。當 Codex 需要建立新的本機外掛、加入選用的外掛結構，或產生或更新 repo 根目錄的 `.agents/plugins/marketplace.json` 條目（用於外掛排序與可用性中繼資料）時使用。
---

# 外掛建立器

## 快速開始

1. 執行骨架腳本：

{{CODE:1}}

2. 開啟 `<plugin-path>/.codex-plugin/plugin.json`，替換 `[TODO: ...]` 占位值。

3. 當外掛應該出現在 Codex UI 的排序中時，產生或更新 repo 的 marketplace 條目：

{{CODE:2}}

對於家目錄本機外掛，把 `<home>` 當作根目錄並使用：

{{CODE:3}}

4. 視需要產生/調整選用的附屬資料夾：

{{CODE:4}}

`<parent-plugin-directory>` 是外掛資料夾 `<plugin-name>` 將被建立的目錄（例如 `~/code/plugins`）。

## 本技能會建立什麼

- 如果使用者沒有明確指定外掛位置，在產生 marketplace 條目之前，先詢問他們要 repo 本機外掛還是家目錄本機外掛。
- 在 `/<parent-plugin-directory>/<plugin-name>/` 建立外掛根目錄。
- 一律建立 `/<parent-plugin-directory>/<plugin-name>/.codex-plugin/plugin.json`。
- 以完整的 schema 形狀、占位值以及完整的 `interface` 區段填入清單檔。
- 設定 `--with-marketplace` 時，建立或更新 `<repo-root>/.agents/plugins/marketplace.json`。
  - 如果 marketplace 檔還不存在，在加入第一個外掛條目之前，先填入頂層的 `name` 以及 `interface.displayName` 占位值。
- `<plugin-name>` 依 skill-creator 的命名規則正規化：
  - `My Plugin` → `my-plugin`
  - `My--Plugin` → `my-plugin`
  - 底線、空格與標點符號轉換為 `-`
  - 結果為小寫、以連字號分隔，連續的連字號會合併
- 支援選擇性建立：
  - `skills/`
  - `hooks/`
  - `scripts/`
  - `assets/`
  - `.mcp.json`
  - `.app.json`

## Marketplace 工作流程

- `marketplace.json` 永遠位於 `<repo-root>/.agents/plugins/marketplace.json`。
- 對於家目錄本機外掛，以 `<home>` 為根目錄使用相同的慣例：
  `~/.agents/plugins/marketplace.json` 加上 `./plugins/<plugin-name>`。
- Marketplace 根中繼資料支援頂層 `name` 以及選用的 `interface.displayName`。
- 把 `plugins[]` 中的外掛順序視為 Codex 中的渲染順序。除非使用者明確要求重新排序，否則附加新條目。
- `displayName` 屬於 marketplace 的 `interface` 物件，而不是個別的 `plugins[]` 條目。
- 每個產生的 marketplace 條目都必須包含以下全部：
  - `policy.installation`
  - `policy.authentication`
  - `category`
- 新條目的預設值：
  - `policy.installation: "AVAILABLE"`
  - `policy.authentication: "ON_INSTALL"`
- 只有在使用者明確指定其他允許的值時，才覆寫預設值。
- 允許的 `policy.installation` 值：
  - `NOT_AVAILABLE`
  - `AVAILABLE`
  - `INSTALLED_BY_DEFAULT`
- 允許的 `policy.authentication` 值：
  - `ON_INSTALL`
  - `ON_USE`
- 把 `policy.products` 視為覆寫。除非使用者明確要求依產品限制，否則省略它。
- 產生的外掛條目形狀為：

{{CODE:5}}

- 只有在刻意要取代同名外掛的既有 marketplace 條目時，才使用 `--force`。
- 如果 `<repo-root>/.agents/plugins/marketplace.json` 還不存在，就建立它，包含頂層 `"name"`、含有 `"displayName"` 的 `"interface"` 物件，以及一個 `plugins` 陣列，然後加入新條目。

- 對於全新的 marketplace 檔，根物件應該像這樣：

{{CODE:6}}

## 必要行為

- 外層資料夾名稱與 `plugin.json` 的 `"name"` 永遠是同一個正規化後的外掛名稱。
- 不要移除必要的結構；保持 `.codex-plugin/plugin.json` 存在。
- 在人類或後續步驟明確填入之前，讓清單檔的值保持為占位值。
- 如果是在既有的外掛路徑中建立檔案，只有在刻意覆寫時才使用 `--force`。
- 保留任何既有的 marketplace `interface.displayName`。
- 產生 marketplace 條目時，一律寫入 `policy.installation`、`policy.authentication` 與 `category`，即使它們的值是預設值。
- 只有在使用者明確要求該覆寫時，才加入 `policy.products`。
- 讓 marketplace 的 `source.path` 保持相對於 repo 根目錄，為 `./plugins/<plugin-name>`。

## 確切規格範例的參考

外掛清單檔與 marketplace 條目確切的標準範例 JSON，請使用：

- `references/plugin-json-spec.md`

## 驗證

編輯 `SKILL.md` 之後，執行：

{{CODE:7}}
