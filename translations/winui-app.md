<!--meta
{"title":"WinUI 3 桌面應用","category":"前端與設計","tags":["WinUI 3","Windows App SDK","C#","桌面應用","OpenAI Codex"],
"summary":"OpenAI Codex 官方技能：依微軟官方指引、WinUI Gallery 與 Windows App SDK 範例，用 C# 建立、開發與設計現代 WinUI 3 桌面應用——檢查並安裝開發環境、建立新專案、導覽與視窗、主題（預設支援亮暗模式）、無障礙、響應式、效能與部署；每次修改後都會建置並實際啟動驗證視窗出現。",
"usage":"- Codex：`$skill-installer winui-app`（需 Windows）\n- 說「建一個新的 WinUI 筆記 App」「檢查這台電腦能不能開發 WinUI」\n- 會用內附的 WinGet `config.yaml` 安裝 Visual Studio 等必要元件（會改動電腦，純檢查時會先徵求同意）\n- 新專案用 `dotnet new winui -o <名稱>`；優先使用原生 WinUI 控制項而非自製元件"}
-->
---
name: winui-app
description: 使用官方的微軟指引、WinUI Gallery 模式、Windows App SDK 範例與 CommunityToolkit 元件，以 C# 與 Windows App SDK 建立骨架、開發與設計現代的 WinUI 3 桌面應用程式。在建立全新應用程式、為機器準備 WinUI 環境、審查、重構、規劃、疑難排解、檢查環境，或設定 WinUI 3 的 XAML、控制項、導覽、視窗、主題、無障礙、響應式、效能、部署或相關的 Windows 應用程式設計與開發工作時使用。
---

# WinUI 應用程式

當 WinUI 3 與 Windows App SDK 的工作需要有依據的設定指引、應用程式初始化、現代 Windows UX 決策或具體的實作模式時，使用本技能。

## 必要流程

1. 把任務分類為環境/設定、新應用程式初始化、設計、實作、審查或疑難排解。
2. 如果任務是為機器準備 WinUI、稽核準備程度，或建立全新的應用程式，在進行更廣泛的設計、實作或疑難排解之前，先從本技能內附的「設定與建立骨架」流程開始：
   - 當請求是新應用程式時，挑選應用程式名稱。
   - 當使用者給的名稱已經是安全的資料夾名稱時，就使用那個確切的名稱。
   - 如果使用者沒有給名稱，就從請求推導出一個簡短的 PascalCase 名稱，並說明你選了什麼。
   - 除非使用者要求其他位置，否則在使用者目前的工作區中建立專案。
   - 除非使用者明確要求覆寫既有檔案，否則不要使用 `--force`。
   - 從技能目錄執行內附的 WinGet 設定，讓相對路徑剛好是 `config.yaml`：

{{CODE:1}}

   - 把這份設定視為用來啟用開發人員模式、安裝或更新 Visual Studio Community 2026，以及安裝 WinUI 開發所需的 Managed Desktop、Universal 與 Windows App SDK C# 元件。
   - 繼續之前先評估設定的結果。成功就繼續。如果失敗，檢查輸出而不是猜測。如果 `winui` 模板已經可用、且工具鏈可以使用，就記下這個部分失敗並繼續。如果前置條件仍然缺少，就停下來並清楚回報阻礙。
   - 建立骨架之前，確認模板可用：

{{CODE:2}}

   - 對於只做診斷的環境請求，說明內附的初始化可能會改變機器，並在執行前取得確認。如果使用者拒絕變更，就使用 `references/foundation-environment-audit-and-remediation.md` 中的手動驗證指引，並以 `present`、`missing`、`uncertain` 與 `recommended optional tools` 摘要準備程度。
   - 對於全新的應用程式，用 `dotnet new winui -o <name>` 建立骨架。只有在使用者要求時才加入模板選項。支援的選項：`-f|--framework net10.0|net9.0|net8.0`、`-slnx|--use-slnx`、`-cpm|--central-pkg-mgmt`、`-mvvm|--use-mvvm`、`-imt|--include-mvvm-toolkit`、`-un|--unpackaged`、`-nsf|--no-solution-file`、`--force`。不要發明不支援的旗標。如果使用者要求封裝的行為，就傳入 `--unpackaged false`。否則保持模板的預設值。
   - 透過確認預期的專案檔存在，並對產生的 `.csproj` 執行 `dotnet build`，來驗證新的骨架。
   - 依新骨架實際的封裝模型，透過正確的路徑啟動它，並確認出現了真正的頂層視窗，而不是只依賴啟動程序的結束代碼。
