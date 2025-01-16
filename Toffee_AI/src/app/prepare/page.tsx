'use client';
import React, { useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';

export default function PrepareMeeting() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    linkedInUrl: '',
    purpose: '',
    meetingDate: '',
    meetingPlace: '',
  });

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (!session) {
    return (
      <div className="text-center py-10">
        <p className="mb-4">Please sign in to prepare for your meeting</p>
        <button
          onClick={() => router.push('/api/auth/signin')}
          className="bg-amber-600 text-white px-6 py-2 rounded-full"
        >
          Sign In
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold text-amber-800 mb-8">
        Prepare for Your Meeting
      </h1>
      
      {/* Form implementation will go here */}
      
    </div>
  );
} 