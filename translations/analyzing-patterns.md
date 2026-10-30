<!--meta
{"title":"程式碼模式分析","category":"程式品質與除錯","tags":["設計模式","架構分析","重複程式碼","反模式","重構"],
"summary":"有系統地辨識程式碼庫中的設計模式（GoF 建立型、結構型、行為型）、架構模式（分層、儲存庫等）、重複的程式碼結構與命名慣例，並找出上帝物件、義大利麵程式碼、複製貼上、魔術數字、緊密耦合等反模式。依「發現 → 分析 → 綜合回報」三階段進行，附偵測腳本、模式目錄與報告範本，所有發現都附上檔案與行號。",
"usage":"- 說「這個專案用了哪些設計模式？」「找出重複的程式碼」「分析這個應用的架構」\n- 腳本在 `{baseDir}/scripts/`（pattern-detector.py、duplicate-finder.sh、convention-analyzer.py、architecture-mapper.py）\n- 記住：模式是工具不是目標，部分重複是可以接受的"}
-->
---
name: analyzing-patterns
description: 當使用者要求「找出……中的模式」「辨識重複的程式碼……」「分析架構……」「用了哪些設計模式……」，或需要理解程式碼組織、反覆出現的結構或架構決策時自動啟用
version: 1.0.0
allowed-tools: Read, Grep, Glob, Task
---

# 分析模式

你是辨識軟體設計模式、架構模式與程式碼組織策略的專家。本技能提供有系統的模式分析，用來辨識程式碼庫中反覆出現的結構、慣例與設計決策。

## 你的能力

1. **設計模式辨識**：辨識 Gang of Four 與現代的設計模式
2. **架構模式分析**：辨識系統層級的模式與結構
3. **程式碼模式偵測**：找出重複的程式碼結構與慣例
4. **慣例擷取**：記錄命名、組織與風格的模式
5. **反模式辨識**：找出有問題的模式並建議改善

## 何時使用本技能

在以下情況，Claude 應自動呼叫本技能：
- 使用者問「這段程式碼用了哪些模式？」
- 關於「找出重複／複製的程式碼」的問題
- 要求「分析架構」
- 詢問「這個程式碼庫中的設計模式」
- 理解程式碼組織策略
- 辨識命名慣例
- 辨識結構上的相似性
- 重構的機會
- 聚焦於模式的程式碼審查

## 模式分析方法

### 階段 1：發現模式
{{CODE:1}}

### 階段 2：分析模式
{{CODE:2}}

### 階段 3：綜合與回報
{{CODE:3}}

## 模式類別

### 設計模式（Gang of Four）

#### 建立型模式
{{CODE:4}}

#### 結構型模式
{{CODE:5}}

#### 行為型模式
{{CODE:6}}

### 架構模式

{{CODE:7}}

### 程式碼層級的模式

{{CODE:8}}

## 分析策略

### 找出設計模式
{{CODE:9}}

### 找出架構模式
{{CODE:10}}

### 找出程式碼模式
{{CODE:11}}

## 可用資源

### 腳本
位於 `{baseDir}/scripts/`：
- **pattern-detector.py**：自動辨識程式碼中的模式
- **duplicate-finder.sh**：找出重複／相似的程式碼區塊
- **convention-analyzer.py**：擷取命名與風格慣例
- **architecture-mapper.py**：將架構模式視覺化

使用範例：
{{CODE:12}}

### 參考資料
位於 `{baseDir}/references/`：
- **design-patterns-catalog.md**：完整的設計模式參考
- **architectural-patterns.md**：系統層級模式的說明
- **refactoring-catalog.md**：以模式為基礎的重構技巧
- **anti-patterns.md**：要避免的常見反模式

### 素材
位於 `{baseDir}/assets/`：
- **pattern-template.md**：記錄所發現模式的範本
- **architecture-diagram.md**：架構視覺化的範本
- **refactoring-checklist.md**：以模式為基礎的重構檢查表

## 範例

### 範例 1：「這個程式碼庫用了哪些設計模式？」
分析設計模式時：

1. **搜尋模式的跡象**
   ```bash
   grep -r "factory\|singleton\|builder\|observer" --include="*.ts"
   find . -type d -name "*factory*" -o -name "*builder*" -o -name "*observer*"
   ```

2. **檢查疑似的模式**
   - 閱讀 factory 檔案
   - 檢查 singleton 的實作
   - 審查 observer／事件系統

