<!--meta
{"title":"PostgreSQL 唯讀查詢","category":"雲端與 DevOps","tags":["PostgreSQL","SQL","資料庫","唯讀"],
"summary":"安全地對多個 PostgreSQL 資料庫執行唯讀 SQL 查詢：探索結構與資料表、執行 SELECT 做資料分析、檢查資料內容。可設定多組連線並附描述，讓 Claude 依問題自動挑選資料庫；以唯讀工作階段、只允許 SELECT／SHOW／EXPLAIN／WITH、單一敘述、30 秒逾時與每次最多 1 萬列等機制，擋下所有寫入操作。",
"usage":"- 需要 Python 3.8+ 與 `pip install -r requirements.txt`（psycopg2-binary）\n- 在技能目錄或 `~/.config/claude/postgres-connections.json` 建立連線設定，並 `chmod 600`\n- 說「列出有哪些資料庫」「查一下上個月訂單最多的 10 位客戶」\n- 不確定用哪個資料庫時會先 `--list` 再問你"}
-->
---
name: postgres
description: "對多個 PostgreSQL 資料庫執行唯讀的 SQL 查詢。在以下情況使用：(1) 查詢 PostgreSQL 資料庫，(2) 探索資料庫結構／資料表，(3) 為資料分析執行 SELECT 查詢，(4) 檢查資料庫內容。支援多組附描述的資料庫連線，以便智慧地自動選擇。為了安全，封鎖所有寫入操作（INSERT、UPDATE、DELETE、DROP 等）。"
license: Apache-2.0
metadata:
  author: sanjay3290
  version: "1.0"
---

# PostgreSQL 唯讀查詢技能

對設定好的 PostgreSQL 資料庫執行安全的唯讀查詢。

## 需求

- Python 3.8+
- psycopg2-binary：`pip install -r requirements.txt`

## 設定

在技能目錄或 `~/.config/claude/postgres-connections.json` 建立 `connections.json`。

**安全**：因為檔案包含憑證，把權限設為 `600`：
{{CODE:1}}

{{CODE:2}}

### 設定欄位

| 欄位 | 必要 | 說明 |
|-------|----------|-------------|
| name | 是 | 資料庫的識別名稱（不分大小寫） |
| description | 是 | 這個資料庫包含哪些資料（用於自動選擇） |
| host | 是 | 資料庫主機名稱 |
| port | 否 | 連接埠號碼（預設：5432） |
| database | 是 | 資料庫名稱 |
| user | 是 | 使用者名稱 |
| password | 是 | 密碼 |
| sslmode | 否 | SSL 模式：disable、allow、prefer（預設）、require、verify-ca、verify-full |

## 用法

### 列出設定的資料庫
{{CODE:3}}

### 查詢資料庫
{{CODE:4}}

### 列出資料表
{{CODE:5}}

### 顯示結構
{{CODE:6}}

### 限制結果數量
{{CODE:7}}

## 選擇資料庫

把使用者的意圖對應到資料庫的 `description`：

| 使用者問的是 | 尋找描述中包含 |
|-----------------|--------------------------------|
| 使用者、帳號 | users、accounts、customers |
| 訂單、銷售 | orders、transactions、sales |
| 分析、指標 | analytics、metrics、reports |
| 日誌、事件 | logs、events、audit |

如果不清楚，執行 `--list` 並詢問使用者要用哪個資料庫。

## 安全功能

- **唯讀工作階段**：連線使用 PostgreSQL 的 `readonly=True` 模式（主要防護）
- **查詢驗證**：只允許 SELECT、SHOW、EXPLAIN、WITH 查詢
- **單一敘述**：拒絕一次查詢中有多個敘述
- **SSL 支援**：可設定加密連線的 SSL 模式
- **查詢逾時**：強制 30 秒的敘述逾時
- **記憶體保護**：每次查詢最多 10,000 列，避免記憶體不足
- **欄寬上限**：每欄最多 100 個字元，讓輸出易讀
- **憑證清理**：錯誤訊息不會洩露密碼

## 疑難排解

| 錯誤 | 解法 |
|-------|----------|
| 找不到設定 | 在技能目錄中建立 `connections.json` |
| 認證失敗 | 檢查設定中的使用者名稱／密碼 |
| 連線逾時 | 確認主機／連接埠，檢查防火牆／VPN |
| SSL 錯誤 | 本機資料庫試試 `"sslmode": "disable"` |
| 權限警告 | 執行 `chmod 600 connections.json` |

## 結束碼

- **0**：成功
- **1**：錯誤（缺少設定、認證失敗、無效的查詢、資料庫錯誤）

## 工作流程

1. 執行 `--list` 顯示可用的資料庫
2. 把使用者的意圖對應到資料庫描述
3. 執行 `--tables` 或 `--schema` 探索結構
4. 以適當的 LIMIT 執行查詢
