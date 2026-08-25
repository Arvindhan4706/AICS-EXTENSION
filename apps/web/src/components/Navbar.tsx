"use client";

import { Bell, Search, ShieldCheck } from "lucide-react";

export default function Navbar() {
  return (
    <header className="h-16 bg-cyber-bg border-b border-cyber-border px-6 flex items-center justify-between font-mono">
      <div className="flex items-center gap-4 w-96">
        <div className="relative w-full flex items-center">
          <span className="text-cyber-accent mr-2">{">"}</span>
          <input
            type="text"
            placeholder="Search IP, URL, Domain, or Hash..."
            className="w-full bg-transparent border-b border-cyber-border py-1.5 text-sm text-cyber-accent placeholder:text-cyber-muted focus:outline-none focus:border-cyber-accent transition-colors"
          />
          <div className="w-2 h-4 bg-cyber-accent animate-pulse ml-1 opacity-50"></div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1 bg-transparent border border-cyber-accent text-cyber-accent text-xs font-mono uppercase tracking-widest">
          <ShieldCheck className="w-3.5 h-3.5" />
          SYS_GUARD: ON
        </div>

        <button className="relative p-2 text-cyber-muted hover:text-cyber-accent transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-cyber-danger"></span>
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-cyber-border">
          <div className="w-8 h-8 border border-cyber-accent flex items-center justify-center text-cyber-accent font-bold text-sm bg-cyber-accent/10">
            A
          </div>
          <div className="text-left text-xs uppercase tracking-widest">
            <div className="text-white font-bold">ROOT_ADMIN</div>
            <div className="text-cyber-accent opacity-80 text-[10px]">Lvl 9 Access</div>
          </div>
        </div>
      </div>
    </header>
  );
}
