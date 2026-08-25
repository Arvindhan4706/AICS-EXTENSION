class HTMLAnalyzer:
    async def analyze(self, url: str) -> dict:
        return {
            "forms": 1,
            "password_fields": 0,
            "external_resources": 5,
            "result": "NORMAL"
        }
