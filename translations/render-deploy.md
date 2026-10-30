<!--meta
{"title":"部署到 Render","category":"雲端與 DevOps","tags":["Render","部署","render.yaml","MCP","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：分析你的程式碼，判斷該用 Blueprint（產生 render.yaml、適合多服務與資料庫）還是 MCP 直接建立服務（適合單一網站），引導設定 Render MCP 或 CLI 認證，產生 Dashboard 深層連結，部署後檢查狀態、錯誤日誌與健康指標。",
"usage":"- Codex：`$skill-installer render-deploy`\n- 說「幫我把這個專案部署到 Render」「產生 render.yaml」\n- 前提：程式碼要先推到 GitHub／GitLab／Bitbucket\n- 單一服務優先用 MCP 直接建立；有資料庫、worker、cron 就用 Blueprint\n- 標成 `sync: false` 的密鑰要到 Render Dashboard 自己填"}
-->
---
name: render-deploy
description: 透過分析程式碼、產生 render.yaml Blueprint 並提供 Dashboard 深層連結，把應用程式部署到 Render。當使用者想在 Render 雲端平台上部署、託管、發布或設定他們的應用程式時使用。
---

# 部署到 Render

Render 支援 **以 Git 為來源** 的服務與 **預先建置的 Docker 映像** 服務。

本技能涵蓋 **以 Git 為來源** 的流程：
1. **Blueprint 方法** —— 產生 render.yaml，用於基礎設施即程式碼（IaC）的部署
2. **直接建立** —— 透過 MCP 工具立即建立服務

Blueprint 也可以透過 `runtime: image` 執行 **預先建置的 Docker 映像**，但 `render.yaml` 仍必須放在 Git repo 中。

如果沒有 Git remote，就停下來請使用者二選一：
- 建立／推送一個 Git remote（如果只需要 Blueprint，可以是極簡的 repo），或
- 使用 Render Dashboard／API 部署預先建置的 Docker 映像（MCP 無法建立以映像為來源的服務）。

## 前置需求

- 當沙箱阻擋部署的網路呼叫時，以 `sandbox_permissions=require_escalated` 重新執行。
- 部署可能需要幾分鐘。請使用適當的逾時值。

## 何時使用本技能

當使用者想要以下事情時啟用本技能：
- 把應用程式部署到 Render
- 建立 render.yaml Blueprint 檔案
- 為他們的專案設定 Render 部署
- 在 Render 雲端平台上託管或發布他們的應用程式
- 建立資料庫、cron 工作或其他 Render 資源

## 順利路徑（新使用者）

在深入分析之前，先用這段簡短的提問順序來減少阻力：
1. 詢問他們想從 Git repo 部署，還是從預先建置的 Docker 映像部署。
2. 詢問 Render 是否該佈建應用程式需要的一切（依使用者描述推斷可能需要的東西），還是只部署應用程式、基礎設施由他們自備。如果相依項目不明確，簡短追問確認他們是否需要資料庫、worker、cron 或其他服務。

然後依下方適當的方法進行。

## 選擇你的來源路徑

**Git Repo 路徑：** Blueprint 與直接建立都需要。repo 必須推送到 GitHub、GitLab 或 Bitbucket。

**預先建置 Docker 映像路徑：** Render 透過以映像為來源的服務支援。**MCP 不支援**此方式；請使用 Dashboard／API。需詢問：
- 映像 URL（registry + tag）
- Registry 認證（若為私有）
- 服務類型（web／worker）與連接埠

如果使用者選擇 Docker 映像，引導他們到 Render Dashboard 的映像部署流程，或請他們加入 Git remote（這樣你就能用含 `runtime: image` 的 Blueprint）。

## 選擇你的部署方法（Git Repo）

兩種方法都需要推送到 GitHub、GitLab 或 Bitbucket 的 Git repository。（若使用 `runtime: image`，repo 可以是極簡的，只包含 `render.yaml`。）

| 方法 | 最適合 | 優點 |
|--------|----------|------|
| **Blueprint** | 多服務應用程式、IaC 工作流程 | 受版本控制、可重現、支援複雜設定 |
| **直接建立** | 單一服務、快速部署 | 立即建立，不需要 render.yaml 檔案 |

### 方法選擇的經驗法則

除非使用者要求特定方法，否則預設使用這條決策規則。先分析程式碼；只有在部署意圖不明確時（例如資料庫、worker、cron）才詢問。

**以下全部成立時，使用直接建立（MCP）：**
- 單一服務（一個 web 應用程式或一個靜態網站）
- 沒有獨立的 worker／cron 服務
- 沒有附加的資料庫或 Key Value
- 只有簡單的環境變數（沒有共用的環境群組）
如果適合這條路徑但 MCP 尚未設定，就先停下來引導 MCP 設定，再繼續。

**以下任一成立時，使用 Blueprint：**
- 多個服務（web + worker、API + 前端等）
- 需要資料庫、Redis／Key Value 或其他資料儲存
- Cron 工作、背景 worker 或私有服務
- 你想要可重現的 IaC，或要把 render.yaml 提交進 repo
- 需要一致設定的 monorepo 或多環境設定

如果不確定，簡短問個釐清問題，但為了安全預設使用 Blueprint。對於單一服務，強烈偏好透過 MCP 直接建立，並在需要時引導 MCP 設定。

## 前置需求檢查

開始部署時，依序確認這些需求：

**1. 確認來源路徑（Git 或 Docker）**

如果使用以 Git 為基礎的方法（Blueprint 或直接建立），repo 必須推送到 GitHub／GitLab／Bitbucket。參照預先建置映像的 Blueprint 仍需要含有 `render.yaml` 的 Git repo。

{{CODE:1}}

- 如果沒有 remote，停下來請使用者建立／推送 remote，**或**改用 Docker 映像部署。

**2. 檢查 MCP 工具是否可用（單一服務優先）**

MCP 工具提供最好的體驗。嘗試以下呼叫來檢查是否可用：
{{CODE:2}}

如果 MCP 工具可用，大多數操作可以跳過安裝 CLI。

**3. 檢查 Render CLI 是否已安裝（用於驗證 Blueprint）**
{{CODE:3}}
如果沒有安裝，主動提議安裝：
- macOS：`brew install render`
- Linux／macOS：`curl -fsSL https://raw.githubusercontent.com/render-oss/cli/main/bin/install.sh | sh`

**4. MCP 設定（若 MCP 尚未設定）**

如果 `list_services()` 因為 MCP 未設定而失敗，詢問他們想設定 MCP（偏好）還是繼續使用 CLI 備案。如果他們選 MCP，詢問他們使用哪個 AI 工具，然後提供下方對應的指示。一律使用他們自己的 API 金鑰。

### Cursor

帶使用者走過這些步驟：

1) 取得 Render API 金鑰：
{{CODE:4}}

