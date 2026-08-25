"use client";

import { useState } from "react";
import { 
  Globe, 
  Search, 
  Brain, 
  FileText, 
  Cpu, 
  CheckCircle2,
  TerminalSquare
} from "lucide-react";

export default function RealTimeScannerPage() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setErrorMsg(null);
    setResult(null);
    try {
      // Import functions dynamically so we don't have to change top-level imports and break other things
      const { submitScan, getScanStatus } = await import('@/lib/api');
      
      const { scan_id } = await submitScan(url);
      
      // Polling loop
      let scanCompleted = false;
      let data = null;
      while (!scanCompleted) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
        data = await getScanStatus(scan_id);
        if (data.status === 'completed' || data.status === 'failed') {
          scanCompleted = true;
        }
      }

      if (data && data.status === 'completed') {
        // Map API response from backend to UI model
        const mappedResult = {
          threat_score: data.verdict?.risk_score ?? 0,
          risk_level: data.verdict?.risk_level || "UNKNOWN",
          category: data.verdict?.classification || "UNKNOWN",
          probability: data.ml?.confidence ?? ((data.verdict?.risk_score || 0) / 100),
          threat_intelligence: {
            virustotal: data.analysis?.virustotal || { status: "CLEAN", positives: 0 }
          },
          explainable_ai: {
            reasons: (data.explanations || []).map((exp: any) => ({
              title: exp.feature ? exp.feature.replace('_', ' ').toUpperCase() : "HEURISTIC",
              contribution_percentage: `${((exp.importance ?? 0) * 100).toFixed(1)}%`,
              description: exp.description || "Risk indicator evaluated."
            })),
            mitre_attack: data.mitre_mappings || ["M1021 - Network Intrusion Prevention"],
            owasp_top10: data.owasp_mappings || ["A00:2021 - Compliant Baseline"],
            recommendations: data.recommendations || ["Proceed under standard security policies."]
          },
          model_breakdown: data.ml?.model_breakdown ? {
            xgboost_prob: data.ml.model_breakdown.xgboost ?? 0.5,
            random_forest_prob: data.ml.model_breakdown.random_forest ?? 0.5,
            ensemble_prob: data.ml.model_breakdown.ensemble ?? 0.5
          } : {
            xgboost_prob: (data.verdict?.risk_score || 0) / 100,
            random_forest_prob: (data.verdict?.risk_score || 0) / 100,
            ensemble_prob: (data.verdict?.risk_score || 0) / 100
          },
          features_extracted: data.features || data.analysis?.url || {}
        };
        
        setResult(mappedResult);
      } else if (data && data.status === 'failed') {
        setErrorMsg(data.error || "An unknown error occurred during analysis.");
      }
    } catch (err: any) {
      console.error("Scan error:", err);
      setErrorMsg(err.message || "Failed to communicate with the scanning engine.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <Globe className="w-6 h-6 text-cyber-accent" />
          TARGET_SCANNER_PROTOCOL
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Deep structural, lexical, DOM, and ML ensemble evaluation with SHAP XAI override.
        </p>
      </div>

      <form onSubmit={handleScan} className="bg-cyber-bg border border-cyber-border p-4 flex flex-col md:flex-row gap-3">
        <div className="relative flex-1 flex items-center border-b border-cyber-border">
          <span className="text-cyber-accent mr-2">{">"}</span>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="ENTER TARGET URL, IP, OR DOMAIN..."
            className="w-full bg-transparent py-3 text-cyber-accent placeholder:text-cyber-muted focus:outline-none focus:border-cyber-accent font-mono text-sm uppercase tracking-widest"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-cyber-accent hover:bg-cyber-accent/80 text-black font-bold px-8 py-3 transition-all flex items-center justify-center gap-2 disabled:opacity-50 uppercase tracking-widest border border-cyber-accent"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></span>
              EXTRACTING...
            </span>
          ) : (
            <>
              <TerminalSquare className="w-5 h-5" />
              [ EXEC_SCAN ]
            </>
          )}
        </button>
      </form>

      <div className="flex items-center gap-2 text-[10px] text-cyber-muted uppercase tracking-widest">
        <span>PRESET_TARGETS:</span>
        <button
          onClick={() => setUrl("http://192.168.1.1/paypal-verify-billing/login.php")}
          className="px-2 py-1 bg-transparent hover:bg-cyber-danger/10 border border-cyber-danger text-cyber-danger font-mono"
        >
          [ PHISH_IP ]
        </button>
        <button
          onClick={() => setUrl("https://chase-bank-verify-account.top")}
          className="px-2 py-1 bg-transparent hover:bg-cyber-warning/10 border border-cyber-warning text-cyber-warning font-mono"
        >
          [ HIGH_RISK_TLD ]
        </button>
        <button
          onClick={() => setUrl("https://google.com")}
          className="px-2 py-1 bg-transparent hover:bg-cyber-accent/10 border border-cyber-accent text-cyber-accent font-mono"
        >
          [ SECURE_DOMAIN ]
        </button>
      </div>

      {errorMsg && (
        <div className="bg-cyber-danger/10 border border-cyber-danger p-4 text-cyber-danger font-mono text-sm animate-in fade-in zoom-in">
          <div className="font-bold uppercase tracking-widest mb-1">SCAN_FAILED_EXCEPTION:</div>
          <div>{errorMsg}</div>
        </div>
      )}

      {result && (
        <div className="space-y-6 animate-in fade-in zoom-in duration-300">
          <div className="bg-cyber-card border border-cyber-border p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col items-center justify-center p-4 bg-cyber-bg border border-cyber-accent relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-cyber-accent/30 animate-pulse"></div>
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest mb-2">THREAT_SCORE</div>
              <div className={`text-5xl font-black font-mono ${
                result.threat_score > 70 ? "text-cyber-danger" : result.threat_score > 40 ? "text-cyber-warning" : "text-cyber-accent"
              }`}>
                {result.threat_score}/100
              </div>
              <div className="mt-3">
                <span className={`px-4 py-1 text-[10px] font-bold tracking-widest uppercase ${
                  result.risk_level === "CRITICAL" ? "bg-cyber-danger text-black" :
                  result.risk_level === "HIGH" ? "bg-cyber-warning text-black" :
                  result.risk_level === "MEDIUM" ? "bg-cyber-warning text-black" :
                  "bg-cyber-accent text-black"
                }`}>
                  [{result.risk_level}_RISK]
                </span>
              </div>
            </div>

            <div className="space-y-3 col-span-2">
              <div className="border-b border-cyber-border pb-3">
                <div className="text-[10px] text-cyber-muted uppercase tracking-widest">THREAT_CLASSIFICATION</div>
                <div className="text-xl font-bold text-white mt-1 uppercase tracking-widest">{result.category}</div>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="p-3 bg-cyber-bg border border-cyber-border hover:border-cyber-accent transition-colors">
                  <div className="text-[10px] text-cyber-muted uppercase tracking-widest">ENSEMBLE_PROBABILITY</div>
                  <div className="text-lg font-bold font-mono text-cyber-accent mt-1">
                    {(result.probability * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="p-3 bg-cyber-bg border border-cyber-border hover:border-cyber-danger transition-colors">
                  <div className="text-[10px] text-cyber-muted uppercase tracking-widest">VT_TELEMETRY</div>
                  <div className="text-lg font-bold font-mono text-cyber-danger mt-1 uppercase">
                    {result.threat_intelligence.virustotal.status} [{result.threat_intelligence.virustotal.positives}/90]
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-cyber-card border border-cyber-border p-6">
            <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2 uppercase tracking-widest border-b border-cyber-border pb-2">
              <Brain className="w-4 h-4 text-cyber-accent" />
              XAI_LOGS // SHAP_OVERRIDE
            </h3>
            <p className="text-[10px] text-cyber-muted mb-6 uppercase tracking-widest">
              Translating model weights to human-readable rationale.
            </p>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-3">
                {result.explainable_ai.reasons.map((r: any, idx: number) => (
                  <div key={idx} className="p-4 bg-cyber-bg border-l-2 border-cyber-danger">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[11px] text-white uppercase tracking-widest">{r.title}</span>
                      <span className="text-[10px] font-mono text-cyber-danger font-bold">[{r.contribution_percentage}]</span>
                    </div>
                    <p className="text-[10px] text-cyber-muted mt-2 uppercase tracking-wider">{r.description}</p>
                  </div>
                ))}
              </div>

              <div className="space-y-4">
                <div className="p-4 bg-cyber-bg border border-cyber-border space-y-3">
                  <div className="text-[10px] font-bold text-cyber-accent uppercase tracking-widest">MITRE_ATTACK_MAPPING</div>
                  <div className="flex flex-wrap gap-2">
                    {result.explainable_ai.mitre_attack.map((item: string, i: number) => (
                      <span key={i} className="px-2 py-1 bg-cyber-accent/10 border border-cyber-accent/30 text-cyber-accent text-[10px] font-mono uppercase">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 bg-cyber-bg border border-cyber-border space-y-3">
                  <div className="text-[10px] font-bold text-cyber-warning uppercase tracking-widest">OWASP_TOP_10_MAPPING</div>
                  <div className="flex flex-wrap gap-2">
                    {result.explainable_ai.owasp_top10.map((item: string, i: number) => (
                      <span key={i} className="px-2 py-1 bg-cyber-warning/10 border border-cyber-warning/30 text-cyber-warning text-[10px] font-mono uppercase">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 bg-cyber-bg border border-cyber-border space-y-3">
                  <div className="text-[10px] font-bold text-white uppercase tracking-widest">SYS_RECOMMENDATIONS</div>
                  <ul className="space-y-2 text-[10px] text-cyber-muted uppercase tracking-wider">
                    {result.explainable_ai.recommendations.map((rec: string, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-cyber-accent">{">"}</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-cyber-card border border-cyber-border p-6">
              <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2 uppercase tracking-widest border-b border-cyber-border pb-2">
                <Cpu className="w-4 h-4 text-cyber-accent" />
                ENSEMBLE_PROBABILITY_MATRIX
              </h3>
              <div className="space-y-4 font-mono text-[10px] uppercase tracking-widest mt-4">
                {Object.entries(result.model_breakdown).map(([model, prob]: any) => (
                  <div key={model} className="space-y-1">
                    <div className="flex justify-between text-cyber-muted">
                      <span>{model.replace('_prob', '').replace('_', ' ')}</span>
                      <span className="text-cyber-accent">{(prob * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-1 bg-cyber-bg w-full">
                      <div className="h-full bg-cyber-accent" style={{ width: `${prob * 100}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-cyber-card border border-cyber-border p-6">
              <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2 uppercase tracking-widest border-b border-cyber-border pb-2">
                <FileText className="w-4 h-4 text-cyber-accent" />
                EXTRACTED_VECTORS
              </h3>
              <div className="grid grid-cols-2 gap-2 text-[10px] font-mono max-h-56 overflow-y-auto pr-2 custom-scrollbar uppercase tracking-widest">
                {Object.entries(result.features_extracted).map(([key, val]: any) => (
                  <div key={key} className="p-2 bg-cyber-bg border border-cyber-border flex justify-between hover:border-cyber-accent transition-colors">
                    <span className="text-cyber-muted truncate mr-2" title={key}>{key}</span>
                    <span className="text-white font-bold">{String(val)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
