import os
import yfinance as yf
import pandas as pd
from src.core import TechIndicatorAnalyzer
from datetime import datetime


def main():
    stock_list = ["6451.TW", "2330.TW", "2454.TW", "3163.TWO"]
    analyzer = TechIndicatorAnalyzer()
    all_results = []

    print(f"--- 啟動台股量化監控系統 ({datetime.now().strftime('%Y-%m-%d')}) ---")

    for symbol in stock_list:
        try:
            # 擷取數據
            df = yf.download(symbol, period="90d", interval="1d", progress=False, auto_adjust=True)
            if df.empty: continue

            # 計算指標
            df = analyzer.calculate_dmi(df)

            analyzer.plot_dmi(df, symbol)

            signal = analyzer.get_signal(df)

            # 收集關鍵數據
            curr = df.iloc[-1]
            all_results.append({
                "Symbol": symbol,
                "Plus_DI": round(curr['plus_di'].item(), 2),
                "Minus_DI": round(curr['minus_di'].item(), 2),
                "ADX": round(curr['adx'].item(), 2),
                "Signal": signal
            })
            print(f"Checked {symbol}: {signal}")

        except Exception as e:
            print(f"Error checking {symbol}: {e}")

    # 確保 data 資料夾存在
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

     # 定義路徑
    report_dir = os.path.join(output_dir , "reports")
    plot_dir = os.path.join(output_dir , "plots")

    # 確保子資料夾存在 (exist_ok=True 可以簡化寫法)
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    # 存檔與顯示 (指定路徑到 data/reports 下)
    file_path = os.path.join(report_dir, "stock_analysis_result.csv")
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(file_path, index=False)

    print(f"\n✅ 分析結果已存至: {file_path}")

    print("\n--- 分析摘要 ---")
    print(results_df)
    print(f"\n產業平均趨勢強度 (ADX Avg): {results_df['ADX'].mean():.2f}")


if __name__ == "__main__":
    main()