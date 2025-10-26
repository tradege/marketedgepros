import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/layout/Layout';
import { DollarSign, TrendingUp, Users, Award, Clock, CreditCard } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function AffiliateLanding() {
  const navigate = useNavigate();
  const [programInfo, setProgramInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [registering, setRegistering] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProgramInfo();
  }, []);

  const fetchProgramInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/affiliate/info`);
      setProgramInfo(response.data.program);
    } catch (err) {
      console.error('Failed to fetch program info:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      navigate('/login?redirect=/affiliate');
      return;
    }

    setRegistering(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post(
        `${API_URL}/affiliate/register`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setSuccess('Successfully registered as affiliate!');
      setTimeout(() => {
        navigate('/affiliate/dashboard');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to register');
    } finally {
      setRegistering(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
          <div className="text-xl text-white">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-slate-900">
        
        {/* Hero Section */}
        <section className="relative pt-32 pb-20 overflow-hidden">
          {/* Background Effects */}
          <div className="absolute inset-0">
            <div className="absolute top-20 left-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
            <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="inline-block mb-4 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full">
              <span className="text-blue-400 text-sm font-semibold">EARN WHILE YOU PROMOTE</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">Join Our </span>
              <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">Affiliate</span>
              <br />
              <span className="bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">Program</span>
            </h1>

            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Earn generous commissions by promoting MarketEdgePros' industry-leading prop trading programs. 
              Help traders succeed while building your income.
            </p>

            {error && (
              <div className="mb-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 max-w-md mx-auto">
                {error}
              </div>
            )}
            
            {success && (
              <div className="mb-4 p-4 bg-green-500/10 border border-green-500/30 rounded-lg text-green-400 max-w-md mx-auto">
                {success}
              </div>
            )}
            
            <button
              onClick={handleRegister}
              disabled={registering || !programInfo?.is_active}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-bold text-lg hover:from-blue-600 hover:to-purple-700 transition transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {registering ? 'Registering...' : 'Join Now - It\'s Free!'}
            </button>

            {/* Commission Highlight */}
            {programInfo && (
              <div className="mt-16 p-8 bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-white/10 rounded-2xl">
                <div className="text-6xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                  {programInfo.commission_rate}%
                </div>
                <div className="text-2xl text-white mb-2">Commission on All Sales</div>
                <div className="text-gray-400">
                  ${programInfo.min_payout} minimum payout • {programInfo.cookie_duration_days}-day cookie duration
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Benefits Grid */}
        <section className="py-20 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">Why Join Our Program?</h2>
              <p className="text-gray-400 text-lg">Everything you need to succeed as an affiliate</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <DollarSign className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">High Commissions</h3>
                <p className="text-gray-400">
                  Earn {programInfo?.commission_rate}% commission on every sale you refer. No limits on your earnings potential.
                </p>
              </div>

              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Real-Time Tracking</h3>
                <p className="text-gray-400">
                  Monitor your clicks, conversions, and earnings in real-time with our comprehensive dashboard.
                </p>
              </div>

              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-orange-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <Award className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Marketing Materials</h3>
                <p className="text-gray-400">
                  Access professional banners, landing pages, and email templates to maximize your conversions.
                </p>
              </div>

              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <Clock className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Long Cookie Duration</h3>
                <p className="text-gray-400">
                  {programInfo?.cookie_duration_days}-day cookie ensures you get credit for sales even if they don't convert immediately.
                </p>
              </div>

              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-yellow-500 to-green-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <CreditCard className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Monthly Payouts</h3>
                <p className="text-gray-400">
                  Receive your earnings monthly via PayPal, bank transfer, or crypto. Minimum payout: ${programInfo?.min_payout}.
                </p>
              </div>

              <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition group">
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <Users className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Dedicated Support</h3>
                <p className="text-gray-400">
                  Get help from our affiliate team whenever you need it. We're here to help you succeed.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 relative">
          <div className="absolute inset-0">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
              <p className="text-gray-400 text-lg">Start earning in 4 simple steps</p>
            </div>
            
            <div className="grid md:grid-cols-4 gap-8">
              {[
                { num: 1, title: 'Sign Up', desc: 'Register for free and get instant access to your affiliate dashboard' },
                { num: 2, title: 'Get Your Link', desc: 'Receive your unique referral link and marketing materials' },
                { num: 3, title: 'Promote', desc: 'Share your link on social media, blogs, or with your network' },
                { num: 4, title: 'Earn Money', desc: `Get paid ${programInfo?.commission_rate}% commission on every sale you refer` }
              ].map((step) => (
                <div key={step.num} className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                    {step.num}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
                  <p className="text-gray-400 text-sm">{step.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 relative">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="p-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-white/10 rounded-2xl">
              <h2 className="text-4xl font-bold text-white mb-4">Ready to Start Earning?</h2>
              <p className="text-xl text-gray-300 mb-8">
                Join hundreds of affiliates already earning with MarketEdgePros
              </p>
              <button
                onClick={handleRegister}
                disabled={registering || !programInfo?.is_active}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-bold text-lg hover:from-blue-600 hover:to-purple-700 transition transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {registering ? 'Registering...' : 'Join the Affiliate Program'}
              </button>
            </div>
          </div>
        </section>

      </div>
    </Layout>
  );
}
