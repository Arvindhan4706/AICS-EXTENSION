import os
import requests
import base64

class VirusTotalClient:
    def __init__(self):
        # We use the key provided by the user
        self.api_key = "c1fbbdcda8d6e7fb41b9a9ab87fdff77fa465e8da15f67ae532b30ce05dd596a"
        self.base_url = "https://www.virustotal.com/api/v3"

    def scan_url(self, url: str) -> dict:
        """
        Queries the VirusTotal API v3 for an existing URL report.
        Returns a formatted dictionary with telemetry data.
        """
        try:
            # VT API v3 URL identifier format
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            
            headers = {
                "accept": "application/json",
                "x-apikey": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/urls/{url_id}", headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                harmless = stats.get("harmless", 0)
                undetected = stats.get("undetected", 0)
                
                total = malicious + suspicious + harmless + undetected
                positives = malicious + suspicious
                
                return {
                    "status": "MALICIOUS" if positives > 0 else "CLEAN",
                    "positives": positives,
                    "total": total,
                    "raw_stats": stats
                }
            else:
                return {
                    "status": "UNKNOWN",
                    "positives": 0,
                    "total": 90,
                    "raw_stats": {}
                }
        except Exception as e:
            print(f"[!] VirusTotal API Error: {e}")
            return {
                "status": "OFFLINE",
                "positives": 0,
                "total": 90,
                "raw_stats": {}
            }
