// CyberShield AI - Manifest V3 Background Service Worker
// Change this to your public Cloud VPS domain when deploying (e.g., "https://cybershield.yourdomain.com/api/v1")
const API_BASE_URL = "http://localhost:8000/api/v1";

// Simple in-memory cache to prevent hammering the API for recent scans
const scanCache = new Map();

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Only trigger on explicit URL changes, not AJAX/DOM updates
  if (changeInfo.url && tab.url.startsWith('http')) {
    analyzeUrl(tab.url, tabId);
  }
});

async function analyzeUrl(url, tabId) {
  try {
    let result;
    
    // Check Cache
    if (scanCache.has(url)) {
      result = scanCache.get(url);
    } else {
      // Step 1: Submit to the new async pipeline
      const submitRes = await fetch(`${API_BASE_URL}/scans/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
      });
      
      if (!submitRes.ok) throw new Error("API Error on Submit");
      const submitData = await submitRes.json();
      const scanId = submitData.scan_id;
      
      // Step 2: Poll for completion
      let scanCompleted = false;
      let apiData = null;
      while (!scanCompleted) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const pollRes = await fetch(`${API_BASE_URL}/scans/${scanId}`);
        apiData = await pollRes.json();
        if (apiData.status === 'completed' || apiData.status === 'failed') {
          scanCompleted = true;
        }
      }
      
      if (apiData.status !== 'completed') throw new Error("Scan Failed");
      
      // Map to old extension schema
      result = {
        threat_score: apiData.risk_score || 0,
        risk_level: apiData.risk_level || "UNKNOWN",
        category: apiData.verdict || "UNKNOWN",
        explainable_ai: {
          reasons: (apiData.explanations || []).map(exp => ({
            title: exp.feature.replace('_', ' ').toUpperCase(),
            description: exp.description
          }))
        }
      };
      
      // Cache result for 5 minutes
      scanCache.set(url, result);
      setTimeout(() => scanCache.delete(url), 5 * 60 * 1000);
    }
    
    // Update toolbar badge
    const badgeText = result.threat_score > 70 ? "DANGER" : (result.threat_score > 40 ? "WARN" : "SAFE");
    const badgeColor = result.threat_score > 70 ? "#EF4444" : (result.threat_score > 40 ? "#F59E0B" : "#10B981");
    
    chrome.action.setBadgeText({ text: badgeText, tabId: tabId });
    chrome.action.setBadgeBackgroundColor({ color: badgeColor, tabId: tabId });
    
    // Retrieve user settings for strict mode (default false)
    chrome.storage.local.get(['strictMode'], (settings) => {
      const threshold = settings.strictMode ? 40 : 70; // Strict blocks Warn too
      
      // Inject warning overlay content script
      if (result.threat_score >= threshold) {
        chrome.tabs.sendMessage(tabId, {
          action: "SHOW_PHISHING_WARNING",
          data: result
        });
      }
    });
    
  } catch (err) {
    console.error("CyberShield Extension Background Scan Error:", err);
    chrome.action.setBadgeText({ text: "ERR", tabId: tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#64748B", tabId: tabId });
  }
}
