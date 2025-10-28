import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/layout/Layout';
import SEO, { SEOConfigs } from '../components/SEO';
import StructuredData from '../components/seo/StructuredData';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Counter Animation Hook
function useCountUp(end, duration = 2000, shouldStart = true) {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    if (!shouldStart) return;
    
    let startTime;
    let animationFrame;
    
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      setCount(Math.floor(progress * end));
      
      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };
    
    animationFrame = requestAnimationFrame(animate);
    
    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration, shouldStart]);
  
  return count;
}

// Intersection Observer Hook
function useInView(options = {}) {
  const [isInView, setIsInView] = useState(false);
  const ref = useRef(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsInView(true);
      }
    }, { threshold: 0.1, ...options });
    
    if (ref.current) {
      observer.observe(ref.current);
    }
    
    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);
  
  return [ref, isInView];
}

export default function NewHomePage() {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('two_phase');
  const navigate = useNavigate();
  
  const [statsRef, statsInView] = useInView();
  const [socialRef, socialInView] = useInView();
  
  const countriesCount = useCountUp(200, 2000, statsInView);
  const payoutCount = useCountUp(10, 2000, statsInView);
  const tradersCount = useCountUp(5000, 2000, statsInView);
  
  const discordCount = useCountUp(10, 2000, socialInView);
  const xCount = useCountUp(5, 2000, socialInView);
  const instaCount = useCountUp(8, 2000, socialInView);
  const tiktokCount = useCountUp(3, 2000, socialInView);

  useEffect(() => {
    fetchPrograms();
  }, []);

  const fetchPrograms = async () => {
    try {
      const response = await axios.get(`${API_URL}/programs/`);
      setPrograms(response.data.programs || []);
    } catch (error) {
      console.error('Error fetching programs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetStarted = (programId) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate(`/register?program=${programId}`);
    } else {
      navigate(`/checkout/${programId}`);
    }
  };

  const filteredPrograms = programs.filter(p => p.type === selectedTab);

  return (
    <Layout>
      <SEO {...SEOConfigs.home} />
      <StructuredData type="website" />
      <StructuredData type="organization" />
      
      {/* Animated Background Blobs */}
      <style>{`
        @keyframes blob1 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        @keyframes blob2 {
          0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); }
          33% { transform: translate(-40px, 30px) scale(1.2) rotate(120deg); }
          66% { transform: translate(20px, -40px) scale(0.8) rotate(240deg); }
        }
        @keyframes blob3 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(50px, 50px) scale(1.3); }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        @keyframes float-slow {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-30px) rotate(5deg); }
        }
        @keyframes gradient-shift {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        @keyframes glow-pulse {
          0%, 100% { opacity: 0.5; }
          50% { opacity: 1; }
        }
        @keyframes slide-in-left {
          from { transform: translateX(-100px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slide-in-right {
          from { transform: translateX(100px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        @keyframes fade-in-up {
          from { transform: translateY(30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
        
        .blob1 { animation: blob1 20s ease-in-out infinite; }
        .blob2 { animation: blob2 25s ease-in-out infinite; }
        .blob3 { animation: blob3 30s ease-in-out infinite; }
        .float { animation: float 6s ease-in-out infinite; }
        .float-slow { animation: float-slow 8s ease-in-out infinite; }
        .gradient-shift {
          background-size: 200% 200%;
          animation: gradient-shift 3s ease infinite;
        }
        .glow-pulse { animation: glow-pulse 2s ease-in-out infinite; }
        .slide-in-left { animation: slide-in-left 0.8s ease-out; }
        .slide-in-right { animation: slide-in-right 0.8s ease-out; }
        .fade-in-up { animation: fade-in-up 0.6s ease-out; }
      `}</style>
      
      {/* Hero Section - Everything Moves! */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950">
        {/* Animated Background Blobs */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="blob1 absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-gradient-to-r from-cyan-500/30 via-teal-500/40 to-blue-500/30 rounded-full blur-[150px]"></div>
          <div className="blob2 absolute top-1/2 right-1/4 w-[700px] h-[700px] bg-gradient-to-br from-purple-500/30 via-pink-500/40 to-purple-500/30 rounded-full blur-[150px]"></div>
          <div className="blob3 absolute bottom-1/4 left-1/2 w-[500px] h-[500px] bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-full blur-[120px]"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center py-32">
          {/* Badge */}
          <div className="inline-block mb-8 px-6 py-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 backdrop-blur-xl float">
            <span className="text-cyan-400 font-semibold text-sm tracking-wider">YOUR TRUSTED TRADING PARTNER</span>
          </div>

          {/* Main Headline with Gradient Animation */}
          <h1 className="text-6xl md:text-8xl font-black mb-8 leading-tight">
            <span className="text-white">The Prop Firm </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-400 gradient-shift">
              Designed
            </span>
            <br />
            <span className="text-white">For Every </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-400 gradient-shift">
              Trader
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto fade-in-up">
            Join traders worldwide and become a funded trader with the world's most trusted prop firm.
          </p>

          {/* CTA Buttons with Hover Glow */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-20">
            <Link 
              to="/register" 
              className="group relative px-12 py-5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl text-white font-bold text-lg transition-all duration-300 transform hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 overflow-hidden"
            >
              <span className="relative z-10">Get Funded Now</span>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </Link>
            <Link 
              to="/programs" 
              className="group relative px-12 py-5 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl text-slate-900 font-bold text-lg transition-all duration-300 transform hover:scale-110 hover:shadow-2xl hover:shadow-yellow-500/50 overflow-hidden"
            >
              <span className="relative z-10">Explore Programs</span>
              <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-orange-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </Link>
          </div>

          {/* Scrolling Features Bar */}
          <div className="relative overflow-hidden py-4 mb-16">
            <div className="flex gap-8 animate-scroll whitespace-nowrap">
              {[...Array(2)].map((_, setIndex) => (
                <div key={setIndex} className="flex gap-8">
                  {[
                    'Up to $400,000 starting capital',
                    'First Withdrawal On Demand',
                    'Unlimited Days Available',
                    'Up to 90% Performance Split',
                    'EAs Allowed',
                    'Backed by a Broker',
                    'Bi-weekly Payouts Available',
                    'No Consistency Rules',
                    'No SL Required',
                    'Hold Over Weekend',
                    'Scale up $4,000,000',
                    'Performance Protect',
                    'Instant Credentials',
                    '100% Refund',
                    'Martingale & Grid Allowed',
                  ].map((feature, index) => (
                    <div key={`${setIndex}-${index}`} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 backdrop-blur-xl border border-white/10 hover:border-cyan-400/50 transition-all duration-300">
                      <svg className="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-gray-300 text-sm font-medium">{feature}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Animated Stats Cards */}
          <div ref={statsRef} className="grid md:grid-cols-3 gap-8">
            {/* Countries Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-cyan-500/10 to-teal-500/10 border-2 border-cyan-400/50 p-8 transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 float" style={{ animationDelay: '0s' }}>
              <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-2xl blur opacity-0 group-hover:opacity-40 transition-opacity duration-500 glow-pulse"></div>
              
              <div className="relative">
                <div className="flex justify-center mb-4 -space-x-2">
                  {['🇺🇸', '🇬🇧', '🇩🇪', '🇫🇷', '🇮🇹', '🇪🇸'].map((flag, i) => (
                    <div key={i} className="w-10 h-10 rounded-full bg-slate-800 border-2 border-cyan-400/50 flex items-center justify-center text-xl float-slow" style={{ animationDelay: `${i * 0.2}s` }}>
                      {flag}
                    </div>
                  ))}
                </div>
                
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-2">
                  {countriesCount}+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Countries</div>
              </div>
            </div>

            {/* Payouts Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-2 border-purple-400/50 p-8 transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-purple-500/50 float" style={{ animationDelay: '0.2s' }}>
              <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl blur opacity-0 group-hover:opacity-40 transition-opacity duration-500 glow-pulse"></div>
              
              <div className="relative">
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
                  ${payoutCount}M+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Capital Deployed</div>
              </div>
            </div>

            {/* Traders Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-orange-500/10 to-red-500/10 border-2 border-orange-400/50 p-8 transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-orange-500/50 float" style={{ animationDelay: '0.4s' }}>
              <div className="absolute -inset-0.5 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl blur opacity-0 group-hover:opacity-40 transition-opacity duration-500 glow-pulse"></div>
              
              <div className="relative">
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-2">
                  {tradersCount.toLocaleString()}+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Active Traders</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof with Animated Counters */}
      <section ref={socialRef} className="relative py-16 bg-slate-950 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { icon: '💬', platform: 'Discord', count: discordCount, label: 'Members', color: 'from-orange-500 to-red-500', border: 'border-orange-400/50' },
              { icon: '𝕏', platform: 'X (Twitter)', count: xCount, label: 'Followers', color: 'from-green-500 to-teal-500', border: 'border-green-400/50' },
              { icon: '📷', platform: 'Instagram', count: instaCount, label: 'Followers', color: 'from-pink-500 to-purple-500', border: 'border-pink-400/50' },
              { icon: '🎵', platform: 'TikTok', count: tiktokCount, label: 'Likes', color: 'from-blue-500 to-cyan-500', border: 'border-blue-400/50' },
            ].map((social, index) => (
              <div key={index} className={`group relative overflow-hidden rounded-xl backdrop-blur-xl bg-white/5 border-2 ${social.border} p-6 transition-all duration-300 hover:scale-110 cursor-pointer float-slow`} style={{ animationDelay: `${index * 0.1}s` }}>
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${social.color} rounded-xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-300 glow-pulse`}></div>
                
                <div className="relative text-center">
                  <div className="text-4xl mb-2">{social.icon}</div>
                  <div className={`text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${social.color} mb-1`}>
                    {social.count}K+
                  </div>
                  <div className="text-sm text-gray-400">{social.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works with Slide-in Animation */}
      <section className="relative py-20 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="text-white">How It </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-400 gradient-shift">Works</span>
            </h2>
            <p className="text-xl text-gray-400">Get funded in 3 simple steps</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { 
                number: '01', 
                title: 'Choose Your Program', 
                desc: 'Choose your preferred funded trader program with account sizes up to $400,000.',
                gradient: 'from-purple-400 to-pink-400',
                border: 'border-purple-400/50',
                animation: 'slide-in-left'
              },
              { 
                number: '02', 
                title: 'Become a Funded Trader', 
                desc: 'Start trading with your account using your unique strategy and risk management.',
                gradient: 'from-orange-400 to-red-400',
                border: 'border-orange-400/50',
                animation: 'fade-in-up'
              },
              { 
                number: '03', 
                title: 'Get Paid for Your Skills', 
                desc: 'Trade your way to the top, earn up to 90% performance split, request payout on demand.',
                gradient: 'from-cyan-400 to-blue-400',
                border: 'border-cyan-400/50',
                animation: 'slide-in-right'
              },
            ].map((step, index) => (
              <div 
                key={index}
                className={`${step.animation} group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-white/5 border-2 ${step.border} p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl float-slow`}
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${step.gradient} rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500 glow-pulse`}></div>
                
                <div className="relative">
                  <div className={`text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r ${step.gradient} mb-4`}>
                    {step.number}
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">{step.title}</h3>
                  <p className="text-gray-400">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Programs Section */}
      <section className="relative py-20 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="text-white">Choose Your </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-400 gradient-shift">Challenge</span>
            </h2>
            <p className="text-xl text-gray-400">Select the program that fits your trading style and goals</p>
          </div>

          {/* Program Tabs */}
          <div className="flex justify-center mb-12 flex-wrap gap-4">
            {[
              { id: 'one_phase', number: '1', label: 'One Phase', icon: '🚀' },
              { id: 'two_phase', number: '2', label: 'Two Phase', icon: '💜' },
              { id: 'three_phase', number: '3', label: 'Three Phase', icon: '💎' },
              { id: 'instant', number: '4', label: 'Instant Funding', icon: '⚡' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`group relative px-8 py-4 rounded-xl font-semibold transition-all duration-300 ${
                  selectedTab === tab.id
                    ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white shadow-2xl shadow-cyan-500/50 scale-110'
                    : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-white/10 hover:scale-105'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                    selectedTab === tab.id ? 'bg-white/20' : 'bg-white/10'
                  }`}>
                    {tab.number}
                  </div>
                  <span>{tab.label}</span>
                  <span className="text-xl">{tab.icon}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Programs Grid */}
          <div className="grid md:grid-cols-3 gap-8">
            {loading ? (
              <div className="col-span-3 text-center text-gray-400">Loading programs...</div>
            ) : filteredPrograms.length === 0 ? (
              <div className="col-span-3 text-center text-gray-400">No programs available for this category</div>
            ) : (
              filteredPrograms.slice(0, 6).map((program, index) => (
                <div 
                  key={program.id}
                  className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-white/5 to-white/10 border border-white/20 hover:border-cyan-400/50 p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/30 float-slow"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500 glow-pulse"></div>
                  
                  <div className="relative">
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-2xl font-bold text-white">{program.name}</h3>
                      <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-sm font-semibold border border-cyan-400/30">
                        {program.type === 'one_phase' ? '1 Phase' : program.type === 'two_phase' ? '2 Phase' : program.type === 'three_phase' ? '3 Phase' : 'Instant'}
                      </span>
                    </div>

                    <p className="text-gray-400 mb-6 text-sm">{program.description}</p>

                    <div className="space-y-4 mb-6">
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5 border border-white/10">
                        <span className="text-gray-400 text-sm">Account Size</span>
                        <span className="text-white font-bold">${program.account_size.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5 border border-white/10">
                        <span className="text-gray-400 text-sm">Profit Target</span>
                        <span className="text-green-400 font-bold">{program.profit_target}%</span>
                      </div>
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5 border border-white/10">
                        <span className="text-gray-400 text-sm">Max Daily Loss</span>
                        <span className="text-red-400 font-bold">{program.max_daily_loss}%</span>
                      </div>
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5 border border-white/10">
                        <span className="text-gray-400 text-sm">Profit Split</span>
                        <span className="text-cyan-400 font-bold">{program.profit_split}%</span>
                      </div>
                    </div>

                    <button
                      onClick={() => handleGetStarted(program.id)}
                      className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 rounded-xl text-white font-bold transition-all duration-300 transform hover:scale-105 shadow-lg shadow-cyan-500/30"
                    >
                      Get Started - ${program.price}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-20 bg-slate-950 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="text-white">Why Choose </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-400 gradient-shift">MarketEdgePros</span>
              <span className="text-white">?</span>
            </h2>
            <p className="text-xl text-gray-400">Everything you need to succeed as a funded trader</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: '💰', title: 'Up to $400K Capital', desc: 'Start with capital up to $400,000', gradient: 'from-cyan-400 to-teal-400', border: 'border-cyan-400/50' },
              { icon: '⚡', title: 'Fast Payouts', desc: 'Request payouts anytime, receive within 24h', gradient: 'from-purple-400 to-pink-400', border: 'border-purple-400/50' },
              { icon: '📈', title: 'Up to 90% Split', desc: 'Keep up to 90% of your profits', gradient: 'from-orange-400 to-red-400', border: 'border-orange-400/50' },
              { icon: '🤖', title: 'EAs Allowed', desc: 'Use expert advisors and bots', gradient: 'from-blue-400 to-indigo-400', border: 'border-blue-400/50' },
              { icon: '🌍', title: 'Trade Anywhere', desc: 'Access from any device, anywhere', gradient: 'from-green-400 to-teal-400', border: 'border-green-400/50' },
              { icon: '📊', title: 'Advanced Dashboard', desc: 'Real-time analytics and insights', gradient: 'from-pink-400 to-purple-400', border: 'border-pink-400/50' },
              { icon: '🔒', title: 'Secure & Reliable', desc: 'Your funds are safe with us', gradient: 'from-yellow-400 to-orange-400', border: 'border-yellow-400/50' },
              { icon: '🎯', title: 'No Consistency Rules', desc: 'Trade your way without restrictions', gradient: 'from-cyan-400 to-blue-400', border: 'border-cyan-400/50' },
              { icon: '📱', title: 'MT4/MT5 Support', desc: 'Use your favorite platform', gradient: 'from-indigo-400 to-purple-400', border: 'border-indigo-400/50' },
            ].map((feature, index) => (
              <div 
                key={index}
                className={`group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-white/5 border-2 ${feature.border} p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl float-slow`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${feature.gradient} rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500 glow-pulse`}></div>
                
                <div className="relative">
                  <div className="text-6xl mb-4 float" style={{ animationDelay: `${index * 0.1}s` }}>{feature.icon}</div>
                  <h3 className={`text-xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r ${feature.gradient}`}>
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 text-sm">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-20 bg-gradient-to-r from-cyan-600 to-blue-600 overflow-hidden">
        <div className="absolute inset-0">
          <div className="blob1 absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
          <div className="blob2 absolute bottom-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-5xl font-bold text-white mb-6 float">Ready to Start Trading?</h2>
          <p className="text-2xl text-cyan-100 mb-10 fade-in-up">Join thousands of successful traders today</p>
          <Link 
            to="/register" 
            className="inline-block px-12 py-5 bg-white text-cyan-600 rounded-xl font-bold text-xl hover:bg-gray-100 transition-all duration-300 transform hover:scale-110 shadow-2xl float-slow"
          >
            Get Funded Now
          </Link>
        </div>
      </section>
    </Layout>
  );
}

