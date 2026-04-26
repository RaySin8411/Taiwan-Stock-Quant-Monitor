import os
import talib
import pandas as pd
import matplotlib.pyplot as plt


class TechIndicatorAnalyzer:
    """專業技術指標分析類別"""

    def __init__(self, timeperiod=14):
        self.timeperiod = timeperiod

    def calculate_dmi(self, df):
        """
        傳入 DataFrame，回傳計算完 DMI/ADX 的結果
        處理 yfinance 升級後的 Multi-Index 結構
        """
        # 1. 數據降維處理 (Handling Multi-Index)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 2. 確保資料為 float64 以利 TA-Lib 計算
        high = df['High'].values.astype(float).flatten()
        low = df['Low'].values.astype(float).flatten()
        close = df['Close'].values.astype(float).flatten()

        # 3. 呼叫 TA-Lib
        df['plus_di'] = talib.PLUS_DI(high, low, close, timeperiod=self.timeperiod)
        df['minus_di'] = talib.MINUS_DI(high, low, close, timeperiod=self.timeperiod)
        df['adx'] = talib.ADX(high, low, close, timeperiod=self.timeperiod)

        return df

    def get_signal(self, df):
        """判斷交叉訊號邏輯"""
        if len(df) < 2:
            return "DATA_INSUFFICIENT"

        target = df.tail(2)
        prev = target.iloc[0]
        curr = target.iloc[1]

        # 封裝為標量
        p_di_now, m_di_now = curr['plus_di'].item(), curr['minus_di'].item()
        p_di_prev, m_di_prev = prev['plus_di'].item(), prev['minus_di'].item()

        if p_di_prev < m_di_prev and p_di_now > m_di_now:
            return "GOLDEN_CROSS"
        elif p_di_prev > m_di_prev and p_di_now < m_di_now:
            return "DEATH_CROSS"
        return "WAIT"

    def plot_dmi(self, df, symbol, save_dir="data/plots"):
        """
        產出 DMI 與價格對照圖並儲存至 data/
        """
        # 建立一個包含兩個子圖的視圖 (15x10 比例)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True,
                                       gridspec_kw={'height_ratios': [3, 2]})

        # --- 子圖 1: 價格走勢 ---
        ax1.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.6)
        ax1.set_title(f"Stock Analysis: {symbol}", fontsize=16)
        ax1.set_ylabel("Price")
        ax1.legend(loc='upper left')
        ax1.grid(True, which='both', linestyle='--', alpha=0.5)

        # --- 子圖 2: DMI 指標 ---
        ax2.plot(df.index, df['plus_di'], label='+DI (Bullish)', color='red', linewidth=1.5)
        ax2.plot(df.index, df['minus_di'], label='-DI (Bearish)', color='green', linewidth=1.5)
        ax2.plot(df.index, df['adx'], label='ADX (Strength)', color='orange', linestyle='--', linewidth=2)

        # 加上 ADX=25 的基準線
        ax2.axhline(y=25, color='black', linestyle=':', alpha=0.7, label='Trend Threshold (25)')

        ax2.set_ylabel("DMI / ADX Value")
        ax2.set_xlabel("Date")
        ax2.legend(loc='upper left')
        ax2.grid(True, which='both', linestyle='--', alpha=0.5)

        # 自動調整佈局
        plt.tight_layout()

        # 儲存圖片 (存到 data/plots 之下)
        plot_path = os.path.join(save_dir, f"{symbol}_analysis.png")
        plt.savefig(plot_path)
        print(f"📈 圖表已生成: {plot_path}")

        # 如果是在 IDE (PyCharm) 執行，可以加上這行彈出視窗
        # plt.show()
        plt.close()  # 關閉畫布釋放記憶體