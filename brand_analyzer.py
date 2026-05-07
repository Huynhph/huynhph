import os
from playwright.sync_api import sync_playwright
from google import genai
from dotenv import load_dotenv
from PIL import Image

# 1. Khởi tạo môi trường
load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_brand_from_url(url):
    """Truy cập website, chụp ảnh và phân tích DNA thương hiệu."""
    if not url.startswith('http'):
        print(">>> Lỗi: URL không hợp lệ.")
        return None

    print(f">>> Đang truy cập website: {url}...")
    screenshot_path = "brand_screenshot.png"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            page.screenshot(path=screenshot_path)
            browser.close()
    except Exception as e:
        print(f">>> Lỗi khi truy cập website: {e}")
        return None

    # --- Phân tích Vision với cơ chế tự động tìm Model ---
    img = Image.open(screenshot_path)
    available_models = [m.name.replace('models/', '') for m in client.models.list()]
    
    priority_list = ['gemini-flash-lite-latest', 'gemini-2.5-flash-image', 'gemini-2.0-flash-lite']
    target_models = [m for m in priority_list if m in available_models] + available_models

    for model_name in target_models:
        try:
            print(f">>> Thử nghiệm Vision với: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    "Hãy đóng vai chuyên gia Brand Identity. Nhìn vào ảnh màn hình website này và phân tích màu sắc chủ đạo (mã Hex), phong cách thiết kế, font chữ và bố cục. Trả về bản tóm tắt ngắn gọn.",
                    img
                ]
            )
            print(f">>> THÀNH CÔNG với model {model_name}!")
            return response.text
        except Exception:
            continue

    print(">>> Rất tiếc, không tìm thấy model nào hỗ trợ phân tích hình ảnh.")
    return None

# --- KHỐI ĐIỀU KHIỂN CHÍNH (ĐÃ FIX LỖI) ---
if __name__ == "__main__":
    target_url = "https://www.hoamaidesignaward.com/"
    
    # Bước 1: Kiểm tra môi trường để tránh lỗi EOFError
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print(f">>> [Automation Mode] Sử dụng URL mặc định: {target_url}")
    else:
        # Nếu chạy trên máy Mac của Huynh, cho phép tùy chỉnh URL
        try:
            print(f"URL hiện tại: {target_url}")
            user_input = input("Nhấn Enter để dùng URL trên hoặc dán URL mới: ").strip()
            if user_input: 
                target_url = user_input
        except (EOFError, KeyboardInterrupt):
            print(f"\n>>> Đang dùng URL mặc định.")

    # Bước 2: Thực thi phân tích
    guidelines = analyze_brand_from_url(target_url)
    
    # Bước 3: Lưu kết quả
    if guidelines:
        output_file = "brand_guidelines.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(guidelines)
        print(f">>> THÀNH CÔNG: Đã tạo file {output_file}")