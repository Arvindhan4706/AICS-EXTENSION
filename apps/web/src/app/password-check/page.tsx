"use client";

import { useState } from "react";
import { KeyRound, CheckCircle2, Lock, TerminalSquare } from "lucide-react";

export default function PasswordCheckPage() {
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleCheck = async () => {
    if (!password) return;
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/assistant/password-check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: password })
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
    <div className="space-y-6 max-w-5xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <KeyRound className="w-6 h-6 text-cyber-accent" />
          CRYPTOGRAPHIC_KEY_INSPECTOR // LEAK_CHECK
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Check if your password has been exposed in public data breach dumps using k-Anonymity privacy hashing.
        </p>
      </div>

      <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        <label className="text-[10px] font-bold text-cyber-muted uppercase tracking-widest flex items-center gap-2">
          <span className="text-cyber-accent">{">"}</span> INPUT_CREDENTIAL_KEY
        </label>
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-cyber-muted" />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="ENTER STRING..."
              className="w-full bg-transparent border border-cyber-border pl-10 pr-4 py-3 font-mono text-xs text-cyber-accent focus:outline-none focus:border-cyber-accent uppercase tracking-widest"
            />
          </div>
          <button
            onClick={handleCheck}
            disabled={loading}
            className="bg-transparent hover:bg-cyber-accent hover:text-black text-cyber-accent border border-cyber-accent font-bold px-6 py-2 transition-all flex items-center justify-center gap-2 disabled:opacity-50 uppercase tracking-widest text-xs"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 border-2 border-cyber-accent border-t-transparent rounded-full animate-spin"></span>
                QUERYING_DB...
              </span>
            ) : (
              <>
                <TerminalSquare className="w-4 h-4" />
                [ EXEC_VERIFY ]
              </>
            )}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-cyber-card border border-cyber-border p-6 space-y-6 animate-in fade-in zoom-in duration-300">
          <div className="flex items-center justify-between border-b border-cyber-border pb-4">
            <div>
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">BREACH_STATUS</div>
              <div className={result.is_leaked ? "text-xl font-bold text-cyber-danger mt-1 uppercase" : "text-xl font-bold text-cyber-accent mt-1 uppercase"}>
                {result.is_leaked ? `[ COMPROMISED ] (${result.leak_count.toLocaleString()} HITS)` : "[ SAFE_NO_LEAKS_FOUND ]"}
              </div>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-cyber-muted uppercase tracking-widest">ENTROPY_STRENGTH</div>
              <div className={`text-3xl font-bold font-mono mt-1 ${result.strength_score < 50 ? 'text-cyber-danger' : result.strength_score < 80 ? 'text-cyber-warning' : 'text-cyber-accent'}`}>
                {result.strength_score}/100
              </div>
            </div>
          </div>

          <div className="p-4 bg-cyber-bg border border-cyber-border space-y-3">
            <h4 className="text-[10px] font-bold text-cyber-muted uppercase tracking-widest">SYSTEM_RECOMMENDATIONS</h4>
            <ul className="space-y-2 text-[10px] text-cyber-muted uppercase tracking-wider">
              {result.recommendations.map((rec: string, i: number) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-cyber-accent font-bold">{">"}</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
