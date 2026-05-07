import os
import sys
import time
import pandas as pd
from google import genai
from dotenv import load_dotenv

# --- CUSTOM SKILL LIBRARIES ---
from marketing_skills_expert import MarketingSkills
from video_ads_expert import VideoAdsKnowledge

load_dotenv()

def run_optimization():
    # 1. VS Code & Git Validation: Fail fast if dependencies are missing
    if not os.path.exists('ads_performance.csv'):
        print(">>> ERROR: ads_performance.csv not found. Run meta_bridge.py first.")
        sys.exit(1)

    # Load performance data
    try:
        df = pd.read_csv('ads_performance.csv')
        csv_context = df.to_string()
    except Exception as e:
        print(f">>> ERROR: Failed to read ads_performance.csv. {e}")
        sys.exit(1)

    # Load Brand DNA
    brand_style = "Minimalist SaaS aesthetic, professional, sans-serif."
    if os.path.exists('brand_guidelines.txt'):
        with open('brand_guidelines.txt', 'r', encoding='utf-8') as f:
            brand_style = f.read()

    # Load Skills
    master_marketing_skills = MarketingSkills.get_all_skills()
    video_expert_knowledge = VideoAdsKnowledge.get_knowledge_prompt()

    # Validate API Key for GitHub Actions environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print(">>> ERROR: GEMINI_API_KEY is missing from environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    print(">>> System: Generating direct, No-BS action plan...")

    # Define the strict output prompt
    prompt_content = f"""
    ROLE: Performance Marketing Director.
    PROJECT: Hoa Mai Design Award 2026.
    
    DATA: {csv_context}
    BRAND DNA: {brand_style}
    SKILLS: {master_marketing_skills} | {video_expert_knowledge}
    
    STRICT WRITING RULES:
    - ZERO "AI-style" vocabulary. Do not use words like: elevate, delve, unlock, seamless, tapestry, foster, ignite.
    - Use simple, direct, high-authority English.
    - Prompts for image/video tools MUST be simple, comma-separated tags or direct commands. No conversational text.
    
    OUTPUT FORMAT (action_plan.md):
    1. TL;DR SUMMARY: 2-3 bullet points on campaign health.
    2. ADS KILL LIST: Table of bad ads (low CTR / high CPC).
    3. WINNER INSIGHTS: Table comparing Winner vs Average. 1 short sentence explaining the winning hook.
    4. NEW CONTENT (3 Variations): 
       - Headline: < 40 chars. Direct benefit.
       - Primary Text: Hook line -> 2 short bullets -> Direct CTA.
    5. BANNER PROMPT (For Nano Banana / Midjourney / Canva): 
       - Write a literal prompt string. Clean, comma-separated keywords (e.g., "minimalist interior, white background, soft lighting, 8k"). 
    6. CANVA VIDEO PROMPT:
       - Direct text-to-video instructions for Magic Media.
       - BULK CREATE TABLE: Headline | Subheadline | CTA (5 rows formatted as a markdown table).
    """

    # Model Fallback Configuration
    models = ['gemini-2.5-flash', 'gemini-2.5-flash-lite']
    max_retries = 3

    # Retry Loop
    for model_name in models:
        for attempt in range(max_retries):
            try:
                print(f">>> System: Requesting analysis from {model_name} (Attempt {attempt + 1}/{max_retries})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_content
                )
                
                with open('action_plan.md', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f">>> SUCCESS: action_plan.md generated using {model_name}.")
                return # Exit function completely on success

            except Exception as e:
                error_msg = str(e)
                if '503' in error_msg or '429' in error_msg:
                    print(f"--- WARNING: API overloaded or rate limit hit. Waiting 10 seconds before retry...")
                    time.sleep(10)
                else:
                    print(f"--- ERROR: {error_msg}")
                    break # Stop retrying this model if it's a hard error (e.g., Auth error)
        
        print(f">>> System: {model_name} failed. Switching to fallback model...")

    # If the loop finishes without returning, all models failed.
    print(">>> CRITICAL ERROR: All models and retries failed.")
    sys.exit(1)

if __name__ == "__main__":
    if os.path.exists('brand_guidelines.txt'):
        run_optimization()
    else:
        print(">>> ERROR: brand_guidelines.txt missing. Run brand_analyzer.py first.")
        sys.exit(1)