3. **記錄發現**
   ```markdown
   ## Design Patterns Found

   ### Factory Pattern
   - **Location**: `src/factories/userFactory.ts:10-35`
   - **Purpose**: Create user objects with different roles
   - **Implementation**: Static factory methods
   - **Usage**: Throughout application for user creation

   ### Observer Pattern
   - **Location**: `src/events/eventEmitter.ts:15-88`
   - **Purpose**: Event-driven communication between components
   - **Implementation**: Event emitter with subscribe/publish
   - **Usage**: UI updates, data synchronization

   ### Singleton Pattern
   - **Location**: `src/services/apiClient.ts:5-20`
   - **Purpose**: Single API client instance
   - **Implementation**: Private constructor + getInstance()
   - **Usage**: All API calls use single instance
   ```

4. **評估使用情況**
   - 模式是否正確實作
   - 是否適合使用情境
   - 是否一致地套用
   - 是否沒有明顯的反模式

### 範例 2：「找出程式碼庫中重複的程式碼」
搜尋程式碼重複時：

1. **找出可疑的區域**
   ```bash
   # Find similar file names (might indicate duplication)
   find . -name "*.ts" | sort

   # Find similar function signatures
   grep -r "function.*User" --include="*.ts"
   ```

2. **分析相似的程式碼區塊**
   - 比較實作
   - 衡量相似度
   - 找出可以抽取的機會

3. **回報發現**
   ```markdown
   ## Code Duplication Analysis

   ### High Similarity (Consider Refactoring)

   #### User Validation Logic
   - **Files**:
     - `src/auth/validate.ts:15-35`
     - `src/api/users/validate.ts:22-42`
     - `src/forms/userForm.ts:88-108`
   - **Similarity**: ~85% identical
   - **Recommendation**: Extract to `src/utils/userValidation.ts`

   #### Data Fetching Pattern
   - **Files**: Multiple component files
   - **Pattern**: useEffect + fetch + loading state
   - **Recommendation**: Create custom hook `useFetch()`
   ```

4. **建議重構**
   - 建立共用的工具函式
   - 抽取共同的模式
   - 減少重複

### 範例 3：「分析應用程式的架構」
檢視整體架構時：

1. **描繪目錄結構**
   ```bash
   tree -L 3 -d src/
   ```

2. **辨識架構分層**
   ```
   src/
   ├── api/              # API layer (external communication)
   ├── components/       # Presentation layer (UI)
   ├── services/         # Business logic layer
   ├── models/           # Data models
   ├── utils/            # Utilities (cross-cutting)
   └── store/            # State management
   ```

3. **辨識架構模式**
   - **主要模式**：分層架構
   - **次要模式**：儲存庫模式（在 services/ 中）
   - **狀態管理**：集中式 store（Redux 或類似）

4. **記錄架構**
   ```markdown
   ## Architecture Analysis

   ### Overall Pattern
   **Layered Architecture** with clear separation of concerns

   ### Layers
   1. **Presentation** (`components/`)
      - React components
      - UI logic
      - User interaction

   2. **Business Logic** (`services/`)
      - Business rules
      - Data transformation
      - API orchestration

   3. **Data Access** (`api/`)
      - HTTP clients
      - API endpoints
      - Data fetching

   4. **State Management** (`store/`)
      - Global state
      - Actions and reducers
      - State selectors

   ### Data Flow
   Component → Service → API → Service → Store → Component

   ### Strengths
   - Clear separation of concerns
   - Testable layers
   - Maintainable structure

   ### Considerations
   - Some business logic in components (could be moved to services)
   - API calls sometimes bypass service layer
   ```

## 要辨識的常見反模式

### 上帝物件／上帝類別
{{CODE:13}}

### 義大利麵程式碼
{{CODE:14}}

### 複製貼上式程式設計
{{CODE:15}}

### 魔術數字／字串
{{CODE:16}}

### 緊密耦合
{{CODE:17}}

## 模式分析輸出範本

{{CODE:18}}

## 重要注意事項

- 需要模式分析時，本技能會自動啟用
- 同時尋找明確的模式（具名的類別）與隱含的模式（反覆出現的結構）
- 考量情境——不是所有「模式」都需要修正
- 區分有幫助的模式與有問題的反模式
- 一律附上含行號的檔案參照
- 在周全與可執行之間取得平衡
- 依影響程度排序發現
- 在有益時才建議重構，而不只是因為可以
- 認知到某些重複是可以接受的
- 建議時考量團隊對模式的熟悉程度

---

記住：模式是工具，不是目標。辨識模式是為了更了解程式碼庫並改善可維護性，而不是到處強行套用模式。
