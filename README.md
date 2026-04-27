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

## 🛠️ 快速上手 (Quick Start)

### 1. 環境建置
建議使用虛擬環境 (venv) 以確保依賴隔離：
```bash
python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate
pip install -r requirements.txt
```
### 2. 執行監控
啟動主程式進行批次掃描與分析：

```Bash
python main.py
```
### 3. 執行單元測試 (Unit Testing)
確保核心指標計算邏輯準確無誤：

```Bash
# 使用 Python 內建單元測試框架
python -m unittest discover tests
```

## 📂 專案結構 (Project Structure)

```text
Taiwan-Stock-Quant-Monitor/
├── data/               # 數據輸出目錄
│   ├── reports/        # 存放分析彙整 CSV (例如: stock_analysis_result.csv)
│   └── plots/          # 存放分析圖表 PNG (例如: 2330.TW_analysis.png)
├── logs/               # 系統執行日誌 (存放 app.log)
├── src/                # 核心原始碼
│   ├── __init__.py
│   ├── core.py         # 核心邏輯：指標計算、訊號判斷、繪圖引擎
│   └── logger_config.py # 日誌系統配置
├── tests/              # 單元測試 (指標精度驗證、訊號邏輯測試)
├── main.py             # 程式進入點
├── requirements.txt    # 專案依賴
├── LICENSE             # MIT 授權條款
└── README.md           # 專案說明文件
```