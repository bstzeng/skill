<!--meta
{"title":"進階 Git 操作","category":"雲端與 DevOps","tags":["Git","rebase","衝突解決","bisect","reflog"],
"summary":"處理複雜版本控制情境的進階 Git 工作流程：互動式 rebase 整理提交歷史（pick／reword／edit／squash／fixup／drop）、看懂衝突標記並以三方差異解決衝突、用 git bisect 二分搜尋找出引入 bug 的提交、cherry-pick、以 reflog 找回刪除的分支或錯誤 reset，以及 Git Flow 與主幹開發等分支策略。附安全守則與疑難排解。",
"usage":"- 說「幫我在 push 前把這些 WIP 提交整理乾淨」「這個合併衝突怎麼解」「找出是哪個提交讓測試壞掉」「我不小心刪了分支，救得回來嗎」\n- 改寫歷史前一定先 `git branch backup`\n- 絕不 rebase 已推送到共用分支的提交；強制推送用 `--force-with-lease`\n- 詳細範例見 `examples/` 與 `references/`"}
-->
---
name: git-advanced
description: "進階的 Git 操作與工作流程，包括互動式 rebase、衝突解決、歷史操作、用 bisect 找 bug、cherry-pick、reflog 復原與分支管理策略。用於：(1) 互動式 rebase 與整理提交，(2) 複雜的合併衝突解決，(3) 用 Git bisect 追查 bug，(4) 改寫與整理歷史，(5) 實作分支策略（Git Flow、主幹開發），(6) 用 reflog 找回遺失的提交"
---

# 進階 Git 操作

## 概覽

掌握進階的 Git 工作流程，應付複雜的版本控制情境。本技能涵蓋超越基本提交與合併的精細操作，包括互動式 rebase、進階衝突解決、歷史操作與策略性的分支管理。

在以下需要時使用本技能：
- 在程式碼審查前整理凌亂的提交歷史
- 有策略地解決複雜的合併衝突
- 用二分搜尋（bisect）追查 bug
- 找回遺失的提交或復原錯誤
- 實作團隊的分支策略
- 安全地改寫歷史

## 核心能力

### 互動式 Rebase
- 重新排序提交，讓歷史合乎邏輯
- 把多個提交壓縮成一個
- 事後編輯提交訊息
- 把提交拆成更小的部分
- 從歷史中移除不要的提交

### 衝突解決
- 有策略地處理合併衝突
- 理解三方合併
- 選擇 ours 或 theirs 策略
- 解讀衝突標記
- 衝突期間部分暫存檔案

### Git Bisect
- 二分搜尋 bug 的引入點
- 以腳本自動化 bisect
- 辨識好／壞的提交
- 有效率地除錯回歸問題

### 歷史操作
- 安全地修改（amend）提交
- filter-branch 操作
- 用 BFG Repo-Cleaner 清除大型檔案
- 謹慎地改寫歷史
- 保留作者資訊與日期

### 分支策略
- Git Flow 工作流程
- 主幹開發（trunk-based）
- 功能分支工作流程
- 發布分支管理
- 緊急修復程序

## 指令速查

### 互動式 Rebase
{{CODE:1}}

### 衝突解決
{{CODE:2}}

### Git Bisect
{{CODE:3}}

### Cherry-Pick
{{CODE:4}}

### Reflog 復原
{{CODE:5}}

## 核心工作流程

### 1. 互動式 Rebase 工作流程

**何時使用：**
- 推送前整理凌亂的提交歷史
- 合併「WIP」或「修正錯字」之類的提交
- 重新排序提交，讓進展合乎邏輯
- 把大型提交拆成聚焦的變更

**步驟：**

{{CODE:6}}

**Rebase 指令：**
- `pick`（p）：原樣保留提交
- `reword`（r）：保留提交，編輯訊息
- `edit`（e）：保留提交，停下來修改
- `squash`（s）：與前一個提交合併，保留訊息
- `fixup`（f）：與前一個提交合併，捨棄訊息
- `drop`（d）：整個移除提交

**範例：**
{{CODE:7}}

**安全提示：**
- 絕不 rebase 已經推送到共用分支的提交
- 建立備份分支：`git branch backup`
- 出問題時使用 `git reflog`
- 謹慎地強制推送：`git push --force-with-lease`

