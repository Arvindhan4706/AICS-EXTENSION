class DNSAnalyzer:
    async def analyze(self, url: str) -> dict:
        return {
            "a_records": ["93.184.216.34"],
            "mx_records": ["FOUND"],
            "txt_records": ["FOUND"],
            "status": "NORMAL"
        }
