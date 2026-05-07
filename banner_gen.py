import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_banner_from_plan():
    # 1. Đọc nội dung từ action_plan.md
    if not os.path.exists('action_plan.md'):
        print("Lỗi: Không tìm thấy file action_plan.md.")
        return

    with open('action_plan.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Dùng Regex để lấy nội dung sau mục ### 4
    # Tìm đoạn văn bản nằm giữa "### 4." và hết file (hoặc mục tiếp theo)
    match = re.search(r'### 4\..*?\n(.*)', content, re.DOTALL)
    if not match:
        print("Lỗi: Không tìm thấy mục ### 4 trong action_plan.md")
        return

    image_prompt = match.group(1).strip()
    print(f">>> Đang gửi yêu cầu tạo ảnh với Prompt: {image_prompt[:100]}...")

    # 3. Gọi Agent Imagen 4.0 để tạo ảnh (Dựa trên danh sách model của Huynh)
    try:
        response = client.models.generate_images(
            model='imagen-4.0-fast-generate-001',
            prompt=f"Professional marketing banner, high quality, 4k, for: {image_prompt}",
            config={'number_of_images': 1, 'aspect_ratio': '16:9'}
        )

        # 4. Lưu ảnh về máy
        for i, image in enumerate(response.generated_images):
            image_path = f'generated_banner_{i}.png'
            image.image.save(image_path)
            print(f">>> THÀNH CÔNG! Đã lưu banner tại: {image_path}")

    except Exception as e:
        print(f">>> Lỗi khi generate ảnh: {e}")

if __name__ == "__main__":
    generate_banner_from_plan()