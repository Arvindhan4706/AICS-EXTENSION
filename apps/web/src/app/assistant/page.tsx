"use client";

import { useState } from "react";
import { Bot, Send, User, Shield, TerminalSquare } from "lucide-react";

export default function AssistantPage() {
  const [messages, setMessages] = useState<any[]>([
    {
      sender: "ai",
      text: "HELLO! I AM CYBER_SHIELD_AI_SENTINEL. ASK ME ANYTHING ABOUT PHISHING DETECTION, HOMOGRAPH ATTACKS, EMAIL HEADER VALIDATION, OR SUSPICIOUS URL MITIGATION STRATEGIES."
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setMessages((prev) => [...prev, { sender: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/assistant/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg })
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { sender: "ai", text: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "ai", text: "ERROR_CONNECTING_TO_AI_ASSISTANT_SERVER" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-4 h-[calc(100vh-8rem)] flex flex-col font-mono">
      <div className="border-l-4 border-cyber-accent pl-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 uppercase tracking-widest">
          <Bot className="w-6 h-6 text-cyber-accent" />
          AI_SENTINEL // RAG_ASSISTANT
        </h1>
        <p className="text-[10px] text-cyber-muted uppercase tracking-widest mt-1">
          Interactive security knowledge advisor for incident resolution and threat mitigation guidance.
        </p>
      </div>

      <div className="flex-1 bg-cyber-bg border border-cyber-border p-4 flex flex-col justify-between overflow-hidden relative">
        <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-accent/5 rounded-full blur-3xl"></div>
        
        <div className="flex-1 overflow-y-auto space-y-4 p-2 custom-scrollbar relative z-10">
          {messages.map((m, i) => (
            <div key={i} className={`flex items-start gap-3 ${m.sender === "user" ? "flex-row-reverse" : ""}`}>
              <div className={`w-8 h-8 flex items-center justify-center shrink-0 border ${
                m.sender === "user" ? "bg-cyber-bg border-cyber-accent text-cyber-accent" : "bg-cyber-bg border-cyber-danger text-cyber-danger"
              }`}>
                {m.sender === "user" ? <User className="w-4 h-4" /> : <Shield className="w-4 h-4" />}
              </div>
              <div className={`max-w-lg p-3.5 text-[11px] uppercase tracking-widest leading-relaxed border ${
                m.sender === "user" ? "bg-cyber-accent/10 border-cyber-accent/30 text-cyber-accent" : "bg-cyber-bg border-cyber-border text-gray-300"
              }`}>
                {m.sender === "ai" && <div className="text-cyber-danger font-bold mb-1 border-b border-cyber-border pb-1">AI_RESPONSE:</div>}
                {m.sender === "user" && <div className="text-cyber-accent font-bold mb-1 border-b border-cyber-accent/30 pb-1">USER_QUERY:</div>}
                {m.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-[10px] text-cyber-muted italic animate-pulse flex items-center gap-2 uppercase tracking-widest">
              <span className="w-2 h-2 bg-cyber-accent rounded-full animate-bounce"></span>
              COMPILING_RESPONSE...
            </div>
          )}
        </div>

        <form onSubmit={handleSend} className="pt-4 border-t border-cyber-border flex gap-3 relative z-10">
          <div className="flex-1 flex items-center border border-cyber-border bg-cyber-bg px-3">
            <span className="text-cyber-accent mr-2">{">"}</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="ENTER QUERY..."
              className="w-full bg-transparent py-3 text-[11px] text-cyber-accent placeholder:text-cyber-muted focus:outline-none uppercase tracking-widest"
            />
          </div>
          <button
            type="submit"
            className="bg-transparent hover:bg-cyber-accent hover:text-black text-cyber-accent border border-cyber-accent px-4 transition-all flex items-center justify-center uppercase tracking-widest"
          >
            <TerminalSquare className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
