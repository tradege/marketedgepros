import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/layout/Layout';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function AffiliateDashboard() {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [creatingLink, setCreatingLink] = useState(false);
  const [linkName, setLinkName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [copiedLink, setCopiedLink] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      navigate('/login?redirect=/affiliate/dashboard');
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/affiliate/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDashboard(response.data);
    } catch (err) {
      if (err.response?.status === 404) {
        navigate('/affiliate');
      }
      console.error('Failed to fetch dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLink = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    
    setCreatingLink(true);
    
    try {
      await axios.post(
        `${API_URL}/affiliate/links`,
        { name: linkName },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setLinkName('');
      setShowCreateForm(false);
      fetchDashboard();
    } catch (err) {
      console.error('Failed to create link:', err);
    } finally {
      setCreatingLink(false);
    }
  };

  const copyToClipboard = (url, id) => {
    navigator.clipboard.writeText(url);
    setCopiedLink(id);
    setTimeout(() => setCopiedLink(null), 2000);
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

  if (!dashboard) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-xl">Failed to load dashboard</div>
        </div>
      </Layout>
    );
  }

  const { stats, links, recent_referrals } = dashboard;

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Affiliate Dashboard
            </h1>
            <p className="text-gray-600">Track your performance and manage your affiliate links</p>
          </div>

          {/* Stats Grid */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-gray-600 text-sm mb-1">Total Clicks</div>
              <div className="text-3xl font-bold text-purple-600">{stats.total_clicks}</div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-gray-600 text-sm mb-1">Conversions</div>
              <div className="text-3xl font-bold text-blue-600">{stats.total_conversions}</div>
              <div className="text-sm text-gray-500 mt-1">{stats.conversion_rate}% rate</div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-gray-600 text-sm mb-1">Total Revenue</div>
              <div className="text-3xl font-bold text-green-600">${stats.total_revenue.toFixed(2)}</div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-gray-600 text-sm mb-1">Total Commission</div>
              <div className="text-3xl font-bold text-purple-600">${stats.total_commission.toFixed(2)}</div>
            </div>
          </div>

          {/* Commission Breakdown */}
          <div className="bg-white rounded-xl p-8 shadow-lg mb-12">
            <h2 className="text-2xl font-bold mb-6">Commission Breakdown</h2>
            
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <div className="text-gray-600 text-sm mb-1">Pending</div>
                <div className="text-2xl font-bold text-yellow-600">${stats.pending_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500">Awaiting approval</div>
              </div>

              <div>
                <div className="text-gray-600 text-sm mb-1">Approved</div>
                <div className="text-2xl font-bold text-green-600">${stats.approved_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500">Ready for payout</div>
              </div>

              <div>
                <div className="text-gray-600 text-sm mb-1">Paid</div>
                <div className="text-2xl font-bold text-blue-600">${stats.paid_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500">Already received</div>
              </div>
            </div>

            {stats.approved_commission > 0 && (
              <div className="mt-6">
                <Link
                  to="/affiliate/payout"
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all inline-block"
                >
                  Request Payout (${stats.approved_commission.toFixed(2)})
                </Link>
              </div>
            )}
          </div>

          {/* Affiliate Links */}
          <div className="bg-white rounded-xl p-8 shadow-lg mb-12">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Your Affiliate Links</h2>
              <button
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:shadow-lg transition-all"
              >
                {showCreateForm ? 'Cancel' : 'Create New Link'}
              </button>
            </div>

            {showCreateForm && (
              <form onSubmit={handleCreateLink} className="mb-6 p-4 bg-gray-50 rounded-lg">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Link Name
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={linkName}
                    onChange={(e) => setLinkName(e.target.value)}
                    placeholder="e.g., YouTube Campaign, Blog Post"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                  <button
                    type="submit"
                    disabled={creatingLink}
                    className="bg-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors disabled:opacity-50"
                  >
                    {creatingLink ? 'Creating...' : 'Create'}
                  </button>
                </div>
              </form>
            )}

            <div className="space-y-4">
              {links.map((link) => (
                <div key={link.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-bold text-lg">{link.name}</h3>
                      <div className="text-sm text-gray-500">Code: {link.code}</div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      link.is_active 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-gray-100 text-gray-700'
                    }`}>
                      {link.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>

                  <div className="bg-gray-50 p-3 rounded-lg mb-3 flex items-center justify-between">
                    <code className="text-sm text-gray-700 break-all">{link.url}</code>
                    <button
                      onClick={() => copyToClipboard(link.url, link.id)}
                      className="ml-2 px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition-colors whitespace-nowrap"
                    >
                      {copiedLink === link.id ? 'Copied!' : 'Copy'}
                    </button>
                  </div>

                  <div className="grid grid-cols-4 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-purple-600">{link.clicks}</div>
                      <div className="text-xs text-gray-500">Clicks</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-blue-600">{link.conversions}</div>
                      <div className="text-xs text-gray-500">Conversions</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-600">${link.total_revenue.toFixed(0)}</div>
                      <div className="text-xs text-gray-500">Revenue</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-purple-600">${link.total_commission.toFixed(0)}</div>
                      <div className="text-xs text-gray-500">Commission</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Referrals */}
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <h2 className="text-2xl font-bold mb-6">Recent Referrals</h2>
            
            {recent_referrals.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No referrals yet. Start promoting your links!
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">User</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                      <th className="text-right py-3 px-4 font-semibold text-gray-700">Purchase</th>
                      <th className="text-right py-3 px-4 font-semibold text-gray-700">Commission</th>
                      <th className="text-right py-3 px-4 font-semibold text-gray-700">Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recent_referrals.map((referral) => (
                      <tr key={referral.id} className="border-b border-gray-100">
                        <td className="py-3 px-4">
                          {referral.referred_user ? referral.referred_user.email : 'Pending'}
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            referral.status === 'converted'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}>
                            {referral.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right">
                          ${referral.purchase_amount ? referral.purchase_amount.toFixed(2) : '0.00'}
                        </td>
                        <td className="py-3 px-4 text-right font-semibold text-purple-600">
                          ${referral.commission_amount ? referral.commission_amount.toFixed(2) : '0.00'}
                        </td>
                        <td className="py-3 px-4 text-right text-sm text-gray-500">
                          {new Date(referral.click_date).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

        </div>
      </div>
    </Layout>
  );
}

