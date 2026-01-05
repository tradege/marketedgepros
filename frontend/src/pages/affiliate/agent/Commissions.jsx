import { useEffect, useState } from 'react';
import { DollarSign, TrendingUp, Clock, CheckCircle, Download, Calendar } from 'lucide-react';
import AffiliateLayout from '../../componen../affiliate/AffiliateLayout';
import api from '../../services/api';

export default function Commissions() {
  const [commissions, setCommissions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterPeriod, setFilterPeriod] = useState('all');
  const [stats, setStats] = useState({
    totalEarned: 0,
    pendingCommissions: 0,
    paidCommissions: 0,
    thisMonth: 0,
  });

  useEffect(() => {
    loadCommissions();
  }, []);

  const loadCommissions = async () => {
    try {
      setIsLoading(true);
      
      // Fetch commissions from real API
      const commissionsResponse = await api.get('/api/v1/commissions');
      const commissionsData = commissionsResponse.data.commissions || [];
      
      // Transform API data to match component format
      const transformedCommissions = commissionsData.map(commission => ({
        id: commission.id,
        date: commission.created_at,
        trader: {
          name: commission.referral?.referred_user?.name || 'N/A',
          email: commission.referral?.referred_user?.email || 'N/A'
        },
        type: 'enrollment', // Default type
        program: `Challenge #${commission.challenge_id}`,
        amount: commission.commission_amount,
        rate: commission.commission_rate,
        status: commission.status,
        payout_date: commission.paid_at
      }));
      
      setCommissions(transformedCommissions);
      
      // Fetch stats from real API
      const statsResponse = await api.get('/api/v1/commissions/stats');
      const statsData = statsResponse.data;
      
      setStats({
        totalEarned: statsData.total_earned || 0,
        pendingCommissions: statsData.pending_balance || 0,
        paidCommissions: statsData.paid?.amount || 0,
        thisMonth: statsData.pending?.amount || 0 // Approximation
      });
      
    } catch (error) {
      setCommissions([]);
      setStats({
        totalEarned: 0,
        pendingCommissions: 0,
        paidCommissions: 0,
        thisMonth: 0
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Removed calculateStats - now fetched from API

  const exportCommissions = () => {
    const headers = ['Date', 'Trader', 'Type', 'Program', 'Amount', 'Rate', 'Status', 'Payout Date'];
    const rows = filteredCommissions.map((commission) => [
      new Date(commission.date).toLocaleDateString(),
      commission.trader.name,
      commission.type,
      commission.program,
      commission.amount,
      `${commission.rate}%`,
      commission.status,
      commission.payout_date ? new Date(commission.payout_date).toLocaleDateString() : 'Pending',
    ]);

    const csv = [headers, ...rows].map((row) => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `commissions-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  const filteredCommissions = commissions.filter((commission) => {
    if (filterPeriod === 'all') return true;
    
    const commissionDate = new Date(commission.date);
    const now = new Date();
    
    if (filterPeriod === 'this_month') {
      return commissionDate.getMonth() === now.getMonth() && 
             commissionDate.getFullYear() === now.getFullYear();
    } else if (filterPeriod === 'last_month') {
      const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1);
      return commissionDate.getMonth() === lastMonth.getMonth() && 
             commissionDate.getFullYear() === lastMonth.getFullYear();
    } else if (filterPeriod === 'this_year') {
      return commissionDate.getFullYear() === now.getFullYear();
    }
    
    return true;
  });

  const getTypeColor = (type) => {
    switch (type) {
      case 'enrollment':
        return 'bg-blue-100 text-blue-800';
      case 'profit_share':
        return 'bg-green-100 text-green-800';
      case 'renewal':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-slate-700/50 text-gray-100';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-slate-700/50 text-gray-100';
    }
  };

  if (isLoading) {
    return (
      <AffiliateLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="text-gray-300 mt-4">Loading commissions...</p>
          </div>
        </div>
      </AffiliateLayout>
    );
  }

  return (
    <AffiliateLayout>
      <div className="min-h-screen bg-slate-900">
        {/* Header */}
        <div className="bg-slate-800/50 border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Commissions</h1>
                <p className="text-gray-300 mt-2">Track your earnings and payouts</p>
              </div>
              <button
                onClick={exportCommissions}
                className="btn btn-primary flex items-center gap-2"
              >
                <Download className="w-5 h-5" />
                Export
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Total Earned</p>
                  <p className="text-2xl font-bold text-white mt-1">
                    ${stats.totalEarned.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">This Month</p>
                  <p className="text-2xl font-bold text-white mt-1">
                    ${stats.thisMonth.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Pending</p>
                  <p className="text-2xl font-bold text-white mt-1">
                    ${stats.pendingCommissions.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Paid Out</p>
                  <p className="text-2xl font-bold text-white mt-1">
                    ${stats.paidCommissions.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>
          </div>

          {/* Filter */}
          <div className="bg-slate-800/50 rounded-lg shadow-sm p-4 mb-6">
            <div className="flex items-center gap-4">
              <Calendar className="w-5 h-5 text-gray-400" />
              <select
                value={filterPeriod}
                onChange={(e) => setFilterPeriod(e.target.value)}
                className="input"
              >
                <option value="all">All Time</option>
                <option value="this_month">This Month</option>
                <option value="last_month">Last Month</option>
                <option value="this_year">This Year</option>
              </select>
            </div>
          </div>

          {/* Commissions Table */}
          <div className="bg-slate-800/50 rounded-lg shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-900 border-b border-white/10">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Trader
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Program
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Payout Date
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-slate-800/50 divide-y divide-gray-200">
                  {filteredCommissions.map((commission) => (
                    <tr key={commission.id} className="hover:bg-slate-900">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                        {new Date(commission.date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-white">{commission.trader.name}</div>
                        <div className="text-sm text-gray-400">{commission.trader.email}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(commission.type)}`}>
                          {commission.type.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-white">
                        {commission.program}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                        {commission.rate}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-white">
                        ${commission.amount}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(commission.status)}`}>
                          {commission.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                        {commission.payout_date 
                          ? new Date(commission.payout_date).toLocaleDateString()
                          : 'Pending'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {filteredCommissions.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-300">No commissions found</p>
              </div>
            )}
          </div>

          {/* Commission Types Info */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="font-bold text-white">Enrollment Commission</h3>
              </div>
              <p className="text-sm text-gray-300">
                Earn commission when a trader enrolls in a program through your referral link.
              </p>
              <p className="text-lg font-bold text-blue-600 mt-2">30% Rate</p>
            </div>

            <div className="card">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="font-bold text-white">Profit Share Commission</h3>
              </div>
              <p className="text-sm text-gray-300">
                Earn commission from the profits generated by your traders on funded accounts.
              </p>
              <p className="text-lg font-bold text-green-600 mt-2">10% Rate</p>
            </div>

            <div className="card">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-5 h-5 text-purple-600" />
                </div>
                <h3 className="font-bold text-white">Renewal Commission</h3>
              </div>
              <p className="text-sm text-gray-300">
                Earn commission when your traders renew their challenge or upgrade their account.
              </p>
              <p className="text-lg font-bold text-purple-600 mt-2">20% Rate</p>
            </div>
          </div>
        </div>
      </div>
    </AffiliateLayout>
  );
}

