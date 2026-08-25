class DomainAnalyzer:
    async def analyze(self, url: str) -> dict:
        return {
            "tld": ".com",
            "age_days": 100,
            "status": "ANALYZED"
        }
