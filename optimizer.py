import os
from google import genai
import pandas as pd
from dotenv import load_dotenv

# --- IMPORT MODULE KIẾN THỨC MỚI ---
from video_ads_expert import VideoAdsKnowledge

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def run_optimization():
    # 1. Kiểm tra file dữ liệu quảng cáo
    if not os.path.exists('ads_performance.csv'):
        print("Lỗi: Chưa có file ads_performance.csv. Hãy chạy meta_bridge.py trước.")
        return

    df = pd.read_csv('ads_performance.csv')
    csv_context = df.to_string()

    # 2. Đọc Brand Guidelines
    if os.path.exists('brand_guidelines.txt'):
        with open('brand_guidelines.txt', 'r', encoding='utf-8') as f:
            brand_style = f.read()
    else:
        brand_style = "Style hiện đại, chuyên nghiệp, tập trung vào kết quả thực tế."

    # Lấy bộ quy tắc từ chuyên gia video
    video_skills = VideoAdsKnowledge.get_knowledge_prompt()

    # 3. Tìm model khả dụng
    target_models = []
    try:
        available_models = [m.name for m in client.models.list()]
        target_models = [name for name in available_models if 'flash' in name.lower()]
    except Exception as e:
        print(f"Warning: Không thể lấy danh sách model ({e})")
        
    # Thêm model fallback
    if not target_models:
        target_models.append('models/gemini-2.5-flash')
    target_models.append('models/gemini-2.5-flash-lite') 

    print(f">>> Đang sử dụng dữ liệu từ: ads_performance.csv và brand_guidelines.txt")

    for model_id in target_models:
        model_name = model_id.replace('models/', '')
        try:
            print(f">>> Thử nghiệm với bộ não: {model_name}...")
            
            response = client.models.generate_content(
                model=model_name,
                contents=f"""
                Bạn là Performance Marketing Leader. Hãy sử dụng bộ kỹ năng chuyên gia dưới đây:
                
                {video_skills}

                Nhiệm vụ: Phân tích dữ liệu {csv_context} và Brand Style {brand_style}.

                YÊU CẦU ĐẦU RA (File action_plan.md):
                1. ADS KILL LIST
                2. WINNER INSIGHTS
                3. HEADLINES (Authority Tone)
                4. BANNER ADS STRATEGY (Conversion layout)
                5. VIDEO ADS PROMPT (10-15s):
                   - Phải áp dụng đúng [VIDEO ADS EXPERT SKILLS].
                   - 5 giây đầu phải tập trung vào USP bóc tách từ Winner Insights.
                   - Final Frame phải có CTA.
                   - Prompt viết bằng tiếng Anh chuẩn cho model Veo.
                """
            )
            
            # Lưu kế hoạch hành động
            with open('action_plan.md', 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f">>> THÀNH CÔNG với model {model_name}! Đã xuất kế hoạch tại action_plan.md")
            return 

        except Exception as e:
            print(f"--- Model {model_name} chưa sẵn sàng ({e}). Đang thử model tiếp theo...")
            continue

    print(">>> Lỗi: Không có model nào phản hồi.")

if __name__ == "__main__":
    # Không gọi analyze_brand_from_url() ở đây vì script trước đã làm rồi.
    # Chỉ cần kiểm tra file đã tồn tại chưa và chạy tối ưu.
    if os.path.exists('brand_guidelines.txt'):
        print(">>> Đã tìm thấy Brand Guidelines. Bắt đầu tối ưu hóa...")
        run_optimization()
    else:
        print(">>> Lỗi: Không tìm thấy brand_guidelines.txt. Chạy brand_analyzer.py trước.")