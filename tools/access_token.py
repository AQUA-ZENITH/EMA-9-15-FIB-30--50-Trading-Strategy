from kiteconnect import KiteConnect

# 1. Enter your details here
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# 2. Initialize Kite
kite = KiteConnect(api_key=API_KEY)

# 3. Ask user for the Request Token (from the browser URL)
request_token = input("Paste your Request Token here: ").strip()

try:
    # 4. Generate Session (Exchange Request Token for Access Token)
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    
    access_token = data["access_token"]
    
    print("\n✅ SUCCESS! Here is your Access Token:")
    print("---------------------------------------------------")
    print(access_token)
    print("---------------------------------------------------")
    print("👉 Copy this and paste it into your main bot script.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
