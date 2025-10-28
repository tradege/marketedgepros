import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, TrendingUp, Shield, Zap, ArrowRight, Target, Trophy, Gem } from 'lucide-react';
import Layout from '../components/layout/Layout';
import useAuthStore from '../store/authStore';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com';

export default function ProgramsNew() {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [programs, setPrograms] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('two_phase'); // Default to most popular

  useEffect(() => {
    loadPrograms();
  }, []);

  const loadPrograms = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('/api/v1/programs/');
      setPrograms(response.data.programs || []);
    } catch (error) {
      setError(error.message || 'Failed to load programs');
    } finally {
      setIsLoading(false);
    }
  };

  const getProgramIcon = (type) => {
    switch (type) {
      case 'instant_funding':
        return <Zap className="w-6 h-6" />;
      case 'one_phase':
        return <Target className="w-6 h-6" />;
      case 'two_phase':
        return <Trophy className="w-6 h-6" />;
      case 'three_phase':
        return <Gem className="w-6 h-6" />;
      default:
        return <Shield className="w-6 h-6" />;
    }
  };

  const getProgramColor = (type) => {
    switch (type) {
      case 'instant_funding':
        return 'from-yellow-500 to-orange-600';
      case 'one_phase':
        return 'from-blue-500 to-cyan-600';
      case 'two_phase':
        return 'from-purple-500 to-pink-600';
      case 'three_phase':
        return 'from-green-500 to-emerald-600';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  const getProgramBadge = (type) => {
    switch (type) {
      case 'instant_funding':
        return { text: 'Instant', color: 'bg-yellow-500/20 text-yellow-400' };
      case 'one_phase':
        return { text: '1 Phase', color: 'bg-blue-500/20 text-blue-400' };
      case 'two_phase':
        return { text: '2 Phase', color: 'bg-purple-500/20 text-purple-400' };
      case 'three_phase':
        return { text: '3 Phase', color: 'bg-green-500/20 text-green-400' };
      default:
        return { text: 'Challenge', color: 'bg-gray-500/20 text-gray-400' };
    }
  };

  const handleGetStarted = (programId) => {
    if (!user) {
      navigate('/login', { state: { from: `/programs/${programId}` } });
    } else {
      navigate(`/programs/${programId}/checkout`);
    }
  };

  const filteredPrograms = programs.filter(p => p.type === activeTab);

  const tabs = [
    { id: 'two_phase', label: 'Two Phase', icon: Trophy, description: 'Most Popular' },
    { id: 'instant_funding', label: 'Instant Funding', icon: Zap, description: 'Fastest' },
    { id: 'one_phase', label: 'One Phase', icon: Target, description: 'Direct' },
    { id: 'three_phase', label: 'Three Phase', icon: Gem, description: 'Most Affordable' },
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Choose Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">Challenge</span>
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Select the program that fits your trading style and goals. All programs include up to 90% profit split and fast payouts.
            </p>
          </div>

          {/* Tabs */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    group relative px-8 py-4 rounded-xl font-semibold transition-all duration-300
                    ${activeTab === tab.id
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/50 scale-105'
                      : 'bg-slate-800/50 text-gray-400 hover:text-white hover:bg-slate-700/50'
                    }
                  `}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-5 h-5" />
                    <div className="text-left">
                      <div className="font-bold">{tab.label}</div>
                      <div className="text-xs opacity-75">{tab.description}</div>
                    </div>
                  </div>
                  {activeTab === tab.id && (
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-12 h-1 bg-gradient-to-r from-blue-400 to-purple-600 rounded-full" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Programs Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {isLoading ? (
              <div className="col-span-full text-center text-gray-400 py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                Loading programs...
              </div>
            ) : error ? (
              <div className="col-span-full text-center text-red-400 py-20">
                <p className="text-xl mb-4">⚠️ Error loading programs</p>
                <p className="text-gray-400">{error}</p>
                <button 
                  onClick={loadPrograms}
                  className="mt-6 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition"
                >
                  Try Again
                </button>
              </div>
            ) : filteredPrograms.length === 0 ? (
              <div className="col-span-full text-center text-gray-400 py-20">
                <p className="text-xl">No programs available for this category</p>
                <p className="text-sm mt-2">Please check back later or contact support</p>
              </div>
            ) : (
              filteredPrograms.map((program) => {
                const badge = getProgramBadge(program.type);
                const colorClass = getProgramColor(program.type);
                
                return (
                  <div
                    key={program.id}
                    className="group relative bg-gradient-to-b from-slate-800/80 to-slate-900/80 backdrop-blur-sm border border-blue-500/20 rounded-2xl p-8 hover:border-blue-500/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/20"
                  >
                    {/* Badge */}
                    <div className="flex items-center justify-between mb-6">
                      <span className={`px-4 py-2 ${badge.color} rounded-full text-sm font-bold`}>
                        {badge.text}
                      </span>
                      <div className={`p-3 rounded-xl bg-gradient-to-r ${colorClass}`}>
                        {getProgramIcon(program.type)}
                      </div>
                    </div>

                    {/* Program Name */}
                    <h3 className="text-3xl font-bold text-white mb-3">
                      {program.name}
                    </h3>

                    {/* Description */}
                    <p className="text-gray-400 mb-6 min-h-[60px]">
                      {program.description}
                    </p>

                    {/* Price */}
                    <div className="border-t border-gray-700 pt-6 mb-6">
                      <div className="flex items-baseline justify-between">
                        <div>
                          <span className="text-4xl font-bold text-white">${program.price}</span>
                          <span className="text-gray-400 ml-2">one-time</span>
                        </div>
                      </div>
                    </div>

                    {/* Features */}
                    <div className="space-y-3 mb-8">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Account Size</span>
                        <span className="text-white font-semibold">${program.account_size?.toLocaleString()}</span>
                      </div>
                      {program.profit_target > 0 && (
                        <div className="flex justify-between items-center">
                          <span className="text-gray-400">Profit Target</span>
                          <span className="text-green-400 font-semibold">{program.profit_target}%</span>
                        </div>
                      )}
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Max Daily Loss</span>
                        <span className="text-red-400 font-semibold">{program.max_daily_loss}%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Profit Split</span>
                        <span className="text-blue-400 font-semibold">{program.profit_split}%</span>
                      </div>
                    </div>

                    {/* CTA Button */}
                    <button
                      onClick={() => handleGetStarted(program.id)}
                      className={`
                        w-full py-4 bg-gradient-to-r ${colorClass} rounded-xl text-white font-bold
                        hover:shadow-lg hover:shadow-blue-500/50 transition-all duration-300
                        flex items-center justify-center gap-2 group-hover:scale-105
                      `}
                    >
                      Get Started
                      <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </button>
                  </div>
                );
              })
            )}
          </div>

          {/* Features Section */}
          <div className="mt-20 grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-slate-800/50 rounded-xl border border-blue-500/20">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Fast Payouts</h3>
              <p className="text-gray-400">Request payouts anytime, receive within 24 hours</p>
            </div>
            <div className="text-center p-6 bg-slate-800/50 rounded-xl border border-blue-500/20">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full flex items-center justify-center">
                <Trophy className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Up to 90% Split</h3>
              <p className="text-gray-400">Keep up to 90% of your trading profits</p>
            </div>
            <div className="text-center p-6 bg-slate-800/50 rounded-xl border border-blue-500/20">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Secure & Reliable</h3>
              <p className="text-gray-400">Your funds are safe with us, backed by industry leaders</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

