// CyberShield AI Content Script - Injects protective warning overlay on threat pages
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SHOW_PHISHING_WARNING") {
    injectWarningBanner(request.data);
  }
});

function injectWarningBanner(threatData) {
  if (document.getElementById('cybershield-warning-overlay')) return;

  const overlay = document.createElement('div');
  overlay.id = 'cybershield-warning-overlay';
  overlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(15, 23, 42, 0.96);
    backdrop-filter: blur(12px);
    z-index: 999999999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #F8FAFC;
    padding: 2rem;
    box-sizing: border-box;
  `;

  overlay.innerHTML = `
    <div style="max-width: 650px; background: #0F172A; border: 1px solid #334155; border-top: 4px solid #EF4444; border-radius: 12px; padding: 2.5rem; text-align: left; box-shadow: 0 25px 50px -12px rgba(239, 68, 68, 0.15);">
      <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; color: #EF4444; font-size: 1.5rem; font-weight: bold;">
          🛡️
        </div>
        <h1 style="color: #F8FAFC; margin: 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.025em;">CyberShield Security Alert</h1>
      </div>
      
      <p style="color: #EF4444; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
        Malicious Threat Detected
      </p>
      <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 1.5rem; word-break: break-all;">
        Target: <span style="color: #E2E8F0; font-family: monospace;">${threatData.url}</span>
      </p>
      
      <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 0.75rem; font-size: 0.9rem;">
          <span style="color: #94A3B8;">Threat Assessment: <span style="color: #EF4444; font-weight: 700;">${threatData.threat_score}/100</span></span>
          <span style="color: #F59E0B; background: rgba(245, 158, 11, 0.1); padding: 2px 8px; border-radius: 4px;">${threatData.risk_level} RISK</span>
        </div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5;">
          <strong>Explanation:</strong> ${threatData.explainable_ai.reasons[0]?.description || "High probability of credential harvesting and identity theft."}
        </div>
      </div>

      <div style="display: flex; gap: 1rem; justify-content: flex-end;">
        <button id="cybershield-proceed-btn" style="background: transparent; color: #64748B; border: none; padding: 0.75rem 1rem; font-size: 0.85rem; cursor: pointer; text-decoration: underline;">
          Proceed Anyway (Unsafe)
        </button>
        <button id="cybershield-leave-btn" style="background: #EF4444; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2);">
          Back to Safety
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  document.getElementById('cybershield-leave-btn').addEventListener('click', () => {
    window.history.back();
  });

  document.getElementById('cybershield-proceed-btn').addEventListener('click', () => {
    overlay.remove();
  });
}
