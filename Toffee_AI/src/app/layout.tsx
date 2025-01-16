import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import React from 'react';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Toffee.ai - AI-Powered Networking Assistant",
  description: "Prepare for meaningful coffee catchups and networking events with AI-generated insights and questions.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="min-h-screen bg-gradient-to-b from-amber-50 to-white">
          {children}
        </main>
      </body>
    </html>
  );
} 