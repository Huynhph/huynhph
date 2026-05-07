class VideoAdsKnowledge:
    """
    Bộ quy tắc cốt lõi để tạo Video Ads Prompt hiệu suất cao.
    Dùng để nạp vào Prompt System.
    """
    
    STRUCTURE = {
        "HOOK_0_5S": "Must reveal the primary USP or core benefit immediately. Use fast motion or bold text overlays to stop the scroll.",
        "EXPERIENCE_5_12S": "Build immersion with professional camera movements (tracking shots, smooth easing) and cinematic lighting.",
        "CTA_FINAL": "The last 2-3 seconds must display the Brand Logo and a clear Call To Action (e.g., Register Now, Shop Now)."
    }

    CAMERA_VOCABULARY = [
        "Cinematic tracking shot", "Smooth drone sweep", "Dynamic zoom-in", 
        "Slow-motion reveal", "Macro close-up", "Parallax effect"
    ]

    VISUAL_QUALITY_TOKENS = [
        "Photorealistic", "4K resolution", "High-contrast lighting", 
        "Professional studio finish", "Motion blur for realism", "Sharp focus"
    ]

    @classmethod
    def get_knowledge_prompt(cls):
        return f"""
        [VIDEO ADS EXPERT SKILLS]
        - Frame Structure: {cls.STRUCTURE}
        - Professional Camera Vocabulary: {', '.join(cls.CAMERA_VOCABULARY)}
        - Quality Standards: {', '.join(cls.VISUAL_QUALITY_TOKENS)}
        - Timing: 10-15 seconds total.
        """