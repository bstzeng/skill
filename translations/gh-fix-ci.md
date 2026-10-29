<!--meta
{"title":"修復 PR 的 CI 失敗","category":"雲端與 DevOps","tags":["GitHub Actions","CI/CD","gh CLI","除錯","OpenAI Codex"],
"summary":"用 gh CLI 找出 PR 中失敗的 GitHub Actions 檢查，抓取日誌、摘要失敗片段、擬定修復計畫，經你明確核准後才動手修改。",
"usage":"- Codex：`$skill-installer gh-fix-ci`；其他代理複製 skill 資料夾即可\n- 先 `gh auth login`（需 repo + workflow 權限）\n- 說「幫我看這個 PR 為什麼 CI 掛了」，或直接執行 `python scripts/inspect_pr_checks.py --repo . --pr 123`\n- Buildkite 等外部 CI 不處理，只回報連結"}
-->
---
name: "gh-fix-ci"
description: "當使用者要求除錯或修復在 GitHub Actions 中執行、失敗的 GitHub PR 檢查時使用；用 `gh` 檢視檢查與日誌、摘要失敗脈絡、擬定修復計畫，並且只在明確核准後才實作。把外部供應商（例如 Buildkite）視為範圍外，只回報其詳細資訊 URL。"
---


# Gh PR 檢查：規劃與修復

## 概述

用 gh 找出失敗的 PR 檢查，針對可處理的失敗抓取 GitHub Actions 日誌，摘要失敗片段，然後提出修復計畫，並在明確核准後實作。
- 如果有以規劃為主的技能（例如 `create-plan`）可用就使用它；否則直接擬定簡潔的計畫，並在實作前請求核准。

前置條件：用標準 GitHub CLI 驗證一次（例如執行 `gh auth login`），再用 `gh auth status` 確認（通常需要 repo + workflow 權限範圍）。

## 輸入

- `repo`：repo 內的路徑（預設 `.`）
- `pr`：PR 編號或 URL（選填；預設為目前分支的 PR）
- 該 repo 主機的 `gh` 驗證

## 快速開始

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- 如果想要方便機器摘要的輸出，加上 `--json`。

## 工作流程

1. 驗證 gh 是否已登入。
   - 在 repo 中執行 `gh auth status`。
   - 如果未驗證，先請使用者執行 `gh auth login`（確保有 repo + workflow 權限）再繼續。
2. 確定 PR。
   - 優先使用目前分支的 PR：`gh pr view --json number,url`。
   - 如果使用者提供了 PR 編號或 URL，就直接使用。
3. 檢查失敗的檢查（僅限 GitHub Actions）。
   - 建議做法：執行內附的腳本（會處理 gh 欄位變動與 job 日誌的備援）：
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - 加上 `--json` 取得方便機器處理的輸出。
   - 手動備援：
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - 如果某個欄位被拒絕，就改用 `gh` 回報的可用欄位重新執行。
     - 對每個失敗的檢查，從 `detailsUrl` 取出 run id 並執行：
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - 如果 run 日誌顯示仍在執行中，就直接抓取 job 日誌：
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. 界定非 GitHub Actions 的檢查。
   - 如果 `detailsUrl` 不是 GitHub Actions 的 run，就標記為外部並只回報 URL。
   - 不要嘗試處理 Buildkite 或其他供應商；保持流程精簡。
5. 向使用者摘要失敗情形。
   - 提供失敗檢查的名稱、run URL（如果有）以及精簡的日誌片段。
   - 明確指出缺少日誌的情況。
6. 建立計畫。
   - 使用 `create-plan` 技能擬定簡潔的計畫並請求核准。
7. 核准後實作。
   - 套用核准的計畫，摘要 diff 與測試，並詢問是否要開 PR。
8. 重新檢查狀態。
   - 修改後，建議重新執行相關測試與 `gh pr checks` 以確認。

## 內附資源

### scripts/inspect_pr_checks.py

抓取失敗的 PR 檢查、拉取 GitHub Actions 日誌，並擷取失敗片段。仍有失敗時會以非零狀態碼結束，因此可用於自動化。

使用範例：
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
