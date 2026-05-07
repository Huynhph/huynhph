class MarketingSkills:
    @staticmethod
    def get_headline_skills():
        return """
        [SKILL: AUTHORITY HEADLINE GENERATION]
        - Tone: High-authority, results-driven, No-BS.
        - Structure: Focus on the "End-Result" or "Core Benefit" in under 40 characters.
        - Constraint: No clickbait, no flowery adjectives, no 'AI-style' excitement.
        - Examples: "Scale B2B Acquisition," "Design for the AI Era," "Premium Link Building."
        """

    @staticmethod
    def get_primary_text_skills():
        return """
        [SKILL: CONVERSION PRIMARY TEXT]
        - Structure: Hook (1st line) -> Benefit Bullets (Clean) -> Direct CTA.
        - Hook: Address a technical or budget friction point immediately.
        - Body: Use minimalist bullet points to list 2-3 mechanical benefits.
        - CTA: Use authoritative commands (e.g., "Apply for the Award," "Get the Audit").
        - Constraint: Zero emojis, no fluff, professional sans-serif mindset.
        """

    @staticmethod
    def get_banner_skills():
        return """
        [SKILL: MINIMALIST BANNER PROMPTING]
        - Style: Modern SaaS dashboard aesthetic or Clean Architectural photography.
        - Composition: High negative space (left or right) for text overlay.
        - Typography: Suggest professional sans-serif fonts in the layout description.
        - Technicals: Natural lighting, neutral tones (Grey/White/Wood), 8k resolution.
        - Constraint: No glossy filters, no cluttered backgrounds.
        """

    @staticmethod
    def get_video_skills():
        return """
        [SKILL: CANVA/VEO VIDEO PROMPTING]
        - Hook: 0-5s must show the USP or core design element in motion.
        - Motion: Smooth, cinematic transitions; no-BS fast cuts.
        - Audio Cues: Calm, professional background atmosphere.
        - Final Frame: Brand logo centered with a persistent CTA.
        """

    @classmethod
    def get_all_skills(cls):
        return f"{cls.get_headline_skills()}\n{cls.get_primary_text_skills()}\n{cls.get_banner_skills()}\n{cls.get_video_skills()}"