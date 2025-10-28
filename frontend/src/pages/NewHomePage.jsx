import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/layout/Layout';
import SEO, { SEOConfigs } from '../components/SEO';
import StructuredData from '../components/seo/StructuredData';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

export default function NewHomePage() {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('two_phase');
  const navigate = useNavigate();

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
      
      {/* Hero Section - Fxify Style */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950">
        {/* Massive Neon Glow Background */}
        <div className="absolute inset-0">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/30 via-teal-500/40 to-purple-500/30 rounded-full blur-[150px] animate-pulse-slow"></div>
          <div className="absolute top-1/3 left-1/3 w-[600px] h-[600px] bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full blur-[120px] animate-pulse-slow" style={{ animationDelay: '2s' }}></div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center py-32">
          {/* Small Badge */}
          <div className="inline-block mb-8 px-6 py-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 backdrop-blur-xl">
            <span className="text-cyan-400 font-semibold text-sm tracking-wider">YOUR TRUSTED TRADING PARTNER</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-6xl md:text-8xl font-black mb-8 leading-tight">
            <span className="text-white">The Prop Firm </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 animate-pulse-slow">Designed</span>
            <br />
            <span className="text-white">For Every </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 animate-pulse-slow">Trader</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto">
            Join traders worldwide and become a funded trader with the world's most trusted prop firm.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-20">
            <Link 
              to="/register" 
              className="group relative px-12 py-5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 rounded-xl text-white font-bold text-lg transition transform hover:scale-105 shadow-2xl shadow-cyan-500/50 overflow-hidden"
            >
              <span className="relative z-10">Get Funded Now</span>
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            </Link>
            <Link 
              to="/programs" 
              className="group relative px-12 py-5 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-400 hover:to-orange-400 rounded-xl text-slate-900 font-bold text-lg transition transform hover:scale-105 shadow-2xl shadow-yellow-500/50 overflow-hidden"
            >
              <span className="relative z-10">Explore Programs</span>
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
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
                    <div key={`${setIndex}-${index}`} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 backdrop-blur-xl border border-white/10">
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

          {/* Stats Cards - Fxify Style */}
          <div className="grid md:grid-cols-3 gap-8">
            {/* Community Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-cyan-500/10 to-teal-500/10 border-2 border-cyan-400/50 p-8 hover:border-cyan-400 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/50">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500"></div>
              
              <div className="relative">
                {/* Country Flags */}
                <div className="flex justify-center mb-4 -space-x-2">
                  {['🇺🇸', '🇬🇧', '🇩🇪', '🇫🇷', '🇮🇹', '🇪🇸'].map((flag, i) => (
                    <div key={i} className="w-10 h-10 rounded-full bg-slate-800 border-2 border-cyan-400/50 flex items-center justify-center text-xl">
                      {flag}
                    </div>
                  ))}
                </div>
                
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-2">
                  200+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Countries</div>
              </div>
            </div>

            {/* Payouts Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-2 border-purple-400/50 p-8 hover:border-purple-400 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/50">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500"></div>
              
              <div className="relative">
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
                  $10M+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Capital Deployed</div>
              </div>
            </div>

            {/* Traders Card */}
            <div className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-orange-500/10 to-red-500/10 border-2 border-orange-400/50 p-8 hover:border-orange-400 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-orange-500/50">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500"></div>
              
              <div className="relative">
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-400 mb-2">
                  5,000+
                </div>
                <div className="text-lg text-gray-400 font-semibold">Active Traders</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="relative py-16 bg-slate-950 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { icon: '💬', platform: 'Discord', count: '10K+', label: 'Members', color: 'from-orange-500 to-red-500', border: 'border-orange-400/50' },
              { icon: '𝕏', platform: 'X (Twitter)', count: '5K+', label: 'Followers', color: 'from-green-500 to-teal-500', border: 'border-green-400/50' },
              { icon: '📷', platform: 'Instagram', count: '8K+', label: 'Followers', color: 'from-pink-500 to-purple-500', border: 'border-pink-400/50' },
              { icon: '🎵', platform: 'TikTok', count: '3K+', label: 'Likes', color: 'from-blue-500 to-cyan-500', border: 'border-blue-400/50' },
            ].map((social, index) => (
              <div key={index} className={`group relative overflow-hidden rounded-xl backdrop-blur-xl bg-white/5 border-2 ${social.border} p-6 hover:scale-105 transition-all duration-300 cursor-pointer`}>
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${social.color} rounded-xl blur opacity-0 group-hover:opacity-20 transition-opacity duration-300`}></div>
                
                <div className="relative text-center">
                  <div className="text-4xl mb-2">{social.icon}</div>
                  <div className={`text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${social.color} mb-1`}>
                    {social.count}
                  </div>
                  <div className="text-sm text-gray-400">{social.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative py-20 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="text-white">How It </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Works</span>
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
                border: 'border-purple-400/50'
              },
              { 
                number: '02', 
                title: 'Become a Funded Trader', 
                desc: 'Start trading with your account using your unique strategy and risk management.',
                gradient: 'from-orange-400 to-red-400',
                border: 'border-orange-400/50'
              },
              { 
                number: '03', 
                title: 'Get Paid for Your Skills', 
                desc: 'Trade your way to the top, earn up to 90% performance split, request payout on demand.',
                gradient: 'from-cyan-400 to-blue-400',
                border: 'border-cyan-400/50'
              },
            ].map((step, index) => (
              <div 
                key={index}
                className={`group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-white/5 border-2 ${step.border} p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl`}
              >
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${step.gradient} rounded-2xl blur opacity-0 group-hover:opacity-20 transition-opacity duration-500`}></div>
                
                <div className="relative">
                  <div className={`text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r ${step.gradient} mb-4`}>
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

      {/* Programs Section - Fxify Style */}
      <section className="relative py-20 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="text-white">Choose Your </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Challenge</span>
            </h2>
            <p className="text-xl text-gray-400">Select the program that fits your trading style and goals</p>
          </div>

          {/* Program Tabs - Numbered */}
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
                    ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white shadow-2xl shadow-cyan-500/50 scale-105'
                    : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-white/10'
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
              filteredPrograms.slice(0, 6).map((program) => (
                <div 
                  key={program.id}
                  className="group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-gradient-to-br from-white/5 to-white/10 border border-white/20 hover:border-cyan-400/50 p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/30"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-2xl blur opacity-0 group-hover:opacity-20 transition-opacity duration-500"></div>
                  
                  <div className="relative">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-2xl font-bold text-white">{program.name}</h3>
                      <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-sm font-semibold border border-cyan-400/30">
                        {program.type === 'one_phase' ? '1 Phase' : program.type === 'two_phase' ? '2 Phase' : program.type === 'three_phase' ? '3 Phase' : 'Instant'}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-gray-400 mb-6 text-sm">{program.description}</p>

                    {/* Stats */}
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

                    {/* CTA Button */}
                    <button
                      onClick={() => handleGetStarted(program.id)}
                      className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 rounded-xl text-white font-bold transition transform hover:scale-105 shadow-lg shadow-cyan-500/30"
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
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">MarketEdgePros</span>
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
                className={`group relative overflow-hidden rounded-2xl backdrop-blur-xl bg-white/5 border-2 ${feature.border} p-8 transition-all duration-500 hover:scale-105 hover:shadow-2xl`}
              >
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${feature.gradient} rounded-2xl blur opacity-0 group-hover:opacity-20 transition-opacity duration-500`}></div>
                
                <div className="relative">
                  <div className="text-6xl mb-4">{feature.icon}</div>
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
      <section className="relative py-20 bg-gradient-to-r from-cyan-600 to-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-5xl font-bold text-white mb-6">Ready to Start Trading?</h2>
          <p className="text-2xl text-cyan-100 mb-10">Join thousands of successful traders today</p>
          <Link 
            to="/register" 
            className="inline-block px-12 py-5 bg-white text-cyan-600 rounded-xl font-bold text-xl hover:bg-gray-100 transition transform hover:scale-105 shadow-2xl"
          >
            Get Funded Now
          </Link>
        </div>
      </section>
    </Layout>
  );
}

