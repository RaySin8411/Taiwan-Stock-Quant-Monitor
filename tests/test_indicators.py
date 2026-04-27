import unittest
import pandas as pd
import numpy as np
from src.core import TechIndicatorAnalyzer


class TestDMIIndicators(unittest.TestCase):
    def setUp(self):
        """測試前的初始化"""
        self.analyzer = TechIndicatorAnalyzer()

        # 建立一組模擬數據：股價從下跌轉為上漲（製造黃金交叉）
        data = {
            'High': [110, 108, 105, 107, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160],
            'Low': [100, 98, 95, 96, 98, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150],
            'Close': [105, 102, 98, 103, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155]
        }
        self.df = pd.DataFrame(data)

    def test_dmi_calculation(self):
        """測試 DMI 是否成功算出數值"""
        df_result = self.analyzer.calculate_dmi(self.df.copy())

        # 檢查是否產生了對應的欄位
        self.assertIn('plus_di', df_result.columns)
        self.assertIn('minus_di', df_result.columns)
        self.assertIn('adx', df_result.columns)

        # 確保最後一個數值不是 NaN (因為 DMI 需要足夠樣本)
        self.assertFalse(np.isnan(df_result['plus_di'].iloc[-1]))

    def test_signal_logic(self):
        """測試訊號判斷邏輯"""
        # 建立一個已知是多頭排列的最後兩筆數據
        mock_data = pd.DataFrame({
            'plus_di': [20.0, 30.0],
            'minus_di': [25.0, 15.0]
        })

        signal = self.analyzer.get_signal(mock_data)
        self.assertEqual(signal, "GOLDEN_CROSS")


if __name__ == '__main__':
    unittest.main()