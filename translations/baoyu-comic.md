<!--meta
{"title":"寶玉知識漫畫","category":"影片與多媒體","tags":["知識漫畫","圖片生成","分鏡","教育","PDF"],
"summary":"建立原創的知識／教育漫畫：分析內容、產生分鏡與角色設定，為每頁寫好提示詞檔案，先產生角色參考表再批次生成各頁圖片，最後合併成 PDF。可組合 6 種畫風（清線、日漫、寫實、水墨、粉筆、極簡）、7 種基調、7 種分格版面，以及歐姆社、武俠、少女、概念故事、四格等預設；依執行環境自動選用 Codex imagegen、Cursor GenerateImage 或 baoyu-image-gen 等圖片後端，絕不用 SVG／HTML 代替點陣圖，也不在生成圖上用程式改字。",
"usage":"- 需要 bun 或 npx；第一次使用會先設定 `EXTEND.md`（浮水印、偏好畫風、語言、圖片後端、批次大小）\n- 說「把圖靈的生平做成知識漫畫」「用歐姆社風格畫一本講資料庫的漫畫」\n- 常用參數：`--art manga --tone warm --layout webtoon --aspect 3:4 --lang zh`\n- 只要分鏡：`--storyboard-only`；只重畫第 3 頁：`--regenerate 3`\n- 輸出在 `comic/<主題>/`，含分鏡、提示詞、各頁圖片與合併 PDF"}
-->
---
name: baoyu-comic
description: 支援多種畫風與基調的知識漫畫創作工具。以詳細的分格版面與可批次的圖片生成，建立原創的教育漫畫。當使用者要求製作「知識漫畫」「教育漫畫」「傳記漫畫」「教學漫畫」或「Logicomix 風格漫畫」時使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-comic
    requires:
      anyBins:
        - bun
        - npx
---

# 知識漫畫創作

以彈性的「畫風 × 基調」組合，建立原創的知識漫畫。

## 使用者輸入工具

當本技能需要詢問使用者時，遵循這條工具選擇規則（依優先順序）：

1. **偏好目前代理執行環境提供的內建使用者輸入工具**——例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何同等工具。
2. **備案**：如果沒有這類工具，就輸出一則編號的純文字訊息，請使用者針對每個問題回覆所選的編號／答案。
3. **批次**：如果工具支援一次呼叫多個問題，就把所有適用的問題合併到一次呼叫中；如果只支援單一問題，就依優先順序一次問一個。

下方具體的 `AskUserQuestion` 參照只是範例——在其他執行環境中換成本地的同等工具。

## 圖片生成工具

當本技能需要渲染圖片時，依以下順序決定後端：

1. **目前請求的覆寫**——如果使用者在目前的訊息中指定了特定後端，就使用它。
2. **已儲存的偏好**——如果 `EXTEND.md` 把 `preferred_image_backend` 設為目前可用的後端，就使用它。
3. **自動選擇**（當偏好為 `auto`、未設定，或指定的後端無法使用時）：
   - **Codex（`imagegen`）**——首先檢查你可用的技能／工具清單。如果列出了名為 `imagegen` 的技能，代表你正在 Codex 中執行，「必須」使用它：透過 `Skill` 工具以 `skill: "imagegen"` 呼叫，傳入已儲存之提示詞檔案的內容（再依 Codex `imagegen` 自己的參數傳入輸出路徑與長寬比）。Codex `imagegen` 是該執行環境的官方點陣後端，除非使用者明確指定了不同的 `preferred_image_backend`，否則它的優先順序高於任何非原生的技能（例如 `baoyu-image-gen`）。
   - **透過 `codex exec` 的 Codex（`codex-imagegen`）**——如果目前的執行環境沒有原生的 `imagegen` 技能，但 `codex` CLI 在 `PATH` 中且已執行 `codex login`，就透過 `baoyu-image-gen --provider codex-cli`（偏好）處理，或者——如果無法使用 baoyu-image-gen——直接呼叫內附的包裝程式。細節、參數與執行環境探索程序在 [references/codex-imagegen.md](references/codex-imagegen.md)——只有選到這個分支時才載入該檔案。
   - **Cursor（`GenerateImage`）**——如果執行環境提供原生的 `GenerateImage` 工具，代表你正在 Cursor 中執行，它和 Codex `imagegen` 一樣優先於任何非原生的技能。兩個硬性注意事項：(a) 它沒有長寬比參數——在作為 `description` 傳入的提示詞文字中明確寫出目標長寬比／尺寸；(b) 它不接受輸出目錄——它會存到工具管理的位置，所以生成後要把檔案複製／移動到技能預期的輸出路徑（例如 `outputs/.../NN-xxx.png`）。參考圖片放在 `reference_image_paths`。
   - **其他執行環境原生的工具**——如果執行環境提供不同的原生圖片工具（例如 Hermes 的 `image_generate`），以同樣的方式使用。
   - 否則，如果剛好只安裝了一個非原生的後端（例如 `baoyu-image-gen`），就使用它。
   - 否則（有多個非原生後端且沒有執行環境原生的工具），詢問使用者一次——與其他初始問題一起批次詢問。
