import talib
import pandas as pd


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