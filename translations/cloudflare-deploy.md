<!--meta
{"title":"部署到 Cloudflare","category":"雲端與 DevOps","tags":["Cloudflare","Workers","Pages","部署","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：在 Cloudflare 平台上建構與部署應用和基礎設施——Workers、Pages、Durable Objects、KV、D1、R2、Workers AI、Tunnel、WAF 等。用決策樹（「我要跑程式」「我要存資料」「我要 AI」……）找出合適的產品，再載入詳細參考。部署前必先確認 wrangler 驗證。",
"usage":"- Codex：`$skill-installer cloudflare-deploy`\n- 說「把這個網站部署到 Cloudflare Pages」「我需要一個存使用者上傳檔案的地方，用 Cloudflare 哪個產品？」\n- 本機用 `wrangler login`、CI 用 `CLOUDFLARE_API_TOKEN` 驗證\n- 每個產品的細節在 `references/<產品>/`"}
-->
---
name: cloudflare-deploy
description: 使用 Workers、Pages 與相關平台服務，把應用程式與基礎設施部署到 Cloudflare。當使用者要求在 Cloudflare 上部署、託管、發布或設定專案時使用。
---

# Cloudflare 部署

在 Cloudflare 平台上建構的整合技能。用下方的決策樹找到合適的產品，然後載入詳細的參考。

## 前置條件

- 當沙箱阻擋了部署的網路呼叫時，以 `sandbox_permissions=require_escalated` 重新執行。
- 部署可能需要幾分鐘。使用適當的逾時值。

## 驗證（部署前必要）

在 `wrangler deploy`、`wrangler pages deploy` 或 `npm run deploy` 之前驗證登入狀態：

{{CODE:1}}

沒有驗證？→ `references/wrangler/auth.md`
- 互動式/本機：`wrangler login`（一次性 OAuth）
- CI/CD：設定 `CLOUDFLARE_API_TOKEN` 環境變數

## 快速決策樹

### 「我需要執行程式碼」

{{CODE:2}}

### 「我需要儲存資料」

{{CODE:3}}

### 「我需要 AI/ML」

{{CODE:4}}

### 「我需要網路/連線」

{{CODE:5}}

### 「我需要資安」

{{CODE:6}}

### 「我需要媒體/內容」

{{CODE:7}}

### 「我需要基礎設施即程式碼」

{{CODE:8}}

## 產品索引

### 運算與執行環境
| 產品 | 參考 |
|------|------|
| Workers | `references/workers/` |
| Pages | `references/pages/` |
| Pages Functions | `references/pages-functions/` |
| Durable Objects | `references/durable-objects/` |
| Workflows | `references/workflows/` |
| Containers | `references/containers/` |
| Workers for Platforms | `references/workers-for-platforms/` |
| Cron Triggers | `references/cron-triggers/` |
| Tail Workers | `references/tail-workers/` |
| Snippets | `references/snippets/` |
| Smart Placement | `references/smart-placement/` |

### 儲存與資料
| 產品 | 參考 |
|------|------|
| KV | `references/kv/` |
| D1 | `references/d1/` |
| R2 | `references/r2/` |
| Queues | `references/queues/` |
| Hyperdrive | `references/hyperdrive/` |
| DO Storage | `references/do-storage/` |
| Secrets Store | `references/secrets-store/` |
| Pipelines | `references/pipelines/` |
| R2 Data Catalog | `references/r2-data-catalog/` |
| R2 SQL | `references/r2-sql/` |

### AI 與機器學習
| 產品 | 參考 |
|------|------|
| Workers AI | `references/workers-ai/` |
| Vectorize | `references/vectorize/` |
| Agents SDK | `references/agents-sdk/` |
| AI Gateway | `references/ai-gateway/` |
| AI Search | `references/ai-search/` |

### 網路與連線
| 產品 | 參考 |
|------|------|
| Tunnel | `references/tunnel/` |
| Spectrum | `references/spectrum/` |
| TURN | `references/turn/` |
| Network Interconnect | `references/network-interconnect/` |
| Argo Smart Routing | `references/argo-smart-routing/` |
| Workers VPC | `references/workers-vpc/` |

### 資安
| 產品 | 參考 |
|------|------|
| WAF | `references/waf/` |
| DDoS Protection | `references/ddos/` |
| Bot Management | `references/bot-management/` |
| API Shield | `references/api-shield/` |
| Turnstile | `references/turnstile/` |

### 媒體與內容
| 產品 | 參考 |
|------|------|
| Images | `references/images/` |
| Stream | `references/stream/` |
| Browser Rendering | `references/browser-rendering/` |
| Zaraz | `references/zaraz/` |

### 即時通訊
| 產品 | 參考 |
|------|------|
| RealtimeKit | `references/realtimekit/` |
| Realtime SFU | `references/realtime-sfu/` |

### 開發者工具
| 產品 | 參考 |
|------|------|
| Wrangler | `references/wrangler/` |
| Miniflare | `references/miniflare/` |
| C3 | `references/c3/` |
| Observability | `references/observability/` |
| Analytics Engine | `references/analytics-engine/` |
| Web Analytics | `references/web-analytics/` |
| Sandbox | `references/sandbox/` |
| Workerd | `references/workerd/` |
| Workers Playground | `references/workers-playground/` |

### 基礎設施即程式碼
| 產品 | 參考 |
|------|------|
| Pulumi | `references/pulumi/` |
| Terraform | `references/terraform/` |
| API | `references/api/` |

### 其他服務
| 產品 | 參考 |
|------|------|
| Email Routing | `references/email-routing/` |
| Email Workers | `references/email-workers/` |
| Static Assets | `references/static-assets/` |
| Bindings | `references/bindings/` |
| Cache Reserve | `references/cache-reserve/` |

## 疑難排解

### 提升的網路存取

如果部署因網路問題（逾時、DNS 錯誤、連線重設）而失敗，就以提升的權限重新執行部署（使用 `sandbox_permissions=require_escalated`）。當沙箱網路阻擋對外請求時，部署需要提升的網路存取。

給使用者的指引範例：

{{CODE:9}}