4. **如果都無法使用**，告知使用者並詢問如何進行。

**⛔ 絕不以 SVG、HTML、canvas 或其他以程式碼為基礎的渲染取代點陣圖片生成。** Codex `imagegen` 自己的描述就說，它應該用於「輸出應該是點陣素材，而不是 repo 原生的程式碼或向量時」。如果你無法透過步驟 3 決定點陣後端，就進入步驟 4 詢問使用者——**不要**默默輸出 SVG、寫行內的 `<svg>` 標記，或產出 HTML/CSS 美術作為替代。即使文章／章節看起來「像圖表」也一樣：呼叫這條規則的技能已經決定了它需要的是點陣圖片。

**⛔ 絕不透過在生成的點陣圖上塗改來修正渲染出的文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 腳本或任何其他程式化的疊加，去覆蓋、改寫、擦除、描邊或替換已生成之漫畫頁中的對白、狀聲詞、分格標籤或任何其他文字。如果文字錯誤或不清楚，就以修正後的提示詞重新生成、以較少或沒有圖中文字的方式重畫該頁，或詢問使用者要保留哪個不完美的候選。

設定 `preferred_image_backend: ask` 會強制每次執行都進行步驟 3 的詢問，不論可用的後端為何。使用者可以透過下方的「## 變更偏好」章節更改指定的後端。

**提示詞檔案要求（硬性）**：在呼叫任何後端之前，把每張圖片完整、最終的提示詞寫到 `prompts/` 下的獨立檔案（命名：`NN-{type}-[slug].md`）。後端接收的是提示詞檔案（或其內容）；這個檔案是可重現性的紀錄，也讓你可以在不重新產生提示詞的情況下切換後端。

上面的具體工具名稱（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）只是範例——依同樣的規則換成本地的同等工具。

## 批次生成政策

目前生成群組的每個提示詞檔案都儲存並確認之後，預設以批次方式生成圖片。

優先順序：

1. 如果選定的後端有原生的批次／多任務介面，就使用它。每個任務必須保有自己的提示詞檔案、輸出路徑、長寬比、工作階段 ID 與直接參考圖片。
2. 如果沒有原生批次介面，但執行環境可以發出平行的工具呼叫，一次派發最多 `generation_batch_size` 張圖片。預設：`4`。目前訊息中的明確使用者要求，例如 `--batch-size 4` 或「並行4張一起生成」，會覆蓋 EXTEND.md。
3. 如果既沒有原生批次也沒有平行工具呼叫，就依序生成。

規則：

- 先遵守工作流程的相依：在使用 `characters/characters.png` 作為參考的頁面之前先生成它。
- 在所有選定頁面的提示詞檔案都存在於磁碟上之前，絕不開始第一批頁面。
- 失敗的項目重試一次，不重新生成成功的項目。
- 不要只為了平行渲染圖片而使用子代理。子代理只用於獨立的提示詞迭代或創意探索。

