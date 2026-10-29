<!--meta
{"title":"Azure 故障診斷","category":"雲端與 DevOps","tags":["Azure","故障排除","AKS","KQL","Microsoft"],
"summary":"Microsoft 官方技能：用 AppLens、Azure Monitor、資源健康狀態與安全的分流流程，系統化診斷 Azure 正式環境問題——App Service 高 CPU/部署失敗、Container Apps 503、Functions 遙測中斷、AKS Pod 異常、VM 無法 RDP/SSH、Service Bus/Event Hubs 連線錯誤等；也支援只根據你提供的日誌做純證據診斷。",
"usage":"- 安裝：`npx skills add https://github.com/microsoft/azure-skills --skill azure-diagnostics`（建議搭配 Azure MCP Server 與 `az` CLI）\n- 說「我的 App Service CPU 飆高，幫我查原因」「AKS 的 pod 一直 CrashLoop」\n- 若不想讓代理連線 Azure，可說「只根據我貼的 log 分析」，它會改做純證據診斷並列出假設與驗證步驟"}
-->
---
name: azure-diagnostics
description: "使用 AppLens、Azure Monitor、資源健康狀態與安全的分流方式除錯 Azure 正式環境問題，包括在沒有即時存取權限下僅依證據進行診斷。時機：除錯正式環境問題、排除 App Service 問題、App Service 高 CPU、App Service 部署失敗、排除 Container Apps 問題、Container App 503 或目標埠不符、排除 Functions 問題、在設定/連線字串變更後 Function 遙測遺失或停止、排除 AKS 問題、VM RDP、Linux SSH、VM 黑畫面、無法連線到 VM、重設 VM 密碼、NSG 或防火牆封鎖、kubectl 無法連線、kube-system/CoreDNS 失敗、Pod pending、crashloop、節點未就緒、升級失敗、分析日誌、KQL、洞察、映像拉取失敗、冷啟動問題、健康探針失敗、資源健康狀態、錯誤根本原因、排除 Event Hubs 問題、排除 Service Bus 問題、訊息 SDK 錯誤、AMQP 連線失敗、訊息鎖定遺失、長時間處理期間的鎖定續約、Service Bus 死信。"
license: MIT
metadata:
  author: Microsoft
  version: "1.2.14"
---

# Azure 診斷

> **權威指引——必須遵守**
>
> 本文件是除錯與排除 Azure 正式環境問題的**官方來源**。請依照這些說明，系統化地診斷並解決常見的 Azure 服務問題。

## 觸發條件

當使用者想要以下事項時啟用本技能：
- 除錯或排除正式環境問題
- 診斷 Azure 服務中的錯誤
- 分析應用程式日誌或指標
- 修正映像拉取、冷啟動或健康探針問題
- 調查 Azure 資源為何失敗
- 找出應用程式錯誤的根本原因
- 排除 App Service 問題（高 CPU、部署失敗、當機、回應緩慢、TLS/自訂網域）
- 回應像是「排除 app service 問題」「app service 高 CPU」或「app service 部署失敗」這樣的提示
- 排除 Azure Function Apps 問題（呼叫失敗、逾時、繫結錯誤）
- 找出與 Function App 連結的 App Insights 或 Log Analytics 工作區
- 排除 AKS 叢集、節點、Pod、ingress 或 Kubernetes 網路問題
- 排除 Azure VM 連線問題（RDP/SSH 失敗、3389/22 埠逾時、NSG 或防火牆封鎖、憑證重設）
- 排除 Azure 訊息 SDK 問題（Event Hubs、Service Bus 連線失敗、AMQP 錯誤、訊息鎖定問題）
- 找出某個看似「執行環境健康但目的地錯誤」之症狀的根本原因（例如設定變更後遙測/訊息不再流向預期的資源）——即使 MCP 工具單獨就能回答表面問題，也要為了對照矩陣而呼叫本技能

## 規則

