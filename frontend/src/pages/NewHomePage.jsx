import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/layout/Layout';

const NewHomePage = () => {
  const [programs, setPrograms] = useState([]);
  const [selectedPhase, setSelectedPhase] = useState('two');
  const [stats, setStats] = useState({
    countries: 0,
    capital: 0,
    traders: 0,
    profitSplit: 0
  });
  const [imagesLoaded, setImagesLoaded] = useState(false);

  const heroRef = useRef(null);
  const statsRef = useRef(null);

  // Preload images
  useEffect(() => {
    const images = [
      '/images/abstract-trading-flow.png',
      '/images/hero-trading-3d.png',
      '/images/stats-globe-hologram.png'
    ];
    
    let loadedCount = 0;
    images.forEach(src => {
      const img = new Image();
      img.onload = () => {
        loadedCount++;
        if (loadedCount === images.length) {
          setImagesLoaded(true);
        }
      };
      img.src = src;
    });
  }, []);

  // Fetch programs
  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/programs`);
        const apiPrograms = Array.isArray(response.data) ? response.data : [];
        
        // If API returns empty, use static fallback
        if (apiPrograms.length === 0) {
          setPrograms([
            // One Phase
            { id: 1, account_size: 10000, profit_target: 8, max_daily_loss: 5, profit_split: 80, phases: 1 },
            { id: 2, account_size: 25000, profit_target: 8, max_daily_loss: 5, profit_split: 80, phases: 1 },
            { id: 3, account_size: 50000, profit_target: 8, max_daily_loss: 5, profit_split: 85, phases: 1 },
            { id: 4, account_size: 100000, profit_target: 8, max_daily_loss: 5, profit_split: 90, phases: 1 },
            // Two Phase
            { id: 5, account_size: 10000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
            { id: 6, account_size: 25000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
            { id: 7, account_size: 50000, profit_target: 10, max_daily_loss: 5, profit_split: 85, phases: 2 },
            { id: 8, account_size: 100000, profit_target: 10, max_daily_loss: 5, profit_split: 90, phases: 2 },
            // Three Phase
            { id: 9, account_size: 10000, profit_target: 12, max_daily_loss: 4, profit_split: 75, phases: 3 },
            { id: 10, account_size: 25000, profit_target: 12, max_daily_loss: 4, profit_split: 75, phases: 3 },
            { id: 11, account_size: 50000, profit_target: 12, max_daily_loss: 4, profit_split: 80, phases: 3 },
            { id: 12, account_size: 100000, profit_target: 12, max_daily_loss: 4, profit_split: 85, phases: 3 },
            // Instant Funding
            { id: 13, account_size: 5000, profit_target: 0, max_daily_loss: 3, profit_split: 50, instant_funding: true },
            { id: 14, account_size: 10000, profit_target: 0, max_daily_loss: 3, profit_split: 50, instant_funding: true },
            { id: 15, account_size: 25000, profit_target: 0, max_daily_loss: 3, profit_split: 60, instant_funding: true },
            { id: 16, account_size: 50000, profit_target: 0, max_daily_loss: 3, profit_split: 70, instant_funding: true },
          ]);
        } else {
          setPrograms(apiPrograms);
        }
      } catch (error) {
        console.error('Error fetching programs:', error);
        // Fallback to static programs on error
        setPrograms([
          // One Phase
          { id: 1, account_size: 10000, profit_target: 8, max_daily_loss: 5, profit_split: 80, phases: 1 },
          { id: 2, account_size: 25000, profit_target: 8, max_daily_loss: 5, profit_split: 80, phases: 1 },
          { id: 3, account_size: 50000, profit_target: 8, max_daily_loss: 5, profit_split: 85, phases: 1 },
          { id: 4, account_size: 100000, profit_target: 8, max_daily_loss: 5, profit_split: 90, phases: 1 },
          // Two Phase
          { id: 5, account_size: 10000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
          { id: 6, account_size: 25000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
          { id: 7, account_size: 50000, profit_target: 10, max_daily_loss: 5, profit_split: 85, phases: 2 },
          { id: 8, account_size: 100000, profit_target: 10, max_daily_loss: 5, profit_split: 90, phases: 2 },
          // Three Phase
          { id: 9, account_size: 10000, profit_target: 12, max_daily_loss: 4, profit_split: 75, phases: 3 },
          { id: 10, account_size: 25000, profit_target: 12, max_daily_loss: 4, profit_split: 75, phases: 3 },
          { id: 11, account_size: 50000, profit_target: 12, max_daily_loss: 4, profit_split: 80, phases: 3 },
          { id: 12, account_size: 100000, profit_target: 12, max_daily_loss: 4, profit_split: 85, phases: 3 },
          // Instant Funding
          { id: 13, account_size: 5000, profit_target: 0, max_daily_loss: 3, profit_split: 50, instant_funding: true },
          { id: 14, account_size: 10000, profit_target: 0, max_daily_loss: 3, profit_split: 50, instant_funding: true },
          { id: 15, account_size: 25000, profit_target: 0, max_daily_loss: 3, profit_split: 60, instant_funding: true },
          { id: 16, account_size: 50000, profit_target: 0, max_daily_loss: 3, profit_split: 70, instant_funding: true },
        ]);
      }
    };
    fetchPrograms();
  }, []);

  // Animated counter
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateStats();
          }
        });
      },
      { threshold: 0.5 }
    );

    if (statsRef.current) {
      observer.observe(statsRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const animateStats = () => {
    const duration = 2000;
    const steps = 60;
    const stepDuration = duration / steps;

    const targets = {
      countries: 200,
      capital: 10,
      traders: 5000,
      profitSplit: 90
    };

    let currentStep = 0;

    const interval = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;

      setStats({
        countries: Math.floor(targets.countries * progress),
        capital: Math.floor(targets.capital * progress),
        traders: Math.floor(targets.traders * progress),
        profitSplit: Math.floor(targets.profitSplit * progress)
      });

      if (currentStep >= steps) {
        clearInterval(interval);
        setStats(targets);
      }
    }, stepDuration);
  };

  const filteredPrograms = Array.isArray(programs) ? programs.filter(p => {
    if (selectedPhase === 'one') return p.phases === 1;
    if (selectedPhase === 'two') return p.phases === 2;
    if (selectedPhase === 'three') return p.phases === 3;
    if (selectedPhase === 'instant') return p.instant_funding;
    return false;
  }) : [];

  return (
    <Layout>
      <div className="min-h-screen overflow-hidden scroll-smooth">
        
        {/* Hero Section */}
        <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 z-0">
            <img 
              src="/images/abstract-trading-flow.png" 
              alt="" 
              loading="eager"
              className="w-full h-full object-cover opacity-30"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black"></div>
          </div>

          {/* 3D Trading Screens - Floating */}
          <div className="absolute inset-0 z-10 pointer-events-none">
            <img 
              src="/images/hero-trading-3d.png" 
              alt="" 
              loading="eager"
              className="absolute top-1/4 left-1/4 w-96 h-auto opacity-60 animate-float"
            />
          </div>

          {/* Content */}
          <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            
            {/* Main Heading */}
            <h1 className="text-6xl md:text-8xl font-bold mb-8 leading-tight">
              Where <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 animate-gradient-shift">Talent</span>
              <br />
              Meets <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 animate-gradient-shift">Capital</span>
            </h1>

            {/* Subheading */}
            <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
              Trade with up to <span className="text-cyan-400 font-bold">$400,000</span> in capital.
              Keep up to <span className="text-purple-400 font-bold">90%</span> of your profits.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <Link
                to="/programs"
                className="group relative px-12 py-5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-lg font-bold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50"
              >
                <span className="relative z-10">Get Funded Now</span>
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-600 to-teal-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </Link>
              
              <Link
                to="/free-course"
                className="px-12 py-5 border-2 border-white/20 rounded-full text-lg font-semibold backdrop-blur-sm hover:bg-white/10 transition-all duration-300"
              >
                Start Free Course
              </Link>
            </div>

            {/* Trust Indicators */}
            <div className="mt-16 flex flex-wrap items-center justify-center gap-8 text-sm text-gray-400">
              <div className="flex items-center gap-2">
                <span className="text-2xl">✓</span>
                <span>Instant Payouts</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">✓</span>
                <span>No Time Limits</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">✓</span>
                <span>Trade Your Way</span>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section ref={statsRef} className="relative py-32 overflow-hidden">
          {/* Background */}
          <div className="absolute inset-0 z-0">
            <img 
              src="/images/stats-globe-hologram.png" 
              alt="" 
              className="w-full h-full object-cover opacity-20"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black"></div>
          </div>

          {/* Content */}
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {/* Stat 1 */}
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-2">
                  {stats.countries}+
                </div>
                <div className="text-gray-400 text-lg">Countries</div>
              </div>

              {/* Stat 2 */}
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
                  ${stats.capital}M+
                </div>
                <div className="text-gray-400 text-lg">Capital Funded</div>
              </div>

              {/* Stat 3 */}
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-2">
                  {stats.traders}+
                </div>
                <div className="text-gray-400 text-lg">Active Traders</div>
              </div>

              {/* Stat 4 */}
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-2">
                  {stats.profitSplit}%
                </div>
                <div className="text-gray-400 text-lg">Profit Split</div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how-it-works" className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                How It <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Works</span>
              </h2>
              <p className="text-xl text-gray-400 max-w-3xl mx-auto">
                Get funded in 3 simple steps and start trading with our capital
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              {/* Step 1 */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-teal-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 transition-all duration-300 hover:scale-105">
                  <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-6">01</div>
                  <h3 className="text-2xl font-bold mb-4">Choose Your Challenge</h3>
                  <p className="text-gray-400">
                    Select from our range of funding programs. From $10K to $400K accounts.
                  </p>
                </div>
              </div>

              {/* Step 2 */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 transition-all duration-300 hover:scale-105">
                  <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-6">02</div>
                  <h3 className="text-2xl font-bold mb-4">Pass The Evaluation</h3>
                  <p className="text-gray-400">
                    Trade and hit the profit targets while following our simple rules.
                  </p>
                </div>
              </div>

              {/* Step 3 */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 transition-all duration-300 hover:scale-105">
                  <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-6">03</div>
                  <h3 className="text-2xl font-bold mb-4">Get Funded & Trade</h3>
                  <p className="text-gray-400">
                    Receive your funded account and keep up to 90% of your profits.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Programs Section */}
        <section id="programs" className="relative py-32 bg-gradient-to-b from-transparent via-white/5 to-transparent">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Choose Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Challenge</span>
              </h2>
            </div>

            {/* Phase Tabs */}
            <div className="flex flex-wrap justify-center gap-4 mb-16">
              <button
                onClick={() => setSelectedPhase('one')}
                className={`px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ${
                  selectedPhase === 'one'
                    ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white shadow-2xl shadow-cyan-500/50'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                1️⃣ One Phase
              </button>
              <button
                onClick={() => setSelectedPhase('two')}
                className={`px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ${
                  selectedPhase === 'two'
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl shadow-purple-500/50'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                2️⃣ Two Phase
              </button>
              <button
                onClick={() => setSelectedPhase('three')}
                className={`px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ${
                  selectedPhase === 'three'
                    ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-2xl shadow-orange-500/50'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                3️⃣ Three Phase
              </button>
              <button
                onClick={() => setSelectedPhase('instant')}
                className={`px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ${
                  selectedPhase === 'instant'
                    ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-2xl shadow-blue-500/50'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                4️⃣ Instant Funding
              </button>
            </div>

            {/* Programs Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {filteredPrograms.map((program) => (
                <div
                  key={program.id}
                  className="group relative bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/30"
                >
                  <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-4">
                    ${(program.account_size / 1000).toFixed(0)}K
                  </div>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Profit Target:</span>
                      <span className="text-white font-semibold">{program.profit_target}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Max Daily Loss:</span>
                      <span className="text-white font-semibold">{program.max_daily_loss}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Profit Split:</span>
                      <span className="text-cyan-400 font-bold">{program.profit_split}%</span>
                    </div>
                  </div>
                  <Link
                    to={`/programs/${program.id}`}
                    className="mt-6 block w-full py-3 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-center font-semibold transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/50"
                  >
                    Get Started
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Why Choose <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Us</span>
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">⚡</div>
                <h3 className="text-2xl font-bold mb-4">Instant Payouts</h3>
                <p className="text-gray-400">
                  Request payouts anytime. Get paid within 24 hours.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">🎯</div>
                <h3 className="text-2xl font-bold mb-4">No Time Limits</h3>
                <p className="text-gray-400">
                  Trade at your own pace. No pressure, no deadlines.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">📈</div>
                <h3 className="text-2xl font-bold mb-4">Scale Your Account</h3>
                <p className="text-gray-400">
                  Grow your account up to $400K based on performance.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">🛡️</div>
                <h3 className="text-2xl font-bold mb-4">Simple Rules</h3>
                <p className="text-gray-400">
                  Clear, straightforward rules. No hidden conditions.
                </p>
              </div>

              {/* Feature 5 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">💰</div>
                <h3 className="text-2xl font-bold mb-4">Up to 90% Profit Split</h3>
                <p className="text-gray-400">
                  Keep the majority of your profits. You deserve it.
                </p>
              </div>

              {/* Feature 6 */}
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
                <div className="text-4xl mb-4">🌍</div>
                <h3 className="text-2xl font-bold mb-4">Global Community</h3>
                <p className="text-gray-400">
                  Join traders from 200+ countries worldwide.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-32">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-5xl md:text-6xl font-bold mb-8">
              Ready to Start <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Trading</span>?
            </h2>
            <p className="text-xl text-gray-300 mb-12">
              Join thousands of traders worldwide and get funded today
            </p>
            <Link
              to="/programs"
              className="inline-block px-16 py-6 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 rounded-full text-xl font-bold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-purple-500/50"
            >
              Get Funded Now
            </Link>
          </div>
        </section>

        {/* Custom Animations */}
        <style jsx>{`
          @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
          }

          @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
          }

          @keyframes pulse-slow {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
          }

          .animate-float {
            animation: float 6s ease-in-out infinite;
          }

          .animate-gradient-shift {
            background-size: 200% 200%;
            animation: gradient-shift 3s ease infinite;
          }

          .animate-pulse-slow {
            animation: pulse-slow 4s ease-in-out infinite;
          }
        `}</style>

      </div>
    </Layout>
  );
};

export default NewHomePage;

