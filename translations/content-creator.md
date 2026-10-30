<!--meta
{"title":"內容創作者（已轉址）","category":"社群行銷","tags":["內容行銷","轉址","SEO","品牌語氣"],
"summary":"已停用的轉址技能：原本的 content-creator 什麼都做（規劃、撰寫、SEO、社群、品牌語氣），新版拆成兩個專門技能。本技能不直接處理請求，只判斷你的意圖後轉給 content-production（撰寫、SEO、品牌語氣分析）或 content-strategy（主題叢集、內容行事曆等規劃）；社群內容則轉給 social-content。",
"usage":"- 說「content creator」或「幫我寫一篇部落格」→ 轉給 content-production\n- 說「幫我規劃內容」「我該寫什麼」「做內容行事曆」→ 轉給 content-strategy\n- 需要同時安裝後繼技能才有實際功能"}
-->
---
name: "content-creator"
description: "已停用的轉址技能，把舊的「content creator」請求轉給正確的專門技能。當使用者呼叫「content creator」、要求撰寫部落格文章、文章、指南或品牌語氣分析（轉給 content-production），或要求規劃內容、建立主題叢集或建立內容行事曆（轉給 content-strategy）時使用。不直接處理請求——辨識使用者意圖後，撰寫／SEO／品牌語氣任務轉給 content-production，規劃任務轉給 content-strategy。"
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
  status: deprecated
---

# 內容創作者 → 已轉址

> **本技能已拆分成兩個專門技能。** 請使用符合你意圖的那一個：

| 你想要…… | 改用這個 |
|----------------|-----------------|
| **撰寫** 部落格文章、文章或指南 | [content-production](../content-production/) |
| **規劃** 要做哪些內容、主題叢集、行事曆 | [content-strategy](../content-strategy/) |
| **分析品牌語氣** | [content-production](../content-production/)（含 `brand_voice_analyzer.py`） |
| 為既有內容 **最佳化 SEO** | [content-production](../content-production/)（含 `seo_optimizer.py`） |
| **建立社群媒體內容** | [social-content](../social-content/) |

## 為什麼改變

原本的 `content-creator` 試圖包辦一切：規劃、撰寫、SEO、社群、品牌語氣。這讓它成了樣樣通、樣樣鬆。專門技能能把每一項工作做得更好：

- **content-production** —— 完整流水線：研究 → 簡報 → 草稿 → 最佳化 → 發布。包含原本 content-creator 的所有 Python 工具。
- **content-strategy** —— 策略規劃：主題叢集、關鍵字研究、內容行事曆、優先順序框架。

## 主動觸發

- **使用者說「content creator」** → 轉給 content-production（最可能的意圖是撰寫）。
- **使用者說「content plan」或「我該寫什麼」** → 轉給 content-strategy。

## 輸出產物

| 當你要求…… | 轉給…… |
|---------------------|-------------|
| 「寫一篇部落格文章」 | content-production |
| 「內容行事曆」 | content-strategy |
| 「品牌語氣分析」 | content-production（`brand_voice_analyzer.py`） |
| 「SEO 最佳化」 | content-production（`seo_optimizer.py`） |

## 溝通

這是一個轉址技能。把使用者轉給正確的專門技能——不要嘗試在這裡處理請求。

## 相關技能

- **content-production**：完整的內容執行流水線（後繼者）。
- **content-strategy**：內容規劃與選題（後繼者）。
- **content-humanizer**：對 AI 內容做後製，讓它聽起來更真實。
- **marketing-context**：兩個後繼者都會讀取的基礎情境。