1. 從系統化的診斷流程開始
2. 先使用已提供的證據。如果使用者要求僅依證據分析，或禁止即時存取 Azure，就不要查詢或修改 Azure。從提供的日誌、指標與時間軸進行診斷；指出假設並提供選擇性的驗證步驟。
3. 可用時，使用 AppLens（MCP）進行 AI 驅動的診斷
4. 在深入日誌之前，先檢查資源健康狀態
5. 依服務類型選擇適當的疑難排解指南
6. 記錄發現與嘗試過的修復步驟
7. 在允許即時蒐集且已知識別碼時，優先使用內附的診斷腳本，而非臨時呼叫。如果已提供的證據足夠或禁止即時存取，就不要執行它們；否則先執行適用的腳本。
8. 把 AKS 事件導向專門的 AKS 疑難排解文件
9. 即使選用的 `aks-skills` 附加元件不存在、被拒絕或主機不支援，也要保持基本的 AKS 診斷可用

---

## 快速診斷流程

1. **辨識症狀**——什麼東西失敗了？
2. **檢查資源健康狀態**——Azure 本身健康嗎？
3. **檢閱日誌**——日誌顯示什麼？
4. **分析指標**——有什麼效能模式？
5. **調查近期變更**——改了什麼？

---

## 依服務分類的疑難排解指南

| 服務 | 常見問題 | 參考 |
|------|----------|------|
| **Container Apps** | 映像拉取失敗、冷啟動、健康探針、埠不符 | [container-apps/](references/container-apps/README.md) |
| **App Service** | 高 CPU、部署失敗、當機、回應緩慢、TLS/自訂網域 | [app-service/](references/app-service/README.md) |
| **Function Apps** | 應用程式詳細資訊、呼叫失敗、逾時、繫結錯誤、冷啟動、缺少應用程式設定 | [functions/](references/functions/README.md) |
| **AKS** | 叢集存取、節點、`kube-system`、排程、crash loop、ingress、DNS、升級 | [AKS 疑難排解](troubleshooting/aks/aks-troubleshooting.md) |
| **運算** | VM RDP/SSH 連線、NSG/防火牆封鎖、憑證重設、VM 代理程式/工具問題 | [VM 連線疑難排解](troubleshooting/compute/vm-troubleshooting.md) |
| **訊息** | Event Hubs 與 Service Bus SDK 錯誤、AMQP 失敗、訊息鎖定、連線 | [訊息疑難排解](troubleshooting/messaging/README.md) |

---

## 路由

- Container Apps 與 Function Apps 的診斷保留在這個父技能中。
- 把進行中的 AKS 事件、AKS 專屬的受理、證據蒐集與修復指引導向 [AKS 疑難排解](troubleshooting/aks/aks-troubleshooting.md)。
- 把 Azure VM 的 RDP/SSH 連線、NSG/防火牆、憑證重設與 VM 代理程式疑難排解導向 [VM 連線疑難排解](troubleshooting/compute/vm-troubleshooting.md)。
- 把 Azure 訊息 SDK 疑難排解（Event Hubs、Service Bus）導向 [訊息疑難排解](troubleshooting/messaging/README.md)。

---

## 快速參考

### 常用診斷指令

{{CODE:1}}

### AppLens（MCP 工具）

進行 AI 驅動的診斷時使用：
{{CODE:2}}

### Azure Monitor（MCP 工具）

查詢日誌與指標：
{{CODE:3}}

常用的診斷查詢請見 [kql-queries.md](references/kql-queries.md)。

---

## 檢查 Azure 資源健康狀態

### 使用 MCP

{{CODE:4}}

### 使用 CLI

{{CODE:5}}

---

## 參考資料

- [KQL 查詢庫](references/kql-queries.md)
- [Azure Resource Graph 查詢](references/azure-resource-graph.md)
- [App Service 疑難排解](references/app-service/README.md)
- [Function Apps 疑難排解](references/functions/README.md)
- [VM 連線疑難排解](troubleshooting/compute/vm-troubleshooting.md)
- [訊息疑難排解](troubleshooting/messaging/README.md)
