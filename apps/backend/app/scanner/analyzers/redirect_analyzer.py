class RedirectAnalyzer:
    async def analyze(self, url: str) -> dict:
        return {
            "redirects": 0,
            "cross_domain": "NO",
            "risk": "LOW",
            "final_url": url
        }
