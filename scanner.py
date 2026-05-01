# scanner.py
import yfinance as yf
import pandas as pd
from src.core import TechIndicatorAnalyzer
from src.notifier import TelegramNotifier


def run_daily_scan():
    # 1. 初始化
    analyzer = TechIndicatorAnalyzer()
    notifier = TelegramNotifier()

    try:
        stocks = pd.read_csv("config/stocks.csv")
    except FileNotFoundError:
        print("❌ 找不到 config/stocks.csv")
        return

    print(f"🚀 開始掃描 {len(stocks)} 檔標的...")

    for _, row in stocks.iterrows():
        # 這裡使用你之前修正過的代碼格式
        ticker = f"{row['code']}.{row['market']}"

        # 抓取最近一個月的資料 (足夠計算 MA20 和 DMI)
        df = yf.download(ticker, period="3mo", progress=False)
        if df.empty or len(df) < 30:
            continue
        # 計算指標
        df = analyzer.calculate_dmi(df)

        # 排除空值並抓取最後兩筆進行交叉判斷
        df = df.dropna(subset=['plus_di', 'minus_di', 'adx', 'MA20'])
        if len(df) < 2:
            print(f"⚠️ {row['name']} 資料不足以計算指標，跳過...")
            continue

        curr_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        # 判斷邏輯
        gold_cross = (prev_row['plus_di'] < prev_row['minus_di']) and (curr_row['plus_di'] > curr_row['minus_di'])
        ma_ok = curr_row['Close'] > curr_row['MA20']
        adx_ok = curr_row['adx'] > 18

        if gold_cross and ma_ok and adx_ok:
            print(f"🎯 發現訊號: {row['name']} ({row['code']})")
            notifier.send_stock_alert(
                stock_name=row['name'],
                stock_code=row['code'],
                price=round(float(curr_row['Close']), 2),
                signal_type="✨ DMI 黃金交叉 (趨勢確立)"
            )
        else:
            print(f"🎯 沒發現訊號: {row['name']} ({row['code']})")
            notifier.send_stock_alert(
                stock_name=row['name'],
                stock_code=row['code'],
                price=round(float(curr_row['Close']), 2),
                signal_type="✨ 無訊號"
            )


if __name__ == "__main__":
    run_daily_scan()