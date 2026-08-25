"use client";

import { useState } from "react";
import { Mail, TerminalSquare } from "lucide-react";

export default function EmailScannerPage() {
  const [rawText, setRawText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/email/scan-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: rawText })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <Mail className="w-6 h-6 text-cyber-accent" />
          EML_HEADER_INSPECTOR
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Validate SPF, DKIM, DMARC signatures, detect spoofed headers, and extract suspicious links.
        </p>
      </div>

      <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        <label className="text-[10px] font-bold text-cyber-muted uppercase tracking-widest flex items-center gap-2">
          <span className="text-cyber-accent">{">"}</span> INPUT_RAW_EMAIL_SOURCE
        </label>
        <textarea
          rows={8}
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          className="w-full bg-transparent border border-cyber-border p-4 font-mono text-xs text-cyber-accent focus:outline-none focus:border-cyber-accent uppercase tracking-widest custom-scrollbar"
        />
        <div className="flex justify-end">
          <button
            onClick={handleScan}
            disabled={loading}
            className="bg-transparent hover:bg-cyber-accent hover:text-black text-cyber-accent border border-cyber-accent font-bold px-6 py-2 transition-all flex items-center gap-2 disabled:opacity-50 uppercase tracking-widest text-xs"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 border-2 border-cyber-accent border-t-transparent rounded-full animate-spin"></span>
                PARSING_HEADERS...
              </span>
            ) : (
              <>
                <TerminalSquare className="w-4 h-4" />
                [ EXEC_MAIL_SCAN ]
              </>
            )}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-cyber-card border border-cyber-border p-6 space-y-6 animate-in fade-in zoom-in duration-300">
          <div className="flex items-center justify-between border-b border-cyber-border pb-4">
            <div>
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">OVERALL_MAIL_RISK</div>
              <div className="text-xl font-bold text-cyber-danger uppercase tracking-widest mt-1">{result.email_risk_level}</div>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">THREAT_SCORE</div>
              <div className="text-3xl font-bold font-mono text-cyber-danger mt-1">{result.overall_threat_score}/100</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs uppercase tracking-widest">
            <div className="p-4 bg-cyber-bg border border-cyber-border hover:border-cyber-accent transition-colors">
              <div className="text-[10px] text-cyber-muted mb-2">SPF_VERIFICATION</div>
              <div className={result.parsed_metadata.spf_status === 1 ? "text-cyber-accent font-bold" : "text-cyber-danger font-bold"}>
                {result.parsed_metadata.spf_status === 1 ? "[ PASS ]" : "[ FAIL_OR_MISSING ]"}
              </div>
            </div>
            <div className="p-4 bg-cyber-bg border border-cyber-border hover:border-cyber-accent transition-colors">
              <div className="text-[10px] text-cyber-muted mb-2">DKIM_VERIFICATION</div>
              <div className={result.parsed_metadata.dkim_status === 1 ? "text-cyber-accent font-bold" : "text-cyber-danger font-bold"}>
                {result.parsed_metadata.dkim_status === 1 ? "[ PASS ]" : "[ FAIL_OR_MISSING ]"}
              </div>
            </div>
            <div className="p-4 bg-cyber-bg border border-cyber-border hover:border-cyber-danger transition-colors">
              <div className="text-[10px] text-cyber-muted mb-2">HEADER_SPOOFING_STATUS</div>
              <div className={result.parsed_metadata.spoofing_detected ? "text-cyber-danger font-bold" : "text-cyber-accent font-bold"}>
                {result.parsed_metadata.spoofing_detected ? "[ SPOOFING_DETECTED ]" : "[ CLEAN ]"}
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-bold text-sm text-white mb-4 uppercase tracking-widest border-b border-cyber-border pb-2">EXTRACTED_EMBEDDED_URLS</h4>
            <div className="space-y-3">
              {result.link_analysis_results.map((link: any, i: number) => (
                <div key={i} className="p-3 bg-cyber-bg border border-cyber-border flex items-center justify-between text-[11px] font-mono hover:border-cyber-accent transition-colors">
                  <span className="text-white truncate max-w-md">{link.url}</span>
                  <span className={`font-bold ${link.threat_score > 70 ? "text-cyber-danger" : link.threat_score > 40 ? "text-cyber-warning" : "text-cyber-accent"}`}>
                    SCORE: {link.threat_score}/100 [{link.risk_level}]
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
