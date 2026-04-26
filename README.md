# Taiwan Stock Quant Monitor (DMI Strategy)

這是一個基於 Python 開發的自動化台股監控工具，專注於半導體與光通訊產業鏈的趨勢分析。

## 🌟 核心功能
- **批次監控**：支援同時監控上市 (.TW) 與上櫃 (.TWO) 股票。
- **指標分析**：運用 TA-Lib 計算工業級 DMI (Directional Movement Index) 與 ADX。
- **數據持久化**：自動將分析結果導出為 CSV，便於後續數據追蹤。
- **異常處理**：針對 yfinance API 變動（如 Multi-Index 問題）進行了穩健性處理。

## 🛠️ 技術棧
- **Python 3.13**
- **Pandas**: 資料處理與降維。
- **TA-Lib**: 高性能技術指標運算。
- **yfinance**: 金融數據擷取。

## 📈 為什麼選擇 DMI/ADX？
針對半導體這類具有強烈趨勢性的題材股，DMI 配合 ADX 能有效過濾震盪雜訊，捕捉強勢波段。

## 📂 專案結構 (Project Structure)

```text
Taiwan-Stock-DMI-Monitor/
├── data/               # 儲存分析產出的 CSV 結果檔案
├── logs/               # (Optional) 系統執行日誌存放處
├── src/                # 原始程式碼目錄
│   ├── __init__.py     # 使 src 成為一個 Python Package
│   └── core.py         # 核心邏輯：包含技術指標計算與策略判斷
├── main.py             # 程式進入點：負責批次執行與資料流調度
├── requirements.txt    # 專案依賴套件清單
├── .gitignore          # 排除不需進入版本控制的檔案 (如 venv, __pycache__)
└── README.md           # 專案說明文件
```