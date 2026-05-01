import os
import requests
import pandas as pd
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()


class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TG_TOKEN")
        self.chat_id = os.getenv("TG_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_stock_alert(self, stock_name, stock_code, price, signal_type):
        """
        發送推播通知
        """
        message = (
            f"🚀 *DMI 策略訊號觸發*\n"
            f"----------------------------\n"
            f"📈 *標的*：{stock_name} ({stock_code})\n"
            f"💰 *現價*：`{price}`\n"
            f"🔔 *訊號*：{signal_type}\n"
            f"----------------------------\n"
            f"🕒 _監控時間：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}_"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(self.api_url, data=payload)
            if response.status_code == 200:
                print(f"✅ {stock_name} 通知發送成功")
            else:
                print(f"❌ 發送失敗，狀態碼：{response.status_code}")
        except Exception as e:
            print(f"⚠️ 發送異常：{e}")


# 測試用 (直接執行此檔案時)
if __name__ == "__main__":
    notifier = TelegramNotifier()
    notifier.send_stock_alert("測試股票", "0000", 100.5, "黃金交叉 (MA20之上)")