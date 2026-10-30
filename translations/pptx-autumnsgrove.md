<!--meta
{"title":"PowerPoint 簡報製作（python-pptx）","category":"文件與辦公","tags":["PowerPoint","PPTX","python-pptx","圖表","自動化"],
"summary":"用 Python 的 python-pptx 函式庫建立、編輯與自動化 PowerPoint 簡報：七個工作流程涵蓋商業簡報、長條／折線／圓餅圖、圖片、表格、編輯既有簡報、套用範本，以及從 CSV／JSON 批次產生投影片。附設計原則（60-30-10 配色、WCAG 對比、三分法、6×6 規則）、常見模式與疑難排解，以及 `pptx_helper.py` 輔助函式。",
"usage":"- 安裝：`pip install python-pptx`\n- 說「用這份 CSV 每一列產生一張投影片」「做一份 10 頁的季度報告簡報並加上圖表」「把舊簡報裡的公司名稱全部換掉」\n- 輔助函式在 `scripts/pptx_helper.py`\n- 完整範例在 `examples/`，設計指引在 `references/design-best-practices.md`"}
-->
---
name: pptx
description: "專業的 PowerPoint 簡報建立、編輯與自動化，支援版面配置、範本、圖表、圖片與格式設定。處理 .pptx 檔案時使用，用於：(1) 從零建立簡報，(2) 編輯既有簡報，(3) 套用範本與佈景主題，(4) 加入圖表與視覺化，(5) 批次產生投影片，(6) 簡報自動化"
---

# PowerPoint（PPTX）技能

## 概覽

本技能使用 Python 的 `python-pptx` 函式庫，提供全面的 PowerPoint 簡報建立、編輯與自動化能力。以程式方式建立專業的簡報，完整掌控版面配置、佈景主題、內容、圖表與視覺化。

## 核心能力

- **建立簡報**：新簡報、範本、中繼資料、頁面設定
- **投影片管理**：以預定義的版面配置新增、複製、刪除、重新排序投影片
- **內容類型**：文字、圖形、圖片、表格、圖表、SmartArt、超連結
- **設計與格式**：佈景主題、配色、字型、填色、框線、效果
- **進階功能**：轉場、動畫、內嵌物件、影片／音訊、註解

## 安裝

安裝必要的函式庫：

{{CODE:1}}

基本的 import：

{{CODE:2}}

完整的函式庫設定與輔助套件（Pillow、pandas、matplotlib），請見 `references/library-setup.md`。

## 核心工作流程

### 工作流程 1：建立商業簡報

**目標：** 建立一份包含標題投影片、內容投影片與結論的專業簡報。

**步驟：**

1. **初始化簡報**
   - 建立新的簡報物件
   - 設定投影片尺寸（標準 16:9 或 4:3）
   - 設定中繼資料（標題、作者、主旨、關鍵字）

2. **加入標題投影片**
   - 使用標題投影片版面（通常是 `prs.slide_layouts[0]`）
   - 設定標題與副標題文字
   - 套用格式（字級、顏色、粗體）

3. **加入內容投影片**
   - 使用適當的版面配置（項目符號、雙欄、僅標題、空白）
   - 填入預留位置或加入文字方塊
   - 以適當的層級設定文字格式

4. **加入視覺元素**
   - 以適當的大小與位置插入圖片
   - 加入資料格式化的圖表
   - 建立帶儲存格樣式的表格

5. **儲存簡報**
   - 存成 .pptx 格式
   - 確認檔案已建立

**快速範例：**

{{CODE:3}}

完整實作請見 `examples/business-presentation.md`。

### 工作流程 2：加入圖表

**目標：** 用長條圖、折線圖與圓餅圖建立資料視覺化。

**步驟：**

1. 使用 `CategoryChartData` 準備圖表資料
2. 定義類別與數列
3. 以指定位置把圖表加入投影片
4. 設定圖表格式（圖例、格線、標籤）

**快速範例：**

{{CODE:4}}

所有圖表類型請見 `examples/chart-examples.md`。

### 工作流程 3：處理圖片

**目標：** 在簡報中加入圖片並設定位置與格式。

**步驟：**

1. 用 `slide.shapes.add_picture()` 加入圖片
2. 指定位置（left、top）與大小（width、height）
3. 需要時計算置中的位置
4. 加入前先最佳化圖片（用 Pillow 做前處理）

**快速範例：**

{{CODE:5}}

進階技巧請見 `examples/image-handling.md`。

### 工作流程 4：建立表格

**目標：** 加入帶格式的結構化資料表格。

**步驟：**

1. 定義表格尺寸（列、欄）
2. 以指定位置加入表格
3. 設定欄寬
4. 以粗體格式與背景色填入標題列
5. 以適當的對齊填入資料儲存格

**快速範例：**

{{CODE:6}}

進階格式請見 `examples/table-examples.md`。

### 工作流程 5：編輯既有簡報

**目標：** 修改既有的 PowerPoint 檔案。

**步驟：**

1. 用 `Presentation('file.pptx')` 開啟簡報
2. 逐一走訪投影片找出內容
3. 修改文字、圖形或加入新元素
4. 以相同或不同的檔名儲存

**快速範例：**

{{CODE:7}}

