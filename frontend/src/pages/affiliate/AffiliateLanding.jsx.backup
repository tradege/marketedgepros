import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/layout/Layout';

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
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-xl">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Join Our Affiliate Program
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Earn generous commissions by promoting MarketEdgePros' industry-leading prop trading programs. 
              Help traders succeed while building your income.
            </p>
            
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 max-w-md mx-auto">
                {error}
              </div>
            )}
            
            {success && (
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-600 max-w-md mx-auto">
                {success}
              </div>
            )}
            
            <button
              onClick={handleRegister}
              disabled={registering || !programInfo?.is_active}
              className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {registering ? 'Registering...' : 'Join Now - It\'s Free!'}
            </button>
          </div>

          {/* Commission Highlight */}
          {programInfo && (
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white text-center mb-16">
              <div className="text-6xl font-bold mb-2">{programInfo.commission_rate}%</div>
              <div className="text-2xl">Commission on All Sales</div>
              <div className="mt-4 text-purple-100">
                Earn ${programInfo.min_payout} minimum payout • {programInfo.cookie_duration_days}-day cookie duration
              </div>
            </div>
          )}

          {/* Benefits Grid */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-bold mb-3">High Commissions</h3>
              <p className="text-gray-600">
                Earn {programInfo?.commission_rate}% commission on every sale you refer. No limits on your earnings potential.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-3">Real-Time Tracking</h3>
              <p className="text-gray-600">
                Monitor your clicks, conversions, and earnings in real-time with our comprehensive dashboard.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-3">Marketing Materials</h3>
              <p className="text-gray-600">
                Access professional banners, landing pages, and email templates to maximize your conversions.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">⏰</div>
              <h3 className="text-xl font-bold mb-3">Long Cookie Duration</h3>
              <p className="text-gray-600">
                {programInfo?.cookie_duration_days}-day cookie ensures you get credit for sales even if they don't convert immediately.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">💳</div>
              <h3 className="text-xl font-bold mb-3">Monthly Payouts</h3>
              <p className="text-gray-600">
                Receive your earnings monthly via PayPal, bank transfer, or crypto. Minimum payout: ${programInfo?.min_payout}.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">🤝</div>
              <h3 className="text-xl font-bold mb-3">Dedicated Support</h3>
              <p className="text-gray-600">
                Get help from our affiliate team whenever you need it. We're here to help you succeed.
              </p>
            </div>
          </div>

          {/* How It Works */}
          <div className="bg-white rounded-2xl p-12 shadow-lg mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            
            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  1
                </div>
                <h3 className="font-bold mb-2">Sign Up</h3>
                <p className="text-gray-600 text-sm">
                  Register for free and get instant access to your affiliate dashboard
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  2
                </div>
                <h3 className="font-bold mb-2">Get Your Link</h3>
                <p className="text-gray-600 text-sm">
                  Receive your unique referral link and marketing materials
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  3
                </div>
                <h3 className="font-bold mb-2">Promote</h3>
                <p className="text-gray-600 text-sm">
                  Share your link on social media, blogs, or with your network
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  4
                </div>
                <h3 className="font-bold mb-2">Earn Money</h3>
                <p className="text-gray-600 text-sm">
                  Get paid {programInfo?.commission_rate}% commission on every sale you refer
                </p>
              </div>
            </div>
          </div>

          {/* FAQ */}
          <div className="bg-white rounded-2xl p-12 shadow-lg mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
            
            <div className="space-y-6 max-w-3xl mx-auto">
              <div>
                <h3 className="font-bold mb-2">How much can I earn?</h3>
                <p className="text-gray-600">
                  There's no limit! You earn {programInfo?.commission_rate}% on every sale. Top affiliates earn $5,000+ per month.
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2">When do I get paid?</h3>
                <p className="text-gray-600">
                  Payouts are processed monthly. You can request a payout once you reach the minimum of ${programInfo?.min_payout}.
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2">What payment methods do you support?</h3>
                <p className="text-gray-600">
                  We support PayPal, bank transfer, and cryptocurrency payments.
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2">Do I need a website?</h3>
                <p className="text-gray-600">
                  No! You can promote via social media, YouTube, email lists, or any other channel.
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2">How long does the cookie last?</h3>
                <p className="text-gray-600">
                  Our cookie lasts {programInfo?.cookie_duration_days} days, giving you credit for sales even if they don't convert immediately.
                </p>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Start Earning?</h2>
            <p className="text-xl text-gray-600 mb-8">
              Join hundreds of affiliates already earning with MarketEdgePros
            </p>
            <button
              onClick={handleRegister}
              disabled={registering || !programInfo?.is_active}
              className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {registering ? 'Registering...' : 'Join the Affiliate Program'}
            </button>
          </div>

        </div>
      </div>
    </Layout>
  );
}

