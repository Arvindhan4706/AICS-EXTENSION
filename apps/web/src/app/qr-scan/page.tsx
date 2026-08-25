"use client";

import { useState } from "react";
import { QrCode, Scan, TerminalSquare } from "lucide-react";

export default function QRScannerPage() {
  const [qrInput, setQrInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = async () => {
    if (!qrInput.trim()) return;
    setLoading(true);
    try {
      // Decode QR payload string minimally to a URL
      let targetUrl = qrInput.trim();
      if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = 'http://' + targetUrl;
      }
      
      const { submitScan, getScanStatus } = await import('@/lib/api');
      
      const { scan_id } = await submitScan(targetUrl);
      
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
          extracted_target_url: targetUrl,
          quishing_threat_analysis: {
            threat_score: data.risk_score || 0,
            explainable_ai: {
              reasons: (data.explanations || []).map((exp: any) => ({
                title: exp.feature.replace('_', ' ').toUpperCase(),
                description: exp.description
              }))
            }
          }
        };
        setResult(mappedResult);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <QrCode className="w-6 h-6 text-cyber-accent" />
          QR_PAYLOAD_DECODER // QUISHING_SCANNER
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Decodes QR payloads, inspects embedded target domains, and prevents QR phishing scams.
        </p>
      </div>

      <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        <label className="text-[10px] font-bold text-cyber-muted uppercase tracking-widest flex items-center gap-2">
          <span className="text-cyber-accent">{">"}</span> INPUT_DECODED_QR_PAYLOAD
        </label>
        <div className="flex flex-col md:flex-row gap-3">
          <input
            type="text"
            value={qrInput}
            onChange={(e) => setQrInput(e.target.value)}
            className="flex-1 bg-transparent border border-cyber-border p-3 font-mono text-xs text-cyber-accent focus:outline-none focus:border-cyber-accent uppercase tracking-widest"
          />
          <button
            onClick={handleScan}
            disabled={loading}
            className="bg-transparent hover:bg-cyber-accent hover:text-black text-cyber-accent border border-cyber-accent font-bold px-6 py-2 transition-all flex items-center justify-center gap-2 disabled:opacity-50 uppercase tracking-widest text-xs"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 border-2 border-cyber-accent border-t-transparent rounded-full animate-spin"></span>
                DECODING...
              </span>
            ) : (
              <>
                <TerminalSquare className="w-4 h-4" />
                [ EXEC_DECODE ]
              </>
            )}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-cyber-card border border-cyber-border p-6 space-y-4 animate-in fade-in zoom-in duration-300">
          <div className="flex items-center justify-between border-b border-cyber-border pb-4">
            <div>
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">DECODED_TARGET_URL</div>
              <div className="text-md font-bold font-mono text-white mt-1">{result.extracted_target_url}</div>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">QUISHING_THREAT_SCORE</div>
              <div className="text-3xl font-bold font-mono text-cyber-danger mt-1">
                {result.quishing_threat_analysis.threat_score}/100
              </div>
            </div>
          </div>

          <div className="p-4 bg-cyber-bg border border-cyber-border border-l-2 border-l-cyber-danger">
            <h4 className="text-[10px] font-bold text-cyber-muted uppercase tracking-widest mb-3">THREAT_VECTORS_IDENTIFIED</h4>
            <ul className="space-y-2 text-[10px] text-cyber-muted uppercase tracking-wider">
              {result.quishing_threat_analysis.explainable_ai.reasons.map((r: any, i: number) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-cyber-danger font-bold">{">"}</span>
                  <span>
                    <strong className="text-white">{r.title}:</strong> {r.description}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
