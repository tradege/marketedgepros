import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from "../../services/api";
import Layout from '../../components/layout/Layout';
import { DollarSign, CreditCard, Clock, CheckCircle, XCircle, Send } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function AffiliatePayout() {
  const navigate = useNavigate();
  const [balance, setBalance] = useState({
    pending: 0,
    approved: 0,
    paid: 0,
    available: 0
  });
  const [payouts, setPayouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [payoutMethod, setPayoutMethod] = useState('paypal');
  const [payoutDetails, setPayoutDetails] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchPayoutData();
  }, []);

  const fetchPayoutData = async () => {
    
    if (!token) {
      navigate('/login?redirect=/affiliate/payout');
      return;
    }

    try {
      const [balanceRes, payoutsRes] = await Promise.all([
        api.get(`${API_URL}/affiliate/balance`),
        api.get(`${API_URL}/affiliate/payouts`)
      ]);
      
      setBalance(balanceRes.data.balance);
      setPayouts(payoutsRes.data.payouts);
    } catch (err) {
      if (err.response?.status === 404) {
        navigate('/affiliate');
      }
      console.error('Failed to fetch payout data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestPayout = async (e) => {
    e.preventDefault();
    
    setRequesting(true);
    setError('');
    setSuccess('');

    try {
      await api.post(
        `${API_URL}/affiliate/payouts/request`,
        {
          method: payoutMethod,
          details: payoutDetails
        }
      );
      
      setSuccess('Payout request submitted successfully!');
      setShowRequestForm(false);
      setPayoutDetails('');
      fetchPayoutData();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to request payout');
    } finally {
      setRequesting(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
          <div className="text-xl text-white">Loading payout information...</div>
        </div>
      </Layout>
    );
  }

  const minPayout = 50;
  const canRequestPayout = balance.available >= minPayout;

  return (
    <Layout>
      <div className="min-h-screen bg-slate-900 py-12">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Payout Management</h1>
            <p className="text-gray-400">Request payouts and view your payment history</p>
          </div>

          {/* Balance Overview */}
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="p-6 bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 backdrop-blur-sm border border-yellow-500/20 rounded-xl">
              <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center mb-4">
                <Clock className="w-6 h-6 text-yellow-400" />
              </div>
              <div className="text-2xl font-bold text-white mb-1">${balance.pending.toFixed(2)}</div>
              <div className="text-sm text-gray-400">Pending</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-green-500/10 to-green-600/5 backdrop-blur-sm border border-green-500/20 rounded-xl">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
              <div className="text-2xl font-bold text-white mb-1">${balance.approved.toFixed(2)}</div>
              <div className="text-sm text-gray-400">Approved</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-blue-500/10 to-blue-600/5 backdrop-blur-sm border border-blue-500/20 rounded-xl">
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                <DollarSign className="w-6 h-6 text-blue-400" />
              </div>
              <div className="text-2xl font-bold text-white mb-1">${balance.paid.toFixed(2)}</div>
              <div className="text-sm text-gray-400">Paid</div>
            </div>

            <div className="p-6 bg-gradient-to-br from-purple-500/10 to-purple-600/5 backdrop-blur-sm border border-purple-500/20 rounded-xl">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                <CreditCard className="w-6 h-6 text-purple-400" />
              </div>
              <div className="text-2xl font-bold text-white mb-1">${balance.available.toFixed(2)}</div>
              <div className="text-sm text-gray-400">Available</div>
            </div>
          </div>

          {/* Request Payout Section */}
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl mb-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Request Payout</h2>
                <p className="text-gray-400">Minimum payout amount: ${minPayout}</p>
              </div>
              {!showRequestForm && (
                <button
                  onClick={() => setShowRequestForm(true)}
                  disabled={!canRequestPayout}
                  className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-semibold hover:from-blue-600 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <Send className="w-5 h-5" />
                  Request Payout
                </button>
              )}
            </div>

            {!canRequestPayout && !showRequestForm && (
              <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg text-yellow-400">
                You need at least ${minPayout} in available balance to request a payout. 
                Current available: ${balance.available.toFixed(2)}
              </div>
            )}

            {error && (
              <div className="mb-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">
                {error}
              </div>
            )}
            
            {success && (
              <div className="mb-4 p-4 bg-green-500/10 border border-green-500/30 rounded-lg text-green-400">
                {success}
              </div>
            )}

            {showRequestForm && (
              <form onSubmit={handleRequestPayout} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Payout Method
                  </label>
                  <select
                    value={payoutMethod}
                    onChange={(e) => setPayoutMethod(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="paypal">PayPal</option>
                    <option value="bank_transfer">Bank Transfer</option>
                    <option value="crypto">Cryptocurrency</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    {payoutMethod === 'paypal' && 'PayPal Email'}
                    {payoutMethod === 'bank_transfer' && 'Bank Account Details'}
                    {payoutMethod === 'crypto' && 'Crypto Wallet Address'}
                  </label>
                  <textarea
                    value={payoutDetails}
                    onChange={(e) => setPayoutDetails(e.target.value)}
                    placeholder={
                      payoutMethod === 'paypal' ? 'your@email.com' :
                      payoutMethod === 'bank_transfer' ? 'Bank name, Account number, Routing number' :
                      'Wallet address'
                    }
                    rows={3}
                    className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>

                <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-400 text-sm">
                  <strong>Amount to be paid:</strong> ${balance.available.toFixed(2)}
                </div>

                <div className="flex gap-4">
                  <button
                    type="submit"
                    disabled={requesting}
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-semibold hover:from-blue-600 hover:to-purple-700 transition disabled:opacity-50"
                  >
                    {requesting ? 'Submitting...' : 'Submit Request'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowRequestForm(false);
                      setError('');
                      setSuccess('');
                    }}
                    className="px-6 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-300 hover:bg-white/10 transition"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>

          {/* Payout History */}
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl">
            <h2 className="text-2xl font-bold text-white mb-6">Payout History</h2>
            {payouts && payouts.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-white/10">
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Date</th>
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Method</th>
                      <th className="text-left py-3 px-4 text-gray-400 font-semibold">Status</th>
                      <th className="text-right py-3 px-4 text-gray-400 font-semibold">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {payouts.map((payout) => (
                      <tr key={payout.id} className="border-b border-white/5 hover:bg-white/5">
                        <td className="py-3 px-4 text-gray-300">
                          {new Date(payout.requested_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-4 text-gray-300 capitalize">
                          {payout.method.replace('_', ' ')}
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            payout.status === 'paid' ? 'bg-green-500/20 text-green-400' :
                            payout.status === 'approved' ? 'bg-blue-500/20 text-blue-400' :
                            payout.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {payout.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right text-white font-semibold">
                          ${payout.amount.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <CreditCard className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No payout history yet</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </Layout>
  );
}

