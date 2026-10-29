<!--meta
{"title":"Jupyter 筆記本產生器","category":"文件與辦公","tags":["Jupyter","資料分析","教學","Python","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：建立或重構乾淨、可重現的 Jupyter 筆記本（.ipynb），分為「實驗探索」與「教學導覽」兩種模板，用內附腳本產生骨架，避免手寫 JSON 出錯。",
"usage":"- Codex：`$skill-installer jupyter-notebook`\n- 說「幫我建一個比較不同 temperature 效果的實驗筆記本」或「把這支腳本改寫成教學 notebook」\n- 腳本：`python new_notebook.py --kind experiment --title \"...\" --out output/jupyter-notebook/xxx.ipynb`\n- 完成後會盡量從頭到尾執行一次驗證"}
-->
---
name: "jupyter-notebook"
description: "當使用者要求為實驗、探索或教學建立、搭建骨架或編輯 Jupyter 筆記本（`.ipynb`）時使用；優先使用內附模板，並執行輔助腳本 `new_notebook.py` 產生乾淨的起始筆記本。"
---


# Jupyter 筆記本技能

為兩種主要模式建立乾淨、可重現的 Jupyter 筆記本：

- 實驗與探索式分析
- 教學與以教學為導向的導覽

優先使用內附的模板與輔助腳本，讓結構一致並減少 JSON 錯誤。

## 何時使用
- 從零建立新的 `.ipynb` 筆記本。
- 把粗略的筆記或腳本轉換成有結構的筆記本。
- 重構既有筆記本，使其更可重現、更容易快速瀏覽。
- 建立會被其他人閱讀或重新執行的實驗或教學。

## 決策樹
- 如果請求是探索性、分析性或假設驅動的，選擇 `experiment`。
- 如果請求是教學性、逐步的或針對特定受眾，選擇 `tutorial`。
- 如果是編輯既有筆記本，就當作重構：保留原意並改善結構。

## 技能路徑（設定一次）

{{CODE:1}}

使用者範圍的技能安裝在 `$CODEX_HOME/skills` 之下（預設：`~/.codex/skills`）。

## 工作流程
1. 鎖定意圖。
辨識筆記本類型：`experiment` 或 `tutorial`。
記錄目標、受眾，以及「完成」的樣子。

2. 從模板搭建骨架。
使用輔助腳本，避免手寫原始的筆記本 JSON。

{{CODE:2}}

{{CODE:3}}

3. 用小而可執行的步驟填充筆記本。
每個程式碼儲存格聚焦在一個步驟。
加入簡短的 markdown 儲存格說明目的與預期結果。
簡短摘要就夠時，避免冗長、雜亂的輸出。

4. 套用正確的模式。
實驗請遵循 `references/experiment-patterns.md`。
教學請遵循 `references/tutorial-patterns.md`。

5. 處理既有筆記本時安全地編輯。
保留筆記本結構；除非能改善由上到下的敘事，否則避免重新排序儲存格。
優先做針對性的修改，而非整份重寫。
如果必須編輯原始 JSON，先閱讀 `references/notebook-structure.md`。

6. 驗證結果。
環境允許時，從頭到尾執行筆記本。
如果無法執行，要明確說明，並指出如何在本機驗證。
使用 `references/quality-checklist.md` 中的最終檢查清單。

## 模板與輔助腳本
- 模板位於 `assets/experiment-template.ipynb` 與 `assets/tutorial-template.ipynb`。
- 輔助腳本會載入模板、更新標題儲存格，並寫出筆記本。

腳本路徑：
- `$JUPYTER_NOTEBOOK_CLI`（安裝後預設：`$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`）

## 暫存與輸出慣例
- 中間檔案使用 `tmp/jupyter-notebook/`；完成後刪除。
- 在這個 repo 中工作時，最終產出物寫在 `output/jupyter-notebook/` 之下。
- 使用穩定、具描述性的檔名（例如 `ablation-temperature.ipynb`）。

## 相依套件（只在需要時安裝）
優先使用 `uv` 管理相依套件。

本機執行筆記本的選用 Python 套件：

{{CODE:4}}

內附的骨架腳本只使用 Python 標準函式庫，不需要額外的相依套件。

## 環境
沒有必要的環境變數。

## 參考對照
- `references/experiment-patterns.md`：實驗結構與經驗法則。
- `references/tutorial-patterns.md`：教學結構與教學流程。
- `references/notebook-structure.md`：筆記本 JSON 形狀與安全編輯規則。
- `references/quality-checklist.md`：最終驗證檢查清單。