## 參考圖片

使用者可以提供參考圖片來引導畫風、配色、場景構圖或主體。這與自動生成的角色設定表（步驟 7.1）**是分開的**——兩者可以並存：使用者的參考引導外觀，角色設定表則錨定反覆出現之角色的身分。

**收取**：透過 `--ref <files...>` 接受，或當使用者在對話中提供檔案路徑／貼上圖片時接受。
- 檔案路徑 → 複製到漫畫輸出旁的 `refs/NN-ref-{slug}.{ext}`
- 沒有路徑的貼上圖片 → 詢問使用者路徑（依上方的使用者輸入工具規則），或作為文字備案，以文字描述擷取風格特徵
- 沒有參考 → 跳過本節

**使用模式**（每張參考）：

| 用法 | 效果 |
|-------|--------|
| `direct` | 在每一頁（或選定的頁面）把檔案作為參考圖片傳給後端 |
| `style` | 擷取風格特徵（線條處理、質感、氛圍），附加到每一頁提示詞的內文 |
| `palette` | 擷取十六進位色碼，附加到每一頁提示詞的內文 |

有參考時，**記錄在每一頁提示詞的 frontmatter 中**：

{{CODE:1}}

**生成時**：
- 確認每個參考的檔案都存在於磁碟上
- 如果是 `usage: direct` 且選定的後端接受多張參考圖片 → 透過後端的參考參數同時傳入角色設定表（步驟 7.2）與使用者的參考；依步驟 7.1 的指引先壓縮圖片，以避免資料量過大而失敗
- 如果後端只接受一張參考 → 有反覆出現角色的頁面偏好使用角色設定表；改把使用者參考的特徵嵌入提示詞內文
- 對於 `style`／`palette` 用法 → 把擷取的特徵嵌入每一頁的提示詞文字（不論後端能力為何都適用）

## 選項

### 視覺維度

