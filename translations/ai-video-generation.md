<!--meta
{"title":"AI 影片生成","category":"影片與多媒體","tags":["AI 影片","文字轉影片","圖片轉影片","對嘴","Veo","Seedance"],
"summary":"透過 inference.sh 的 `belt` CLI，一次串接 40 多種 AI 影片模型（Google Veo 3.1、Seedance 2.0、HappyHorse、Wan 2.5、Grok、OmniHuman 等），支援文字轉影片、圖片轉影片、參考轉影片、影片編輯、對嘴、虛擬人像、畫質提升與擬音音效。",
"usage":"- 安裝：`npx skills add https://github.com/101-skills/superpowers --skill ai-video-generation`，另需 `npx skills add belt-sh/cli` 並安裝 `belt` CLI 登入\n- 說「用 Veo 3.1 生成一段 8 秒海邊日落的影片」「把這張產品照做成旋轉展示影片」\n- 用 `belt app list --category video` 瀏覽所有模型；各模型按次計費"}
-->
---
name: ai-video-generation
description: "透過 inference.sh CLI，使用 Google Veo、Seedance 2.0、HappyHorse、Wan、Grok 與 40 多種模型生成 AI 影片。模型：Veo 3.1、Veo 3、Seedance 2.0、HappyHorse 1.0、Wan 2.5、Grok Imagine Video、OmniHuman、Fabric、HunyuanVideo。能力：文字轉影片、圖片轉影片、參考轉影片、影片編輯、對嘴、虛擬人像動畫、影片畫質提升、擬音音效。用於：社群媒體影片、行銷內容、解說影片、產品示範、AI 虛擬人像。觸發詞：video generation、ai video、text to video、image to video、veo、animate image、video from image、ai animation、video generator、generate video、t2v、i2v、ai video maker、create video with ai、runway alternative、pika alternative、sora alternative、kling alternative、seedance、happyhorse"
allowed-tools: Bash(belt *)
---

> **安裝 belt CLI 技能：** `npx skills add belt-sh/cli`

# AI 影片生成

透過 [inference.sh](https://inference.sh) CLI 使用 40 多種 AI 模型生成影片。

![AI 影片生成](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg2c0egyg243mnyth4y6g51q.jpeg)

## 快速開始

> 需要 inference.sh CLI（`belt`）。[安裝說明](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

{{CODE:1}}


## 可用模型

### 文字轉影片

| 模型 | App ID | 最適合 |
|------|--------|--------|
| Veo 3.1 Fast | `google/veo-3-1-fast` | 快速，可選擇加入音訊 |
| Veo 3.1 | `google/veo-3-1` | 最佳品質，影格插補 |
| Veo 3 | `google/veo-3` | 高品質，含音訊 |
| Veo 3 Fast | `google/veo-3-fast` | 快速，含音訊 |
| Veo 2 | `google/veo-2` | 寫實影片 |
| **P-Video** | `pruna/p-video` | 快速、經濟，支援音訊 |
| **WAN-T2V** | `pruna/wan-t2v` | 經濟的 480p/720p |
| Grok Video | `xai/grok-imagine-video` | xAI，可設定長度 |
| **Seedance 2.0** | `bytedance/seedance-2-0` | 文字/圖片/參考轉影片，同步音訊，最高 1080p |
| **Seedance 2.0 Fast** | `bytedance/seedance-2-0-fast` | 快速版，能力相同 |
| **HappyHorse T2V** | `alibaba/happyhorse-1-0-t2v` | 物理擬真，最長 15 秒 |

### 圖片轉影片

| 模型 | App ID | 最適合 |
|------|--------|--------|
| Wan 2.5 | `falai/wan-2-5` | 讓任何圖片動起來 |
| Wan 2.5 I2V | `falai/wan-2-5-i2v` | 高品質圖片轉影片 |
| **WAN-I2V** | `pruna/wan-i2v` | 經濟的 480p/720p |
| **P-Video** | `pruna/p-video` | 快速圖片轉影片，含音訊 |
| **Seedance 2.0** | `bytedance/seedance-2-0` | 讓圖片動起來並同步音訊，最高 1080p |
| **Seedance 2.0 Fast** | `bytedance/seedance-2-0-fast` | 快速版，能力相同 |
| **HappyHorse I2V** | `alibaba/happyhorse-1-0-i2v` | 讓圖片動起來，最高 1080P/15 秒 |
| **HappyHorse R2V** | `alibaba/happyhorse-1-0-r2v` | 依參考保持角色一致 |

### 虛擬人像 / 對嘴

| 模型 | App ID | 最適合 |
|------|--------|--------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 多角色 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 單一角色 |
| Fabric 1.0 | `falai/fabric-1-0` | 讓圖片開口說話並對嘴 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 寫實對嘴 |

### 影片編輯

| 模型 | App ID | 最適合 |
|------|--------|--------|
| HappyHorse Edit | `alibaba/happyhorse-1-0-video-edit` | 用自然語言編輯影片 |

### 工具

| 工具 | App ID | 說明 |
|------|--------|------|
| HunyuanVideo Foley | `infsh/hunyuanvideo-foley` | 為影片加入音效 |
| Topaz Upscaler | `falai/topaz-video-upscaler` | 提升影片畫質 |
| Media Merger | `infsh/media-merger` | 以轉場合併影片 |

## 瀏覽所有影片應用

{{CODE:2}}

## 範例

### 用 Veo 做文字轉影片

{{CODE:3}}

### Grok Video

{{CODE:4}}

### 用 Wan 2.5 做圖片轉影片

{{CODE:5}}

### AI 虛擬人像 / 說話人頭

{{CODE:6}}

### Fabric 對嘴

{{CODE:7}}

### Seedance 2.0 文字轉影片（含音訊）

{{CODE:8}}

### Seedance 2.0 圖片轉影片

{{CODE:9}}

### Seedance 2.0 參考轉影片

{{CODE:10}}

### HappyHorse 文字轉影片

{{CODE:11}}

### HappyHorse 影片編輯

{{CODE:12}}

### PixVerse 對嘴

{{CODE:13}}

### 影片畫質提升

{{CODE:14}}

### 加入音效（擬音）

{{CODE:15}}

### 合併影片

{{CODE:16}}

## 相關技能

{{CODE:17}}

瀏覽所有應用：`belt app list`

## 文件

- [執行應用](https://inference.sh/docs/apps/running) - 如何透過 CLI 執行應用
- [串流結果](https://inference.sh/docs/api/sdk/streaming) - 即時進度更新
- [內容產線範例](https://inference.sh/docs/examples/content-pipeline) - 建構媒體工作流程
