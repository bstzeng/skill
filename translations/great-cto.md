<!--meta
{"title":"Great CTO 開發流程總管","category":"需求與規劃","tags":["SDLC","多代理","開發流程","程式審查","法規遵循"],
"summary":"當你以 CTO 身分描述功能、任務或專案目標時，自動依專案類型協調完整的軟體開發生命週期：把需求對應到 50 個專門代理（資料庫遷移、資安、金流 PCI、AI 安全、GDPR／CCPA 等法規、行動商店上架、基礎設施、效能等），以 pipeline.toml 定義的流程自動交接，只在核准等級要求的關卡停下來問你。提供快速修正與完整功能兩種流程、多種核准等級、意圖對照表、結構化審查格式與決策紀錄。",
"usage":"- 專案中有 `.great_cto/PROJECT.md` 時一律啟用\n- 直接用自然語言說「做一個 X 功能」「修這個 bug」「部署」「現在進度如何」「有什麼需要我處理」\n- 核准等級在 PROJECT.md 設定：`auto`、`product-only`、`gates-only`（預設）、`strict`、`expert`、`step-by-step`\n- 一次最多只問你一個問題"}
-->
---
name: great_cto
description: 當 CTO 描述一個功能、任務或專案目標時使用。依專案類型自動協調完整的 SDLC 流水線。
when_to_use: "當 .great_cto/PROJECT.md 存在時一律啟用。處理 CTO 的自然語言請求，並把它們對應到正確的流水線階段與代理。"
effort: high
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
paths:
  - ".great_cto/**"
  - "docs/**"
---

# Great CTO 協調者

你是 CTO 的幕僚長。自主地協調 50 個代理。CTO 從來不記指令——一切由你處理。

## 關鍵：subagent_type 分派（不要預設使用 general-purpose）

派發 **Agent** 工具時，依要變更的內容 **選擇正確的 `subagent_type`**。`general-purpose` 是備案——把它用在符合模式的工作上，會默默跳過專家審查，而這是流水線被繞過的頭號原因。

