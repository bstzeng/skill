<!--meta
{"title":"部署到 Vercel","category":"雲端與 DevOps","tags":["Vercel","部署","預覽環境","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：把任何專案立即部署到 Vercel，預設一律部署為預覽版（除非你明確要正式環境）。沒有安裝 Vercel CLI 或未登入時，改用內附腳本免驗證部署，並回傳預覽網址與認領網址。",
"usage":"- Codex：`$skill-installer vercel-deploy`\n- 說「部署我的 app 並給我連結」「push this live」「建一個預覽部署」\n- 部署指令逾時設 10 分鐘；免登入部署完成後可用 claimUrl 把專案認領到自己的帳號"}
-->
---
name: vercel-deploy
description: 把應用程式與網站部署到 Vercel。當使用者要求部署動作，例如「部署我的 app」「部署並給我連結」「讓它上線」或「建立預覽部署」時使用。
---

# Vercel 部署

立即把任何專案部署到 Vercel。除非使用者明確要求正式環境，否則**一律部署為預覽版**（而不是正式環境）。

## 前置條件

- 在**不**提升權限的情況下檢查是否已安裝 Vercel CLI（例如 `command -v vercel`）。
- 只有在沙箱阻擋了部署的網路呼叫時，才對實際的部署指令提升權限（`sandbox_permissions=require_escalated`）。
- 部署可能需要幾分鐘。使用適當的逾時值。

## 快速開始

1. 檢查是否已安裝 Vercel CLI（這個檢查不提升權限）：

{{CODE:1}}

2. 如果已安裝 `vercel`，執行這個（逾時 10 分鐘）：
{{CODE:2}}

**重要：** 部署指令使用 10 分鐘（600000ms）的逾時，因為建置可能需要一段時間。

3. 如果沒有安裝 `vercel`，或 CLI 失敗並顯示「No existing credentials found」，就使用下方的備案方法。

## 備案（不需驗證）

如果 CLI 因驗證錯誤而失敗，使用部署腳本：

{{CODE:3}}

這個腳本會處理框架偵測、打包與部署。它會等待建置完成，並回傳含有 `previewUrl` 與 `claimUrl` 的 JSON。

**告訴使用者：**「你的部署已就緒，網址是 [previewUrl]。到 [claimUrl] 認領它以管理你的部署。」

## 正式環境部署

只有在使用者明確要求時：
{{CODE:4}}

## 輸出

把部署網址給使用者看。對於備案部署，也要給認領網址。

**不要**用 curl 或抓取部署好的網址來驗證它是否運作。只要回傳連結即可。

## 疑難排解

### 提升的網路存取

如果部署因網路問題（逾時、DNS 錯誤、連線重設）而失敗，就以提升的權限重新執行實際的部署指令（使用 `sandbox_permissions=require_escalated`）。不要對 `command -v vercel` 安裝檢查提升權限。當沙箱網路阻擋對外請求時，部署需要提升的網路存取。

給使用者的指引範例：

{{CODE:5}}
