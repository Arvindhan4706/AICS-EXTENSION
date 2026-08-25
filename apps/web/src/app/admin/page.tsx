"use client";

import { useState } from "react";
import { Settings, Cpu, ShieldAlert, Plus, TerminalSquare } from "lucide-react";

export default function AdminPage() {
  const [retrainStatus, setRetrainStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [ruleEntry, setRuleEntry] = useState("");

  const triggerRetraining = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/admin/retrain-models`, { method: "POST" });
      const data = await res.json();
      alert(data.message || "Model retraining initiated!");
    } catch (err) {
      console.error(err);
      alert("Failed to retrain models.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddRule = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ruleEntry) return;
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/admin/rules`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entry: ruleEntry, list_type: "BLACKLIST" })
      });
      alert(`BLACKLIST_RULE_ADDED: [${ruleEntry}]`);
      setRuleEntry("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <Settings className="w-6 h-6 text-cyber-accent" />
          ROOT_ACCESS // ML_OPERATIONS
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Manage system rules, blacklists, user access, and trigger automated machine learning ensemble retraining.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4 hover:border-cyber-accent transition-colors">
          <h3 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-widest border-b border-cyber-border pb-2">
            <Cpu className="w-5 h-5 text-cyber-accent" />
            ML_MODEL_RETRAINING_PIPELINE
          </h3>
          <p className="text-[10px] text-cyber-muted uppercase tracking-widest">
            Re-fit Random Forest, Gradient Boosting, and Decision Tree ensemble classifiers using newly ingested threat logs.
          </p>

          <button
            onClick={triggerRetraining}
            disabled={loading}
            className="w-full bg-transparent border border-cyber-accent hover:bg-cyber-accent hover:text-black text-cyber-accent font-bold py-3 transition-all flex justify-center items-center gap-2 disabled:opacity-50 uppercase tracking-widest text-xs"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 border-2 border-cyber-accent border-t-transparent rounded-full animate-spin"></span>
                COMPILING_WEIGHTS...
              </span>
            ) : (
              <>
                <TerminalSquare className="w-4 h-4" />
                [ EXEC_MODEL_RETRAIN ]
              </>
            )}
          </button>

          {retrainStatus && (
            <div className="p-4 bg-cyber-card border-l-2 border-cyber-accent space-y-2 text-[10px] font-mono uppercase tracking-widest">
              <div className="text-cyber-accent font-bold flex items-center gap-2">
                <span className="text-cyber-accent">{">"}</span>
                {retrainStatus.message}
              </div>
              <div className="text-cyber-muted pl-4 border-l border-cyber-border mt-2 space-y-1">
                <div>RANDOM_FOREST_F1: <span className="text-white">{retrainStatus.metrics.random_forest_accuracy}</span></div>
                <div>GRADIENT_BOOST_F1: <span className="text-white">{retrainStatus.metrics.gradient_boosting_accuracy}</span></div>
                <div className="text-cyber-accent font-bold mt-2 pt-2 border-t border-cyber-border/50">ENSEMBLE_F1_SCORE: {retrainStatus.metrics.f1_score}</div>
              </div>
            </div>
          )}
        </div>

        <div className="bg-cyber-bg border border-cyber-border p-6 space-y-4 hover:border-cyber-danger transition-colors">
          <h3 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-widest border-b border-cyber-border pb-2">
            <ShieldAlert className="w-5 h-5 text-cyber-danger" />
            EXPLICIT_THREAT_BLACKLIST
          </h3>
          <p className="text-[10px] text-cyber-muted uppercase tracking-widest">
            Add hard override domains or IP addresses to immediately block access across backend and extension.
          </p>

          <form onSubmit={handleAddRule} className="space-y-3">
            <div className="flex items-center border border-cyber-border">
              <span className="pl-3 text-cyber-danger">{">"}</span>
              <input
                type="text"
                value={ruleEntry}
                onChange={(e) => setRuleEntry(e.target.value)}
                placeholder="TARGET_IP_OR_DOMAIN"
                className="w-full bg-transparent px-3 py-3 text-[11px] text-cyber-danger placeholder:text-cyber-muted focus:outline-none focus:border-cyber-danger font-mono uppercase tracking-widest"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-transparent border border-cyber-danger hover:bg-cyber-danger hover:text-black text-cyber-danger font-bold py-3 transition-all flex items-center justify-center gap-2 uppercase tracking-widest text-xs"
            >
              <Plus className="w-4 h-4" />
              [ APPEND_BLACKLIST ]
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