2) 把這段加到 `~/.cursor/mcp.json`（替換 `<YOUR_API_KEY>`）：
{{CODE:5}}

3) 重新啟動 Cursor，然後重試 `list_services()`。

### Claude Code

帶使用者走過這些步驟：

1) 取得 Render API 金鑰：
{{CODE:6}}

2) 用 Claude Code 加入 MCP 伺服器（替換 `<YOUR_API_KEY>`）：
{{CODE:7}}

3) 重新啟動 Claude Code，然後重試 `list_services()`。

### Codex

帶使用者走過這些步驟：

1) 取得 Render API 金鑰：
{{CODE:8}}

2) 在他們的 shell 中設定：
{{CODE:9}}

3) 用 Codex CLI 加入 MCP 伺服器：
{{CODE:10}}

4) 重新啟動 Codex，然後重試 `list_services()`。

### 其他工具

如果使用者使用其他 AI 應用程式，引導他們到 Render MCP 文件，查看該工具的設定步驟與安裝方式。

### 選擇工作區

MCP 設定好之後，請使用者用類似這樣的提示設定目前使用的 Render 工作區：

{{CODE:11}}

**5. 檢查認證（僅限 CLI 備案）**

如果無法使用 MCP，就改用 CLI 並確認你能存取帳戶：
{{CODE:12}}

如果 `render whoami` 失敗或回傳空資料，表示 CLI 尚未認證。CLI 不一定會自動提示，所以要明確提示使用者進行認證：

如果兩者都沒有設定，詢問使用者偏好哪種方式：
- **API 金鑰（CLI）**：`export RENDER_API_KEY="rnd_xxxxx"`（從 https://dashboard.render.com/u/*/settings#api-keys 取得）
- **登入**：`render login`（開啟瀏覽器進行 OAuth）

**6. 檢查工作區情境**

確認目前使用的工作區：
{{CODE:13}}

或透過 CLI：
{{CODE:14}}