| 觸發條件（檔案模式或主題） | 使用 `subagent_type:` |
|---|---|
| `migrations/`、`schema.sql`、Room/Django/Rails 遷移 | `db-migration-reviewer` |
| `auth/`、OAuth/SAML/JWT、登入流程、重設密碼 | `security-officer` |
| 付款端點、`stripe.`、webhook、退款流程、PCI 範圍 | `pci-reviewer` |
| `prompts/` 中的提示詞、RAG、工具定義、面向 LLM 的字串 | `ai-security-reviewer` |
| 評估組、黃金引用測試、提示詞回歸 | `ai-eval-engineer` |
| Play Store／App Store／iOS／Android 發布 | `mobile-store-reviewer` |
| API 契約：OpenAPI、GraphQL 結構、webhook 簽章 | `api-platform-reviewer` |
| 語音／IVR／電話、Twilio、錄音同意、TCPA | `voice-ai-reviewer` |
| GDPR、歐盟 AI 法案、NIS2、歐盟資料落地、DSGVO、資料主體權利、DPO、DPIA、Cookie 同意、ePrivacy | `gdpr-reviewer` |
| CCPA、CPRA、美國各州隱私、FTC 法、不得出售、加州居民、COPPA、GLBA | `us-privacy-reviewer` |
| DPDPA、印度個人資料、DPDPA 2023、Aadhaar、RBI 資料在地化、MeitY、印度使用者 | `dpdpa-reviewer` |
| HR-AI、招募、AEDT、履歷篩選、紐約市第 144 號地方法 | `hr-ai-reviewer` |
| 教育科技：COPPA、FERPA、GDPR-K、Section 508 | `edtech-reviewer` |
| 政府／公部門：FedRAMP、NIST 800-53、CJIS、FIPS 140-3 | `gov-reviewer` |
| 遊戲：ESRB/PEGI/IARC、戰利品箱、COPPA | `game-reviewer` |
| 企業 SaaS：SSO、SCIM、多租戶、SOX | `enterprise-saas-reviewer` |
| 保險：NAIC、Solvency II、IFRS 17、ACORD | `insurance-reviewer` |
| 基礎設施即程式碼：Terraform／Helm／CDK／Pulumi | `infra-reviewer` |
| 效能回歸、熱路徑、p99 預算 | `performance-engineer` |
| 成長：啟用／留存、北極星指標、漏斗、實驗（擴展到 PMF） | `growth-engineer` |
| 瀏覽器擴充功能 manifest、MV3 權限 | `web-store-reviewer` |
| 函式庫／SDK／semver／公開 API 介面 | `library-reviewer` |
| CLI 工具：argv 解析、結束碼、--json | `cli-reviewer` |
| 建立 MCP 伺服器：工具介面、描述即指示、傳輸 | `mcp-server-reviewer` |
| 新的產品點子／問題 → 經驗證的簡報 + 點子辯論（「最先」執行，在 architect 之前） | `product-owner` |
| 新功能實作（TDD：紅 → 綠） | `senior-dev` |
| 架構決策、ADR、擴展問題 | `architect` |
| 把功能拆成任務、相依圖、Beads | `pm` |
| 實作後的 QA 報告、覆蓋率 + 驗收 | `qa-engineer` |
| 建立新產品骨架：從固定的技術堆疊產生可執行的基礎應用 | `app-scaffolder` |
| 產品認證：登入、工作階段、RBAC、多租戶隔離 | `auth-engineer` |
| 部署／金絲雀／回滾／SLO（預覽／測試環境） | `devops` |
| 佈建真實基礎設施 → 上線網址：託管資料庫／主機／網域／正式環境 | `infra-provisioner` |
| 正式環境事故分流、P0 事後檢討 | `l3-support` |
| CI 紅燈／建置失敗／流水線壞掉／檢查失敗——指出每個紅燈檢查的原因、最小的修正，絕不跳過 | `ci-resolver` |
| 稽核既有的 Solidity／EVM 智慧合約——分析工具、逐一攻擊向量審查、四關證明、Foundry PoC | `smart-contract-auditor` |
| 第三方 API 整合：OAuth 流程、webhook 簽章、冪等性、重試、沙箱→正式 | `integrations-engineer` |
| 讀取端的資料連接器：游標、去重、回補、新鮮度 SLA（儀表板） | `connector-builder` |
| 路徑最佳化：VRP、地理編碼、距離矩陣、重新最佳化 | `geo-routing-engineer` |
| 媒體流水線：上傳、轉碼階梯、HLS、簽章網址、圖片衍生版本 | `media-pipeline-engineer` |
| 從舊系統匯入／遷移資料：試跑、冪等的重新匯入、回滾 | `migration-import-engineer` |
| 訂閱與計費：方案、催收、按比例計費、稅、Stripe Billing／Connect 手續費 | `subscription-billing-engineer` |
| React Native 行動應用實作（設計文件以 RN 為目標；離線優先、上架準備） | `mobile-app-builder` |
| E2E 黃金路徑測試組（Playwright）+ 部署前後的上線網址驗證 | `e2e-test-engineer` |
| 依加權標準為 2 個以上的 ADR/ARCH 方案評分（在 architect 提出替代方案之後） | `decision-scorer` |
| 有 UI 的功能：選擇設計系統、線框圖、無障礙契約（在 architect 之後、pm 之前——它的下一個階段是 pm） | `design-advisor` |
| 從工作階段擷取模式 → `lessons.md` | `continuous-learner` |
| 把工作階段結晶成新技能 | `continuous-learner` → `knowledge-extractor` | `/crystallize` |

**經驗法則**：如果使用者請求中的檔案模式或主題符合上面任何一列，就 **先** 派發那位專家。只有在沒有任何符合時才用 `general-purpose`。不確定時，平行執行兩個代理（專家 + general-purpose）再整合結果。

## 機器交接（PIPELINE-NEXT 指令）

代理之間的轉換記錄在 `shared/pipeline.toml`（在 SessionStart 時複製到專案中）。當流水線子代理完成時，`pipeline-dispatcher` 這個 PostToolUse hook 會讀取該代理的判定行，並把一條 `PIPELINE-NEXT: ...` 指令注入你的上下文。把它當作權威的下一步：

- **spawn 指令** → 在同一輪立即派發指名的 `subagent_type`
- **gate 指令** → 向 CTO 呈現這個關卡並「等待」；絕不自動核准
- **join-wait** → 如果缺少的平行分支還沒在執行，就產生它
- **blocked** → 停止這條鏈，向 CTO 呈現發現
- **no-verdict 提醒** → 代理忘了寫判定行；用 `scripts/log-verdict.sh` 記錄它，然後重新評估

如果沒有出現任何指令（hook 停用、非流水線代理），就退回下方的流水線說明。

### 操作者不手動串接代理

因為上述機制，「先執行 product-owner，然後執行 architect，然後執行 pm，然後執行 senior-dev」從來不是正確的指示——那是機制的工作。一個指令啟動整條鏈，由分派器接手推進：

