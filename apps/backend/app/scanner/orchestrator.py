from typing import Dict, Any
from .analyzers.url_analyzer import URLAnalyzer
from .analyzers.domain_analyzer import DomainAnalyzer
from .analyzers.dns_analyzer import DNSAnalyzer
from .analyzers.ssl_analyzer import SSLAnalyzer
from .analyzers.redirect_analyzer import RedirectAnalyzer
from .analyzers.html_analyzer import HTMLAnalyzer
from .analyzers.playwright_analyzer import PlaywrightAnalyzer
from app.security.gateway import SecurityGateway

class ScanOrchestrator:
    def __init__(self):
        self.url_analyzer = URLAnalyzer()
        self.domain_analyzer = DomainAnalyzer()
        self.dns_analyzer = DNSAnalyzer()
        self.ssl_analyzer = SSLAnalyzer()
        self.redirect_analyzer = RedirectAnalyzer()
        self.html_analyzer = HTMLAnalyzer()
        self.playwright_analyzer = PlaywrightAnalyzer()

    async def run_scan(self, target_url: str) -> Dict[str, Any]:
        """
        Orchestrates the entire scan process for a given URL.
        """
        results = {
            "target": target_url,
            "status": "started",
            "analysis": {}
        }
        
        # 1. Validation & SSRF Check
        SecurityGateway.validate_target(target_url)
        results["ssrf_check"] = "passed"
        
        # 2. Sequential/Parallel Analysis
        results["analysis"]["url"] = await self.url_analyzer.analyze(target_url)
        results["analysis"]["redirects"] = await self.redirect_analyzer.analyze(target_url)
        
        final_url = results["analysis"]["redirects"].get("final_url", target_url)
        SecurityGateway.validate_target(final_url)
        
        results["analysis"]["domain"] = await self.domain_analyzer.analyze(final_url)
        results["analysis"]["dns"] = await self.dns_analyzer.analyze(final_url)
        results["analysis"]["ssl"] = await self.ssl_analyzer.analyze(final_url)
        results["analysis"]["html"] = await self.html_analyzer.analyze(final_url)
        results["analysis"]["browser"] = await self.playwright_analyzer.analyze(final_url)
        
        # 3. VirusTotal Telemetry
        import asyncio
        from app.security.virustotal import VirusTotalClient
        vt_client = VirusTotalClient()
        try:
            vt_result = await asyncio.to_thread(vt_client.scan_url, target_url)
        except Exception:
            vt_result = {"status": "UNKNOWN", "positives": 0, "total": 90}
            
        # VT data needs to be extracted by FeatureEngine, which looks for analysis.virustotal
        results["analysis"]["virustotal"] = vt_result
        
        results["status"] = "completed"
        return results
