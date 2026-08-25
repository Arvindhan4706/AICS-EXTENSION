// Change this to your public Cloud VPS domain when deploying (e.g., "https://cybershield.yourdomain.com/api/v1")
const API_BASE = "http://localhost:8000/api/v1";

document.addEventListener('DOMContentLoaded', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.url) {
    document.getElementById('active-url').textContent = tab.url;
    scanCurrentTab(tab.url);
  }

  document.getElementById('open-dashboard-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: "http://localhost:3005/dashboard" });
  });

  document.getElementById('rescan-btn').addEventListener('click', () => {
    if (tab && tab.url) scanCurrentTab(tab.url);
  });

  // Strict Mode Toggle Logic
  const strictToggle = document.getElementById('strict-mode-toggle');
  chrome.storage.local.get(['strictMode'], (result) => {
    strictToggle.checked = !!result.strictMode;
  });
  
  strictToggle.addEventListener('change', (e) => {
    chrome.storage.local.set({ strictMode: e.target.checked });
  });
});

async function scanCurrentTab(url) {
  try {
    const submitRes = await fetch(`${API_BASE}/scans/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    
    if (!submitRes.ok) throw new Error("API Error on Submit");
    const submitData = await submitRes.json();
    const scanId = submitData.scan_id;
    
    let scanCompleted = false;
    let apiData = null;
    while (!scanCompleted) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      const pollRes = await fetch(`${API_BASE}/scans/${scanId}`);
      apiData = await pollRes.json();
      if (apiData.status === 'completed' || apiData.status === 'failed') {
        scanCompleted = true;
      }
    }

    if (apiData.status !== 'completed') {
      throw new Error("Scan Failed");
    }

    const data = {
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

    document.getElementById('threat-score').textContent = data.threat_score;
    const riskBadge = document.getElementById('risk-level');
    riskBadge.textContent = data.risk_level;
    riskBadge.className = `risk-badge ${data.risk_level.toLowerCase()}`;

    const list = document.getElementById('reasons-list');
    list.innerHTML = '';
    const reasons = data.explainable_ai.reasons;
    if (reasons.length === 0) {
      list.innerHTML = '<li>No security threats detected. URL structure & features appear legitimate.</li>';
    } else {
      reasons.slice(0, 3).forEach(r => {
        const li = document.createElement('li');
        li.textContent = `${r.title}: ${r.description}`;
        list.appendChild(li);
      });
    }
  } catch (err) {
    document.getElementById('threat-score').textContent = "ERR";
    document.getElementById('risk-level').textContent = "INVALID_URL";
    document.getElementById('reasons-list').innerHTML = `<li>${err.message || 'Validation Failed or Offline'}</li>`;
  }
}
