<!--meta
{"title":"通用軟體上線稽核","category":"程式品質與除錯","tags":["稽核","上線把關","資訊安全","評分","證據"],
"summary":"以毫不留情的標準稽核軟體版本：依內附的《通用軟體工程稽核規格 v2.2》，橫跨安全、架構、UX、隱私等十五個核心領域做全生命週期稽核。每個結論都要追溯到證據，證據不足就標「未驗證」；用腳本做確定性評分，並以硬性停止規則把關上線，不論總分多高都不能蓋過上線關卡。",
"usage":"- 說「幫這個 repo 做上線前稽核」「用 standard 深度稽核這個服務」\n- 先確認目標、深度（rapid／standard／deep）與風險等級（P1–P6）\n- 預設只做被動、唯讀檢查；主動測試需填寫交戰規則並取得明確授權\n- 產物放在 `audits/<稽核ID>/`，評分一律用 `scripts/score.py`\n- 結論只會是：核准／附條件核准／需重工／不得上線"}
-->
---
name: universal-audit
description: '以毫不留情的標準稽核軟體版本。當寬鬆的核准或不完整的範圍可能造成部署風險時使用。橫跨十五個核心領域（包括安全、架構、UX 與隱私）執行全生命週期稽核。套用確定性評分、評估確鑿證據，並以硬性停止規則強制執行上線關卡，不論總分為何。'
license: MIT
metadata:
  version: 1.0.3
---

# 通用稽核——正式的生產環境保證

本技能執行 **《通用軟體工程稽核規格 v2.2》**（內附於 `spec/Universal_Software_Engineering_Audit_Specification.md`）。規格是規範性的。本檔案是執行程序。兩者衝突時，以規格為準。

核心紀律，不可妥協：

- 每個結論都追溯到證據。PASS 需要肯定性的證據，絕不是掃描器沒出聲。
- 證據不足就是 **UNVERIFIED（未驗證）**，直白地說出來，並說明需要什麼才能驗證。
- 絕不捏造缺陷，絕不淡化已驗證的風險，絕不為了看起來周全而灌水發現事項。
- 數字分數永遠不能凌駕上線關卡。

## 階段 0——委任設定（阻擋性）

1. 確認目標：repo 路徑、執行中的 URL，或兩者。在做任何事之前，先讀 `package.json`／`requirements.txt`／`wrangler.toml`／同等檔案。
2. 依 `references/templates/intake-template.md` 填寫受理表。只向操作者詢問你自己無法確立的項目。缺少的輸入放進 **稽核限制**，絕不默默假設。
3. 宣告：稽核類型、深度層級（rapid／standard／deep）、環境、存取層級、保證目標，以及風險設定檔（P1–P6，見 `references/depth-and-profiles.md`）。如果操作者沒有指定深度，提出一個並附上理由，然後等待。
4. 指派稽核 ID：`AUD-[PRODUCT]-[YYYYMMDD]-[SEQ]`。
5. 交戰規則（RoE）：本技能預設為 **被動、唯讀的檢查**。不做負載測試、不做破壞性動作、不嘗試繞過認證、不對操作者不擁有的系統進行測試。主動測試需要完成 RoE 範本，並在清單中記錄操作者的明確授權。
6. 關卡控制：先評估 `GOV-SCOPE-001` 與 `GOV-ROE-001`。如果其中任一無法 PASS，這次委任就只具建議性質——現在就說，不要等到報告裡才說。
7. 建立產物目錄：專案根目錄下的 `audits/<audit-id>/`（或操作者指定的位置）。執行 `scripts/init_audit_artifacts.py --audit-id <audit-id> --output audits/<audit-id>`，從 `assets/audit-manifest-template.json` 建立初始清單。它會拒絕覆寫既有的目錄。

## 階段 1——控制項選擇

1. 載入目錄：規格附錄 A。選擇宣告層級以下（含）的所有控制項（Rapid = R；Standard = R+S；Deep = R+S+D）。設定檔關鍵的控制項不論層級都是必選。
2. 標記為 NOT APPLICABLE（不適用）的控制項要記錄理由。沒有理由的 NA 無效。
3. 依規格 A.0 為每個選定的控制項指派評分類別。沒有類別的控制項屬於驗證失敗。
4. 寫出 `selected-controls.json`（結構定義在 `references/schemas/`）。這會在蒐集任何證據之前凍結涵蓋率的分母——之後不能為了灌高涵蓋率而刪減選擇。

## 階段 2——證據蒐集

依規格第 12 節的順序進行。對每個選定的控制項，蒐集目錄中列出的最低 PASS 證據或更強的證據。各控制項家族的實務指引在 `references/control-procedures.md`。為上線關卡選擇證據時，閱讀 `references/release-evidence-catalog.md`。第一次記錄證據之前，閱讀 `docs/evidence-ledger-guide.md`。

