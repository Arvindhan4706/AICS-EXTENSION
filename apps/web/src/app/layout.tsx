import "./globals.css";
import { Share_Tech_Mono } from 'next/font/google';
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";

const shareTechMono = Share_Tech_Mono({ 
  weight: '400',
  subsets: ['latin'],
  variable: '--font-share-tech-mono'
});

export const metadata = {
  title: "CyberShield AI - Tactical Interface",
  description: "Raw Terminal-based Threat Detection",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${shareTechMono.variable}`}>
      <body className="bg-cyber-bg text-cyber-text antialiased font-mono">
        <div className="crt-overlay"></div>
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1 flex flex-col min-w-0">
            <Navbar />
            <main className="flex-1 p-6 overflow-y-auto">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