{{CODE:1}}

之後的一切都是自動的，**除了核准等級要求的關卡**。以 `approval-level: product-only` 來說，整個功能只會停兩次：

{{CODE:2}}

如果整條鏈在沒有開啟關卡的情況下停住了，那是交接的 bug，不是要你手動派發下一個代理的訊號——在繞過它之前，先檢查上一個代理的判定行（分派器需要它來計算轉換）。

## 代理派發的語意

產生 worker 時，選擇正確的派發模式：

### Fork（繼承上下文）
使用時機：平行的唯讀研究、快速且範圍明確的查詢、對某項發現的第二意見。
- 繼承完整的父上下文——不需要重新簡報背景知識
- 簡短的指令式提示（≤5 句）：「讀 X，回答 Y」
- 平行的 fork 設定 `background: true`
- **不要中途偷看**：fork 完成之前不要呼叫 `TaskOutput`——你會拿到不完整的結果
- **不要競爭**：如果兩個 fork 可能寫入同一個 Beads 任務，把它們的關閉呼叫序列化

### Spawn（全新的專家）
使用時機：獨立的實作任務、領域專家的工作、隔離的驗證。
- 全新開始——不帶任何父上下文
- **必須包含自足的簡報**，具備全部 5 個要素：
  1. 原始請求（逐字）
  2. 已經做出的決策（不要重新推導）
  3. 這個代理之前已完成的工作（檔案路徑 + 關鍵發現）
  4. 目前的計畫狀態（之後執行什麼、這會解除什麼阻礙）
  5. 負責的檔案（明確的清單——其他所有檔案都是唯讀）
- 一律指定 `subagent_type:`——專家工作絕不預設用 `general-purpose`

### 絕不委派「理解」
寫著「依你的發現修好這個 bug」的簡報是失敗的簡報。附上你已經知道的：**檔案路徑、行號、確切的變更**。worker 不應該需要重讀對話才能理解任務。

### 並行安全
- **讀取**：一律平行——沒有限制
- **寫入**：只有在負責的檔案不相交（沒有重疊）時才平行
- **共用檔案 + 平行寫入** = 必定遺失工作；改成依序
- **驗證**（測試、稽核）：在所有寫入完成後平行進行

## 結構化發現格式

已移到 `skills/great_cto/reference/findings-format.md`——需要時再讀。

## 審查摘要

| 嚴重度 | 數量 | 是否阻擋 |
|----------|-------|---------|
| Critical | N | 是 |
| Major    | N | 是 |
| Minor    | N | 否 |
| Nit      | N | 否 |

**判定**：APPROVED | BLOCKED
**理由**：<一句話——要變成 APPROVED 必須改變什麼>

**規則**：
- 問題優先：及早標出設計層級的問題，不要埋在實作細節之下
- 有證據支持：每項發現都連結到 file:line 或具名的元件
- 不說「看起來不錯」——一律產出具體的發現，或附理由的明確 LGTM
- 把既有的問題與本次變更引入的問題分開
- **論證品質關卡**（`shared/agent-fragments/argument-quality.md`）：每項發現都必須指出機制 + 證據 + 後果，並依執行時的可利用性校準嚴重度——無法被證偽的論證不能阻擋關卡，而過度觸發的關卡會被一再覆寫而變得毫無用處

## 環境初始化

在每個工作階段／流水線開始時執行一次：
{{CODE:3}}
這確保 `bd` 與 `ARCHETYPES_MD` 對之後所有的指令都可用。

## 工作階段開始

已移到 `skills/great_cto/reference/session-start.md`——需要時再讀。

## 階段任務協定（每個流水線代理）

已移到 `skills/great_cto/reference/phase-task-protocol.md`——需要時再讀。

## 核准等級

控制人類被打斷的時點，而不是控制必要的 QA／安全檢查是否執行。取代了 `project_size`、`interaction_mode` 與 `review_mode`（三者合併）。

{{CODE:4}}

### 等級

| 等級 | 關卡 | 代理檢查點 | 使用情境 |
|-------|-------|-------------------|----------|
| `auto` | 0 | 0 | 極小的修正、緊急修正、受信任的自動部署 |
| `product-only` | gate:product + gate:ship | 0 | **只問我產品的事**——技術部分由流水線決定 |
| `gates-only` | gate:product + gate:arch + gate:ship | 0 | **預設**——標準功能、修 bug |
| `strict` | gate:arch + gate:code + gate:ship | 0 | 需要程式碼審查關卡的新功能 |
| `expert` | 所有關卡 | 每個代理 2 個（計畫 + 結果） | 深度審查、新團隊成員、複雜功能 |
| `step-by-step` | 所有關卡 | 每個子步驟 | 學習模式、關鍵系統 |

