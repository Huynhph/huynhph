import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_video_ads():
    if not os.path.exists('action_plan.md'):
        print(">>> Lỗi: Không tìm thấy action_plan.md.")
        return

    with open('action_plan.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    video_prompt = None
    capture_next = False
    
    # Cơ chế tìm kiếm thông minh: Duyệt từng dòng
    for line in lines:
        clean_line = line.strip()
        
        if capture_next and clean_line.startswith('>'):
            video_prompt = clean_line.lstrip('>').strip().replace('**', '').replace('"', '')
            break
            
        # Tìm dòng chứa "video" và "prompt", không phân biệt hoa thường, chấp nhận dấu :, - hoặc **
        if re.search(r'(?i)video.*prompt', clean_line):
            # Bóc tách phần nội dung sau dấu : hoặc -
            parts = re.split(r'[:\-]', clean_line, maxsplit=1)
            if len(parts) > 1 and len(parts[1].strip()) > 0:
                video_prompt = parts[1].strip().replace('**', '').replace('"', '')
                break
            else:
                capture_next = True

    if not video_prompt:
        print(">>> KHÔNG TÌM THẤY VIDEO PROMPT. Đang kiểm tra nội dung file của Huynh...")
        print("-" * 30)
        # In 5 dòng cuối để debug
        print("Dưới đây là 5 dòng cuối trong action_plan.md của bạn:")
        print("".join(lines[-5:]))
        print("-" * 30)
        print(">>> Mẹo: Hãy mở action_plan.md và đảm bảo có dòng: Video Prompt: [Mô tả tiếng Anh]")
        return

    print(f">>> Đã bóc tách thành công Prompt: {video_prompt[:80]}...")

    try:
        print(">>> Đang kích hoạt Veo sản xuất video (Vui lòng đợi)...")
        operation = client.models.generate_videos(
            model='veo-2.0-generate-001',
            prompt=video_prompt
        )
        
        video_result = operation.result()
        video_path = "video_ads_output.mp4"
        video_result.generated_videos[0].video.save(video_path)
        print(f"\n>>> THÀNH CÔNG! Video lưu tại: {os.path.abspath(video_path)}")

    except Exception as e:
        print(f">>> Lỗi khi render video: {e}")

if __name__ == "__main__":
    generate_video_ads()