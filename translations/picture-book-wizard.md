<!--meta
{"title":"繪本魔法師","category":"影片與多媒體","tags":["兒童繪本","雙語","圖片提示詞","教育"],
"summary":"產生高品質、風格一致的中英雙語兒童繪本，並為「banana nano」圖片生成器最佳化提示詞。支援 4 大類共 18 種視覺風格（含水墨、年畫、青花瓷、皮影等中國文化風格）、12 種場景、依 3–12 歲年齡動態調整內容，以及科學、數學、歷史、心理等學習領域；內建悅悅、小明、樂樂、美美四個角色。",
"usage":"- 指令：`/picture-book-wizard [風格] [場景] [年齡] [頁數-選填] [角色-選填] [靈魂-選填]`\n- 例如「用水彩風格做一本給 5 歲小孩、關於森林的繪本」\n- 預設角色為悅悅（5 歲，好奇溫柔）\n- 完整說明見 `SKILL-zh.md`（中文）或 `SKILL-en.md`（英文）"}
-->
---
name: picture-book-wizard
description: 一個專門的技能，使用「banana nano」產生高品質、一致的兒童雙語繪本。支援 4 大類共 18 種視覺風格（7 種核心兒童繪本風格、5 種氛圍風格、5 種中國文化風格、1 種專業風格）、12 種場景（5 種自然 + 7 種文化）、依年齡驅動的動態內容系統（3–12 歲），以及擴充的學習領域（科學、數學、歷史、心理學等）。當使用者想要製作繪本故事、提示詞或學習素材時使用。
argument-hint: "[style] [scene] [age] [pages-optional] [character-optional]"
---

# 繪本魔法師

專業的繪本創作技能，產生中英雙語的教育內容，並為「banana nano」產生器最佳化圖片提示詞。

---

## 語言版本

| 語言 | 檔案 | 說明 |
|----------|------|-------------|
| **英文** | [`SKILL-en.md`](./SKILL-en.md) | 完整英文文件 |
| **中文** | [`SKILL-zh.md`](./SKILL-zh.md) | 完整中文文件 |

---

## 快速開始

**用法**：`/picture-book-wizard [style] [scene] [age] [pages-optional] [character-optional] [soul-optional]`

### 範例
{{CODE:1}}

---

## 可用風格（共 18 種）

| 類別 | 風格 |
|----------|--------|
| **核心** | `storybook`、`watercolor`、`gouache`、`crayon`、`colored-pencil`、`clay`、`paper-cut` |
| **氛圍** | `dreamy`、`fairytale`、`collage`、`fabric`、`felt` |
| **中國文化** | `ink`、`ink-line`、`nianhua`、`porcelain`、`shadow-puppet` |
| **專業** | `tech` |

---

## 可用角色

| 角色 | 年齡 | 個性 |
|-----------|-----|-------------|
| `yueyue` 悅悅 | 5 歲 | 好奇溫柔（預設） |
| `xiaoming` 小明 | 6 歲 | 愛冒險有活力 |
| `lele` 樂樂 | 3 歲 | 開朗天真 |
| `meimei` 美美 | 4 歲 | 有創意愛想像 |

---

## 完整文件

請參考各語言版本的檔案：

- **英文**：[`SKILL-en.md`](./SKILL-en.md)
- **中文**：[`SKILL-zh.md`](./SKILL-zh.md)
