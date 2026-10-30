<!--meta
{"title": "飛書 OpenAPI 探索器", "category": "文件與辦公", "tags": ["飛書", "Lark", "OpenAPI", "lark-cli", "API 探索"], "summary": "當現有 lark-* 技能或 lark-cli 指令都做不到時，從飛書／Lark 官方 Markdown 文件庫逐層找出原生 OpenAPI 介面，再用 `lark-cli api` 直接呼叫完成任務。原文為簡體中文，以 OpenCC 轉為台灣繁體。", "usage": "- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-openapi-explorer`（需 `lark-cli` 與 lark-shared）\n- 說「飛書有沒有 API 可以批次修改群組設定？幫我查並呼叫」\n- 代理會先確認既有指令不夠用，再從 `open.feishu.cn/llms.txt` 逐層找到正確的 API 文件，不會憑空猜 API"}
-->
---
name: lark-openapi-explorer
version: 1.0.0
description: "飛書/Lark 原生 OpenAPI 探索：從官方文件庫中挖掘未經 CLI 封裝的原生 OpenAPI 介面。當使用者的需求無法被現有 lark-* skill 或 lark-cli 已註冊命令滿足，需要查詢並呼叫原生飛書 OpenAPI 時使用。"
metadata:
  requires:
    bins: ["lark-cli"]
---

# OpenAPI Explorer

> **前置條件：** 先閱讀 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 瞭解認證、身份切換和安全規則。

當使用者的需求**無法被現有 skill 或 CLI 已註冊 API 覆蓋**時，使用本技能從飛書官方 markdown 文件庫中逐層挖掘原生 OpenAPI 介面，然後透過 `lark-cli api` 裸調完成任務。

## 文件庫結構

飛書 OpenAPI 文件以 markdown 層級組織：

{{CODE:1}}

文件入口：

| 品牌 | 入口 URL |
|------|----------|
| 飛書 (Feishu) | `https://open.feishu.cn/llms.txt` |
| Lark | `https://open.larksuite.com/llms.txt` |

> 所有文件以**中文**編寫。如果使用者使用英文交流，需將文件內容翻譯為英文後輸出。

## 挖掘流程

嚴格按以下步驟逐層檢索，**不要跳步或猜測 API**：

### Step 1：確認現有能力不足

{{CODE:2}}

如果已有對應命令或 shortcut，直接使用，**不需要繼續挖掘**。

### Step 2：從頂層索引定位模組

用 WebFetch 獲取頂層索引，找到與需求相關的模組文件連結：

{{CODE:3}}

- 飛書品牌使用 `open.feishu.cn`
- Lark 品牌使用 `open.larksuite.com`
- 如不確定使用者品牌，預設使用飛書

### Step 3：從模組文件定位具體 API

用 WebFetch 獲取模組文件，找到具體 API 的文件連結：

{{CODE:4}}

### Step 4：獲取 API 完整規範

用 WebFetch 獲取具體 API 文件，提取完整的呼叫規範：

{{CODE:5}}

### Step 5：透過 CLI 呼叫 API

使用 `lark-cli api` 裸調：

{{CODE:6}}

## 輸出規範

向使用者呈現挖掘結果時，按以下格式組織：

1. **API 名稱與功能**：一句話描述
2. **HTTP 方法與路徑**：`METHOD /open-apis/...`
3. **關鍵引數**：列出必填和常用可選引數
4. **所需許可權**：scope 列表
5. **呼叫示例**：給出 `lark-cli api` 的完整命令
6. **注意事項**：頻率限制、特殊約束等

如果使用者使用英文交流，將以上所有內容翻譯為英文。

## 安全規則

- **寫入/刪除類 API**（POST/PUT/DELETE）呼叫前必須確認使用者意圖
- 建議先用 `--dry-run` 預覽請求（如支援）
- 不要猜測 API 路徑或引數——必須從文件中獲取確認
- 涉及敏感操作（刪除群、移除成員等）時，向使用者說明影響範圍

## 使用場景示例

### 場景 1：使用者需要拉人進群（未被 CLI 封裝）

{{CODE:7}}

### 場景 2：使用者需要設定群公告

{{CODE:8}}

## 參考

- [lark-shared](../lark-shared/SKILL.md) — 認證和全域性引數
- [lark-skill-maker](../lark-skill-maker/SKILL.md) — 如需將挖掘到的 API 固化為新 Skill
