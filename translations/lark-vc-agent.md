<!--meta
{"title": "飛書會議代理（舊名相容）", "category": "文件與辦公", "tags": ["飛書", "Lark", "視訊會議", "相容入口"], "summary": "為了相容舊名稱而保留的入口：只在使用者或上游設定明確指定 lark-vc-agent 時使用，實際工作一律轉交 lark-meeting 技能處理。原文為簡體中文，以 OpenCC 轉為台灣繁體。", "usage": "- 安裝：`npx skills add https://github.com/larksuite/cli --skill lark-vc-agent`（需同時安裝 lark-meeting）\n- 一般不必直接使用；舊設定指名 lark-vc-agent 時，代理會讀取 lark-meeting 並照它的指引執行"}
-->
---
name: lark-vc-agent
version: 1.0.0
description: "僅當使用者或上游配置顯式指定 lark-vc-agent 時使用，相關請求統一交由 lark-meeting 技能處理。"
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-meeting"]
---

# Compatibility entry

本技能只用於相容舊名稱，不直接處理業務。

**MUST 完整讀取 [`../lark-meeting/SKILL.md`](../lark-meeting/SKILL.md)，並按照其中的路由和行動指南執行。**