詳細範例與進階技巧，請見 `examples/interactive_rebase.md`。

### 2. 衝突解決工作流程

**理解衝突標記：**
{{CODE:8}}

**解決流程：**

{{CODE:9}}

**三方差異：**
{{CODE:10}}

常見的衝突模式與解法，請見 `examples/conflict_resolution.md`。

### 3. 用 Git Bisect 追查 Bug

**情境：** 目前版本存在 bug，要找出是哪個提交引入的。

**手動 Bisect：**
{{CODE:11}}

**自動化 Bisect：**
{{CODE:12}}

### 4. 分支管理

**快速清理：**
{{CODE:13}}

**偵測過時的分支：**
{{CODE:14}}

詳細的分支管理策略，請見 `references/branch-management.md`。

### 5. Reflog 復原

**找回刪除的分支：**
{{CODE:15}}

**復原錯誤的 reset：**
{{CODE:16}}

**找回遺失的提交：**
{{CODE:17}}

完整的復原技巧，請見 `references/reflog-recovery.md`。

## 實作分支策略

本技能支援實作各種分支策略。依團隊的需求選擇：

### Git Flow
**最適合：** 有排定發布時程、多個生產版本的專案

**分支類型：**
- `main`：可上線的程式碼
- `develop`：整合分支
- `feature/*`：新功能
- `release/*`：發布準備
- `hotfix/*`：生產環境修復

**快速開始：**
{{CODE:18}}

### 主幹開發（Trunk-Based Development）
**最適合：** 持續部署、步調快速的團隊

**原則：**
- 單一的 main 分支
- 短命的功能分支（< 1 天）
- 頻繁整合
- 未完成的工作用功能旗標控制

**快速開始：**
{{CODE:19}}

完整的分支策略工作流程，請見 `examples/branch_strategies.md`。

## 最佳實務

### Rebase 之前
- 建立備份分支：`git branch backup`
- 確保工作目錄是乾淨的：`git status`
- 了解你的提交歷史：`git log --oneline`
- 絕不 rebase 公開／共用的分支

### 衝突期間
- 理解衝突雙方的內容
- 解決後徹底測試
- 使用有意義的合併提交訊息
- 記錄複雜的解決方式

### 分支管理
- 及時刪除已合併的分支
- 使用具描述性的分支名稱：`feature/user-login`
- 讓分支保持聚焦且短命
- 定期與 main 分支同步

### 歷史衛生
- 推送前壓縮「fixup」提交
- 撰寫清楚、具描述性的提交訊息
- 保持提交的原子性（一個邏輯變更）
- 可能的話使用 Conventional Commits 格式

完整的最佳實務，請見 `references/best-practices.md`。

## 疑難排解

### Rebase 衝突
{{CODE:20}}

### 遺失的提交
{{CODE:21}}

### 分離的 HEAD 狀態
{{CODE:22}}

### Rebase 後推送失敗
{{CODE:23}}

詳細的疑難排解，請見 `references/troubleshooting.md`。

## 其他資源

### 詳細指南
- `examples/interactive_rebase.md`：附情境的逐步 rebase 範例
- `examples/conflict_resolution.md`：常見的衝突模式與解法
- `examples/branch_strategies.md`：完整的 Git Flow 與主幹開發工作流程

### 參考文件
- `references/branch-management.md`：分支清理自動化與策略
- `references/reflog-recovery.md`：復原技巧與歷史改寫
- `references/best-practices.md`：完整的最佳實務與品質標準
- `references/troubleshooting.md`：常見問題與緊急復原

### 輔助腳本
- `scripts/git_helper.sh`：分支清理與衝突解決工具

## 速查指令

### 必知指令
{{CODE:24}}

### 安全第一
1. 改寫歷史前一律備份：`git branch backup`
2. 絕不強制推送到共用分支：使用 `--force-with-lease`
3. 衝突後要測試：不要假設解決方式是正確的
4. 記錄複雜的操作：在合併提交中留下註解
5. 善用 reflog：它是你 30 天以上的安全網

---

掌握這些進階 Git 操作，保持乾淨的歷史、有效率地解決衝突，並有自信地管理複雜的開發工作流程。
