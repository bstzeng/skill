<!--meta
{"title":"Scanpy 單細胞分析","category":"AI 整合與開發工具","tags":["Scanpy","單細胞 RNA-seq","生物資訊","UMAP","AnnData"],
"summary":"用 Scanpy（建立在 AnnData 上的 Python 工具包）進行完整的單細胞 RNA-seq 分析：載入 .h5ad／10X 資料、品質控管、標準化、高變異基因選擇、PCA／UMAP／t-SNE、Leiden 分群、找出標記基因、細胞類型註解、軌跡推斷、條件間差異表現、基因集評分與批次校正，並產出可發表品質的圖表。附 QC 腳本、分析範本與參數調整建議。",
"usage":"- 需要 Python 與 scanpy（`pip install scanpy`）\n- 說「幫我分析這份 10X 單細胞資料並做 UMAP 分群」「找出每個 cluster 的標記基因」\n- 自動 QC：`scripts/qc_analysis.py`；完整範本：`assets/analysis_template.py`\n- 篩選基因前記得先保存原始計數：`adata.raw = adata`"}
-->
---
name: scanpy
description: "單細胞 RNA-seq 分析。載入 .h5ad／10X 資料、QC、標準化、PCA/UMAP/t-SNE、Leiden 分群、標記基因、細胞類型註解、軌跡，用於 scRNA-seq 分析。"
---

# Scanpy：單細胞分析

## 概覽

Scanpy 是一個可擴展、用於分析單細胞 RNA-seq 資料的 Python 工具包，建立在 AnnData 之上。使用本技能進行完整的單細胞工作流程，包括品質控管、標準化、降維、分群、標記基因辨識、視覺化與軌跡分析。

## 何時使用本技能

在以下情況應使用本技能：
- 分析單細胞 RNA-seq 資料（.h5ad、10X、CSV 格式）
- 對 scRNA-seq 資料集進行品質控管
- 建立 UMAP、t-SNE 或 PCA 視覺化
- 辨識細胞群集並找出標記基因
- 依基因表現註解細胞類型
- 進行軌跡推斷或擬時序分析
- 產生可發表品質的單細胞圖表

## 快速開始

### 基本匯入與設定

{{CODE:1}}

### 載入資料

{{CODE:2}}

### 理解 AnnData 結構

AnnData 物件是 scanpy 的核心資料結構：

{{CODE:3}}

## 標準分析工作流程

### 1. 品質控管

辨識並過濾低品質的細胞與基因：

{{CODE:4}}

**使用 QC 腳本進行自動化分析：**
{{CODE:5}}

### 2. 標準化與前處理

{{CODE:6}}

### 3. 降維

{{CODE:7}}

### 4. 分群

{{CODE:8}}

### 5. 辨識標記基因

{{CODE:9}}

### 6. 細胞類型註解

{{CODE:10}}

### 7. 儲存結果

{{CODE:11}}

## 常見任務

### 建立可發表品質的圖表

{{CODE:12}}

完整的視覺化範例請參考 `references/plotting_guide.md`。

### 軌跡推斷

{{CODE:13}}

### 條件之間的差異表現

{{CODE:14}}

### 基因集評分

{{CODE:15}}

### 批次校正

{{CODE:16}}

## 需要調整的關鍵參數

### 品質控管
- `min_genes`：每個細胞的最少基因數（通常 200–500）
- `min_cells`：每個基因的最少細胞數（通常 3–10）
- `pct_counts_mt`：粒線體門檻（通常 5–20%）

### 標準化
- `target_sum`：每個細胞的目標計數（預設 1e4）

### 特徵選擇
- `n_top_genes`：高變異基因（HVG）數量（通常 2000–3000）
- `min_mean`、`max_mean`、`min_disp`：HVG 選擇參數

### 降維
- `n_pcs`：主成分數量（查看變異比例圖）
- `n_neighbors`：鄰居數量（通常 10–30）

### 分群
- `resolution`：分群的細緻度（0.4–1.2，越高群集越多）

## 常見陷阱與最佳實務

1. **一律保存原始計數**：在過濾基因之前 `adata.raw = adata`
2. **仔細檢查 QC 圖**：依資料集品質調整門檻
3. **使用 Leiden 而非 Louvain**：更有效率、結果更好
4. **嘗試多種分群解析度**：找出最佳的細緻度
5. **驗證細胞類型註解**：使用多個標記基因
6. **基因表現圖使用 `use_raw=True`**：顯示原始計數
7. **檢查 PCA 變異比例**：決定最佳的主成分數量
8. **儲存中間結果**：長流程可能在中途失敗

## 內附資源

### scripts/qc_analysis.py
自動化的品質控管腳本，會計算指標、產生圖表並過濾資料：

{{CODE:17}}

### references/standard_workflow.md
完整的逐步工作流程，附詳細說明與程式碼範例，涵蓋：
- 資料載入與設定
- 附視覺化的品質控管
- 標準化與縮放
- 特徵選擇
- 降維（PCA、UMAP、t-SNE）
- 分群（Leiden、Louvain）
- 標記基因辨識
- 細胞類型註解
- 軌跡推斷
- 差異表現

從零開始進行完整分析時閱讀這份參考。

### references/api_reference.md
依模組整理的 scanpy 函式速查指南：
- 讀寫資料（`sc.read_*`、`adata.write_*`）
- 前處理（`sc.pp.*`）
- 工具（`sc.tl.*`）
- 繪圖（`sc.pl.*`）
- AnnData 結構與操作
- 設定與工具函式

用於快速查詢函式簽名與常用參數。

### references/plotting_guide.md
完整的視覺化指南，包括：
- 品質控管圖
- 降維視覺化
- 分群視覺化
- 標記基因圖（熱圖、點圖、小提琴圖）
- 軌跡與擬時序圖
- 可發表品質的客製化
- 多面板圖
- 配色與樣式

建立可發表的圖表時參考這份指南。

### assets/analysis_template.py
完整的分析範本，提供從資料載入到細胞類型註解的完整工作流程。複製並客製化這個範本以進行新的分析：

{{CODE:18}}

範本包含所有標準步驟，附可設定的參數與有用的註解。

## 其他資源

- **Scanpy 官方文件**：https://scanpy.readthedocs.io/
- **Scanpy 教學**：https://scanpy-tutorials.readthedocs.io/
- **scverse 生態系**：https://scverse.org/（相關工具：squidpy、scvi-tools、cellrank）
- **最佳實務**：Luecken & Theis (2019)「Current best practices in single-cell RNA-seq」

## 有效分析的提示

1. **從範本開始**：以 `assets/analysis_template.py` 作為起點
2. **先執行 QC 腳本**：用 `scripts/qc_analysis.py` 做初步過濾
3. **視需要參考文件**：把工作流程與 API 參考載入上下文
4. **反覆調整分群**：嘗試多種解析度與視覺化方式
5. **以生物學驗證**：確認標記基因符合預期的細胞類型
6. **記錄參數**：記下 QC 門檻與分析設定
7. **儲存檢查點**：在關鍵步驟寫出中間結果
