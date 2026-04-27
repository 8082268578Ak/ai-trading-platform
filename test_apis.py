import os
import requests
from dotenv import load_dotenv

def test_apis():
    load_dotenv()
    
    news_key = os.getenv("NEWS_API_KEY")
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
    
    print("--- API DIAGNOSTICS ---")
    
    # 1. Test NewsAPI
    print("\nTesting NewsAPI...")
    if not news_key:
        print("❌ NEWS_API_KEY is missing from .env")
    else:
        try:
            url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={news_key}"
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ NewsAPI is working perfectly!")
            else:
                print(f"❌ NewsAPI returned an error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception connecting to NewsAPI: {e}")
            
    # 2. Test Alpaca Paper API
    print("\nTesting Alpaca Paper API...")
    if not alpaca_api_key or not alpaca_secret_key:
        print("❌ Alpaca API keys are missing from .env")
    else:
        try:
            url = "https://paper-api.alpaca.markets/v2/account"
            headers = {
                "APCA-API-KEY-ID": alpaca_api_key,
                "APCA-API-SECRET-KEY": alpaca_secret_key
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                account = response.json()
                print("✅ Alpaca Paper API is working perfectly!")
                print(f"   Status: {account.get('status')}")
                print(f"   Currency: {account.get('currency')}")
                print(f"   Cash Balance: ${account.get('cash')}")
                print(f"   Portfolio Value: ${account.get('portfolio_value')}")
            else:
                print(f"❌ Alpaca Paper API returned an error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception connecting to Alpaca: {e}")

if __name__ == "__main__":
    test_apis()
