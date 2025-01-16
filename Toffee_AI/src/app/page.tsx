'use client';
import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-amber-800 mb-6">
          Welcome to Toffee.ai
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Your AI assistant for meaningful networking conversations
        </p>
        <Link 
          href="/prepare"
          className="bg-amber-600 text-white px-8 py-3 rounded-full hover:bg-amber-700 transition"
        >
          Prepare for Your Meeting
        </Link>
      </div>
    </div>
  );
} 