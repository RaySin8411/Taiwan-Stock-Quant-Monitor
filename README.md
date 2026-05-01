# Taiwan Stock Quant Monitor (DMI Strategy)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/github%20actions-active-success.svg)

這是一個專為台股（上市/上櫃）開發的量化監控工具，核心基於 **DMI (Directional Movement Index)** 與 **ADX** 技術指標，旨在捕捉中小型成長股（如半導體、光通訊族群）的趨勢轉折點。

本專案包含回測引擎，經實測特定族群勝率約 **30-40%**。

## 🌟 專案亮點 (Key Features)

- **自動化族群監控**：支援 `.TW` (上市) 與 `.TWO` (上櫃) 標的批量分析。
- **工業級技術指標**：採用 `TA-Lib` 進行高性能數學運算，確保指標精度。
- **資料分層架構**：嚴謹的目錄組織，分離原始碼 (`src/`)、分析報表 (`data/reports/`) 與視覺化圖表 (`data/plots/`)。
- **物件導向設計 (OOP)**：將計算邏輯封裝於 `TechIndicatorAnalyzer` 類別，具備高擴展性與可測試性。
- **視覺化診斷**：自動產出包含價格走勢與 `DMI/ADX` 三線對照的分析圖表，便於快速決策。
- **配置化管理 (Config-Driven)**：透過 `config/stocks.csv` 輕鬆管理監控清單，實現邏輯與資料分離。
- **動態儀表板 (Live Dashboard)**：結合 `GitHub Pages` 與 `Bootstrap`，每日自動更新視覺化分析網頁。


## 🛠️ 快速上手 (Quick Start)
> 🤖 本專案由 GitHub Actions 每日下午 2:00 自動執行。
> 
> [👉 點擊此處查看動態儀表板 (Live Dashboard)](https://raysin8411.github.io/Taiwan-Stock-Quant-Monitor/)

### 1. 環境建置
建議使用虛擬環境 (venv) 以確保依賴隔離：
```bash
python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置環境變數
於根目錄建立 .env 檔案，以啟用 Telegram 通知功能：
```
TG_TOKEN=your_bot_token
TG_CHAT_ID=your_chat_id
```

### 3. 執行監控與預警

* 執行全市場掃描與網頁更新：
    ```Bash
    python main.py
    ```
* 執行即時訊號推播 (Telegram)：
    ```Bash
    python scanner.py
    ```
### 4. 執行單元測試 (Unit Testing)
確保核心指標計算邏輯準確無誤：

```Bash
# 使用 Python 內建單元測試框架
python -m unittest discover tests
```

## 📂 專案結構 (Project Structure)

```text
Taiwan-Stock-Quant-Monitor/
├── config/             # 策略配置
│   └── stocks.csv      # 追蹤標的清單 (代碼,名稱,市場)
├── data/               # 數據輸出目錄
│   ├── reports/        # 存放分析彙整 CSV (例如: stock_analysis_result.csv)
│   └── plots/          # 存放分析圖表 PNG (例如: 2330.TW_analysis.png)
├── logs/               # 系統執行日誌 (存放 app.log)
├── src/                # 核心原始碼
│   ├── __init__.py
│   ├── core.py         # 核心邏輯：指標計算、訊號判斷、繪圖引擎
│   ├── notifier.py     # Telegram 通知模組
│   └── logger_config.py # 日誌系統配置
├── tests/              # 單元測試 (指標精度驗證、訊號邏輯測試)
├── scanner.py          # 獨立監控預警腳本
├── main.py             # 程式進入點
├── build_pages.py      # 自動化網頁生成腳本
├── requirements.txt    # 專案依賴
├── LICENSE             # MIT 授權條款
└── README.md           # 專案說明文件
```

## 策略說明 (Strategy Logic)
本系統採用 DMI 動能趨勢策略：

* 黃金交叉：PDI (陽線) 上穿 MDI (陰線)。

* 趨勢確立：ADX > 18，代表趨勢強度具備攻擊動能。

* 多頭濾網：股價站穩於 MA20 (月線) 之上，確保中期趨勢偏多。

## 安全性說明
若要在 GitHub Actions 中使用 Telegram 通知，請務必於 Repository 的 Settings > Secrets and variables > Actions 設定以下環境變數：

* TG_TOKEN

* TG_CHAT_ID

*Disclaimer: 本專案僅供技術研究與學習使用，不構成任何投資建議。投資有風險，入市需謹慎。*