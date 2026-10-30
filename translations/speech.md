<!--meta
{"title":"文字轉語音","category":"影片與多媒體","tags":["TTS","配音","語音合成","OpenAI API","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：用 OpenAI Audio API 產生語音——旁白、產品示範配音、電話語音選單（IVR）、無障礙朗讀，支援單一片段或大量批次。預設 gpt-4o-mini-tts 與內建聲音 cedar，用內附 CLI 確保結果可重現；不支援自訂聲音。",
"usage":"- Codex：`$skill-installer speech`；需先在本機設定 `OPENAI_API_KEY`\n- 說「幫這段產品介紹配一段沉穩的英文旁白」「把這 20 句客服語音選單批次產生成音檔」\n- 指示依「情緒 → 語氣 → 節奏 → 情感 → 發音/停頓 → 強調」組織，4–8 行即可\n- 每次請求最多 4096 字元、每分鐘 50 次；要向終端使用者揭露聲音是 AI 產生的"}
-->
---
name: "speech"
description: "當使用者透過 OpenAI Audio API 要求文字轉語音的旁白或配音、無障礙朗讀、語音提示或大量語音生成時使用；以內建聲音執行內附的 CLI（`scripts/text_to_speech.py`），即時呼叫需要 `OPENAI_API_KEY`。自訂聲音的建立不在範圍內。"
---


# 語音生成技能

為目前的專案產生語音（旁白、產品示範配音、IVR 提示、無障礙朗讀）。預設使用 `gpt-4o-mini-tts-2025-12-15` 與內建聲音，並優先使用內附的 CLI 以取得決定性、可重現的執行結果。

## 何時使用
- 從文字產生單一語音片段
- 產生一批提示（多行、多個檔案）

## 決策樹（單一 vs 批次）
- 如果使用者提供多行/多個提示，或想要很多輸出 -> **批次**
- 否則 -> **單一**

## 工作流程
1. 決定意圖：單一 vs 批次（見上方決策樹）。
2. 一開始就蒐集輸入：確切的文字（逐字）、想要的聲音、表達風格、格式，以及任何限制。
3. 如果是批次：在 tmp/ 下寫一個暫存的 JSONL（每行一個工作），執行一次，然後刪除 JSONL。
4. 把指示補充成一份簡短、有標籤的規格，但不改寫輸入的文字。
5. 以合理的預設值執行內附的 CLI（`scripts/text_to_speech.py`）（見 references/cli.md）。
6. 對於重要的片段，驗證：清晰度、節奏、發音，以及是否遵守限制。
7. 以單一針對性的修改（聲音、速度或指示）反覆調整，然後再檢查。
8. 儲存/回傳最終輸出，並記下最終使用的文字 + 指示 + 旗標。

## 暫存與輸出慣例
- 中間檔案（例如 JSONL 批次）使用 `tmp/speech/`；完成後刪除。
- 在這個 repo 中工作時，把最終產出物寫在 `output/speech/` 之下。
- 用 `--out` 或 `--out-dir` 控制輸出路徑；保持檔名穩定且具描述性。

## 相依套件（缺少時安裝）
優先使用 `uv` 管理相依套件。

Python 套件：
{{CODE:1}}
如果沒有 `uv`：
{{CODE:2}}

## 環境
- 即時 API 呼叫必須設定 `OPENAI_API_KEY`。

如果缺少金鑰，給使用者這些步驟：
1. 在 OpenAI 平台介面中建立 API 金鑰：https://platform.openai.com/api-keys
2. 在他們的系統中把 `OPENAI_API_KEY` 設為環境變數。
3. 需要時，提議引導他們為自己的作業系統/shell 設定環境變數。
- 絕不要求使用者在對話中貼上完整的金鑰。請他們在本機設定，並在準備好時確認。

如果在這個環境中無法安裝，告訴使用者缺少哪個相依項目，以及如何在本機安裝。

## 預設值與規則
- 除非使用者要求其他模型，否則使用 `gpt-4o-mini-tts-2025-12-15`。
- 預設聲音：`cedar`。如果使用者想要更明亮的語調，優先使用 `marin`。
- 只用內建聲音。自訂聲音不在本技能範圍內。
- GPT-4o mini TTS 模型支援 `instructions`，但 `tts-1` 或 `tts-1-hd` 不支援。
- 每個請求的輸入長度必須 <= 4096 個字元。把較長的文字分塊。
- 強制每分鐘 50 次請求。CLI 把 `--rpm` 上限設為 50。
- 任何即時 API 呼叫之前都要求 `OPENAI_API_KEY`。
- 向終端使用者清楚揭露該聲音是 AI 產生的。
- 所有 API 呼叫都使用 OpenAI Python SDK（`openai` 套件）；不要使用原始 HTTP。
- 優先使用內附的 CLI（`scripts/text_to_speech.py`），而不是另寫一次性的腳本。
- 絕不修改 `scripts/text_to_speech.py`。如果缺少什麼，在做任何其他事之前先詢問使用者。

## 指示補充
把使用者的指導重新整理成一份簡短、有標籤的規格。只把隱含的細節明確化；不要發明新的要求。

快速釐清（補充 vs 發明）：
- 如果使用者說「示範用的旁白」，你可以加上隱含的表達限制（清楚、節奏穩定、語氣友善）。
- 不要引入使用者沒有要求的新角色、口音或情緒風格。

模板（只包含相關的行）：
{{CODE:3}}

補充規則：
- 保持簡短；只加入使用者已經暗示或在別處提供過的細節。
- 不要改寫輸入的文字。
- 如果缺少任何會阻礙成功的關鍵細節，就提問；否則就繼續。

## 範例

### 單一範例（旁白）
{{CODE:4}}

### 批次範例（IVR 提示）
{{CODE:5}}

## 下指示的最佳實踐（簡短清單）
- 把指導組織成：情緒 -> 語氣 -> 節奏 -> 情感 -> 發音/停頓 -> 強調。
- 保持 4 到 8 行簡短的句子；避免互相衝突的指引。
- 對於名稱/縮寫，加上發音提示（例如「enunciate A-I」），或在文字中提供拼音。
- 進行修改/迭代時，重複不變的要求（例如「保持節奏穩定」）以減少偏移。
- 以單一變更的後續調整進行迭代。

更多原則：`references/prompting.md`。可直接複製貼上的規格：`references/sample-prompts.md`。

## 依使用情境的指引
當請求是針對特定的表達風格時，使用這些模組。它們提供針對性的預設值與模板。
- 旁白 / 解說：`references/narration.md`
- 產品示範 / 配音：`references/voiceover.md`
- IVR / 電話提示：`references/ivr.md`
- 無障礙朗讀：`references/accessibility.md`

## CLI 與環境注意事項
- CLI 指令 + 範例：`references/cli.md`
- API 參數快速參考：`references/audio-api.md`
- 指示模式 + 範例：`references/voice-directions.md`
- 如果網路核准 / 沙箱設定造成阻礙：`references/codex-network.md`

## 參考對照
- **`references/cli.md`**：如何透過 `scripts/text_to_speech.py` 執行語音生成/批次（指令、旗標、做法）。
- **`references/audio-api.md`**：API 參數、限制、聲音清單。
- **`references/voice-directions.md`**：指示模式與範例。
- **`references/prompting.md`**：下指示的最佳實踐（結構、限制、迭代模式）。
- **`references/sample-prompts.md`**：可直接複製貼上的指示做法（只有範例；沒有額外理論）。
- **`references/narration.md`**：旁白與解說的模板 + 預設值。
- **`references/voiceover.md`**：產品示範配音的模板 + 預設值。
- **`references/ivr.md`**：IVR/電話提示的模板 + 預設值。
- **`references/accessibility.md`**：無障礙朗讀的模板 + 預設值。
- **`references/codex-network.md`**：環境/沙箱/網路核准的疑難排解。
