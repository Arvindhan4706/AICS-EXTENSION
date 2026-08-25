"use client";

import { useState, useEffect } from "react";
import { 
  ShieldAlert, 
  ShieldCheck, 
  Activity, 
  Globe, 
  Zap, 
  TrendingUp, 
  ExternalLink 
} from "lucide-react";
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from "recharts";
import Link from "next/link";

const RISK_COLORS = {
  CRITICAL: "#ff003c",
  HIGH: "#ffb000",
  MEDIUM: "#ffb000",
  LOW: "#00ff41"
};

export default function SOCDashboardPage() {
  const [stats, setStats] = useState({
    total_scans: 0,
    today_scans: 0,
    threats_detected: 0,
    safety_rate_percentage: 100,
    avg_scan_latency_ms: 0,
    risk_level_distribution: { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 },
    top_dangerous_categories: []
  });

  const [recentScans, setRecentScans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const statsRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || '/api/v1'}/scan/stats`);
        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setStats(statsData);
        }
        
        const historyRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || '/api/v1'}/scan/history?limit=5`);
        if (historyRes.ok) {
          const historyData = await historyRes.json();
          setRecentScans(historyData);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  const pieData = Object.keys(stats.risk_level_distribution).map((level) => ({
    name: level,
    value: stats.risk_level_distribution[level as keyof typeof stats.risk_level_distribution] || 0
  }));

  return (
    <div className="space-y-6 font-mono">
      {/* Top Banner Quick Scan Bar */}
      <div className="bg-cyber-bg border border-cyber-accent p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
              <Zap className="w-5 h-5 text-cyber-accent" />
              TACTICAL_SOC_COMMAND
            </h2>
            <p className="text-xs text-cyber-muted uppercase tracking-widest border-l-2 border-cyber-accent pl-2">
              Inspect suspicious URLs, fake login pages, homograph attacks, and credential portals instantly.
            </p>
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <Link
              href="/scan"
              className="bg-transparent hover:bg-cyber-accent hover:text-black text-cyber-accent border border-cyber-accent font-bold px-6 py-2 transition-all flex items-center gap-2 whitespace-nowrap uppercase tracking-widest text-xs"
            >
              <Globe className="w-4 h-4" />
              [ EXEC_DEEP_SCAN ]
            </Link>
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-cyber-card border border-cyber-border p-5 hover:border-cyber-accent transition-colors">
          <div className="flex items-center justify-between text-cyber-muted mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-cyber-accent">TOTAL_REQ_PROCESSED</span>
            <Activity className="w-4 h-4 text-cyber-accent" />
          </div>
          <div className="text-3xl font-bold text-white">{stats.total_scans.toLocaleString()}</div>
          <div className="text-[10px] text-cyber-accent mt-2 flex items-center gap-1 font-mono uppercase tracking-widest">
            <TrendingUp className="w-3.5 h-3.5" />
            +{stats.today_scans} IN_CURRENT_CYCLE
          </div>
        </div>

        <div className="bg-cyber-card border border-cyber-border p-5 hover:border-cyber-danger transition-colors">
          <div className="flex items-center justify-between text-cyber-muted mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-cyber-danger">THREATS_NEUTRALIZED</span>
            <ShieldAlert className="w-4 h-4 text-cyber-danger" />
          </div>
          <div className="text-3xl font-bold text-cyber-danger">{stats.threats_detected}</div>
          <div className="text-[10px] text-cyber-danger mt-2 font-mono uppercase tracking-widest">
            CRITICAL_HIGH_RISK_LOGS
          </div>
        </div>

        <div className="bg-cyber-card border border-cyber-border p-5 hover:border-cyber-accent transition-colors">
          <div className="flex items-center justify-between text-cyber-muted mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-cyber-accent">SYS_PROTECTION_RATE</span>
            <ShieldCheck className="w-4 h-4 text-cyber-accent" />
          </div>
          <div className="text-3xl font-bold text-cyber-accent">{stats.safety_rate_percentage}%</div>
          <div className="text-[10px] text-cyber-muted mt-2 font-mono uppercase tracking-widest">
            MODEL_STATUS: ENSEMBLE_ACTIVE
          </div>
        </div>

        <div className="bg-cyber-card border border-cyber-border p-5 hover:border-cyber-warning transition-colors">
          <div className="flex items-center justify-between text-cyber-muted mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-cyber-warning">AVG_EXTRACT_LATENCY</span>
            <Zap className="w-4 h-4 text-cyber-warning" />
          </div>
          <div className="text-3xl font-bold text-cyber-warning">{stats.avg_scan_latency_ms || 45}ms</div>
          <div className="text-[10px] text-cyber-muted mt-2 font-mono uppercase tracking-widest">
            INVARIANT_VECTORS_ACTIVE
          </div>
        </div>
      </div>

      {/* Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-cyber-card border border-cyber-border p-6 lg:col-span-1">
          <h3 className="text-sm font-bold text-white mb-1 uppercase tracking-widest border-b border-cyber-border pb-2">THREAT_DISTRIBUTION</h3>
          <p className="text-[10px] text-cyber-muted mb-4 uppercase tracking-widest mt-2">Risk classification matrix</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={2}
                  dataKey="value"
                  stroke="none"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.name as keyof typeof RISK_COLORS]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: "#050505", border: "1px solid #333333", borderRadius: "0", fontFamily: "monospace", textTransform: "uppercase" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 text-[10px] pt-2 uppercase tracking-widest">
            {Object.keys(RISK_COLORS).map((level) => (
              <div key={level} className="flex items-center gap-2 text-cyber-muted">
                <span className="w-2 h-2" style={{ backgroundColor: RISK_COLORS[level as keyof typeof RISK_COLORS] }}></span>
                <span>{level} [{stats.risk_level_distribution[level as keyof typeof stats.risk_level_distribution]}]</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-cyber-card border border-cyber-border p-6 lg:col-span-2">
          <h3 className="text-sm font-bold text-white mb-1 uppercase tracking-widest border-b border-cyber-border pb-2">TOP_ATTACK_VECTORS</h3>
          <p className="text-[10px] text-cyber-muted mb-4 uppercase tracking-widest mt-2">Prevalent phishing classifications</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.top_dangerous_categories} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="2 2" stroke="#333333" vertical={false} />
                <XAxis dataKey="category" stroke="#666666" tick={{ fontSize: 9, fontFamily: 'monospace' }} tickLine={false} axisLine={false} />
                <YAxis stroke="#666666" tick={{ fontSize: 9, fontFamily: 'monospace' }} tickLine={false} axisLine={false} />
                <Tooltip cursor={{fill: '#333333', opacity: 0.4}} contentStyle={{ backgroundColor: "#050505", border: "1px solid #00ff41", borderRadius: "0", fontFamily: "monospace", textTransform: "uppercase" }} />
                <Bar dataKey="count" fill="#00ff41" radius={0} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Live Recent Threat Activity Table */}
      <div className="bg-cyber-card border border-cyber-border p-6">
        <div className="flex items-center justify-between mb-4 border-b border-cyber-border pb-2">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-widest">LIVE_THREAT_ACTIVITY_LOG</h3>
            <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">Real-time scan intercepts from network</p>
          </div>
          <Link href="/scan" className="text-[10px] text-cyber-accent hover:underline flex items-center gap-1 uppercase tracking-widest">
            [ VIEW_ALL_LOGS ] <ExternalLink className="w-3 h-3" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-[11px] uppercase tracking-wider">
            <thead className="bg-cyber-bg text-cyber-muted">
              <tr>
                <th className="p-3 border-b border-cyber-border font-normal">TARGET_URL</th>
                <th className="p-3 border-b border-cyber-border font-normal">THREAT_SCORE</th>
                <th className="p-3 border-b border-cyber-border font-normal">RISK_LVL</th>
                <th className="p-3 border-b border-cyber-border font-normal">CLASSIFICATION</th>
                <th className="p-3 border-b border-cyber-border font-normal">TIMESTAMP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-border">
              {recentScans.map((item) => (
                <tr key={item.id} className="hover:bg-cyber-border/30 transition-colors">
                  <td className="p-3 text-white max-w-xs truncate">{item.target_url}</td>
                  <td className="p-3 font-bold">
                    <span className={item.threat_score > 70 ? "text-cyber-danger" : item.threat_score > 40 ? "text-cyber-warning" : "text-cyber-accent"}>
                      {item.threat_score}/100
                    </span>
                  </td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 font-bold ${
                      item.risk_level === "CRITICAL" ? "bg-cyber-danger text-black" :
                      item.risk_level === "HIGH" ? "bg-cyber-warning text-black" :
                      item.risk_level === "MEDIUM" ? "bg-cyber-warning text-black" :
                      "bg-cyber-accent text-black"
                    }`}>
                      {item.risk_level}
                    </span>
                  </td>
                  <td className="p-3 text-cyber-muted">{item.category}</td>
                  <td className="p-3 text-cyber-muted opacity-60">{new Date(item.created_at).toLocaleTimeString()}</td>
                </tr>
              ))}
              {recentScans.length === 0 && !loading && (
                <tr>
                  <td colSpan={5} className="p-6 text-center text-cyber-muted uppercase tracking-widest">
                    NO_ACTIVITY_LOGGED
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
