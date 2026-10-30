<!--meta
{"title":"語音轉逐字稿","category":"影片與多媒體","tags":["語音辨識","逐字稿","說話者分離","OpenAI API","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：用 OpenAI 的轉錄模型把音訊／影片轉成文字，需要時可做說話者分離（diarization）並提供已知說話者的參考音檔，最多 4 人。預設用 gpt-4o-mini-transcribe 快速轉純文字。",
"usage":"- Codex：`$skill-installer transcribe`；需先在本機設定 `OPENAI_API_KEY`（不要貼在對話中）\n- 說「把這段訪談錄音轉成逐字稿並標出誰在說話」\n- 要分辨說話者時改用 `--model gpt-4o-transcribe-diarize --response-format diarized_json`\n- 輸出存到 `output/transcribe/`"}
-->
---
name: "transcribe"
description: "把音訊檔轉錄成文字，可選擇說話者分離與已知說話者提示。當使用者要求從音訊/影片轉錄語音、從錄音擷取文字，或在訪談或會議中標示說話者時使用。"
---


# 音訊轉錄

使用 OpenAI 轉錄音訊，在被要求時可選擇進行說話者分離。為了取得決定性、可重複的執行結果，優先使用內附的 CLI。

## 工作流程
1. 蒐集輸入：音訊檔路徑、想要的回應格式（text/json/diarized_json）、選用的語言提示，以及任何已知說話者的參考。
2. 確認已設定 `OPENAI_API_KEY`。如果沒有，請使用者在本機設定（不要請他們貼上金鑰）。
3. 以合理的預設值執行內附的 `transcribe_diarize.py` CLI（快速的文字轉錄）。
4. 驗證輸出：轉錄品質、說話者標籤與片段邊界；需要時以單一針對性的修改反覆調整。
5. 在這個 repo 中工作時，把輸出存到 `output/transcribe/`。

## 決策規則
- 預設使用 `gpt-4o-mini-transcribe` 搭配 `--response-format text` 進行快速轉錄。
- 如果使用者想要說話者標籤或說話者分離，使用 `--model gpt-4o-transcribe-diarize --response-format diarized_json`。
- 如果音訊長於約 30 秒，保持 `--chunking-strategy auto`。
- `gpt-4o-transcribe-diarize` 不支援提示詞。

## 輸出慣例
- 評估執行使用 `output/transcribe/<job-id>/`。
- 多個檔案使用 `--out-dir`，避免互相覆寫。

## 相依套件（缺少時安裝）
優先使用 `uv` 管理相依套件。

{{CODE:1}}
如果沒有 `uv`：
{{CODE:2}}

## 環境
- 即時 API 呼叫必須設定 `OPENAI_API_KEY`。
- 如果缺少金鑰，指示使用者在 OpenAI 平台介面中建立一把，並在 shell 中 export。
- 絕不要求使用者在對話中貼上完整的金鑰。

## 技能路徑（設定一次）

{{CODE:3}}

使用者範圍的技能安裝在 `$CODEX_HOME/skills` 之下（預設：`~/.codex/skills`）。

## CLI 快速開始
單一檔案（預設為快速文字）：
{{CODE:4}}

帶已知說話者的說話者分離（最多 4 位）：
{{CODE:5}}

純文字輸出（明確指定）：
{{CODE:6}}

## 參考對照
- `references/api.md`：支援的格式、限制、回應格式，以及已知說話者的注意事項。
