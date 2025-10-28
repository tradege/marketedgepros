import React from 'react';
import LandingNavbar from './LandingNavbar';
import LandingFooter from './LandingFooter';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-black text-white">
      <LandingNavbar />
      <main className="flex-grow pt-16">
        {children}
      </main>
      <LandingFooter />
    </div>
  );
}