投影片複製與進階編輯請見 `examples/editing-presentations.md`。

### 工作流程 6：使用範本

**目標：** 用母片與範本套用一致的品牌形象。

**步驟：**

1. 從範本檔案開始：`Presentation('template.pptx')`
2. 檢視可用的版面配置
3. 使用範本的版面配置新增投影片
4. 一致地套用品牌色彩

**快速範例：**

{{CODE:8}}

母片自訂請見 `references/templates-and-themes.md`。

### 工作流程 7：批次產生投影片

**目標：** 從資料自動產生多張投影片。

**步驟：**

1. 從 CSV、JSON 或資料庫載入資料
2. 建立簡報物件
3. 逐一走訪資料紀錄
4. 每筆紀錄產生一張投影片
5. 用紀錄資料填入投影片

**快速範例：**

{{CODE:9}}

完整實作請見 `examples/bulk-generation.md`。

## 設計原則

### 色彩與字型
- 使用 60-30-10 配色法則（60% 主色、30% 輔色、10% 強調色）
- 確保符合 WCAG AA 對比度（最低 4.5:1）
- 最多使用 2 種字型家族
- 內文最小 18pt 以確保可讀性

### 版面與構圖
- 依三分法放置元素
- 四邊至少保留 0.5 吋邊界
- 每張投影片限制 5–7 個元素
- 使用一致的對齊（對齊格線）

### 視覺層級
- 大小代表重要性（越大越重要）
- 用色彩對比做強調
- 依 Z 字形安排內容流向

### 圖表最佳實務
- 選擇適當的圖表類型（比較用長條圖、趨勢用折線圖、部分與整體用圓餅圖）
- 最多使用 3–5 種顏色
- 一律標示座標軸並加上資料標籤
- 節制地使用格線

完整的設計指引請見 `references/design-best-practices.md`。

## 常見模式

### 套用品牌色彩

{{CODE:10}}

### 置中元素

{{CODE:11}}

### 文字自動調整

{{CODE:12}}

## 疑難排解速查

**「ModuleNotFoundError: No module named 'pptx'」**
{{CODE:13}}

**「AttributeError: 'NoneType' object has no attribute...」**
- 檢查預留位置索引：`[p.placeholder_format.idx for p in slide.placeholders]`
- 確認版面配置有預期的預留位置

**找不到圖片**
- 使用絕對路徑：`os.path.abspath('image.png')`
- 確認檔案存在：`os.path.exists(img_path)`

**文字放不下**
- 啟用自動調整：`text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`
- 以刪節號截斷長文字

**檔案太大**
- 加入前先壓縮圖片（用 Pillow）
- 把圖片縮放到簡報的尺寸（最大 1920x1080）

完整的疑難排解請見 `references/troubleshooting.md`。

## 輔助腳本

`scripts/pptx_helper.py` 模組提供以下工具函式：

- `create_presentation()`：以預設值初始化
- `add_title_slide()`：加入有格式的標題投影片
- `add_bullet_slide()`：加入含項目符號的投影片
- `add_image_slide()`：加入含置中圖片的投影片
- `add_chart_slide()`：加入含圖表的投影片
- `add_table_slide()`：加入有格式的表格
- `apply_brand_colors()`：套用一致的配色
- `optimize_images()`：批次最佳化圖片

**用法：**

{{CODE:14}}

## 其他資源

### 文件
- python-pptx：https://python-pptx.readthedocs.io/
- API 參考：https://python-pptx.readthedocs.io/en/latest/api/
- GitHub：https://github.com/scanny/python-pptx

### 詳細參考
- [函式庫設定與安裝](./references/library-setup.md)
- [設計最佳實務](./references/design-best-practices.md)
- [範本與佈景主題](./references/templates-and-themes.md)
- [進階技巧](./references/advanced-techniques.md)
- [常見陷阱](./references/troubleshooting.md)

### 範例
- [完整的商業簡報](./examples/business-presentation.md)
- [圖表範例（長條、折線、圓餅）](./examples/chart-examples.md)
- [圖片處理](./examples/image-handling.md)
- [表格範例](./examples/table-examples.md)
- [編輯既有簡報](./examples/editing-presentations.md)
- [從資料批次產生](./examples/bulk-generation.md)

### 設計資源
- Microsoft 設計範本：https://templates.office.com/powerpoint
- 配色工具：Coolors.co、Adobe Color
- 免費圖庫：Unsplash、Pexels

## 最佳實務摘要

1. 一律使用範本以維持一致的品牌形象
2. 加入簡報前先最佳化圖片
3. 限制每張投影片的文字（最多 5–7 個項目）
4. 使用高對比以確保可讀性
5. 簡報前在目標裝置上測試
6. 讓檔案大小保持可控（以電子郵件寄送時 <20MB）
7. 用講者備忘稿記錄詳細的講述重點
8. 遵循 6x6 規則：最多 6 個項目，每個項目最多 6 個字
9. 建立圖表前先驗證資料
10. 使用一致的間距與對齊

---

**何時使用本技能：**
- 從資料建立商業簡報
- 自動化報告產生
- 從資料庫批次建立投影片
- 以範本為基礎的簡報
- 含圖表／圖片的教育內容
- 把文件轉換成投影片
