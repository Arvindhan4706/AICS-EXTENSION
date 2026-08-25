"use client";

import { useEffect, useState } from "react";
import { Radio, RefreshCw } from "lucide-react";

export default function ThreatFeedPage() {
  const [feed, setFeed] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFeed = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/threat-intel/feed`);
      const data = await res.json();
      setFeed(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto font-mono">
      <div className="flex items-center justify-between border-l-4 border-cyber-accent pl-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
            <Radio className="w-6 h-6 text-cyber-accent" />
            GLOBAL_THREAT_INTEL_STREAM
          </h1>
          <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
            Live aggregated cyber threat feeds from VirusTotal, PhishTank, AbuseIPDB, and OpenPhish.
          </p>
        </div>
        <button
          onClick={fetchFeed}
          className="p-2 bg-transparent border border-cyber-accent text-cyber-accent hover:bg-cyber-accent hover:text-black transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="bg-cyber-bg border border-cyber-border p-6 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[11px] uppercase tracking-wider">
            <thead className="bg-cyber-card text-cyber-muted">
              <tr>
                <th className="p-4 border-b border-cyber-border font-normal">TARGET_DOMAIN_IP</th>
                <th className="p-4 border-b border-cyber-border font-normal">THREAT_TYPE</th>
                <th className="p-4 border-b border-cyber-border font-normal">CONFIDENCE</th>
                <th className="p-4 border-b border-cyber-border font-normal">INTEL_SOURCE</th>
                <th className="p-4 border-b border-cyber-border font-normal">STATUS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-border text-xs">
              {feed.map((item) => (
                <tr key={item.id} className="hover:bg-cyber-border/30 transition-colors">
                  <td className="p-4 text-white font-bold">{item.domain_or_url}</td>
                  <td className="p-4 text-cyber-danger">{item.threat_type}</td>
                  <td className="p-4 text-cyber-warning">{(item.confidence_score * 100).toFixed(0)}%</td>
                  <td className="p-4 text-cyber-muted">{item.source}</td>
                  <td className="p-4">
                    <span className="px-2 py-1 bg-cyber-danger text-black text-[10px] font-bold">
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
              {feed.length === 0 && !loading && (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-cyber-muted uppercase tracking-widest">
                    NO_THREATS_DETECTED // SYSTEM_SECURE
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