3. 閱讀 `references/_sections.md`，然後只載入符合任務的參考檔。
4. 在建立或重構應用程式之前，先明確決定封裝模型。對於類似商店的產品流程以及 Visual Studio 的部署/F5 流程，預設為封裝。當使用者期望每次變更後都能重複執行 CLI 建置與執行、或直接啟動 `.exe` 時，預設為不封裝。
5. 當任務是一個不透明的 XAML 編譯器失敗，例如 `MSB3073` 或 `XamlCompiler.exe` 時，閱讀 `references/foundation-template-first-recovery.md`，並在發明自訂的恢復結構之前，先朝所選封裝模型目前的 `dotnet new winui` 骨架簡化回去。
6. 對於任何建立或變更 WinUI 應用程式的工作，做出一組完整但最小的編輯，然後在回應使用者之前建置並執行應用程式。即使使用者沒有明確要求驗證，也預設這麼做。如果在還有工作要做時，執行中的應用程式實例鎖住了輸出，就停止它、重新建置、重新啟動並繼續驗證。當工作完成且啟動驗證成功時，除非使用者明確要求不要，否則讓最終驗證過的應用程式實例保持執行，留給使用者。
7. 在應用程式顯示客觀的成功訊號之前——例如有回應的頂層視窗、預期的視窗標題或其他清楚的啟動行為——把啟動驗證視為未完成。單單產生了一個程序是不夠的。
8. 需求、API 預期與平台指引，優先參考 Microsoft Learn。
9. 具體的控制項用法、外殼組成與設計細節，優先參考 WinUI Gallery。
10. 情境層級的 API，例如視窗、生命週期、通知、部署與自訂控制項，優先參考 WindowsAppSDK-Samples。
11. 先朝 WinUI 與 Fluent 指引建構。把原生的 WinUI 外殼、控制項、互動與控制項外觀視為預設的實作路徑。
12. 對於成組的指令介面，例如文件動作、編輯器格式、檢視切換或頁面層級的工具列，在用 `Grid`、`StackPanel`、`Border` 或臨時的按鈕組合打造自訂列之前，優先使用原生的 `CommandBar` 或其他標準的 WinUI 指令介面。
13. 除非使用者明確要求這種客製化、既有的產品設計系統已經要求它，或經驗證的平台缺口讓你沒有乾淨的原生選項，否則不要發明應用程式專屬的控制項、量身打造的元件庫或自訂外觀來取代標準的 WinUI 行為。
14. 需要客製化時，在加入 CommunityToolkit 相依或撰寫新的自訂控制項之前，先組合、套用模板或重新設定內建 WinUI 控制項與系統資源的樣式。
15. 只有在內建的 WinUI 控制項或輔助工具無法乾淨地涵蓋需求時，才使用 CommunityToolkit。
16. 預設同時支援亮色與暗色模式。把單一主題的輸出視為例外，需要使用者的明確要求或既有的產品限制。
17. 建構或修改 UI 時，使用能感知主題的資源、系統筆刷與 WinUI 樣式掛鉤，而不是寫死只適用亮色或只適用暗色的顏色。
18. 讓集合版面的捲動擁有權保持明確。當頁面已經在垂直捲動時，不要假設巢狀的 `GridView` 或其他擁有捲動的集合，仍能正確渲染一條水平的海報列。
19. 除非邊框做的是所包含的控制項或父層介面尚未提供的獨特工作，否則不要在章節、清單或卡片周圍加額外的 `Border` 包裝。避免「雙層卡片」的組成，也就是一個章節 `Border` 包住本身就已經渲染成卡片的子項目。
20. 把響應式視為外殼加頁面的問題，而不只是控制項調整大小的問題。為導覽、內距、內容密度以及頁尾/工具區域，規劃明確的寬、中與手機寬度行為，並隨著寬度縮小而簡化或隱藏非必要的 UI。

