import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

print("--- Danh sách Model khả dụng ---")
try:
    # Lấy danh sách models
    for model in client.models.list():
        # In trực tiếp tên model (ví dụ: models/gemini-1.5-flash)
        print(f"ID: {model.name}")
except Exception as e:
    print(f"Lỗi: {e}")