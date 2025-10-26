import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/layout/Layout';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function AffiliatePayout() {
  const navigate = useNavigate();
  const [payouts, setPayouts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [payoutMethod, setPayoutMethod] = useState('paypal');
  const [payoutDetails, setPayoutDetails] = useState('');
  const [amount, setAmount] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      navigate('/login?redirect=/affiliate/payout');
      return;
    }

    try {
      const [payoutsRes, dashboardRes] = await Promise.all([
        axios.get(`${API_URL}/affiliate/payouts`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API_URL}/affiliate/dashboard`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);
      
      setPayouts(payoutsRes.data.payouts);
      setStats(dashboardRes.data.stats);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestPayout = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    
    setRequesting(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(
        `${API_URL}/affiliate/payouts/request`,
        {
          amount: parseFloat(amount),
          payout_method: payoutMethod,
          payout_details: payoutDetails
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setSuccess('Payout request submitted successfully!');
      setAmount('');
      setPayoutDetails('');
      fetchData();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to request payout');
    } finally {
      setRequesting(false);
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

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-700';
      case 'approved': return 'bg-blue-100 text-blue-700';
      case 'paid': return 'bg-green-100 text-green-700';
      case 'rejected': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Payout Management
            </h1>
            <p className="text-gray-600">Request payouts and view your payout history</p>
          </div>

          {/* Balance Overview */}
          {stats && (
            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="bg-white rounded-xl p-6 shadow-lg">
                <div className="text-gray-600 text-sm mb-1">Pending Commission</div>
                <div className="text-3xl font-bold text-yellow-600">${stats.pending_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500 mt-1">Awaiting approval</div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg">
                <div className="text-gray-600 text-sm mb-1">Available for Payout</div>
                <div className="text-3xl font-bold text-green-600">${stats.approved_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500 mt-1">Ready to withdraw</div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg">
                <div className="text-gray-600 text-sm mb-1">Total Paid</div>
                <div className="text-3xl font-bold text-blue-600">${stats.paid_commission.toFixed(2)}</div>
                <div className="text-sm text-gray-500 mt-1">All-time earnings</div>
              </div>
            </div>
          )}

          {/* Request Payout Form */}
          <div className="bg-white rounded-xl p-8 shadow-lg mb-12">
            <h2 className="text-2xl font-bold mb-6">Request Payout</h2>
            
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
                {error}
              </div>
            )}
            
            {success && (
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-600">
                {success}
              </div>
            )}

            {stats && stats.approved_commission > 0 ? (
              <form onSubmit={handleRequestPayout} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Amount (USD)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="50"
                    max={stats.approved_commission}
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder={`Max: $${stats.approved_commission.toFixed(2)}`}
                    required
                  />
                  <div className="text-sm text-gray-500 mt-1">
                    Minimum payout: $50.00
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Payout Method
                  </label>
                  <select
                    value={payoutMethod}
                    onChange={(e) => setPayoutMethod(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    <option value="paypal">PayPal</option>
                    <option value="bank_transfer">Bank Transfer</option>
                    <option value="crypto">Cryptocurrency</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {payoutMethod === 'paypal' && 'PayPal Email'}
                    {payoutMethod === 'bank_transfer' && 'Bank Account Details'}
                    {payoutMethod === 'crypto' && 'Crypto Wallet Address'}
                  </label>
                  <textarea
                    value={payoutDetails}
                    onChange={(e) => setPayoutDetails(e.target.value)}
                    rows="3"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder={
                      payoutMethod === 'paypal' 
                        ? 'your-email@example.com'
                        : payoutMethod === 'bank_transfer'
                        ? 'Bank Name, Account Number, Routing Number, etc.'
                        : 'Your wallet address'
                    }
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={requesting}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {requesting ? 'Submitting...' : 'Request Payout'}
                </button>
              </form>
            ) : (
              <div className="text-center py-8">
                <div className="text-gray-500 mb-4">
                  You don't have enough approved commission to request a payout.
                </div>
                <div className="text-sm text-gray-400">
                  Minimum payout amount: $50.00
                </div>
              </div>
            )}
          </div>

          {/* Payout History */}
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <h2 className="text-2xl font-bold mb-6">Payout History</h2>
            
            {payouts.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No payout requests yet.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Amount</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Method</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Paid Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {payouts.map((payout) => (
                      <tr key={payout.id} className="border-b border-gray-100">
                        <td className="py-3 px-4 text-sm text-gray-600">
                          {new Date(payout.request_date).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-4 font-semibold">
                          ${payout.amount.toFixed(2)}
                        </td>
                        <td className="py-3 px-4 text-sm">
                          {payout.payout_method.replace('_', ' ').toUpperCase()}
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(payout.status)}`}>
                            {payout.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-sm text-gray-600">
                          {payout.paid_date 
                            ? new Date(payout.paid_date).toLocaleDateString()
                            : '-'
                          }
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Info Box */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-bold text-blue-900 mb-2">Payout Information</h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>• Minimum payout amount: $50.00</li>
              <li>• Payouts are processed within 5-7 business days</li>
              <li>• You can only request payouts for approved commissions</li>
              <li>• PayPal payouts are usually fastest (1-2 days)</li>
              <li>• Bank transfers may take 3-5 business days</li>
              <li>• Cryptocurrency payouts are processed within 24 hours</li>
            </ul>
          </div>

        </div>
      </div>
    </Layout>
  );
}

