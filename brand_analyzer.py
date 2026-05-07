import os
from playwright.sync_api import sync_playwright
from google import genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_brand(url):
    """Analyze website visual DNA via Vision AI."""
    print(f">>> Accessing: {url}...")
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
        print(f">>> BROWSER ERROR: {e}")
        return None

    img = Image.open(screenshot_path)
    # Model fallback logic for 403 or availability issues
    priority_models = ['gemini-flash-lite-latest', 'gemini-2.5-flash-image', 'gemini-2.0-flash-lite']
    
    for model_name in priority_models:
        try:
            print(f">>> Testing Vision with: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=["Analyze primary colors (Hex), design style, fonts, and layout. Return a concise summary.", img]
            )
            print(f">>> SUCCESS: Analysis complete using {model_name}.")
            return response.text
        except Exception:
            continue
    return None

if __name__ == "__main__":
    target_url = "https://www.hoamaidesignaward.com/"
    
    # Bypass input for GitHub Actions environment
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print(f">>> [Automation Mode] Target: {target_url}")
    else:
        try:
            user_input = input(f"Default URL: {target_url} (Press Enter to use or paste new): ").strip()
            if user_input: target_url = user_input
        except (EOFError, KeyboardInterrupt):
            pass

    results = analyze_brand(target_url)
    if results:
        with open("brand_guidelines.txt", "w", encoding="utf-8") as f:
            f.write(results)
        print(">>> SUCCESS: brand_guidelines.txt generated.")