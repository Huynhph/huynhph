import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
try:
    response = client.models.generate_images(
        model='imagen-4.0-fast-generate-001',
        prompt='A simple square',
        config={'number_of_images': 1, 'aspect_ratio': '16:9'}
    )
    print(response)
except Exception as e:
    print("Error:", e)
