<!--meta
{"title":"Gemini 深度研究","category":"溝通與學習","tags":["Gemini","深度研究","市場分析","文獻回顧"],
"summary":"呼叫 Google Gemini Deep Research Agent 執行自主的多步驟研究：自動規劃、搜尋、閱讀並綜合成附引用的詳細報告，適合市場分析、競爭態勢、文獻回顧、技術研究與盡職調查。每個任務約 2–10 分鐘、花費約 2–5 美元，可即時串流進度、背景執行後查詢狀態，或延續先前的研究追問。",
"usage":"- 需要 Python 3.8+、`pip install -r requirements.txt`，並設定 `GEMINI_API_KEY`（到 Google AI Studio 取得）\n- 說「深度研究一下台灣電動機車市場的競爭態勢」\n- 腳本參數：`--query`、`--stream`、`--status`、`--continue`、`--json`\n- 注意每次約花 2–5 美元"}
-->
---
name: deep-research
description: "使用 Google Gemini Deep Research Agent 執行自主的多步驟研究。用於：市場分析、競爭態勢、文獻回顧、技術研究、盡職調查。需要 2–10 分鐘，但會產出詳細、附引用的報告。每個任務花費 2–5 美元。"
license: Apache-2.0
metadata:
  author: sanjay3290
  version: "1.0"
---

# Gemini 深度研究技能

執行自主的研究任務，自動規劃、搜尋、閱讀並把資訊綜合成完整的報告。

## 需求

- Python 3.8+
- httpx：`pip install -r requirements.txt`
- GEMINI_API_KEY 環境變數

## 設定

1. 從 [Google AI Studio](https://aistudio.google.com/) 取得 Gemini API 金鑰
2. 設定環境變數：
   ```bash
   export GEMINI_API_KEY=your-api-key-here
   ```
   或在技能目錄中建立 `.env` 檔案。

## 用法

### 開始一項研究任務
{{CODE:1}}

### 指定結構化的輸出格式
{{CODE:2}}

### 即時串流進度
{{CODE:3}}

### 啟動後不等待
{{CODE:4}}

### 檢查執行中研究的狀態
{{CODE:5}}

### 等待完成
{{CODE:6}}

### 延續先前的研究
{{CODE:7}}

### 列出最近的研究
{{CODE:8}}

## 輸出格式

- **預設**：人類可讀的 markdown 報告
- **JSON**（`--json`）：供程式使用的結構化資料
- **原始**（`--raw`）：未經處理的 API 回應

## 成本與時間

| 指標 | 數值 |
|--------|-------|
| 時間 | 每個任務 2–10 分鐘 |
| 成本 | 每個任務 2–5 美元（依複雜度而異） |
| Token 用量 | 輸入約 25 萬–90 萬，輸出約 6 萬–8 萬 |

## 最佳使用情境

- 市場分析與競爭態勢
- 技術文獻回顧
- 盡職調查研究
- 歷史研究與時間軸
- 比較分析（框架、產品、技術）

## 工作流程

1. 使用者要求研究 → 執行 `--query "..."`
2. 告知使用者預估時間（2–10 分鐘）
3. 用 `--stream` 監看，或用 `--status` 輪詢
4. 回傳格式化的結果
5. 後續問題使用 `--continue`

## 結束碼

- **0**：成功
- **1**：錯誤（API 錯誤、設定問題、逾時）
- **130**：使用者取消（Ctrl+C）
