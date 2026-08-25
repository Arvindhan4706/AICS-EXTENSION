"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Globe, 
  Mail, 
  QrCode, 
  Radio, 
  KeyRound, 
  Bot, 
  Settings, 
  FileCheck,
  Home
} from "lucide-react";

const navItems = [
  { name: "ROOT_ACCESS", href: "/", icon: Home },
  { name: "SOC_DASHBOARD", href: "/dashboard", icon: LayoutDashboard },
  { name: "URL_SCANNER", href: "/scan", icon: Globe },
  { name: "EML_SCANNER", href: "/email-scan", icon: Mail },
  { name: "QR_DECODER", href: "/qr-scan", icon: QrCode },
  { name: "THREAT_FEEDS", href: "/threat-feed", icon: Radio },
  { name: "PWD_LEAK_CHK", href: "/password-check", icon: KeyRound },
  { name: "AI_ASSISTANT", href: "/assistant", icon: Bot },
  { name: "SYS_ADMIN", href: "/admin", icon: Settings },
  { name: "SYS_REPORTS", href: "/reports", icon: FileCheck },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-cyber-bg border-r border-cyber-border min-h-screen flex flex-col justify-between p-4 shrink-0 font-mono">
      <div>
        <div className="flex items-center gap-3 px-2 py-4 mb-6 border-b border-cyber-accent/30">
          <div className="p-2 text-cyber-accent border border-cyber-accent/50 bg-cyber-accent/5">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-white tracking-widest flex items-center gap-1.5 uppercase">
              CYBER_SHIELD <span className="bg-cyber-accent text-black text-xs px-1.5 py-0.5 font-bold animate-pulse">v2.0</span>
            </h1>
            <p className="text-[10px] text-cyber-accent uppercase tracking-widest opacity-80">Terminal Sentinel</p>
          </div>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 text-sm font-medium transition-all uppercase border-l-2 ${
                  isActive
                    ? "border-cyber-accent bg-cyber-accent/10 text-cyber-accent"
                    : "border-transparent text-cyber-muted hover:text-white hover:border-cyber-border hover:bg-cyber-card"
                }`}
              >
                <Icon className="w-4 h-4" />
                {isActive ? `> ${item.name}` : `  ${item.name}`}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-3 bg-cyber-card border border-cyber-border">
        <div className="flex items-center justify-between text-xs text-cyber-muted mb-1 uppercase tracking-widest">
          <span>SYS_STATUS</span>
          <span className="text-cyber-accent font-bold flex items-center gap-2">
            <span className="w-2 h-2 bg-cyber-accent animate-ping"></span>
            ONLINE
          </span>
        </div>
        <div className="text-[10px] text-cyber-muted font-mono uppercase">
          MODELS_ACTIVE: RF,XGB,LGBM
        </div>
      </div>
    </aside>
  );
}
