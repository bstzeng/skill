<!--meta
{"title":"AI 圖片生成","category":"影片與多媒體","tags":["AI 繪圖","文字轉圖片","圖片編輯","FLUX","GPT-Image"],
"summary":"透過 inference.sh 的 `belt` CLI，串接 50 多種 AI 圖片模型（GPT-Image-2、FLUX、Gemini 3 Pro、Grok、Seedream 4.5、Reve 等），支援文字轉圖片、圖片轉圖片、局部重繪、LoRA 風格、圖片編輯、放大與文字渲染。",
"usage":"- 安裝：`npx skills add https://github.com/101-skills/superpowers --skill ai-image-generation`，另需 `npx skills add belt-sh/cli` 並安裝 `belt` CLI\n- 說「用 FLUX 生成一張賽博龐克風格的台北夜景」「把這張產品圖背景換成大理石桌面」\n- 需要清楚文字的海報可選 Reve 或 Seedream 3.0；最便宜的是 FLUX Klein 4B（約 $0.0001/張）"}
-->
---
name: ai-image-generation
description: "透過 inference.sh CLI，使用 GPT-Image-2、FLUX、Gemini、Grok、Seedream、Reve 與 50 多種模型生成 AI 圖片。模型：GPT-Image-2、FLUX Dev LoRA、FLUX.2 Klein LoRA、Gemini 3 Pro Image、Grok Imagine、Seedream 4.5、Reve、ImagineArt。能力：文字轉圖片、圖片轉圖片、局部重繪、LoRA、圖片編輯、畫質放大、文字渲染。用於：AI 藝術、產品模擬圖、概念美術、社群媒體圖像、行銷視覺、插畫。觸發詞：flux、image generation、ai image、text to image、stable diffusion、generate image、ai art、midjourney alternative、dall-e alternative、text2img、t2i、image generator、ai picture、create image with ai、generative ai、ai illustration、grok image、gemini image、gpt image、openai image、chatgpt image"
allowed-tools: Bash(belt *)
---

> **安裝 belt CLI 技能：** `npx skills add belt-sh/cli`

# AI 圖片生成

透過 [inference.sh](https://inference.sh) CLI 使用 50 多種 AI 模型生成圖片。

![AI 圖片生成](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0v0nz7wv0qwqjtq1cam52z.jpeg)

## 快速開始

> 需要 inference.sh CLI（`belt`）。[安裝說明](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

{{CODE:1}}


## 可用模型

| 模型 | App ID | 最適合 |
|------|--------|--------|
| **GPT-Image-2** | `openai/gpt-image-2` | 文字轉圖片、編輯、局部重繪 |
| FLUX Dev LoRA | `falai/flux-dev-lora` | 高品質，可自訂風格 |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | 快速，支援 LoRA（4B/9B） |
| **P-Image** | `pruna/p-image` | 快速、經濟，多種長寬比 |
| **P-Image-LoRA** | `pruna/p-image-lora` | 快速，內建 LoRA 風格 |
| **P-Image-Edit** | `pruna/p-image-edit` | 快速圖片編輯 |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Google 最新模型 |
| Gemini 2.5 Flash | `google/gemini-2-5-flash-image` | 快速的 Google 模型 |
| Grok Imagine | `xai/grok-imagine-image` | xAI 的模型，多種長寬比 |
| Seedream 4.5 | `bytedance/seedream-4-5` | 2K–4K 電影級品質 |
| Seedream 4.0 | `bytedance/seedream-4-0` | 高品質 2K–4K |
| Seedream 3.0 | `bytedance/seedream-3-0-t2i` | 精準的文字渲染 |
| Reve | `falai/reve` | 自然語言編輯、文字渲染 |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | 超高擬真 4K |
| FLUX Klein 4B | `pruna/flux-klein-4b` | 超便宜（每張 $0.0001） |
| Topaz Upscaler | `falai/topaz-image-upscaler` | 專業級放大 |

## 瀏覽所有圖片應用

{{CODE:2}}

## 範例

### GPT-Image-2

{{CODE:3}}

### GPT-Image-2 編輯

{{CODE:4}}

### 用 FLUX 做文字轉圖片

{{CODE:5}}

### 用 FLUX Klein 快速生成

{{CODE:6}}

### Google Gemini 3 Pro

{{CODE:7}}

### Grok Imagine

{{CODE:8}}

### Reve（含文字渲染）

{{CODE:9}}

### Seedream 4.5（4K 品質）

{{CODE:10}}

### 圖片放大

{{CODE:11}}

### 拼接多張圖片

{{CODE:12}}

## 相關技能

{{CODE:13}}

瀏覽所有應用：`belt app list`

## 文件

- [執行應用](https://inference.sh/docs/apps/running) - 如何透過 CLI 執行應用
- [圖片生成範例](https://inference.sh/docs/examples/image-generation) - 完整的圖片生成指南
- [應用總覽](https://inference.sh/docs/apps/overview) - 了解應用生態系
