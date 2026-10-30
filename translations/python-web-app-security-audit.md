<!--meta
{"title":"Python 網頁應用安全稽核","category":"資訊安全","tags":["Python","FastAPI","Django","安全測試","pytest"],
"summary":"上線前對 Python 網頁應用（FastAPI、Django、Flask、ASGI 服務）執行防禦性的安全測試：內附一套可設定的 pytest 測試組，透過 ASGI 在本機直接測試認證、授權、惡意輸入、回應標頭、CORS、Cookie、速率限制、錯誤處理、HTTP 方法與不安全設定，輸出有證據支持的發現事項與清楚的測試邊界。測試組不具破壞性。",
"usage":"- 安裝：`pip install \"pytest>=8\" \"pytest-asyncio>=0.24\" \"httpx>=0.27\" python-dotenv`\n- 用 `scripts/prepare_security_suite.py <專案路徑>` 複製測試組到你的專案\n- 把 `.env.test.template` 複製成 `.env.test`，填入 app 匯入路徑、路由與測試帳號（不要提交）\n- 執行 `pytest security/ -v`\n- 結論分 BLOCKED／REVIEW REQUIRED／PASS；PASS 不代表滲透測試或完整安全"}
-->
---
name: python-web-app-security-audit
description: "為 Python 網頁應用程式執行防禦性的上線前安全測試。用於 FastAPI、Django、Flask 與 ASGI 服務（Python 網頁應用與伺服器之間的共通介面）。測試認證、授權、惡意輸入、標頭、CORS、Cookie、速率限制、錯誤與設定，回傳有證據支持的發現事項與清楚的測試邊界。"
license: MIT
metadata:
  version: 1.1.0
---

# Python 網頁應用安全稽核

在上線前，對本機的 Python 網頁應用程式執行一套可設定的 pytest 測試組。它使用 ASGI（Python 網頁應用與其伺服器之間的介面），因此這些檢查可以在不開啟公開伺服器的情況下，測試 FastAPI、Django、透過轉接器的 Flask，以及類似的服務。

## 範圍

內附的檢查涵蓋認證、授權、輸入驗證、回應標頭、CORS、Cookie、速率限制、錯誤處理、HTTP 方法處理與不安全的設定。在把測試組套用到某個應用程式之前，先閱讀 [設定與邊界](references/setup-and-boundaries.md)、[框架轉接器](references/framework-adapters.md)、[路由設定](references/route-configuration.md)、[fixture 安全](references/fixture-safety.md) 與 [斷言目錄](references/assertion-catalog.md)。

不要把一次通過的執行說成滲透測試或生產環境安全的證明。這套測試組不會驗證部署的 TLS、WAF、相依套件漏洞、外部基礎設施，或任何它無法透過設定的測試應用程式觸及的控制。

## 準備測試組

1. 在目標專案的隔離環境中安裝相依套件。

   ```bash
   pip install "pytest>=8" "pytest-asyncio>=0.24" "httpx>=0.27" python-dotenv
   ```

2. 把內附的測試組複製到目標專案中，不覆寫既有的 security 目錄。

   ```bash
   python scripts/prepare_security_suite.py C:\path\to\your-project
   ```

   這個輔助工具會複製 `security/`、在不存在時複製 `pytest.ini`，以及 `.env.test.template` 檔案。它絕不會建立憑證檔案。

3. 在複製過去的 `security/` 目錄中，把 `.env.test.template` 複製為 `.env.test`。填入 app 的匯入路徑、路由、速率限制、允許的來源，以及專用的測試憑證。讓 `.env.test` 不進入版本控制。

4. 從目標專案的根目錄執行測試組。

   ```bash
   pytest security/ -v
   ```

## 操作規則

1. 測試應用程式的實際行為，而不是框架的預設值。
2. 使用專用的測試帳號與非生產資料。
3. 在把預設路由的失敗視為缺陷之前，先設定好路由變數。
4. 在指派上線關卡之前，檢查每一個失敗。
5. 把應用層的發現事項與基礎設施的發現事項分開。
6. 同時回報已驗證的結果與測試邊界。
7. 不要加入會建立帳號、修改紀錄或發出破壞性資料庫指令的檢查。內附的這套測試組不具破壞性。

## 回報結果

使用 [報告範本](assets/security-audit-report-template.md)、[上線決策指南](docs/release-decision-guide.md) 與 [持續整合指南](docs/continuous-integration-guide.md)。對每一項發現事項，說明受影響的路由或控制、證據、嚴重度、建議的修正，以及沒有測試到的部分。以下列其中一個上線決策作結：

- **BLOCKED（阻擋）：** 有已確認的問題必須在上線前修正。
- **REVIEW REQUIRED（需要審查）：** 仍有實質風險，需要負責人做決定。
- **PASS（通過）：** 設定的檢查沒有發現阻擋級或需審查級的問題。這不代表安全已完整證明。

## 測試組內容

| 檔案 | 用途 |
|---|---|
| `security/conftest.py` | 應用程式匯入、測試客戶端、認證 fixture 與路由輔助函式 |
| `security/test_headers.py` | 標頭是否存在與指令品質 |
| `security/test_validation.py` | 惡意輸入、格式錯誤的酬載與型別強制轉換 |
| `security/test_auth.py` | 認證的強制執行與抗帳號列舉 |
| `security/test_authorization.py` | 物件擁有權、角色邊界與大量賦值 |
| `security/test_rate_limit.py` | 門檻與 429 回應檢查 |
| `security/test_errors.py` | 錯誤訊息清理與內部細節外洩 |
| `security/test_cors.py` | 來源限制與預檢請求處理 |
| `security/test_cookies.py` | Cookie 旗標的強制執行 |
| `security/test_config.py` | 除錯模式暴露、方法處理與設定檢查 |

## 邊界

本技能不能取代人工安全評估、相依套件掃描、生產環境 HTTPS 驗證、WAF 驗證或動態掃描。當會改變狀態的請求使用 Cookie 認證時，加入應用程式專屬的 CSRF 測試。

內附的測試組不會建立帳號、刪除紀錄或執行會變更結構的資料庫指令。任何註冊或其他寫入流程，只能在應用程式自有、使用拋棄式資料庫並明確清理的測試組中評估。
