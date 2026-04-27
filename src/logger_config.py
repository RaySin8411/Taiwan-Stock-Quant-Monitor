import logging
import os

def setup_logger():
    """設定全局日誌配置"""
    # 1. 確保 logs 資料夾存在
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. 建立 logger 實例
    logger = logging.getLogger("StockMonitor")
    logger.setLevel(logging.DEBUG)  # 設定最低紀錄等級

    # 避免重複添加 Handler (防止重複印出日誌)
    if not logger.handlers:
        # 3. 建立格式器 (顯示時間、等級、訊息)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 4. 建立 FileHandler (寫入檔案)
        file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"), encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # 5. 建立 StreamHandler (印到控制台)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # 6. 加入 Handler
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# 實例化以便全域使用
logger = setup_logger()