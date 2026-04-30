import yfinance as yf
import pandas as pd
from src.core import TechIndicatorAnalyzer
from src.backtester import DMIBacktester


def main():
    # 1. 讀取你之前建好的 config
    stocks = pd.read_csv("config/stocks.csv")
    analyzer = TechIndicatorAnalyzer()
    backtester = DMIBacktester()

    all_summary = []

    for _, row in stocks.iterrows():
        code = str(row['code'])
        market = row['market']
        name = row['name']
        ticker = f"{code}.{market}"

        print(f"🔍 正在回測: {name} ({ticker})...")

        # 抓取兩年資料進行長期驗證
        df = yf.download(ticker, period="2y", progress=False)
        if df.empty: continue

        # 計算指標
        df = analyzer.calculate_dmi(df)

        # 執行回測
        results = backtester.run(df, ticker)
        stats = backtester.get_stats(results)

        if isinstance(stats, dict):
            stats['name'] = name
            all_summary.append(stats)

    # 顯示最終彙整報表
    summary_df = pd.DataFrame(all_summary)
    print("\n" + "=" * 50)
    print("📊 多股回測彙整報告")
    print("=" * 50)
    print(summary_df[['name', '勝率', '平均報酬', '交易次數']])


if __name__ == "__main__":
    main()