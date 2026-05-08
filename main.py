import os
import yfinance as yf
import pandas as pd
from src.core import TechIndicatorAnalyzer
from src.logger_config import logger


def main():
    # 讀取配置
    stocks_df = pd.read_csv("config/stocks.csv")
    stock_list = []
    for index, row in stocks_df.iterrows():
        code = str(row['code'])
        name = row['name']
        market = row['market']  # 這是 TW 或 TWO

        # 組合 yfinance 要的代號
        full_code = f"{code}.{market}"
        stock_list.append([full_code,name])

    analyzer = TechIndicatorAnalyzer()
    all_results = []

    logger.info("台股量化監控系統啟動...")

    for symbol in stock_list:
        try:
            # 擷取數據
            df = yf.download(symbol[0], period="90d", interval="1d", progress=False, auto_adjust=True)
            if df.empty:
                logger.warning(f"標的 {symbol[0]} 抓取不到資料，跳過。")
                continue

            # 計算指標
            df = analyzer.calculate_dmi(df)
            analyzer.plot_dmi(df, symbol[0])
            analyzer.generate_diagnostic_plot(df, symbol)

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
            logger.info(f"分析完成: {symbol} | 訊號: {signal}")

        except Exception as e:
            logger.error(f"分析 {symbol} 時發生異常: {str(e)}", exc_info=True)

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

    logger.info(f"全數分析完畢，結果已存至 reports 資料夾。")

    print("\n--- 分析摘要 ---")
    print(results_df)
    print(f"\n產業平均趨勢強度 (ADX Avg): {results_df['ADX'].mean():.2f}")


if __name__ == "__main__":
    main()