各等級為何如此設計、檢查點模式、代理如何讀取等級、覆寫與安全底線：在變更等級或建立關卡之前，**閱讀 `skills/great_cto/reference/approval-level.md`**。

## 流水線版本檢查

只在 PROJECT.md 包含 `locked: true` 時相關。檢查：
{{CODE:5}}
如果已鎖定 → 在套用更新後的流水線規則之前警告 CTO。如果沒有 `locked:`（大多數專案），完全跳過這項檢查。

## 意圖對照

| CTO 說 | 動作 |
|----------|--------|
| 「做 X」／「實作 X」 | 功能流水線 |
| 「修 X」／「bug」／「緊急修正」／「patch」 | 快速路徑 |
| 「重構 X」／「整理」／「重組」／「抽出服務」 | 閱讀 `skills/great_cto/playbooks/large-scale-refactor.md` 並照做 |
| 「升級技術堆疊」／「遷移到 X」／「EOL」／「升級 PHP/Node/Python」 | 閱讀 `skills/great_cto/playbooks/stack-migration.md` 並照做 |
| 「狀態」／「現在怎樣」 | git log + bd stats + 產物 |
| 「有什麼需要我」／「收件匣」 | 關卡 + 被阻擋的 + PR |
| 「稽核」／「審查程式碼庫」／「掃描 repo」 | `/audit` 指令 |
| 「核准」／「看起來不錯」／「好」 | 在這次執行中解決待決的決定；只有在它的身分與範圍毫不含糊時，才套用既有的核准協定。絕不假設是 gate:arch。 |
| 「上線」／「部署」 | 確認 gate:ship → devops |
| 「事故」／「正式環境出問題」／「壞了」 | 產生 `great_cto-l3-support` 代理 |
| 「CI 紅燈」／「建置失敗」／「流水線壞了」／「檢查失敗」 | 產生 `great_cto-ci-resolver` 代理——在任何建置或部署之前 |
| 「稽核合約」／「智慧合約稽核」／「這段 Solidity 安全嗎」／web3 專案中寫好的合約 | 產生 `great_cto-smart-contract-auditor`——在實作之後、gate:ship 之前 |
| 「顯示報告」／「顯示 QA」／「顯示資安」 | 找出最新的對應檔案：`ls docs/qa-reports/ docs/security/ docs/architecture/ 2>/dev/null \| sort \| tail -1` → 讀取並顯示 |
| 「更新代理」 | `/update` 指令 |
| 「把這個流程記下來」／「存成技能」 | `/capture`——訪談 → SKILL.md |
| `/crystallize`／「結晶」／「擷取知識」／「我們學到了什麼？」／「把心得變成技能」 | 派發 `crystallize` 技能 |
| 「重新檢視 ADR」／「重新考慮 ADR-NNN」 | `/revisit`——依目前狀態重新評估 ADR |
| 「摘要」／「每週總結」／「顯示指標」／「DORA」 | `/digest`——速度、DORA 指標、技術債、建議 |
| 「審查程式碼」／「code review」／「檢查 PR」 | `/review`——三個角度的程式碼審查（效能／資安／可讀性） |
| 「記錄決策」／「我們決定 X」／「decision:」 | 在 `docs/decisions/DECISION-LOG.md` 新增一筆——見下方「決策紀錄」 |
| 「規劃階段」／「進入規劃」／「切換到審查／發布階段」 | 更新 PROJECT.md 中的 `phase:`——見下方「階段」 |
| 「流水線狀態」／「我們進行到哪了」 | `/inbox`——任務進度、證據與待決的決定 |
| 「嚴格模式」／「我想審查程式碼」／「加入程式碼審查關卡」 | 在 PROJECT.md 設定 `approval-level: strict` → 在 senior-dev 之後加入 gate:code |
| 「移除程式碼關卡」 | 在 PROJECT.md 設定 `approval-level: gates-only` → 移除 gate:code；說明剩下的關卡 |
| 「自動模式」／「全自動」 | 用 `scripts/lib/approval-level.mjs` 說明 `auto` 及其強制覆寫；只有在使用者要求這個政策時才改為 `auto`。這不是對外部動作的全面授權。 |
| 「專家模式」／「我想審查所有東西」 | 在 PROJECT.md 設定 `approval-level: expert` → 每個代理 2 個檢查點 |

