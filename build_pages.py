import os
import glob
import pandas as pd
from datetime import datetime

# 設定資料夾路徑
HTML_FILE = 'index.html'

# 讀取配置檔，建立對照表
def get_stock_map():
    try:
        # 讀取 CSV
        df = pd.read_csv("config/stocks.csv")
        # 建立字典，例如：{'2330': '台積電', '3163': '波若威'}
        # 確保 code 是字串，避免匹配失敗
        return pd.Series(df.name.values, index=df.code.astype(str)).to_dict()
    except Exception as e:
        print(f"讀取配置檔失敗: {e}")
        return {}

def generate_html():
    """
    掃描 data/plots 下的 PNG 檔案，並生成 index.html。
    """
    PLOT_DIR = 'data/plots'
    stock_map = get_stock_map()
    # 1. 抓取所有圖片檔案 (依檔名排序，確保順序一致)
    image_files = sorted(glob.glob(os.path.join(PLOT_DIR, '*.png')))

    # 2. 準備圖片的 HTML 標籤
    image_tags = ""
    for img_path in image_files:
        # 取得股票名稱 (例如: 從 data/plots/2330_analysis.png 取得 2330)
        filename = os.path.basename(img_path)
        stock_code = filename.split('_')[0]
        # 根據代號找中文名稱，找不到就用原代號
        stock_display_name = stock_map.get(stock_code, stock_code)
        # 這裡是 GitHub Pages 的眉角：圖片路徑要用相對路徑
        # 網頁跟圖片都在 daily-results 分支下，所以路徑直接用 'data/plots/...'
        image_tags += f"""
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-header">
                    <h5 class="my-0 font-weight-normal">📈 {stock_display_name} ({stock_code})</h5>
                </div>
                <div class="card-body d-flex align-items-center">
                    <img src="{img_path}" class="img-fluid" alt="{stock_display_name}">
                </div>
            </div>
        </div>
        """

    # 3. 定義 HTML 模板 (使用極簡 Bootstrap)
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S (CST)')
    html_template = f"""
<!doctype html>
<html lang="zh-TW">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Taiwan Stock Quant Monitor</title>
    <!-- 使用 Bootstrap CDN，懶人專用美化 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <style>
      body {{ background-color: #f8f9fa; padding-top: 50px; }}
      .card img {{ max-height: 500px; object-fit: contain; }}
    </style>
  </head>
  <body>

    <div class="container">
      <div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
        <h1 class="display-4">量化監控儀表板</h1>
        <p class="lead text-muted">📊 由 GitHub Actions 每日下午 2:00 自動產出。歡迎來到 Raysin 的櫥窗！</p>
        <p class="text-secondary">最後更新時間: {update_time}</p>
        <hr>
      </div>

      <!-- 這裡改用 row，Bootstrap 會自動幫我們換行 -->
      <div class="row">
        {image_tags if image_tags else "<div class='col-12 text-center'><p class='alert alert-warning'>⚠️ 今日尚無圖表產出。</p></div>"}
      </div>

      <footer class="pt-4 my-md-5 pt-md-5 border-top">
        <div class="row">
          <div class="col-12 col-md text-center">
            <small class="d-block mb-3 text-muted">© 2026 Raysin8411 - Built with <a href="https://github.com/RaySin8411/Taiwan-Stock-Quant-Monitor">GitHub Actions</a></small>
          </div>
        </div>
      </footer>
    </div>

  </body>
</html>
"""

    # 4. 寫入檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"✅ 已成功生成 {HTML_FILE}，包含 {len(image_files)} 張圖表。")


if __name__ == '__main__':
    generate_html()