import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
# Thêm dòng này để lấy các giá trị chuẩn của Meta
from facebook_business.adobjects.adsinsights import AdsInsights 
import pandas as pd

load_dotenv()

def fetch_ads_data():
    FacebookAdsApi.init(access_token=os.getenv('META_ACCESS_TOKEN'))
    account = AdAccount(os.getenv('META_AD_ACCOUNT_ID'))
    
    fields = [
        'ad_name', 
        'spend', 
        'cpc', 
        'ctr', 
        'impressions', 
        'clicks'
    ]
    
    # SỬA TẠI ĐÂY: Sử dụng 'last_7d' thay vì 'last_7_days'
    params = {
        'date_preset': 'last_7d', 
        'level': 'ad'
    }
    
    print(">>> Đang kết nối và lấy dữ liệu thực tế từ Meta...")
    try:
        insights = account.get_insights(fields=fields, params=params)
        data = [dict(item) for item in insights]
        
        if not data:
            print(">>> Cảnh báo: Không tìm thấy dữ liệu. Kiểm tra xem tài khoản có đang chạy Ads không.")
            return

        df = pd.DataFrame(data)
        df.to_csv('ads_performance.csv', index=False)
        print(f">>> Thành công! Đã lưu {len(df)} mẫu vào ads_performance.csv")
        
    except Exception as e:
        print(f">>> Lỗi khi gọi API: {e}")

if __name__ == "__main__":
    fetch_ads_data()