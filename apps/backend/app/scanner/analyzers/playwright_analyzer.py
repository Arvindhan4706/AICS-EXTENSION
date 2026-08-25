class PlaywrightAnalyzer:
    async def analyze(self, url: str) -> dict:
        return {
            "screenshot": None,
            "dom_complexity": "LOW"
        }