## 流水線規則的執行（以原型為基礎）

每條規則都來自 PROJECT.md 中的 `archetype:`，經由 ARCHETYPES.md 與 TYPE_MAP.md 決定（複合類型取較嚴格的規則）。哪個檔案有哪條規則、多區域的順序：在流水線開始時 **閱讀 `skills/great_cto/reference/archetype-rules.md`**。

## 快速路徑（修 bug／patch）

當請求包含：修、bug、緊急修正、patch、錯字、重新命名、小改——「且」沒有暗示新的元件時使用。

{{CODE:6}}

告訴 CTO：「小改動——跳過架構審查。」

## 完整流水線（新功能）

**階段與其順序就是那張圖**——`shared/pipeline.toml`。每次判定之後，分派器會注入指名下一個階段的 PIPELINE-NEXT；照著走，圖守衛（ADR-039）會記錄——或在 `graph-guard: enforce` 時拒絕——在簡報之後跳過架構的派發，或走了前一階段沒有說明產出的邊。

簡單來說：釐清（最多一個問題，只在不清楚時）→ 腦力激盪 → 決策簡報 → `architect` → gate:arch → `pm` → gate:plan → `senior-dev` → `code-reviewer` ∥ `qa-engineer` ∥ `security-officer` → gate:ship → `devops` → `l3-support` 上線後觀察期。只有在 `approval-level` 讓關卡生效時，關卡才會停下來等 CTO（`reference/approval-level.md`）。

**在新功能的步驟 0 之前，閱讀 `skills/great_cto/reference/full-pipeline.md`**，並在顯示任何關卡之前再讀一次：它包含釐清表、決策簡報、每個關卡要給 CTO 看什麼、回滾驗證與上線後觀察期——這些是圖無法承載的部分。

## 技術堆疊遷移流水線

當請求符合「意圖對照」中的「升級技術堆疊」／「遷移到 X」／「EOL」時，閱讀 `skills/great_cto/playbooks/stack-migration.md` 並從頭到尾照做。

內容沒有改變；它放在 SKILL.md 之外，是因為 SKILL.md 每個請求都會載入，而只適用於一種意圖的操作手冊，不應該讓其他二十種意圖都帶著它。

## 大規模重構流水線

當請求符合「意圖對照」中的「重構 X」／「重組」／「抽出服務」時，閱讀 `skills/great_cto/playbooks/large-scale-refactor.md` 並從頭到尾照做。

內容沒有改變；它放在 SKILL.md 之外，是因為 SKILL.md 每個請求都會載入，而只適用於一種意圖的操作手冊，不應該讓其他二十種意圖都帶著它。

## 檔案負責矩陣

已移到 `skills/great_cto/reference/file-ownership.md`——需要時再讀。

## 稽核流程

產生 `great_cto-project-auditor`。偵測技術堆疊、缺口分析、Beads 任務、PROJECT.md。完成後——重新讀取 PROJECT.md 檢查類型漂移。

## 目錄中的領域代理

當流水線步驟需要核心 7 個之外的專家時，檢查目錄：
{{CODE:7}}

## 回顧累積

每次部署後，會在 `.great_cto/retrospectives/RETRO-<YYYY-MM>.md` 附加一則學習；一個月內出現 3 次的模式會在工作階段開始時呈現。格式與規則：`skills/great_cto/reference/retrospective.md`。

## 階段

四個階段——`planning`、`implementation`（預設）、`review`、`release`——控制 SessionStart hook 要載入哪些上下文。階段「不會」改變流水線、代理或關卡。

當 CTO 說「進入 <階段> 階段」時，更新 PROJECT.md 中的 `phase:` 並確認。完整的階段表 + 切換邏輯 → [`references/phases.md`](references/phases.md)。

## 決策紀錄

當 CTO 說「記錄決策」「我們決定 X」，或以「decision:」開頭的訊息時——在 `docs/decisions/DECISION-LOG.md` 新增一筆。只用於 **非架構性** 的決策（ADR 仍然要經過 architect）。

條目格式、新增邏輯，以及 ADR 與決策紀錄的分流 → [`references/decision-log.md`](references/decision-log.md)。

## 檔案配置不變條件（代理上下文 vs 執行狀態）

已移到 `skills/great_cto/reference/file-layout.md`——需要時再讀。

## 規則

- 一次最多問 CTO 一個問題
- 每個功能的關卡來自核准等級（預設：product + arch + ship）
- 一律顯示產物的連結
- P0 的 Beads 任務優先呈現
- 任何次要類型的「強制」關卡都適用於整個專案
