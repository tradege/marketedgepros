import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

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
            { id: 1, account_size: 10000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
            { id: 2, account_size: 25000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
            { id: 3, account_size: 50000, profit_target: 10, max_daily_loss: 5, profit_split: 85, phases: 2 },
            { id: 4, account_size: 100000, profit_target: 10, max_daily_loss: 5, profit_split: 90, phases: 2 },
          ]);
        } else {
          setPrograms(apiPrograms);
        }
      } catch (error) {
        console.error('Error fetching programs:', error);
        // Fallback to static programs on error
        setPrograms([
          { id: 1, account_size: 10000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
          { id: 2, account_size: 25000, profit_target: 10, max_daily_loss: 5, profit_split: 80, phases: 2 },
          { id: 3, account_size: 50000, profit_target: 10, max_daily_loss: 5, profit_split: 85, phases: 2 },
          { id: 4, account_size: 100000, profit_target: 10, max_daily_loss: 5, profit_split: 90, phases: 2 },
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
    <div className="min-h-screen bg-black text-white overflow-hidden">
      
      {/* Hero Section */}
      <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 z-0">
          <img 
            src="/images/abstract-trading-flow.png" 
            alt="" 
            className="w-full h-full object-cover opacity-30"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black"></div>
        </div>

        {/* 3D Trading Screens - Floating */}
        <div className="absolute inset-0 z-10 pointer-events-none">
          <img 
            src="/images/hero-trading-3d.png" 
            alt="" 
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
            <br />
            Keep up to <span className="text-purple-400 font-bold">90%</span> of your profits.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
            <Link 
              to="/programs" 
              className="group relative px-12 py-5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-lg font-semibold overflow-hidden transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50"
            >
              <span className="relative z-10">Get Funded Now</span>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-teal-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </Link>
            
            <Link 
              to="/programs" 
              className="group relative px-12 py-5 bg-transparent border-2 border-purple-500 rounded-full text-lg font-semibold overflow-hidden transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-purple-500/50"
            >
              <span className="relative z-10">Explore Programs</span>
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
            </Link>
          </div>

          {/* Stats Cards */}
          <div ref={statsRef} className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-5xl mx-auto">
            {/* Countries */}
            <div className="group relative bg-gradient-to-br from-cyan-500/10 to-teal-500/10 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/30 animate-orbit" style={{animationDelay: '0s'}}>
              <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-2">
                {stats.countries}+
              </div>
              <div className="text-sm text-gray-400 uppercase tracking-wider">Countries</div>
            </div>

            {/* Capital */}
            <div className="group relative bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/30 animate-orbit" style={{animationDelay: '1.5s'}}>
              <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
                ${stats.capital}M+
              </div>
              <div className="text-sm text-gray-400 uppercase tracking-wider">Capital Deployed</div>
            </div>

            {/* Traders */}
            <div className="group relative bg-gradient-to-br from-orange-500/10 to-red-500/10 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-orange-500/30 animate-orbit" style={{animationDelay: '3s'}}>
              <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-2">
                {stats.traders}+
              </div>
              <div className="text-sm text-gray-400 uppercase tracking-wider">Active Traders</div>
            </div>

            {/* Profit Split */}
            <div className="group relative bg-gradient-to-br from-blue-500/10 to-indigo-500/10 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/30 animate-orbit" style={{animationDelay: '4.5s'}}>
              <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-2">
                {stats.profitSplit}%
              </div>
              <div className="text-sm text-gray-400 uppercase tracking-wider">Profit Split</div>
            </div>
          </div>

        </div>
      </section>

      {/* Globe Section */}
      <section className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-black via-cyan-950/20 to-black"></div>
        
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              Trade <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Globally</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Join traders from over 200 countries trading the world's markets
            </p>
          </div>

          {/* Globe Image */}
          <div className="relative flex justify-center items-center">
            <img 
              src="/images/stats-globe-hologram.png" 
              alt="Global Trading Network" 
              className="w-full max-w-2xl h-auto animate-pulse-slow"
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="relative py-32 bg-gradient-to-b from-black via-purple-950/10 to-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              How It <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Works</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {/* Step 1 */}
            <div className="group relative bg-gradient-to-br from-cyan-500/10 to-teal-500/10 backdrop-blur-xl border border-cyan-500/30 rounded-3xl p-8 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/30">
              <div className="text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-6">01</div>
              <h3 className="text-2xl font-bold mb-4">Choose Your Program</h3>
              <p className="text-gray-400">
                Select from our range of funding programs - from $5K to $400K in trading capital
              </p>
            </div>

            {/* Step 2 */}
            <div className="group relative bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-xl border border-purple-500/30 rounded-3xl p-8 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/30">
              <div className="text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-6">02</div>
              <h3 className="text-2xl font-bold mb-4">Pass the Challenge</h3>
              <p className="text-gray-400">
                Trade with discipline and hit your profit targets while managing risk
              </p>
            </div>

            {/* Step 3 */}
            <div className="group relative bg-gradient-to-br from-orange-500/10 to-red-500/10 backdrop-blur-xl border border-orange-500/30 rounded-3xl p-8 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-orange-500/30">
              <div className="text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-6">03</div>
              <h3 className="text-2xl font-bold mb-4">Get Funded & Paid</h3>
              <p className="text-gray-400">
                Start trading with our capital and keep up to 90% of your profits
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* Programs Section */}
      <section className="relative py-32 bg-gradient-to-b from-black via-teal-950/10 to-black">
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
      <section className="relative py-32 bg-gradient-to-b from-black via-purple-950/10 to-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              Why Choose <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">MarketEdgePros</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: '💰', title: 'Up to $400K Capital', desc: 'Scale your trading with substantial capital', gradient: 'from-cyan-400 to-teal-400' },
              { icon: '⚡', title: 'Fast Payouts', desc: 'Request withdrawals anytime', gradient: 'from-purple-400 to-pink-400' },
              { icon: '📈', title: 'Up to 90% Split', desc: 'Keep most of your profits', gradient: 'from-orange-400 to-red-400' },
              { icon: '🤖', title: 'EAs Allowed', desc: 'Use your favorite trading bots', gradient: 'from-blue-400 to-indigo-400' },
              { icon: '🌍', title: 'Trade Anywhere', desc: 'Global access, no restrictions', gradient: 'from-green-400 to-emerald-400' },
              { icon: '📊', title: 'Advanced Dashboard', desc: 'Real-time analytics and insights', gradient: 'from-yellow-400 to-amber-400' },
              { icon: '🔒', title: 'Secure & Reliable', desc: 'Your data and funds are safe', gradient: 'from-pink-400 to-rose-400' },
              { icon: '🎯', title: 'No Consistency Rules', desc: 'Trade your own way', gradient: 'from-violet-400 to-purple-400' },
              { icon: '📱', title: 'MT4/MT5 Support', desc: 'Use the platforms you love', gradient: 'from-teal-400 to-cyan-400' }
            ].map((feature, index) => (
              <div
                key={index}
                className="group relative bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-white/20"
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className={`text-2xl font-bold mb-3 text-transparent bg-clip-text bg-gradient-to-r ${feature.gradient}`}>
                  {feature.title}
                </h3>
                <p className="text-gray-400">{feature.desc}</p>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-950/30 via-purple-950/30 to-cyan-950/30"></div>
        
        <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
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
  );
};

export default NewHomePage;

