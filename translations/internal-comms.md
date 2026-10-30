<!--meta
{"title":"內部溝通文件","category":"文件與辦公","tags":["內部溝通","週報","3P 更新","電子報","Anthropic 官方"],
"summary":"Anthropic 官方範例技能：用公司慣用的格式撰寫各種內部溝通——3P 更新（進展／計畫／問題）、公司電子報、FAQ、狀態報告、主管更新、專案更新與事件報告。每種類型都有對應的範例指南檔。",
"usage":"- 安裝：`npx skills add https://github.com/anthropics/skills --skill internal-comms`\n- 說「幫我寫這週的 3P 更新」「把這次服務中斷整理成事件報告」\n- 想套用自家格式：修改 `examples/` 裡的指南檔即可"}
-->
---
name: internal-comms
description: 一組協助我以公司喜歡的格式撰寫各種內部溝通的資源。每當被要求撰寫某種內部溝通（狀態報告、主管更新、3P 更新、公司電子報、FAQ、事件報告、專案更新等）時，Claude 都應使用本技能。
license: 完整條款見 LICENSE.txt
---

## 何時使用本技能
撰寫內部溝通時，以下情況使用本技能：
- 3P 更新（Progress 進展、Plans 計畫、Problems 問題）
- 公司電子報
- FAQ 回覆
- 狀態報告
- 主管更新
- 專案更新
- 事件報告

## 如何使用本技能

撰寫任何內部溝通時：

1. 從請求中**辨識溝通類型**
2. 從 `examples/` 目錄**載入對應的指南檔**：
    - `examples/3p-updates.md` ——用於進展/計畫/問題的團隊更新
    - `examples/company-newsletter.md` ——用於全公司電子報
    - `examples/faq-answers.md` ——用於回答常見問題
    - `examples/general-comms.md` ——用於任何未明確符合上述之一的情況
3. 依照該檔案中關於格式、語氣與內容蒐集的**具體指示**

如果溝通類型不符合任何既有指南，就詢問以釐清，或請對方提供更多關於所需格式的脈絡。

## 關鍵字
3P 更新、公司電子報、公司溝通、週報、FAQ、常見問題、更新、內部溝通
