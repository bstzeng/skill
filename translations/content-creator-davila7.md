<!--meta
{"title":"內容創作者（SEO 與品牌語氣）","category":"社群行銷","tags":["內容行銷","SEO","品牌語氣","社群媒體","內容行事曆"],
"summary":"產出 SEO 最佳化、品牌語氣一致的行銷內容（早期 1.0 版）。內附品牌語氣分析器與 SEO 最佳化工具兩支 Python 腳本、內容框架、社群媒體範本與內容行事曆範本，涵蓋建立品牌語氣、撰寫 SEO 部落格文章、跨平台改寫社群內容，以及每月／每週的內容規劃與績效指標。",
"usage":"- 說「幫我寫一篇 SEO 部落格文章」「分析我們的品牌語氣」「規劃下個月的內容行事曆」\n- 分析語氣：`python scripts/brand_voice_analyzer.py existing_content.txt`\n- SEO 檢查：`python scripts/seo_optimizer.py blog_post.md \"主關鍵字\" \"次要,關鍵字\"`\n- 注意：同作者的新版已改為轉址技能，見 content-creator"}
-->
---
name: content-creator
description: 建立 SEO 最佳化且品牌語氣一致的行銷內容。包含品牌語氣分析器、SEO 最佳化工具、內容框架與社群媒體範本。在撰寫部落格文章、建立社群媒體內容、分析品牌語氣、最佳化 SEO、規劃內容行事曆時，或使用者提到內容創作、品牌語氣、SEO 最佳化、社群媒體行銷或內容策略時使用。
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# 內容創作者

專業等級的品牌語氣分析、SEO 最佳化，以及針對各平台的內容框架。

## 關鍵字
內容創作、部落格文章、SEO、品牌語氣、社群媒體、內容行事曆、行銷內容、內容策略、內容行銷、品牌一致性、內容最佳化、社群媒體行銷、內容規劃、部落格寫作、內容框架、品牌指南、社群媒體策略

## 快速開始

### 建立品牌語氣
1. 對既有內容執行 `scripts/brand_voice_analyzer.py` 以建立基準線
2. 閱讀 `references/brand_guidelines.md` 選擇語氣屬性
3. 在所有內容中一致地套用選定的語氣

### 建立部落格內容
1. 從 `references/content_frameworks.md` 選擇範本
2. 為主題研究關鍵字
3. 依照範本結構撰寫內容
4. 執行 `scripts/seo_optimizer.py [file] [primary-keyword]` 進行最佳化
5. 發布前套用建議

### 社群媒體內容
1. 閱讀 `references/social_media_optimization.md` 中的平台最佳實務
2. 使用 `references/content_frameworks.md` 中適當的範本
3. 依照平台專屬指引最佳化
4. 使用 `assets/content_calendar_template.md` 排程

## 核心工作流程

### 建立品牌語氣（首次設定）

為新品牌或新客戶建立內容時：

