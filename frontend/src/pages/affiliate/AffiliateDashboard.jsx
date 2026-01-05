import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from "../../services/api";
import Layout from '../../components/layout/Layout';
import { TrendingUp, DollarSign, MousePointerClick, Users, Link as LinkIcon, Copy, Check, Plus, ExternalLink } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function AffiliateDashboard() {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState({
    stats: {
      total_clicks: 0,
      total_conversions: 0,
      total_earnings: 0,
      pending_commission: 0,
      approved_commission: 0,
      paid_commission: 0
    },
    links: [],
    recent_referrals: []
  });
  const [loading, setLoading] = useState(true);
  const [creatingLink, setCreatingLink] = useState(false);
  const [linkName, setLinkName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [copiedLink, setCopiedLink] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    
    if (!token) {
      navigate('/login?redirect=/affiliate/dashboard');
      return;
    }

    try {
      const response = await api.get(`${API_URL}/affiliate/dashboard`);
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
    
    setCreatingLink(true);
    
    try {
      await api.post(
        `${API_URL}/affiliate/links`,
        { name: linkName }
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

  const copyToClipboard = (link) => {
    navigator.clipboard.writeText(link);
    setCopiedLink(link);
    setTimeout(() => setCopiedLink(null), 2000);
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
          <div className="text-xl text-white">Loading dashboard...</div>
        </div>
      </Layout>
    );
  }

  const stats = dashboard.stats || {};

  return (
    <Layout>
      <div className="min-h-screen bg-slate-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Affiliate Dashboard</h1>
            <p className="text-gray-400">Track your performance and manage your affiliate links</p>
          </div>

          {/* Stats Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="p-6 bg-gradient-to-br from-blue-500/10 to-blue-600/5 backdrop-blur-sm border border-blue-500/20 rounded-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                  <MousePointerClick className="w-6 h-6 text-blue-400" />
                </div>
                <TrendingUp className="w-5 h-5 text-blue-400" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">{stats.total_clicks || 0}</div>
              <div className="text-sm text-gray-400">Total Clicks</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-purple-500/10 to-purple-600/5 backdrop-blur-sm border border-purple-500/20 rounded-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-purple-400" />
                </div>
                <TrendingUp className="w-5 h-5 text-purple-400" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">{stats.total_conversions || 0}</div>
              <div className="text-sm text-gray-400">Conversions</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-green-500/10 to-green-600/5 backdrop-blur-sm border border-green-500/20 rounded-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-400" />
                </div>
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">${(stats.total_earnings || 0).toFixed(2)}</div>
              <div className="text-sm text-gray-400">Total Earnings</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-orange-500/10 to-orange-600/5 backdrop-blur-sm border border-orange-500/20 rounded-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-orange-400" />
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-1">${(stats.pending_commission || 0).toFixed(2)}</div>
              <div className="text-sm text-gray-400">Pending Commission</div>
            </div>
          </div>

          {/* Commission Breakdown */}
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">Commission Breakdown</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <div className="text-sm text-gray-400 mb-2">Pending</div>
                <div className="text-2xl font-bold text-yellow-400">${(stats.pending_commission || 0).toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-400 mb-2">Approved</div>
                <div className="text-2xl font-bold text-green-400">${(stats.approved_commission || 0).toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-400 mb-2">Paid</div>
                <div className="text-2xl font-bold text-blue-400">${(stats.paid_commission || 0).toFixed(2)}</div>
              </div>
            </div>
            <Link
              to="/affiliate/payout"
              className="mt-6 inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-semibold hover:from-blue-600 hover:to-purple-700 transition"
            >
              Request Payout
              <ExternalLink className="w-4 h-4 ml-2" />
            </Link>
          </div>

          {/* Affiliate Links */}
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Your Affiliate Links</h2>
              <button
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="px-4 py-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 transition flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                Create New Link
              </button>
            </div>

            {showCreateForm && (
              <form onSubmit={handleCreateLink} className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={linkName}
                    onChange={(e) => setLinkName(e.target.value)}
                    placeholder="Link name (e.g., 'Facebook Campaign')"
                    className="flex-1 px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                    required
                  />
                  <button
                    type="submit"
                    disabled={creatingLink}
                    className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-semibold hover:from-blue-600 hover:to-purple-700 transition disabled:opacity-50"
                  >
                    {creatingLink ? 'Creating...' : 'Create'}
                  </button>
                </div>
              </form>
            )}

            <div className="space-y-4">
              {dashboard.links && dashboard.links.length > 0 ? (
                dashboard.links.map((link) => (
                  <div key={link.id} className="p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                          <LinkIcon className="w-5 h-5 text-blue-400" />
                        </div>
                        <div>
                          <div className="text-white font-semibold">{link.name}</div>
                          <div className="text-sm text-gray-400">Code: {link.code}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-white font-semibold">{link.clicks} clicks</div>
                        <div className="text-sm text-gray-400">{link.conversions} conversions</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={link.full_url}
                        readOnly
                        className="flex-1 px-3 py-2 bg-slate-800 border border-slate-700 rounded text-gray-300 text-sm"
                      />
                      <button
                        onClick={() => copyToClipboard(link.full_url)}
                        className="px-4 py-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 transition flex items-center gap-2"
                      >
                        {copiedLink === link.full_url ? (
                          <>
                            <Check className="w-4 h-4" />
                            Copied!
                          </>
                        ) : (
                          <>
                            <Copy className="w-4 h-4" />
                            Copy
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-12 text-gray-400">
                  <LinkIcon className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No affiliate links yet. Create your first one!</p>
                </div>
              )}
            </div>
          </div>

          {/* Recent Referrals */}
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl">
            <h2 className="text-2xl font-bold text-white mb-6">Recent Referrals</h2>
            {dashboard.recent_referrals && dashboard.recent_referrals.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-white/10">
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Date</th>
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Link</th>
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Status</th>
                      <th className="text-right py-3 px-4 text-gray-400 font-semibold">Commission</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboard.recent_referrals.map((referral) => (
                      <tr key={referral.id} className="border-b border-white/5 hover:bg-white/5">
                        <td className="py-3 px-4 text-gray-300">{new Date(referral.created_at).toLocaleDateString()}</td>
                        <td className="py-3 px-4 text-gray-300">{referral.link_name}</td>
                        <td className="py-3 px-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            referral.status === 'converted' ? 'bg-green-500/20 text-green-400' :
                            referral.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-gray-500/20 text-gray-400'
                          }`}>
                            {referral.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right text-white font-semibold">
                          ${(referral.commission || 0).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No referrals yet. Start sharing your links!</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </Layout>
  );
}