## 常見路徑

| 請求 | 先閱讀 |
| --- | --- |
| 檢查這台電腦能否建置 WinUI 應用程式 | `references/foundation-environment-audit-and-remediation.md` |
| 安裝缺少的 WinUI 前置條件 | `references/foundation-environment-audit-and-remediation.md` |
| 開始一個新的封裝或不封裝應用程式 | `references/foundation-setup-and-project-selection.md` |
| 在維持以模板骨架為基礎的同時，從不透明的 XAML 編譯器或啟動失敗中恢復 | `references/foundation-template-first-recovery.md` |
| 建置、執行或驗證 WinUI 應用程式確實啟動了 | `references/build-run-and-launch-verification.md` |
| 審查應用程式結構、頁面、資源與繫結 | `references/foundation-winui-app-structure.md` |
| 選擇外殼、導覽、標題列或多視窗模式 | `references/shell-navigation-and-windowing.md` |
| 選擇控制項或響應式版面模式 | `references/controls-layout-and-adaptive-ui.md` |
| 套用 Mica、主題、字體排印、圖示或 Fluent 樣式 | `references/styling-theming-materials-and-icons.md` |
| 改善無障礙、鍵盤操作或在地化 | `references/accessibility-input-and-localization.md` |
| 診斷響應性或 UI 執行緒效能 | `references/performance-diagnostics-and-responsiveness.md` |
| 決定是否使用 CommunityToolkit | `references/community-toolkit-controls-and-helpers.md` |
| 處理生命週期、通知或部署 | `references/windows-app-sdk-lifecycle-notifications-and-deployment.md` |
| 執行審查檢查清單 | `references/testing-debugging-and-review-checklists.md` |

## 環境規則

- 不要猜測機器是否已準備好進行 WinUI 開發。驗證它。
- 對於全新設定、修補與第一個專案的骨架建立，使用本技能內附的「設定與建立骨架」流程，而不是委派給其他技能。
- 把本技能目錄中的 `config.yaml` 視為內附初始化的真實來源。
- 把不確定的環境訊號視為不確定，而不是成功。
- 如果任務只是稽核、且使用者拒絕機器變更，就使用 `references/foundation-environment-audit-and-remediation.md` 中的手動驗證指引，並讓不確定的訊號保持明確，而不是暗示成功。
- 如果缺少 `config.yaml`，就清楚說明，並退回官方的微軟流程，而不是假裝內附的路徑存在。
- 把環境準備程度、封裝選擇與應用程式啟動驗證視為分開的檢查。通過其中一項並不能證明其他項目。
- 對模稜兩可的啟動結果採取保守態度。如果應用程式沒有清楚地開啟，就繼續除錯。
- 建立或編輯 WinUI 應用程式之後，不要停在建置成功。啟動應用程式、確認客觀的啟動行為，並在把控制權交還給使用者之前，讓最終驗證過的應用程式實例保持執行，除非他們明確說不要執行。

## 參考規則

- 以 C# 作為主要路徑。只有在差異很重要時才提到 C++ 或 C++/WinRT。
- 保留既有程式碼庫的慣例，而不是把通用的範例結構強加在它上面。
- 把 WinUI 設計指引與原生控制項視為基準。除非使用者明確要求，或既有程式碼庫已經依賴它們，否則不要偏向量身打造的元件系統，或為標準控制項做應用程式專屬的替代品。
- 對於應用程式 UI 工作，預設支援亮色與暗色模式，除非使用者明確要求單一主題的結果，或產品已經強制使用一種。
- 在加入 CommunityToolkit 相依、自訂控制項或應用程式專屬的介面系統之前，優先使用內建的 WinUI 控制項與系統樣式掛鉤。
- 把詳細的控制項、主題、外殼、捲動、響應式、封裝與恢復指引放在相符的參考檔中，而不是在這裡重複那些規則。
