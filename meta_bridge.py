import os
import pandas as pd
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

load_dotenv()

def fetch_ads_data():
    access_token = os.getenv('META_ACCESS_TOKEN')
    ad_account_id = os.getenv('META_AD_ACCOUNT_ID')

    if not access_token or not ad_account_id:
        print(">>> ERROR: Missing credentials in .env")
        return

    FacebookAdsApi.init(access_token=access_token)
    account = AdAccount(ad_account_id)
    
    print(">>> Starting high-speed text-only from Meta...")
    try:
        # STEP 1: Bulk Fetch all Creatives (Text/Headlines only)
        # This prevents the long-time response by avoiding per-ad calls
        print(">>> Downloading Creative library...")
        creatives = account.get_ad_creatives(fields=['body', 'title'], params={'limit': 150})
        creative_map = {cr['id']: {'Text': cr.get('body', 'N/A'), 'Headline': cr.get('title', 'N/A')} for cr in creatives}

        # STEP 2: Bulk Fetch all Ad Performance (Last 7 Days)
        print(">>> Downloading Performance data...")
        perf_fields = ['ad_id', 'ad_name', 'spend', 'ctr', 'cpc']
        perf_params = {'level': 'ad', 'date_preset': 'last_7d', 'limit': 150}
        insights = account.get_insights(fields=perf_fields, params=perf_params)
        
        # STEP 3: Map Content to Performance locally
        # We fetch Ad objects specifically to link Creative IDs to Ad IDs
        ads = account.get_ads(fields=['id', 'creative'], params={'limit': 150})
        ad_to_creative = {ad['id']: ad.get('creative', {}).get('id') for ad in ads}

        final_records = []
        for insight in insights:
            ad_id = insight.get('ad_id')
            creative_id = ad_to_creative.get(ad_id)
            content = creative_map.get(creative_id, {'Text': 'N/A', 'Headline': 'N/A'})

            final_records.append({
                'Ad Name': insight.get('ad_name'),
                'Primary Text': content['Text'],
                'Headline': content['Headline'],
                'Spend': insight.get('spend', 0),
                'CTR': insight.get('ctr', 0),
                'CPC': insight.get('cpc', 0)
            })

        if not final_records:
            print(">>> WARNING: No data found.")
            return

        # Export to CSV for the Optimizer
        df = pd.DataFrame(final_records)
        df.to_csv('ads_performance.csv', index=False)
        print(f">>> SUCCESS: Synchronized {len(df)} ads. Performance ready.")
        
    except Exception as e:
        print(f">>> META API ERROR: {e}")

if __name__ == "__main__":
    fetch_ads_data()