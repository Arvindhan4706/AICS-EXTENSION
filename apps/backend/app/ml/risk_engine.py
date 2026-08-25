class RiskEngine:
    def calculate_risk(self, ml_prediction: dict, analysis_results: dict) -> dict:
        """
        Combines ML prediction with hard evidence rules to compute a final risk score (0-100) and verdict.
        """
        evidence = []
        base_score = ml_prediction["confidence"] * 100
        
        # Hard evidence checks overriding or modifying ML
        if analysis_results.get("html", {}).get("password_fields", 0) > 0 and \
           analysis_results.get("redirects", {}).get("cross_domain") == "YES":
            evidence.append({"level": "HIGH", "message": "Credential harvesting form posts to external domain"})
            base_score = max(base_score, 90)
            
        url_data = analysis_results.get("url", {})
        if url_data.get("has_ip"):
            evidence.append({"level": "MEDIUM", "message": "IP address used instead of hostname"})
            base_score = max(base_score, 60)
            
        final_score = min(100, int(base_score))
        
        if final_score >= 80:
            risk_level = "CRITICAL"
            verdict = "PHISHING"
        elif final_score >= 40:
            risk_level = "HIGH"
            verdict = "SUSPICIOUS"
        elif final_score >= 15:
            risk_level = "MEDIUM"
            verdict = "LOW RISK"
        else:
            risk_level = "LOW"
            verdict = "LEGITIMATE"
            
        return {
            "classification": verdict,
            "risk_score": final_score,
            "risk_level": risk_level,
            "evidence": evidence
        }
