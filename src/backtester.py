import pandas as pd

class DMIBacktester:
    def __init__(self, cash=100000, fee_rate=0.001425, tax_rate=0.003):
        self.initial_cash = cash
        self.fee_rate = fee_rate  # 台灣手續費
        self.tax_rate = tax_rate  # 台灣證交稅
        self.trades = []  # 紀錄交易紀錄

    def run(self, df, symbol):
        """
        執行回測邏輯
        """
        holding = False
        buy_price = 0

        # 逐日掃描 (從第 1 天到最後一天)
        for i in range(1, len(df)):
            current_date = df.index[i]
            prev_row = df.iloc[i - 1]
            curr_row = df.iloc[i]

            # 買入條件
            # 1. 核心訊號: DMI 黃金交叉
            gold_cross = (prev_row['plus_di'] < prev_row['minus_di']) and (curr_row['plus_di'] > curr_row['minus_di'])
            # 2. ADX 條件:「只要趨勢開始抬頭」或「ADX 在基本強度 18 以上」
            adx_strong = (curr_row['adx'] > 18) or (curr_row['adx'] >= prev_row['adx'] * 0.95)
            # 3. 成交量條件：「只要今天量比昨天大」，代表動能增加即可。
            vol_breakout = curr_row['Volume'] > prev_row['Volume']

            ma_filter = curr_row['Close'] > curr_row['MA20']

            if not holding:
                if gold_cross and adx_strong and vol_breakout and ma_filter:

                    buy_price = curr_row['Close']
                    holding = True
                    self.trades.append({
                        'symbol': symbol,
                        'entry_date': current_date,
                        'entry_price': buy_price,
                        'action': 'BUY'
                    })

            # --- 賣出條件：DMI 死亡交叉 或 停損 ---
            elif holding:
                # 簡單邏輯：PDI 跌破 MDI 就出場
                if curr_row['plus_di'] < curr_row['minus_di']:
                    sell_price = curr_row['Close']
                    profit = (sell_price - buy_price) / buy_price
                    # 扣除手續費與稅 (買進賣出各一次手續費 + 賣出稅)
                    net_profit = profit - (self.fee_rate * 2 + self.tax_rate)

                    self.trades[-1].update({
                        'exit_date': current_date,
                        'exit_price': sell_price,
                        'return': net_profit
                    })
                    holding = False
                    buy_price = 0

        return pd.DataFrame([t for t in self.trades if 'exit_price' in t])

    def get_stats(self, results_df):
        """
        統計回測績效
        """
        if results_df.empty:
            return "無交易紀錄"

        win_rate = (results_df['return'] > 0).sum() / len(results_df)
        avg_ret = results_df['return'].mean()
        total_ret = (1 + results_df['return']).prod() - 1

        return {
            "交易次數": len(results_df),
            "勝率": f"{win_rate:.2%}",
            "平均報酬": f"{avg_ret:.2%}",
            "累積總報酬": f"{total_ret:.2%}"
        }