列出可用的工作區：
{{CODE:15}}

如果使用者需要切換工作區，必須透過 Dashboard 或 CLI（`render workspace set`）進行。

前置需求都滿足後，繼續部署工作流程。

---

# 方法 1：Blueprint 部署（建議用於複雜應用程式）

## Blueprint 工作流程

### 步驟 1：分析程式碼

分析程式碼以判斷框架／執行環境、建置與啟動指令、必要的環境變數、資料儲存與連接埠綁定。使用 [references/codebase-analysis.md](references/codebase-analysis.md) 中的詳細檢查清單。

### 步驟 2：產生 render.yaml

依照 Blueprint 規格建立 `render.yaml` Blueprint 檔案。

完整規格：[references/blueprint-spec.md](references/blueprint-spec.md)

**重點：**
- 除非使用者另有指定，一律使用 `plan: free`
- 包含應用程式需要的「所有」環境變數
- 用 `sync: false` 標記密鑰（使用者在 Dashboard 中填寫）
- 使用適當的服務類型：`web`、`worker`、`cron`、`static` 或 `pserv`
- 使用適當的執行環境：[references/runtimes.md](references/runtimes.md)

**基本結構：**
{{CODE:16}}

**服務類型：**
- `web`：HTTP 服務、API、web 應用程式（可公開存取）
- `worker`：背景工作處理器（不可公開存取）
- `cron`：依 cron 排程執行的排程任務
- `static`：靜態網站（透過 CDN 提供 HTML/CSS/JS）
- `pserv`：私有服務（僅限內部，同一帳戶內）

服務類型詳情：[references/service-types.md](references/service-types.md)
執行環境選項：[references/runtimes.md](references/runtimes.md)
範本範例：[assets/](assets/)

### 步驟 2.5：立即的下一步（一律提供）

建立 `render.yaml` 之後，一律給使用者一份簡短、明確的檢查清單，並在 CLI 可用時立即執行驗證：
1. **認證（CLI）**：執行 `render whoami -o json`（若未登入，執行 `render login` 或設定 `RENDER_API_KEY`）
2. **驗證（建議）**：執行 `render blueprints validate`
   - 如果沒有安裝 CLI，主動提議安裝並提供指令。
3. **提交 + 推送**：`git add render.yaml && git commit -m "Add Render deployment configuration" && git push origin main`
4. **開啟 Dashboard**：使用 Blueprint 深層連結，若有提示就完成 Git OAuth
5. **填入密鑰**：設定標記為 `sync: false` 的環境變數
6. **部署**：按下「Apply」並監看部署

### 步驟 3：驗證設定

驗證 render.yaml 檔案，在部署前抓出錯誤。如果已安裝 CLI，直接執行指令；只有在 CLI 缺少時才提示使用者：

{{CODE:17}}

繼續之前先修正所有驗證錯誤。常見問題：
- 缺少必要欄位（`name`、`type`、`runtime`）
- 無效的 runtime 值
- 錯誤的 YAML 語法
- 無效的環境變數參照

設定指南：[references/configuration-guide.md](references/configuration-guide.md)

### 步驟 4：提交並推送

**重要：** 部署前你必須把 `render.yaml` 檔案合併進你的 repository。

確保 `render.yaml` 檔案已提交並推送到你的 Git remote：

{{CODE:18}}

如果還沒有 Git remote，就停在這裡，引導使用者建立 GitHub／GitLab／Bitbucket repo、把它加為 `origin` 並推送，然後再繼續。

**為什麼這很重要：** Dashboard 深層連結會從你的 repository 讀取 render.yaml。如果檔案沒有合併並推送，Render 找不到設定，部署就會失敗。

進入下一步之前，先確認檔案已經在你的遠端 repository 中。

### 步驟 5：產生深層連結

取得 Git repository URL：

{{CODE:19}}

這會回傳你 Git 服務商的 URL。**如果 URL 是 SSH 格式，把它轉換成 HTTPS：**

| SSH 格式 | HTTPS 格式 |
|------------|--------------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**轉換規則：** 把 `git@<host>:` 換成 `https://<host>/`，並移除 `.git` 後綴。

用 HTTPS 的 repository URL 組出 Dashboard 深層連結：
{{CODE:20}}

範例：
{{CODE:21}}

### 步驟 6：引導使用者

**關鍵：** 在使用者點擊深層連結之前，確保他們已經把 render.yaml 檔案合併並推送到 repository。如果檔案不在 repository 中，Render 無法讀取 Blueprint 設定，部署就會失敗。

