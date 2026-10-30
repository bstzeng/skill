<!--meta
{"title":"ASP.NET Core 開發","category":"程式品質與除錯","tags":["ASP.NET Core",".NET","Blazor","Web API","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：依微軟目前的官方指引建構、審查、重構或設計 ASP.NET Core 網頁應用——Blazor、Razor Pages、MVC、Minimal API、Web API、SignalR、gRPC、中介軟體、DI、驗證授權、測試、效能、部署與版本升級。新專案預設 .NET 10。",
"usage":"- Codex：`$skill-installer aspnet-core`\n- 說「用 Minimal API 做一個待辦清單 API 並加上 JWT 驗證」「把這個 Startup.cs 專案升級到 .NET 10」\n- 代理只會載入與任務相符的最少參考檔（例如 stack-selection + 一個主要應用模型）\n- 會尊重既有應用模型，不會無故把 Razor Pages 改寫成 MVC"}
-->
---
name: aspnet-core
description: 依照目前官方的 .NET 網頁開發指引，建構、審查、重構或設計 ASP.NET Core 網頁應用程式。在處理 Blazor Web App、Razor Pages、MVC、Minimal API、以 controller 為基礎的 Web API、SignalR、gRPC、中介軟體、相依注入、設定、驗證、授權、測試、效能、部署或 ASP.NET Core 升級時使用。
---

# ASP.NET Core

## 概述

選擇正確的 ASP.NET Core 應用程式模型、正確組合主機與請求管線，並以微軟目前文件所記載的框架風格實作功能。

載入符合任務的最小參考集合。預設不要載入每一份參考。

## 工作流程

1. 確認目標框架、SDK 與目前的應用程式模型。
2. 對於新應用程式或重大重構，先開啟 [references/stack-selection.md](references/stack-selection.md)。
3. 接著開啟 [references/program-and-pipeline.md](references/program-and-pipeline.md)，處理 `Program.cs`、DI、設定、中介軟體、路由、日誌與靜態資產。
4. 恰好開啟一份主要的應用程式模型參考：
   - [references/ui-blazor.md](references/ui-blazor.md)
   - [references/ui-razor-pages.md](references/ui-razor-pages.md)
   - [references/ui-mvc.md](references/ui-mvc.md)
   - [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md)
5. 只在需要時加入跨領域的參考：
   - [references/data-state-and-services.md](references/data-state-and-services.md)
   - [references/security-and-identity.md](references/security-and-identity.md)
   - [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md)
   - [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md)
6. 在把新的平台 API 引入較舊的解決方案之前，或在主要版本之間遷移時，開啟 [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md)。
7. 當你需要的任務沒有被聚焦的參考涵蓋時，使用 [references/source-map.md](references/source-map.md) 找到對應的 Microsoft Learn 章節。

## 預設的操作假設

- 除非 repo 或使用者的請求固定了較舊的目標，否則優先使用最新的穩定版 ASP.NET Core 與 .NET。
- 截至 2026 年 3 月，新的正式環境工作優先使用 .NET 10 / ASP.NET Core 10。除非使用者明確要求預覽功能，否則把 ASP.NET Core 11 視為預覽版。
- 優先使用 `WebApplicationBuilder` 與 `WebApplication`。除非程式碼庫已經在用或任務是遷移，否則避免較舊的 `Startup` 與 `WebHost` 模式。
- 在加入第三方基礎設施之前，優先使用內建的 DI、options/設定、日誌、ProblemDetails、OpenAPI、健康檢查、速率限制、輸出快取與 Identity。
- 讓功能切片保持凝聚，使頁面、元件、端點、controller、驗證、服務、資料存取與測試都容易追蹤。
- 尊重既有的應用程式模型。沒有明確理由，不要把 Razor Pages 改寫成 MVC，或把 controller 改寫成 Minimal API。

## 參考指南

- [references/_sections.md](references/_sections.md)：快速索引與閱讀順序。
- [references/stack-selection.md](references/stack-selection.md)：選擇正確的 ASP.NET Core 應用程式模型與模板。
- [references/program-and-pipeline.md](references/program-and-pipeline.md)：組織 `Program.cs`、服務、中介軟體、路由、設定、日誌與靜態資產。
- [references/ui-blazor.md](references/ui-blazor.md)：建構 Blazor Web App、選擇渲染模式，並正確使用元件、表單與 JS interop。
- [references/ui-razor-pages.md](references/ui-razor-pages.md)：以處理常式、模型繫結與慣例建構以頁面為中心的伺服器端渲染應用程式。
- [references/ui-mvc.md](references/ui-mvc.md)：建構關注點分離清楚的 controller/view 應用程式。
- [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md)：以 Minimal API 或 controller 建構 HTTP API，包括驗證與回應模式。
- [references/data-state-and-services.md](references/data-state-and-services.md)：負責任地使用 EF Core、`DbContext`、options、`IHttpClientFactory`、session、temp data 與應用程式狀態。
- [references/security-and-identity.md](references/security-and-identity.md)：套用驗證、授權、Identity、機密、資料保護、CORS、CSRF 與 HTTPS 指引。
- [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md)：使用 SignalR、gRPC 與託管服務。
- [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md)：加入整合測試、瀏覽器測試、快取、壓縮、健康檢查、速率限制與部署考量。
- [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md)：處理目標框架、破壞性變更、過時的 API 與遷移。
- [references/source-map.md](references/source-map.md)：把官方 ASP.NET Core 文件樹對應到本技能中的參考。

## 執行注意事項

- 產生新程式碼時，從正確的 `dotnet new` 模板開始，並讓產生的結構保持可辨識。
- 編輯既有的解決方案時，先遵循該解決方案的慣例，並用這些參考避免誤用框架或使用過時的模式。
- 當任務提到「最新」時，在依賴記憶之前，先在 Microsoft Learn 或 ASP.NET Core 文件 repo 上確認該功能。
