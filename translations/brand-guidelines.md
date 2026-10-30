<!--meta
{"title":"Anthropic 品牌規範","category":"前端與設計","tags":["品牌","配色","字體","簡報樣式","Anthropic 官方"],
"summary":"Anthropic 官方範例技能：把 Anthropic 官方品牌色（深 #141413、淺 #faf9f5、橘 #d97757 等）與字體（標題 Poppins、內文 Lora）套用到簡報、文件等產出物上。也是「把自家公司品牌規範做成 skill」的參考範本。",
"usage":"- 安裝：`npx skills add https://github.com/anthropics/skills --skill brand-guidelines`\n- 說「把這份簡報改成 Anthropic 品牌風格」\n- 想做自己公司的版本：複製這個 skill，把顏色與字體換成自家品牌即可"}
-->
---
name: brand-guidelines
description: 把 Anthropic 官方的品牌色與字體套用到任何可能因擁有 Anthropic 外觀而受益的產出物上。當涉及品牌色或樣式規範、視覺格式，或公司設計標準時使用。
license: 完整條款見 LICENSE.txt
---

# Anthropic 品牌樣式

## 概述

要取用 Anthropic 官方的品牌識別與樣式資源，請使用本技能。

**關鍵字**：品牌、企業識別、視覺識別、後製、樣式、品牌色、字體排印、Anthropic 品牌、視覺格式、視覺設計

## 品牌規範

### 色彩

**主要色彩：**

- 深色：`#141413` ——主要文字與深色背景
- 淺色：`#faf9f5` ——淺色背景與深色背景上的文字
- 中灰：`#b0aea5` ——次要元素
- 淺灰：`#e8e6dc` ——低調的背景

**強調色：**

- 橘色：`#d97757` ——主要強調色
- 藍色：`#6a9bcc` ——次要強調色
- 綠色：`#788c5d` ——第三強調色

### 字體排印

- **標題**：Poppins（備援為 Arial）
- **內文**：Lora（備援為 Georgia）
- **注意**：為取得最佳效果，字型應預先安裝在你的環境中

## 功能

### 智慧字型套用

- 對標題（24pt 以上）套用 Poppins 字型
- 對內文套用 Lora 字型
- 自訂字型無法使用時，自動退回 Arial/Georgia
- 在所有系統上保持可讀性

### 文字樣式

- 標題（24pt+）：Poppins 字型
- 內文：Lora 字型
- 依背景智慧選擇顏色
- 保留文字層級與格式

### 形狀與強調色

- 非文字的形狀使用強調色
- 在橘、藍、綠三種強調色之間循環
- 在符合品牌的同時維持視覺趣味

## 技術細節

### 字型管理

- 可用時使用系統已安裝的 Poppins 與 Lora 字型
- 自動退回 Arial（標題）與 Georgia（內文）
- 不需安裝字型——可搭配既有的系統字型運作
- 為取得最佳效果，請在環境中預先安裝 Poppins 與 Lora 字型

### 色彩套用

- 使用 RGB 色值以精準符合品牌
- 透過 python-pptx 的 RGBColor 類別套用
- 在不同系統之間維持色彩一致