把深層連結提供給使用者，並附上這些指示：

1. **確認 render.yaml 已合併** —— 確認檔案存在於你在 GitHub／GitLab／Bitbucket 上的 repository
2. 點擊深層連結開啟 Render Dashboard
3. 若有提示，完成 Git 服務商的 OAuth
4. 為 Blueprint 命名（或使用 render.yaml 中的預設名稱）
5. 填入密鑰環境變數（標記為 `sync: false` 的）
6. 檢查服務與資料庫設定
7. 按下「Apply」進行部署

部署會自動開始。使用者可以在 Render Dashboard 中監看進度。

### 步驟 7：確認部署

使用者透過 Dashboard 部署後，確認一切正常運作。

**透過 MCP 檢查部署狀態：**
{{CODE:22}}
尋找 `status: "live"` 來確認部署成功。

**檢查執行階段錯誤（部署後等 2–3 分鐘）：**
{{CODE:23}}

**檢查服務健康指標：**
{{CODE:24}}

如果發現錯誤，進入下方的 **部署後驗證與基本排查** 章節。

---

# 方法 2：直接建立服務（快速的單一服務部署）

對於不需要基礎設施即程式碼的簡單部署，透過 MCP 工具直接建立服務。

## 何時使用直接建立

- 單一 web 服務或靜態網站
- 快速原型或展示
- 當你的 repo 不需要 render.yaml 檔案時
- 為既有專案加入資料庫或 cron 工作

## 直接建立的前置需求

**Repository 必須推送到 Git 服務商。** Render 會複製你的 repository 來建置並部署服務。

{{CODE:25}}

支援的服務商：GitHub、GitLab、Bitbucket

如果沒有 remote，停下來請使用者建立／推送 remote，或改用 Docker 映像部署。

**注意：** MCP 不支援建立以映像為來源的服務。預先建置的 Docker 映像部署請使用 Dashboard／API。

## 直接建立工作流程

使用下方精簡的步驟，完整的 MCP 指令範例與後續設定請參考 [references/direct-creation.md](references/direct-creation.md)。

### 步驟 1：分析程式碼
使用 [references/codebase-analysis.md](references/codebase-analysis.md) 判斷執行環境、建置／啟動指令、環境變數與資料儲存。

### 步驟 2：透過 MCP 建立資源
建立服務（web 或 static）以及任何需要的資料庫或 key-value 儲存。參見 [references/direct-creation.md](references/direct-creation.md)。

如果 MCP 回傳缺少 Git 憑證或 repo 存取權的錯誤，停下來引導使用者在 Render Dashboard 中連接他們的 Git 服務商，然後重試。

### 步驟 3：設定環境變數
建立後透過 MCP 加入必要的環境變數。參見 [references/direct-creation.md](references/direct-creation.md)。

提醒使用者，如果不想透過 MCP 傳遞密鑰，可以在 Dashboard 中設定。

### 步驟 4：確認部署
檢查部署狀態、日誌與指標。參見 [references/direct-creation.md](references/direct-creation.md)。

---

關於服務探索、設定細節、快速指令與常見問題，參見 [references/deployment-details.md](references/deployment-details.md)。

---

# 部署後驗證與基本排查（所有方法）

保持簡短且可重複。如果任何檢查失敗，先修正再重新部署。

1. 確認最新的部署是 `live` 並且正在處理流量
2. 呼叫健康檢查端點（或根路徑），確認回應 200
3. 掃描最近的錯誤日誌，找出明確的失敗特徵
4. 確認必要的環境變數與連接埠綁定（`0.0.0.0:$PORT`）

詳細檢查清單與指令：[references/post-deploy-checks.md](references/post-deploy-checks.md)

如果服務無法啟動或健康檢查逾時，使用基本排查指南：
[references/troubleshooting-basics.md](references/troubleshooting-basics.md)

## 疑難排解

### 提升的網路存取權

如果部署因網路問題失敗（逾時、DNS 錯誤、連線重設），以提升的權限重新執行部署（使用 `sandbox_permissions=require_escalated`）。當沙箱網路阻擋對外請求時，部署需要提升的網路存取權。

給使用者的引導範例：

{{CODE:26}}

選用：如果你需要更深入的診斷（指標／資料庫檢查／錯誤目錄），建議安裝 `render-debug` 技能。核心部署流程不需要它。
