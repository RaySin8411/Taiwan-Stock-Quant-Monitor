# Taiwan Stock Quant Monitor (DMI Strategy)

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

這是一個專為台股（上市/上櫃）開發的量化監控工具，核心基於 **DMI (Directional Movement Index)** 與 **ADX** 技術指標，旨在捕捉半導體、光通訊等強勢族群的趨勢轉折點。

## 🌟 專案亮點 (Key Features)

- **自動化族群監控**：支援 `.TW` (上市) 與 `.TWO` (上櫃) 標的批量分析。
- **工業級技術指標**：採用 `TA-Lib` 進行高性能數學運算，確保指標精度。
- **資料分層架構**：嚴謹的目錄組織，分離原始碼 (`src/`)、分析報表 (`data/reports/`) 與視覺化圖表 (`data/plots/`)。
- **物件導向設計 (OOP)**：將計算邏輯封裝於 `TechIndicatorAnalyzer` 類別，具備高擴展性與可測試性。
- **視覺化診斷**：自動產出包含價格走勢與 DMI/ADX 三線對照的分析圖表，便於快速決策。

## 📂 專案結構 (Project Structure)

```text
Taiwan-Stock-Quant-Monitor/
├── data/               # 數據輸出目錄
│   ├── reports/        # 存放分析彙整 CSV (e.g., stock_analysis_result.csv)
│   └── plots/          # 存放分析圖表 PNG (e.g., 2330.TW_analysis.png)
├── src/                # 核心原始碼
│   ├── __init__.py
│   └── core.py         # 核心邏輯：DMI 計算、訊號判斷、繪圖引擎
├── main.py             # 程式進入點：負責調度執行流程
├── requirements.txt    # 依賴套件清單
├── .gitignore          # 版本控制排除規範
└── README.md           # 專案說明文件
```