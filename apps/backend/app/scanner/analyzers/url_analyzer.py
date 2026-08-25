from urllib.parse import urlparse
import math
import re

class URLAnalyzer:
    SUSPICIOUS_KEYWORDS = ["verify", "account", "login", "secure", "bank", "update", "paypal"]

    async def analyze(self, url: str) -> dict:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        
        # Strip scheme to perfectly match training data URL lengths
        clean_url = url.replace("http://", "").replace("https://", "")
        if clean_url.endswith("/"):
            clean_url = clean_url[:-1]
            
        return {
            "url_length": len(clean_url),
            "hostname_length": len(hostname),
            "subdomain_count": hostname.count(".") - 1 if hostname.count(".") > 0 else 0,
            "has_ip": self._has_ip(hostname),
            "entropy": self._calculate_entropy(hostname),
            "suspicious_keywords": self._find_keywords(clean_url)
        }

    def _has_ip(self, hostname: str) -> bool:
        return bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname))
        
    def _calculate_entropy(self, string: str) -> float:
        if not string:
            return 0.0
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy

    def _find_keywords(self, url: str) -> list[str]:
        found = []
        url_lower = url.lower()
        for kw in self.SUSPICIOUS_KEYWORDS:
            if kw in url_lower:
                found.append(kw)
        return found
