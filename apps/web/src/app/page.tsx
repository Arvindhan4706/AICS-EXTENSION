"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  ShieldAlert, 
  ShieldCheck, 
  Zap, 
  Brain, 
  Globe, 
  ArrowRight, 
  Check, 
  Cpu, 
  Server,
  TerminalSquare
} from "lucide-react";

export default function SaaSProductLandingPage() {
  const [demoUrl, setDemoUrl] = useState("");
  const [demoResult, setDemoResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runQuickDemo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!demoUrl.trim()) return;

    setLoading(true);
    try {
      const { submitScan, getScanStatus } = await import('@/lib/api');
      
      const { scan_id } = await submitScan(demoUrl);
      
      let scanCompleted = false;
      let data = null;
      while (!scanCompleted) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        data = await getScanStatus(scan_id);
        if (data.status === 'completed' || data.status === 'failed') {
          scanCompleted = true;
        }
      }

      if (data && data.status === 'completed') {
        const mappedResult = {
          threat_score: data.risk_score || 0,
          risk_level: data.risk_level || "UNKNOWN",
          category: data.verdict || "UNKNOWN"
        };
        setDemoResult(mappedResult);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-16 max-w-7xl mx-auto pb-12 font-mono">
      {/* Hero Section */}
      <section className="relative pt-6 pb-12 text-left space-y-6 border border-cyber-accent p-8 bg-cyber-accent/5">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 border border-cyber-accent text-cyber-accent text-xs font-mono tracking-widest uppercase">
          <TerminalSquare className="w-4 h-4" />
          ROOT_ACCESS // CYBER_SHIELD_v2.0
        </div>

        <h1 className="text-4xl md:text-6xl font-black text-white tracking-widest leading-tight max-w-4xl uppercase">
          TACTICAL <span className="text-cyber-accent">THREAT DEFENSE</span> PROTOCOL
        </h1>

        <p className="text-sm text-cyber-muted max-w-2xl leading-relaxed uppercase tracking-widest border-l-2 border-cyber-accent pl-4">
          Initiate ML Ensembles. Extract 40+ vectors in real-time. Deploy SHAP XAI overrides. Secure sector via Manifest V3 protocol. T-Minus 5 minutes to total integration.
        </p>

        <div className="flex flex-wrap items-center gap-4 pt-4">
          <Link
            href="/dashboard"
            className="bg-cyber-accent hover:bg-cyber-accent/80 text-black font-bold text-sm px-8 py-3 transition-all flex items-center gap-2 uppercase tracking-widest"
          >
            [ INIT_DASHBOARD ] <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/scan"
            className="bg-transparent hover:bg-cyber-accent/10 text-cyber-accent border border-cyber-accent font-bold text-sm px-8 py-3 transition-all flex items-center gap-2 uppercase tracking-widest"
          >
            <Globe className="w-4 h-4" />
            [ EXEC_SCANNER ]
          </Link>
        </div>

        {/* Live Interactive Hero Scanner Widget */}
        <div className="pt-8 w-full max-w-3xl">
          <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4">
            <div className="flex items-center justify-between text-xs text-cyber-muted font-mono uppercase tracking-widest border-b border-cyber-border pb-2">
              <span className="flex items-center gap-2 text-cyber-accent">
                <span className="w-2 h-2 bg-cyber-accent animate-ping"></span>
                LIVE_SCAN_TERMINAL
              </span>
              <span>SYS_PRECISION: 98.2%</span>
            </div>

            <form onSubmit={runQuickDemo} className="flex flex-col md:flex-row gap-2">
              <span className="text-cyber-accent p-3 hidden md:block">{">"}</span>
              <input
                type="text"
                value={demoUrl}
                onChange={(e) => setDemoUrl(e.target.value)}
                placeholder="ENTER TARGET URL OR DOMAIN..."
                className="flex-1 bg-transparent border border-cyber-border px-4 py-3 text-sm text-cyber-accent font-mono focus:outline-none focus:border-cyber-accent transition-colors uppercase tracking-widest placeholder:text-cyber-muted"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-cyber-accent hover:bg-cyber-accent/80 text-black font-bold px-6 py-3 transition-all flex items-center gap-2 shrink-0 uppercase tracking-widest"
              >
                {loading ? "EXECUTING..." : <><Zap className="w-4 h-4" /> RUN_TEST</>}
              </button>
            </form>

            {demoResult && (
              <div className="p-4 bg-cyber-bg border border-cyber-accent text-left space-y-3 font-mono text-xs uppercase tracking-widest mt-4">
                <div className="flex justify-between items-center border-b border-cyber-accent/30 pb-2">
                  <span className="text-white font-bold">THREAT_LEVEL: <span className={demoResult.threat_score > 70 ? "text-cyber-danger" : "text-cyber-accent"}>{demoResult.threat_score}/100</span></span>
                  <span className={`px-2 py-1 font-bold ${
                    demoResult.risk_level === "CRITICAL" ? "bg-cyber-danger text-black" : "bg-cyber-accent text-black"
                  }`}>
                    {demoResult.risk_level} RISK
                  </span>
                </div>
                <div className="text-cyber-muted">VECTOR: <span className="text-white">{demoResult.category}</span></div>
                <div className="text-cyber-muted">XAI_OUTPUT: <span className="text-cyber-warning">{demoResult.explainable_ai.reasons[0]?.title} - {demoResult.explainable_ai.reasons[0]?.description}</span></div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Trusted By Enterprise Ticker */}
      <section className="text-center space-y-4 border-y border-cyber-border py-4">
        <p className="text-[10px] font-mono text-cyber-muted uppercase tracking-widest">
          SEC_PROTOCOLS_ACTIVE_AT
        </p>
        <div className="flex flex-wrap justify-center items-center gap-8 text-cyber-accent font-bold text-xs opacity-50 uppercase tracking-widest">
          <span>[ CROWDSTRIKE ]</span>
          <span>[ CLOUDFLARE ]</span>
          <span>[ PALO_ALTO ]</span>
          <span>[ OKTA_SEC ]</span>
          <span>[ MSFT_DEF ]</span>
        </div>
      </section>

      {/* Enterprise Feature Grid */}
      <section className="space-y-8">
        <div className="text-left space-y-2 border-l-4 border-cyber-accent pl-4">
          <h2 className="text-2xl font-bold text-white uppercase tracking-widest">SYS_ARCHITECTURE</h2>
          <p className="text-xs text-cyber-muted uppercase tracking-widest">Multi-vector mitigation parameters active.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-cyber-card border border-cyber-border p-6 space-y-4 hover:border-cyber-accent transition-all">
            <div className="text-cyber-accent border-b border-cyber-border pb-4 flex items-center justify-between">
              <Cpu className="w-6 h-6" />
              <span className="text-[10px] tracking-widest">MOD_01</span>
            </div>
            <h3 className="text-sm font-bold text-white uppercase tracking-widest">Ensemble Engine</h3>
            <p className="text-[11px] text-cyber-muted leading-relaxed uppercase tracking-wider">
              RF, XGB, LGBM weighted voting models. Evaluating 40+ vectors in &lt;120ms.
            </p>
          </div>

          <div className="bg-cyber-card border border-cyber-border p-6 space-y-4 hover:border-cyber-accent transition-all">
            <div className="text-cyber-accent border-b border-cyber-border pb-4 flex items-center justify-between">
              <Brain className="w-6 h-6" />
              <span className="text-[10px] tracking-widest">MOD_02</span>
            </div>
            <h3 className="text-sm font-bold text-white uppercase tracking-widest">SHAP XAI</h3>
            <p className="text-[11px] text-cyber-muted leading-relaxed uppercase tracking-wider">
              Translating black-box outputs to MITRE ATT&CK / OWASP directives.
            </p>
          </div>

          <div className="bg-cyber-card border border-cyber-border p-6 space-y-4 hover:border-cyber-accent transition-all">
            <div className="text-cyber-accent border-b border-cyber-border pb-4 flex items-center justify-between">
              <ShieldCheck className="w-6 h-6" />
              <span className="text-[10px] tracking-widest">MOD_03</span>
            </div>
            <h3 className="text-sm font-bold text-white uppercase tracking-widest">Manifest V3</h3>
            <p className="text-[11px] text-cyber-muted leading-relaxed uppercase tracking-wider">
              Background workers blocking credential exfiltration at the browser level.
            </p>
          </div>
        </div>
      </section>


      {/* CTA Bottom Banner */}
      <section className="border border-cyber-accent bg-cyber-accent/10 p-10 text-center space-y-6">
        <h2 className="text-2xl font-black text-white uppercase tracking-widest">SECURE_SECTOR_NOW</h2>
        <p className="text-xs text-cyber-accent max-w-xl mx-auto uppercase tracking-widest">
          Initiate protocols. Scan URLs, EML, and QR vectors via terminal.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/dashboard" className="bg-cyber-accent hover:bg-cyber-accent/80 text-black font-bold px-8 py-3 transition-all text-sm uppercase tracking-widest">
            [ EXECUTE_LOGIN ]
          </Link>
        </div>
      </section>
    </div>
  );
}