- 在 `evidence-ledger.json` 中記錄每一個重要的觀察：ID、類別、時間戳、位置（file:line、端點、設定鍵）、方法、去敏後的摘錄、限制。
- 無法取得 repository：依賴原始碼的主張標為 `UNVERIFIED - Runtime inference only`。
- 工具輸出（linter、SCA、掃描器）是要評估的證據，不是判決。接受嚴重度之前先驗證。
- 邊做邊去敏：帳本中不得出現密鑰、token、個人資料或可用的攻擊酬載。
- 對於大型目標，依控制項家族把證據蒐集分派給子代理，之後合併成一本帳本。進入階段 3 之前，跨家族去除重複的觀察。

## 階段 3——發現事項與狀態

1. 為每個選定的控制項指派剛好一個狀態：PASS／FAIL／WARN／NOTE／UNVERIFIED／NOT APPLICABLE。
2. 每個 FAIL 與 WARN 都要依二十欄位標準（規格第 9 節）成為一項發現事項，寫入 `findings.json`。嚴重度是影響，可能性另計，信心程度另計。低信心的疑慮通常維持 UNVERIFIED。
3. 圍繞根本原因合併重複項目。只有在四個條件全部成立時，才套用系統性風險規則（規格 13.5）。
4. WARN 不得帶有 Critical 嚴重度。C3 控制項上的 WARN - High 必須通過階段 5 的挑戰，否則重新分類為 FAIL - High。

## 階段 4——評分與判決

1. 執行 `scripts/score.py`：

   ```
   python scripts/score.py audits/<audit-id>/selected-controls.json \
       --profile P4 --tier standard --out audits/<audit-id>/score-sheet.json
   ```

它會計算各類別的暫定分數、套用強制上限、計算相對於層級的涵蓋率（對 Rapid 稽核另算以 Standard 為分母的數字）、驗證類別對應，並評估上線關卡。不要手算分數；腳本是唯一的算術來源。
2. 從腳本的關卡評估，加上腳本無法檢查的質性關卡（關鍵工作流程驗證、暫行控制的負責人），選出剛好一個判決——APPROVED（核准）／APPROVED WITH CONDITIONS（附條件核准）／REQUIRES REWORK（需重工）／DO NOT SHIP（不得上線）。逐條對照關卡說明判決的理由。

## 階段 5——獨立挑戰

Standard 層級：執行一輪獨立的反駁——由一個沒有撰寫這些發現事項的全新子代理，嘗試推翻每一項 Critical／High 發現、每一項對上線有影響的 Medium／WARN，以及每一項支持核准的 C3 PASS，並重新計算評分表。Deep 層級：挑戰必須是真正獨立的代理或人工審查。

在 `verification-log.json` 中記錄每項挑戰的結果：UPHELD（維持）／MODIFIED（修改）／REJECTED（駁回）／NEEDS MORE EVIDENCE（需要更多證據），並附上理由。透明地解決分歧。

## 階段 6——報告與上線

1. 從 `references/templates/report-template.md` 產生 `report.md`。執行摘要最多七句。
2. 確認十二點品質關卡（規格 19.2）。任何一點失敗都代表報告還沒準備好——修好它，不要附註後就交出去。
3. `audits/<audit-id>/` 中的最終產物組：`audit-manifest.json`、`selected-controls.json`、`evidence-ledger.json`、`findings.json`、`score-sheet.json`、`risk-register.json`、`verification-log.json`、`report.md`。
4. 在最終訊息中交付判決、主要風險與涵蓋率數字。使用平實的語言，不危言聳聽，也不淡化。

## 複稽模式

如果操作者提供了先前的稽核 ID 或報告，就執行規格第 16 節，而不是重新做階段 1–3：對照原本的重現方式驗證先前每一項 FAIL／WARN，分類（OPEN 未解決／PARTIALLY REMEDIATED 部分修復／REMEDIATED 已修復／ACCEPTED 已接受／REGRESSED 退步／NOT REPRODUCIBLE 無法重現），重新執行所有適用的 C3 控制項，依目前的證據重新計算，並產出差異表。絕不在未確認證據仍然成立的情況下沿用先前的 PASS。

## 範圍控制

- 時間限制改變的是涵蓋範圍，不是真實性標準。時間用完：剩下的控制項為 UNVERIFIED，並如實回報。
- 絕不把有限的稽核呈現為完整的生產環境保證。
- 如果超出授權範圍、某項測試有造成實質損害的風險，或無法確立受稽核的版本，立即停止。
