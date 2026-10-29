<!--meta
{"title":"Sleek 行動 App 設計","category":"前端與設計","tags":["App 設計","UI 設計","React Native","Sleek","API"],
"summary":"透過 sleek.design 的 REST API，用一段需求描述產生行動 App 畫面設計、編輯 Sleek 專案，並把設計實作成 React Native（Expo）或 HTML 程式碼。",
"usage":"- 安裝：`npx skills add https://github.com/designed-by-ai/skills --skill design-mobile-apps`\n- 需要 `SLEEK_API_KEY`；若未設定，代理會用裝置授權流程讓你在瀏覽器核准，不需手動貼金鑰\n- 說「幫我設計一個健身 App 的首頁和個人頁，然後用 Expo 實作」\n- 免費帳號有一次試用額度（約一次設計），持續使用需 Pro 方案"}
-->
---
name: design-mobile-apps
description: 用 Sleek 設計行動 App 畫面、編輯 Sleek 專案，並以 React Native 或 HTML 實作其設計。
metadata:
  requires-env: SLEEK_API_KEY
---

# 用 Sleek 設計

[![幾分鐘內設計行動 App](https://raw.githubusercontent.com/sleekdotdesign/agent-skills/main/assets/hero.png)](https://sleek.design)

## 概述

[sleek.design](https://sleek.design) 在 `/api/v1/*` 提供 REST API，可建立專案、依需求簡述設計畫面，並取得畫面的 HTML 與渲染圖。

**Base URL**：`https://sleek.design`
**驗證**：`Authorization: Bearer $SLEEK_API_KEY`，公開的裝置 start/poll 端點除外
**Content-Type**：JSON 請求主體請送 `application/json`。
**CORS**：所有 `/api/v1/*` 端點皆已啟用
**外層結構**：先檢查 HTTP 狀態。成功的 JSON 把內容包在 `data` 中；清單另外帶有同層的 `pagination`。錯誤使用頂層的 `code`、`status` 與 `message`，並可能有 `data.url`。成功的截圖與分享卡回傳圖片位元組；`204` 沒有主體。
**ID**：不透明的 11 字元 token，例如 `V1StGXR8Z5j`，沒有型別前綴。ID 本身完全看不出它指的是專案、畫面、元件、版本還是主題，所以要依它出現在哪個回應欄位來追蹤每一個 ID。
**解析回應**：把主體寫入檔案（`curl -o run.json`）再解析該檔案。用 `echo` 導管傳遞 JSON 會損壞它：zsh 會把字串值中跳脫的 `\n` 展開成真正的換行，讓主體變成無效的 JSON。
**API 文件**：OpenAPI 規格在 `https://sleek.design/api/v1/spec.json`；可瀏覽的文件在 `https://sleek.design/api/v1/docs`。這裡沒涵蓋的任何契約細節，請抓取規格查詢。

---

## 設計或實作

單次執行可以兩個方向都做——「幫我設計一個健身 App 並用 Expo 做出來」就是一輪設計接著一輪實作。根據你眼前的產出物來決定看哪份指引，而不是只讀一次請求就決定：

**設計**——你即將傳送聊天訊息給 Sleek。先讀 [designing.md](designing.md)；它包含「建立 → 聊天 → 截圖」的循環、如何撰寫風格方向，以及何時改從參考範例來設定風格。

**實作。** 在根據 Sleek 設計撰寫程式碼之前，先讀 [implementing.md](implementing.md)，了解版本選擇、原生轉換、可運作的功能與驗收檢查。

## 使用者截圖與審查截圖

截圖有兩種框法，下方每個檔案都會指名要哪一種：

- **使用者截圖**是預設渲染：視窗高度、手機外型。這是你給使用者看的。
- **審查截圖**加上 `fullHeight: true`，每次請求一個元件。這是你用來評判自己作品的。

---

## 前置條件：API 金鑰

如果沒有設定 `SLEEK_API_KEY`，就使用裝置流程，讓使用者永遠不必經手原始金鑰：

1. `POST https://sleek.design/api/v1/device/start`（不需驗證），主體為 `{"source": "your-tool-slug"}`。回應包含 `verificationUrl`、可供人工核對的 `userCode`、機密的 `deviceCode`，以及以秒為單位的輪詢 `interval`。
2. 把 `verificationUrl` 與 `userCode` 給使用者，並告訴他們在核准前確認代碼相符。
3. 每 `interval` 秒以 `{"deviceCode": "..."}` 輪詢 `POST https://sleek.design/api/v1/device/poll`。收到 `pending` 就繼續等待。收到 `approved` 時，在第一次讀取時就把 `data.key` 私密地存為 `SLEEK_API_KEY`：金鑰只會交付一次。收到 `expired` 或 `404 NOT_FOUND` 時，重新開始流程。回應契約見 [Device: Poll](endpoints.md#device-poll)。

備案：引導使用者前往 **https://sleek.design/agents/setup**，在一處完成登入、方案升級與金鑰建立，並請他們把金鑰貼回給你。金鑰也可以在 **https://sleek.design/dashboard/api-keys** 管理。完整的金鑰值只在建立時顯示一次，免費帳號同時只能有一把有效金鑰。

**方案**：免費帳號可以用一次性的試用點數試用 API（約一次設計執行），讓新使用者在做任何付費決定前先看到第一份設計。持續使用需要 Pro 或以上方案。這份檔案刻意不寫任何數字——請從 **https://sleek.design/agents.md** 讀取目前的價格、計費週期與點數額度（它由 Sleek 的即時定價產生），並從那裡引用。當費用變得相關時（使用者問起、需要升級才能繼續，或你即將引導他們到付款頁），清楚說明定價，包括年繳選項，讓使用者在到達付款步驟之前就知道它即將出現。

---

## 快速參考：所有端點

API 提供的每個端點：

| 方法     | 路徑                                           | 權限範圍          |
| -------- | ---------------------------------------------- | ----------------- |
| `GET`    | `/api/v1/projects`                             | `projects:read`   |
| `POST`   | `/api/v1/projects`                             | `projects:write`  |
| `GET`    | `/api/v1/projects/:id`                         | `projects:read`   |
| `DELETE` | `/api/v1/projects/:id`                         | `projects:write`  |
| `GET`    | `/api/v1/projects/:id/components`              | `components:read` |
| `GET`    | `/api/v1/projects/:id/components/:componentId` | `components:read` |
| `GET`    | `/api/v1/references`                           | 任何有效金鑰      |
| `POST`   | `/api/v1/projects/:id/chat/messages`           | `chats:write`     |
| `GET`    | `/api/v1/projects/:id/chat/runs/:runId`        | `chats:read`      |
| `POST`   | `/api/v1/projects/:id/chat/runs/:runId/cancel` | `chats:write`     |
| `POST`   | `/api/v1/screenshots`                          | `screenshots`     |
| `POST`   | `/api/v1/share-cards`                          | `screenshots`     |
| `POST`   | `/api/v1/device/start`                         | 公開、不需驗證    |
| `POST`   | `/api/v1/device/poll`                          | 公開、不需驗證    |

建立金鑰時只給予任務會用到的權限範圍。

上表每一列的完整規格——請求主體、回應形狀、欄位預設值、狀態碼——都在 [endpoints.md](endpoints.md)。這張表足以挑選端點；需要表中沒有的契約細節時再讀參考文件。

---

## 錯誤形狀

{{CODE:1}}

| HTTP | 代碼                    | 時機                                                                     |
| ---- | ----------------------- | ------------------------------------------------------------------------ |
| 401  | `UNAUTHORIZED`          | API 金鑰缺少/無效/過期                                                   |
| 403  | `FORBIDDEN`             | 金鑰有效，但權限範圍或方案不對                                           |
| 404  | `NOT_FOUND`             | 資源不存在                                                               |
| 400  | `BAD_REQUEST`           | 驗證失敗                                                                 |
| 409  | `CONFLICT`              | 此專案已有另一個執行中的 run                                             |
| 429  | `TOO_MANY_REQUESTS`     | 渲染上限：每個組織每小時 1000 次截圖＋分享卡，只計算 API 金鑰請求        |
| 500  | `INTERNAL_SERVER_ERROR` | 伺服器錯誤                                                               |

`401`、`403` 與 `429` 的主體可能包含 `data.url`：一個使用者可以修正該狀況的頁面（建立金鑰、升級方案）。原樣分享它。

聊天 run 層級的錯誤（在 `data.error` 中）：

| 代碼                              | 意義                                                       |
| --------------------------------- | ---------------------------------------------------------- |
| `out_of_credits`                  | 組織已無剩餘點數                                           |
| `execution_failed`                | AI 執行錯誤                                                |
| `cancelled`                       | run 已透過取消端點取消                                     |
| `request_message_persist_failed`  | run 在到達 AI 之前就失敗了；訊息從未被儲存                 |

遇到 `out_of_credits` 時，轉達 `error.url` 並等待使用者解決。在任一可恢復的失敗之後，要重送還是重新嘗試，請依照[安全重試](designing.md#2-send-a-chat-message)。