1. **分析既有內容**（如果有的話）
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```
   
2. **定義語氣屬性**
   - 閱讀 `references/brand_guidelines.md` 中的品牌個性原型
   - 選擇主要與次要原型
   - 選擇 3–5 個語調屬性
   - 記錄在品牌指南中

3. **建立語氣範例**
   - 用選定的語氣寫 3 篇範例
   - 使用分析器測試一致性
   - 依結果調整

### 建立 SEO 最佳化的部落格文章

1. **關鍵字研究**
   - 找出主要關鍵字（每月搜尋量 500–5000）
   - 找出 3–5 個次要關鍵字
   - 列出 10–15 個 LSI 關鍵字

2. **內容結構**
   - 使用 `references/content_frameworks.md` 中的部落格範本
   - 在標題、第一段與 2–3 個 H2 中放入關鍵字
   - 以 1,500–2,500 字為目標，達到完整的涵蓋

3. **最佳化檢查**
   ```bash
   python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
   ```

4. **套用 SEO 建議**
   - 把關鍵字密度調整到 1–3%
   - 確保正確的標題結構
   - 加入內部與外部連結
   - 最佳化 meta 描述

### 建立社群媒體內容

1. **選擇平台**
   - 依受眾找出主要平台
   - 閱讀 `references/social_media_optimization.md` 中的平台專屬指引

2. **內容改寫**
   - 從部落格文章或核心訊息開始
   - 使用 `references/content_frameworks.md` 中的再利用矩陣
   - 依照範本為各平台改寫

3. **最佳化檢查清單**
   - 適合平台的長度
   - 最佳發文時間
   - 正確的圖片尺寸
   - 平台專屬的主題標籤
   - 互動元素（投票、提問）

### 規劃內容行事曆

1. **每月規劃**
   - 複製 `assets/content_calendar_template.md`
   - 設定每月目標與 KPI
   - 找出主要的活動／主題

2. **每週分配**
   - 遵循 40/25/25/10 的內容支柱比例
   - 在一週內平衡各平台
   - 配合最佳發文時間

3. **批次製作**
   - 在一次工作時段內製作整週的內容
   - 在各篇之間保持一致的語氣
   - 一起準備所有視覺素材

## 主要腳本

### brand_voice_analyzer.py
分析文字內容的語氣特徵、可讀性與一致性。

**用法**：`python scripts/brand_voice_analyzer.py <file> [json|text]`

**回傳**：
- 語氣輪廓（正式程度、語調、觀點）
- 可讀性分數
- 句子結構分析
- 改善建議

### seo_optimizer.py
分析內容的 SEO 最佳化程度，並提供可執行的建議。

**用法**：`python scripts/seo_optimizer.py <file> [primary_keyword] [secondary_keywords]`

**回傳**：
- SEO 分數（0–100）
- 關鍵字密度分析
- 結構評估
- Meta 標籤建議
- 具體的最佳化建議

## 參考指南

### 何時使用各份參考文件

**references/brand_guidelines.md**
- 建立新的品牌語氣
- 確保各內容之間的一致性
- 訓練新進團隊成員
- 解決語氣／語調的問題

**references/content_frameworks.md**
- 開始任何新的內容
- 為不同類型的內容建立結構
- 建立內容範本
- 規劃內容再利用

**references/social_media_optimization.md**
- 平台專屬的最佳化
- 制定主題標籤策略
- 了解演算法因素
- 設定分析追蹤

## 最佳實務

### 內容創作流程
1. 一律從受眾的需求／痛點開始
2. 寫之前先研究
3. 用範本建立大綱
4. 寫初稿時先不要編修
5. 為 SEO 最佳化
6. 依品牌語氣編修
7. 校對與事實查核
8. 為平台最佳化
9. 有策略地排程

### 品質指標
- SEO 分數高於 75/100
- 可讀性適合受眾
- 全文品牌語氣一致
- 清楚的價值主張
- 可執行的重點
- 適當的視覺格式
- 已針對平台最佳化

### 要避免的常見陷阱
- 研究關鍵字之前就開始寫
- 忽略平台專屬的要求
- 品牌語氣不一致
- SEO 過度最佳化（關鍵字堆砌）
- 缺少清楚的行動呼籲（CTA）
- 沒有校對就發布
- 忽略分析數據的回饋

## 績效指標

追蹤這些 KPI 來衡量內容的成效：

### 內容指標
- 自然流量成長
- 平均頁面停留時間
- 跳出率
- 社群分享數
- 獲得的反向連結

### 互動指標
- 留言與討論
- 電子郵件點閱率
- 社群媒體互動率
- 內容下載數
- 表單送出數

### 商業指標
- 產生的潛在客戶
- 轉換率
- 顧客取得成本
- 營收歸因
- 每篇內容的投資報酬率

## 整合點

本技能搭配以下工具效果最好：
- 分析平台（Google Analytics、社群媒體洞察）
- SEO 工具（用於關鍵字研究）
- 設計工具（用於視覺內容）
- 排程平台（用於內容發布）
- 電子郵件行銷系統（用於電子報內容）

## 快速指令

{{CODE:1}}
