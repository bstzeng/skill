<!--meta
{"title": "Figma Plugin API 操作", "category": "前端與設計", "tags": ["Figma", "Plugin API", "MCP", "OpenAI Codex"], "summary": "OpenAI Codex 官方技能：每次呼叫 use_figma 之前都必須先載入的前置技能。透過 Plugin API 在 Figma 檔案中執行 JavaScript——建立、編輯、刪除節點，設定變數與 token、建立元件與變體、修改 auto-layout 或填色、綁定變數，或以程式檢查檔案結構；內含頁面規則、回傳值規則、漸進式工作流程與錯誤恢復方法。", "usage": "- Codex：`$skill-installer figma-use`；需要 Figma MCP Server\n- 代理在任何 Figma 寫入動作前會自動載入；要建整頁畫面時再搭配 figma-generate-design\n- 授權為 Figma Developer Terms，本站只提供中文介紹"}
-->
