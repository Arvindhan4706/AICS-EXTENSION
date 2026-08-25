"use client";

import { useState, useEffect } from "react";
import { FileCheck, Download, TerminalSquare } from "lucide-react";

export default function ReportsPage() {
  const [scans, setScans] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/scan/history`)
      .then((res) => res.json())
      .then((data) => setScans(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <FileCheck className="w-6 h-6 text-cyber-accent" />
          THREAT_AUDIT_LOGS // CERTIFICATES
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Export verified cryptographic scan certificates and executive compliance summary reports.
        </p>
      </div>

      <div className="bg-cyber-bg border border-cyber-border p-6 overflow-hidden relative">
        <div className="absolute top-0 left-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        <div className="overflow-x-auto relative z-10">
          <table className="w-full text-left text-[11px] uppercase tracking-wider">
            <thead className="bg-cyber-card text-cyber-muted">
              <tr>
                <th className="p-4 border-b border-cyber-border font-normal">CERTIFICATE_ID</th>
                <th className="p-4 border-b border-cyber-border font-normal">TARGET_URL</th>
                <th className="p-4 border-b border-cyber-border font-normal">THREAT_SCORE</th>
                <th className="p-4 border-b border-cyber-border font-normal">RISK_LVL</th>
                <th className="p-4 border-b border-cyber-border font-normal">EXPORT_ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-border text-xs">
              {scans.map((item) => (
                <tr key={item.id} className="hover:bg-cyber-border/30 transition-colors">
                  <td className="p-4 text-cyber-accent font-bold">CS-CERT-2026-{String(item.id).padStart(6, '0')}</td>
                  <td className="p-4 text-white truncate max-w-xs">{item.target_url}</td>
                  <td className="p-4 font-bold text-cyber-muted">{item.threat_score}/100</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 text-[10px] font-bold ${
                      item.risk_level === "CRITICAL" ? "bg-cyber-danger text-black" : "bg-cyber-accent text-black"
                    }`}>
                      [{item.risk_level}]
                    </span>
                  </td>
                  <td className="p-4">
                    <button
                      onClick={() => alert(`DOWNLOADING_CRYPTOGRAPHIC_CERTIFICATE: [CS-CERT-2026-${String(item.id).padStart(6, '0')}]`)}
                      className="px-3 py-1.5 bg-transparent hover:bg-cyber-accent hover:text-black border border-cyber-accent text-cyber-accent flex items-center gap-1.5 transition-colors uppercase tracking-widest text-[10px] font-bold"
                    >
                      <Download className="w-3 h-3" />
                      EXPORT_PDF
                    </button>
                  </td>
                </tr>
              ))}
              {scans.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-cyber-muted uppercase tracking-widest">
                    NO_AUDIT_LOGS_FOUND // INITIATE_SCAN_FIRST
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