| 選項 | 值 | 說明 |
|--------|--------|-------------|
| `--art` | ligne-claire（預設）、manga、realistic、ink-brush、chalk、minimalist | 畫風／渲染技法 |
| `--tone` | neutral（預設）、warm、dramatic、romantic、energetic、vintage、action | 情緒／氛圍 |
| `--layout` | standard（預設）、cinematic、dense、splash、mixed、webtoon、four-panel | 分格配置 |
| `--aspect` | 3:4（預設，直式）、4:3（橫式）、16:9（寬螢幕） | 頁面長寬比 |
| `--lang` | auto（預設）、zh、en、ja 等 | 輸出語言 |
| `--ref <files...>` | 檔案路徑 | 套用到每一頁的參考圖片，用於風格／配色／場景引導。見上方的 [參考圖片](#reference-images)。 |
| `--batch-size <n>` | 1-8 | 本次執行的暫時頁面生成批次大小。預設：EXTEND.md 中的 `generation_batch_size`，否則為 4。 |

### 部分工作流程選項

| 選項 | 說明 |
|--------|-------------|
| `--storyboard-only` | 只產生分鏡，跳過提示詞與圖片 |
| `--prompts-only` | 產生分鏡 + 提示詞，跳過圖片 |
| `--images-only` | 從既有的提示詞目錄產生圖片 |
| `--regenerate N` | 只重新生成特定頁面（例如 `3` 或 `2,5,8`） |

細節：[references/partial-workflows.md](references/partial-workflows.md)

### 畫風、基調與預設目錄

- **畫風**（6 種）：`ligne-claire`（清線）、`manga`（日漫）、`realistic`（寫實）、`ink-brush`（水墨）、`chalk`（粉筆）、`minimalist`（極簡）。完整定義在 `references/art-styles/<style>.md`。
- **基調**（7 種）：`neutral`、`warm`、`dramatic`、`romantic`、`energetic`、`vintage`、`action`。完整定義在 `references/tones/<tone>.md`。
- **預設**（5 種），具有超出單純畫風＋基調的特殊規則：

  | 預設 | 等同於 | 特色 |
  |--------|-----------|------|
  | `ohmsha` | manga + neutral | 視覺隱喻、不用大頭對話、道具揭曉 |
  | `wuxia` | ink-brush + action | 氣勁效果、打鬥視覺、氛圍感 |
  | `shoujo` | manga + romantic | 裝飾元素、眼睛細節、浪漫節拍 |
  | `concept-story` | manga + warm | 視覺符號系統、成長弧線、對白與動作平衡 |
  | `four-panel` | minimalist + neutral + four-panel 版面 | 起承轉合結構、黑白 + 點綴色、火柴人角色 |

  完整規則在 `references/presets/<preset>.md`——選定預設時才載入該檔案。

- **相容性矩陣** 與 **內容訊號 → 預設** 對照表在 [references/auto-selection.md](references/auto-selection.md)。在步驟 2 推薦組合之前先閱讀它。

## 腳本目錄

**重要**：所有腳本都位於本技能的 `scripts/` 子目錄中。

**代理執行指示**：
1. 把這份 SKILL.md 所在的目錄路徑判定為 `{baseDir}`
2. 腳本路徑 = `{baseDir}/scripts/<script-name>.ts`
3. 把本文件中所有的 `{baseDir}` 換成實際路徑
4. 解析 `${BUN_X}` 執行環境：若已安裝 `bun` → `bun`；若可使用 `npx` → `npx -y bun`；否則建議安裝 bun

**腳本參考**：
| 腳本 | 用途 |
|--------|---------|
| `scripts/merge-to-pdf.ts` | 把漫畫頁合併成 PDF |

## 檔案結構

輸出目錄：`comic/{topic-slug}/`
- Slug：從主題取 2–4 個字的 kebab-case（例如 `alan-turing-bio`）
- 衝突時：附加時間戳（例如 `turing-story-20260118-143052`）

**內容**：
| 檔案 | 說明 |
|------|-------------|
| `source-{slug}.{ext}` | 來源檔案 |
| `analysis.md` | 內容分析 |
| `storyboard.md` | 含分格拆解的分鏡 |
| `characters/characters.md` | 角色定義 |
| `characters/characters.png` | 角色參考表 |
| `prompts/NN-{cover\|page}-[slug].md` | 生成提示詞 |
| `NN-{cover\|page}-[slug].png` | 生成的圖片 |
| `{topic-slug}.pdf` | 最終合併的 PDF |

## 語言處理

**偵測優先順序**：
1. `--lang` 旗標（明確指定）
2. EXTEND.md 的 `language` 設定
3. 使用者的對話語言
4. 來源內容的語言

**規則**：所有互動都使用使用者的輸入語言或已儲存的語言偏好：
- 分鏡大綱與場景描述
- 圖片生成提示詞
- 使用者的選項與確認
- 進度更新、問題、錯誤、摘要

技術術語維持英文。

## 工作流程

### 進度檢查表

{{CODE:2}}

### 流程

{{CODE:3}}

### 步驟摘要

| 步驟 | 動作 | 主要輸出 |
|------|--------|------------|
| 1.1 | 載入 EXTEND.md 偏好 ⛔ 找不到時阻擋 | 已載入設定 |
| 1.2 | 分析內容 | `analysis.md` |
| 1.3 | 檢查既有目錄 | 處理衝突 |
| 2 | 確認風格、重點、受眾、審閱 | 使用者偏好 |
| 3 | 產生分鏡 + 角色 | `storyboard.md`、`characters/` |
| 4 | 審閱大綱（若有要求） | 使用者核准 |
| 5 | 產生提示詞 | `prompts/*.md` |
| 6 | 審閱提示詞（若有要求） | 使用者核准 |
| 7.1 | 產生角色設定表（若需要） | `characters/characters.png` |
| 7.2 | 產生頁面（有角色參考時使用） | `*.png` 檔案 |
| 8 | 合併成 PDF | `{slug}.pdf` |
| 9 | 完成報告 | 摘要 |

### 步驟 7：圖片生成

**每個工作階段選定一次後端**，使用頂端的「## 圖片生成工具」規則。如果後端是 repo 技能（例如 `baoyu-image-gen`），閱讀它的 `SKILL.md` 並使用其文件記載的介面，而不是它的腳本。

**`codex-imagegen` 的呼叫方式**：當規則決定使用 `codex-imagegen` 時，參見 [references/codex-imagegen.md](references/codex-imagegen.md) 中的呼叫契約（偏好的 `baoyu-image-gen --provider codex-cli` 路徑、執行環境包裝程式探索、參數說明、stdout 結構、批次語意——每次呼叫 n=1，所以頁面批次必須每頁派發一次包裝程式呼叫）。

**7.1 角色設定表**——當漫畫是多頁且有反覆出現的角色時，產生它（存到 `characters/characters.png`，長寬比 `4:3`）。簡單的預設（例如四格極簡）或單頁漫畫則跳過。作為 `--ref` 使用前先壓縮成 JPEG（macOS 上用 `sips -s format jpeg -s formatOptions 80 …`，其他平台用 `pngquant --quality=65-80 …`），以避免資料量過大而失敗。在呼叫後端之前，`characters/characters.md` 的提示詞檔案必須存在。

**7.2 頁面**——在呼叫後端之前，每一頁的提示詞「必須」已經在 `prompts/NN-{cover|page}-[slug].md`；這個檔案是可重現性的紀錄。策略取決於角色設定表：

| 角色設定表 | 後端 `--ref` | 策略 |
|-----------------|-----------------|----------|
| 存在 | 支援 | 每一頁都把設定表作為 `--ref` 傳入 |
| 存在 | 不支援 | 在每個提示詞檔案前面加上角色描述 |
| 已跳過 | — | 所有描述都寫在提示詞內 |

**執行策略**：需要時先產生角色設定表。然後從已儲存的提示詞檔案建立選定的頁面任務清單，依「## 批次生成政策」分批派發頁面：先用後端原生批次，其次用執行環境的平行工具呼叫，依序生成只作為備案。`--regenerate N` 與 `--images-only` 對選定的既有提示詞套用同樣的批次規則。

**備份規則**：重新生成之前，把既有的 `prompts/…md` 與 `…png` 檔案加上 `-backup-YYYYMMDD-HHMMSS` 後綴重新命名。長寬比依分鏡（預設 `3:4`；預設組合可能覆寫）。

**`--ref` 失敗的復原**：壓縮設定表 → 重試 → 仍失敗 → 捨棄 `--ref`，把角色描述嵌入提示詞文字。

完整的逐步工作流程（分析、分鏡、審閱關卡、重新生成的變體）：[references/workflow.md](references/workflow.md)。

### EXTEND.md 路徑 ⛔ 阻擋性

如果找不到 EXTEND.md，首次設定是 **阻擋性的**——在任何內容分析或風格／基調問題之前先完成它。

| 優先順序 | 路徑 | 範圍 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-comic/EXTEND.md` | 專案 |
| 2 | `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 使用者家目錄 |

| 結果 | 動作 |
|--------|--------|
| 找到 | 讀取、解析、顯示摘要 → 繼續 |
| 找不到 | ⛔ 執行首次設定（[references/config/first-time-setup.md](references/config/first-time-setup.md)）→ 儲存 EXTEND.md → 繼續 |

**EXTEND.md 支援**：浮水印、偏好的畫風／基調／版面、自訂風格定義、角色預設、語言偏好、偏好的圖片後端、生成批次大小。結構定義：[references/config/preferences-schema.md](references/config/preferences-schema.md)。

## 參考資料

**核心範本**：
- [analysis-framework.md](references/analysis-framework.md) —— 深度內容分析
- [character-template.md](references/character-template.md) —— 角色定義格式
- [storyboard-template.md](references/storyboard-template.md) —— 分鏡結構
- [ohmsha-guide.md](references/ohmsha-guide.md) —— 歐姆社漫畫的特點

**風格定義**：
- `references/art-styles/` —— 畫風（ligne-claire、manga、realistic、ink-brush、chalk、minimalist）
- `references/tones/` —— 基調（neutral、warm、dramatic、romantic、energetic、vintage、action）
- `references/presets/` —— 具特殊規則的預設（ohmsha、wuxia、shoujo、concept-story、four-panel）
- `references/layouts/` —— 版面（standard、cinematic、dense、splash、mixed、webtoon、four-panel）

**工作流程**：
- [workflow.md](references/workflow.md) —— 完整的工作流程細節
- [auto-selection.md](references/auto-selection.md) —— 內容訊號分析
- [partial-workflows.md](references/partial-workflows.md) —— 部分工作流程選項

**設定**：
- [config/preferences-schema.md](references/config/preferences-schema.md) —— EXTEND.md 結構定義
- [config/first-time-setup.md](references/config/first-time-setup.md) —— 首次設定
- [config/watermark-guide.md](references/config/watermark-guide.md) —— 浮水印設定

## 修改頁面

| 動作 | 步驟 |
|--------|-------|
| **編輯** | **先更新提示詞檔案** → `--regenerate N` → 重新產生 PDF |
| **新增** | 在對應位置建立提示詞 → 以角色參考生成 → 重新編號後續頁面 → 更新分鏡 → 重新產生 PDF |
| **刪除** | 移除檔案 → 重新編號後續頁面 → 更新分鏡 → 重新產生 PDF |

**重要**：更新頁面時，重新生成之前「一律」先更新提示詞檔案（`prompts/NN-{cover|page}-[slug].md`）。這確保變更有紀錄且可重現。

文字修正政策：

- 如果對白、狀聲詞、分格標籤或任何其他渲染出的文字拼錯、亂碼、難以閱讀或視覺上薄弱，不要用程式修補點陣圖。
- 為修正文字而重新生成時，寫一個新的提示詞檔案與新的輸出路徑，讓有缺陷的候選保留下來以供比較。
- 後製只限於不改變文字或主要構圖的裁切、縮放、壓縮或格式轉換。

## 注意事項

- 圖片生成：每頁 10–30 秒
- 生成失敗時自動重試一次
- 對敏感的公眾人物使用風格化的替代
- 透過工作階段 ID 維持風格一致
- **步驟 2 的確認是必要的**——不要跳過
- **步驟 4／6 是條件式的**——只有在使用者於步驟 2 要求時才進行
- **步驟 7.1 角色設定表**——建議用於多頁漫畫，簡單的預設可選用
- **步驟 7.2 角色參考**——若設定表存在就使用 `--ref`；失敗時壓縮／轉檔；最後退回只用提示詞
- 浮水印／語言在 EXTEND.md 中設定一次即可

## 變更偏好

EXTEND.md 位於 `.baoyu-skills/baoyu-comic/EXTEND.md`（專案）或 `~/.baoyu-skills/baoyu-comic/EXTEND.md`（使用者）。有三種變更方式：

- **直接編輯**——開啟 EXTEND.md 並修改欄位。完整結構定義：`references/config/preferences-schema.md`。
- **互動式重新設定**——刪除 EXTEND.md（或說「重新設定 baoyu-comic 偏好」／「重新配置」）。下次執行會重新觸發首次設定。
- **常見的一行修改**：
  - `preferred_image_backend: auto` —— 預設；執行環境原生的工具優先，退回唯一安裝的後端，只有在有多個非原生後端時才詢問。
  - `preferred_image_backend: codex-imagegen` —— 指定使用 Codex 的內建工具。
  - `preferred_image_backend: baoyu-image-gen` —— 指定使用 baoyu-image-gen 技能。
  - `preferred_image_backend: ask` —— 每次執行都確認後端。
  - `generation_batch_size: 4` —— 當後端／執行環境支援批次或平行生成時，同時渲染的預設頁面圖片數量。
  - `watermark.enabled: true`、`preferred_art`、`preferred_tone`、`preferred_layout`、`language` —— 調整自動選擇的預設值與外觀選擇。
