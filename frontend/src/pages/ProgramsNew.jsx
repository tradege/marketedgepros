import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, TrendingUp, Shield, Zap, ArrowRight, Target, Trophy, Gem, Star, Users, Clock, Award, CheckCircle, X } from 'lucide-react';
import Layout from '../components/layout/Layout';
import useAuthStore from '../store/authStore';
import api from "../services/api";



export default function ProgramsNew() {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [programs, setPrograms] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('two_phase');
  const [activeFaq, setActiveFaq] = useState(null);

  useEffect(() => {
    loadPrograms();
  }, []);

  const loadPrograms = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await api.get('/programs/');
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
        return 'from-cyan-400 to-teal-400';
      case 'one_phase':
        return 'from-cyan-400 to-teal-400';
      case 'two_phase':
        return 'from-cyan-400 to-teal-400';
      case 'three_phase':
        return 'from-cyan-400 to-teal-400';
      default:
        return 'from-cyan-400 to-teal-400';
    }
  };

  const getProgramBadge = (type) => {
    switch (type) {
      case 'instant_funding':
        return { text: 'Instant', color: 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' };
      case 'one_phase':
        return { text: '1 Phase', color: 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' };
      case 'two_phase':
        return { text: '2 Phase', color: 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' };
      case 'three_phase':
        return { text: '3 Phase', color: 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' };
      default:
        return { text: 'Challenge', color: 'bg-gray-500/20 text-gray-400 border border-gray-500/30' };
    }
  };

  const handleGetStarted = (programId) => {
    if (!user) {
      navigate('/login', { state: { from: `/programs/${programId}/checkout` } });
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

  const testimonials = [
    {
      name: "Michael Chen",
      role: "Funded Trader",
      image: "MC",
      rating: 5,
      text: "MarketEdgePros gave me the capital I needed to prove my strategy. Within 3 weeks, I passed the evaluation and now I'm trading with $100K. The support team is amazing!"
    },
    {
      name: "Sarah Johnson",
      role: "Professional Trader",
      image: "SJ",
      rating: 5,
      text: "Best prop firm I've worked with. Fast payouts, fair rules, and excellent technology. I've scaled from $25K to $200K in just 6 months."
    },
    {
      name: "David Martinez",
      role: "Full-Time Trader",
      image: "DM",
      rating: 5,
      text: "The two-phase challenge is perfectly designed. Realistic targets and no time pressure. I'm now making consistent profits with 90% split."
    }
  ];

  const faqs = [
    {
      question: "What's the difference between the challenge types?",
      answer: "Two-Phase has 2 evaluation stages, One-Phase has a single evaluation, Instant Funding gives you immediate access to capital, and Three-Phase offers the most affordable entry with 3 evaluation stages."
    },
    {
      question: "How long does it take to get funded?",
      answer: "Most traders complete the Two-Phase challenge in 2-4 weeks. One-Phase can be completed in 1-2 weeks, while Instant Funding gives you immediate access. There are no time limits on any challenge."
    },
    {
      question: "What happens if I fail the challenge?",
      answer: "You can retake the challenge at any time. We also offer a refund policy for first-time participants who don't violate any rules. Check our refund policy for details."
    },
    {
      question: "Can I trade during news events?",
      answer: "Yes! Unlike many prop firms, we allow trading during high-impact news events. We believe in giving traders full flexibility to implement their strategies."
    },
    {
      question: "How fast are the payouts?",
      answer: "We process payout requests within 24 hours on business days. You can request payouts as frequently as you like once you're funded."
    },
    {
      question: "Can I scale my account?",
      answer: "Absolutely! Funded traders can scale up to $2M based on consistent performance. We also increase your profit split to 90% as you grow."
    }
  ];

  const whyChooseUs = [
    {
      icon: Shield,
      title: "No Time Limits",
      description: "Trade at your own pace. We don't pressure you with tight deadlines."
    },
    {
      icon: Zap,
      title: "Fast Payouts",
      description: "Request withdrawals anytime. Receive your profits within 24 hours."
    },
    {
      icon: Trophy,
      title: "Up to 90% Profit Split",
      description: "Keep the majority of what you earn. Scale up to 90% profit share."
    },
    {
      icon: Users,
      title: "24/7 Support",
      description: "Our team is always available to help you succeed."
    },
    {
      icon: Target,
      title: "Realistic Targets",
      description: "Achievable profit targets designed for sustainable trading."
    },
    {
      icon: Award,
      title: "Industry Leading",
      description: "Trusted by thousands of traders worldwide since 2020."
    }
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-black py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Choose Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Challenge</span>
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
                      ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white shadow-lg shadow-cyan-500/50 scale-105'
                      : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-white/10'
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
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-12 h-1 bg-gradient-to-r from-cyan-400 to-teal-400 rounded-full" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Programs Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
            {isLoading ? (
              <div className="col-span-full text-center text-gray-400 py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto mb-4"></div>
                Loading programs...
              </div>
            ) : error ? (
              <div className="col-span-full text-center text-red-400 py-20">
                <p className="text-xl mb-4">⚠️ Error loading programs</p>
                <p className="text-gray-400">{error}</p>
                <button 
                  onClick={loadPrograms}
                  className="mt-6 px-6 py-3 bg-gradient-to-r from-cyan-500 to-teal-500 hover:shadow-lg hover:shadow-cyan-500/50 text-white rounded-lg transition"
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
                    className="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/20"
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
                    <div className="border-t border-white/10 pt-6 mb-6">
                      <div className="flex items-baseline justify-between">
                        <div>
                          <span className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">${program.price}</span>
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
                          <span className="text-cyan-400 font-semibold">{program.profit_target}%</span>
                        </div>
                      )}
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Max Daily Loss</span>
                        <span className="text-red-400 font-semibold">{program.max_daily_loss}%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Profit Split</span>
                        <span className="text-cyan-400 font-semibold">{program.profit_split}%</span>
                      </div>
                    </div>

                    {/* CTA Button */}
                    <button
                      onClick={() => handleGetStarted(program.id)}
                      className={`
                        w-full py-4 bg-gradient-to-r ${colorClass} rounded-xl text-white font-bold
                        hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300
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

          {/* Why Choose Us Section */}
          <div className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                Why Choose <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">MarketEdgePros</span>
              </h2>
              <p className="text-gray-400 text-lg">Join thousands of successful traders who trust us with their trading career</p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {whyChooseUs.map((item, index) => {
                const Icon = item.icon;
                return (
                  <div key={index} className="bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-lg flex items-center justify-center mb-4">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{item.title}</h3>
                    <p className="text-gray-400">{item.description}</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Success Stories */}
          <div className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                Success <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Stories</span>
              </h2>
              <p className="text-gray-400 text-lg">See what our funded traders have to say</p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-500/50 transition-all duration-300">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center text-white font-bold">
                      {testimonial.image}
                    </div>
                    <div>
                      <h4 className="text-white font-bold">{testimonial.name}</h4>
                      <p className="text-gray-400 text-sm">{testimonial.role}</p>
                    </div>
                  </div>
                  <div className="flex gap-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 fill-cyan-400 text-cyan-400" />
                    ))}
                  </div>
                  <p className="text-gray-300 italic">"{testimonial.text}"</p>
                </div>
              ))}
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                Frequently Asked <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Questions</span>
              </h2>
              <p className="text-gray-400 text-lg">Everything you need to know about our programs</p>
            </div>
            <div className="max-w-3xl mx-auto space-y-4">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:border-cyan-500/50 transition-all duration-300">
                  <button
                    onClick={() => setActiveFaq(activeFaq === index ? null : index)}
                    className="w-full px-6 py-4 flex items-center justify-between text-left"
                  >
                    <span className="text-white font-semibold pr-4">{faq.question}</span>
                    <div className={`transform transition-transform ${activeFaq === index ? 'rotate-180' : ''}`}>
                      <svg className="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </button>
                  {activeFaq === index && (
                    <div className="px-6 pb-4 text-gray-400">
                      {faq.answer}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Features Section */}
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white/5 rounded-xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Fast Payouts</h3>
              <p className="text-gray-400">Request payouts anytime, receive within 24 hours</p>
            </div>
            <div className="text-center p-6 bg-white/5 rounded-xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                <Trophy className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Up to 90% Split</h3>
              <p className="text-gray-400">Keep up to 90% of your trading profits</p>
            </div>
            <div className="text-center p-6 bg-white/5 rounded-xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
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

