import { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, Users, DollarSign, Calendar, Download } from 'lucide-react';
import AffiliateLayout from '../../components/affiliate/AffiliateLayout';

export default function Reports() {
  const [period, setPeriod] = useState('this_month');
  const [isLoading, setIsLoading] = useState(true);
  const [reportData, setReportData] = useState({
    overview: {
      newTraders: 12,
      activeTraders: 32,
      totalCommissions: 4250,
      avgCommissionPerTrader: 132.8,
    },
    performance: {
      passRate: 68.5,
      avgWinRate: 71.2,
      avgProfitPerTrader: 2340,
      fundedAccounts: 11,
    },
    topTraders: [
      { name: 'Bob Wilson', profit: 15890, winRate: 74.3, trades: 124 },
      { name: 'John Trader', profit: 2450, winRate: 68.5, trades: 47 },
      { name: 'Jane Smith', profit: 1230, winRate: 71.2, trades: 32 },
    ],
    monthlyData: [
      { month: 'Jun', traders: 8, commissions: 2400, funded: 3 },
      { month: 'Jul', traders: 10, commissions: 3200, funded: 5 },
      { month: 'Aug', traders: 15, commissions: 4800, funded: 7 },
      { month: 'Sep', traders: 12, commissions: 3850, funded: 6 },
      { month: 'Oct', traders: 14, commissions: 4250, funded: 8 },
    ],
  });

  useEffect(() => {
    loadReportData();
  }, [period]);

  const loadReportData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Data is already set in state
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  const exportReport = () => {
    const reportContent = `
Affiliate Performance Report
Period: ${period}
Generated: ${new Date().toLocaleString()}

OVERVIEW
--------
New Traders: ${reportData.overview.newTraders}
Active Traders: ${reportData.overview.activeTraders}
Total Commissions: $${reportData.overview.totalCommissions}
Avg Commission Per Trader: $${reportData.overview.avgCommissionPerTrader}

PERFORMANCE
-----------
Pass Rate: ${reportData.performance.passRate}%
Avg Win Rate: ${reportData.performance.avgWinRate}%
Avg Profit Per Trader: $${reportData.performance.avgProfitPerTrader}
Funded Accounts: ${reportData.performance.fundedAccounts}

TOP TRADERS
-----------
${reportData.topTraders.map((t, i) => `${i + 1}. ${t.name} - Profit: $${t.profit}, Win Rate: ${t.winRate}%, Trades: ${t.trades}`).join('\n')}
    `.trim();

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `affiliate-report-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
  };

  if (isLoading) {
    return (
      <AffiliateLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="text-gray-300 mt-4">Loading reports...</p>
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
                <h1 className="text-3xl font-bold text-white">Reports & Analytics</h1>
                <p className="text-gray-300 mt-2">Insights into your performance and traders</p>
              </div>
              <button
                onClick={exportReport}
                className="btn btn-primary flex items-center gap-2"
              >
                <Download className="w-5 h-5" />
                Export Report
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Period Filter */}
          <div className="bg-slate-800/50 rounded-lg shadow-sm p-4 mb-6">
            <div className="flex items-center gap-4">
              <Calendar className="w-5 h-5 text-gray-400" />
              <select
                value={period}
                onChange={(e) => setPeriod(e.target.value)}
                className="input"
              >
                <option value="this_week">This Week</option>
                <option value="this_month">This Month</option>
                <option value="last_month">Last Month</option>
                <option value="this_quarter">This Quarter</option>
                <option value="this_year">This Year</option>
              </select>
            </div>
          </div>

          {/* Overview Stats */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-white mb-4">Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-300">New Traders</p>
                    <p className="text-2xl font-bold text-white mt-1">
                      {reportData.overview.newTraders}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Users className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-300">Active Traders</p>
                    <p className="text-2xl font-bold text-white mt-1">
                      {reportData.overview.activeTraders}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-300">Total Commissions</p>
                    <p className="text-2xl font-bold text-white mt-1">
                      ${reportData.overview.totalCommissions.toLocaleString()}
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
                    <p className="text-sm text-gray-300">Avg Per Trader</p>
                    <p className="text-2xl font-bold text-white mt-1">
                      ${reportData.overview.avgCommissionPerTrader.toFixed(2)}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <BarChart3 className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-white mb-4">Performance Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="card">
                <p className="text-sm text-gray-300 mb-2">Pass Rate</p>
                <p className="text-3xl font-bold text-white">{reportData.performance.passRate}%</p>
                <div className="mt-3 w-full bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full" 
                    style={{ width: `${reportData.performance.passRate}%` }}
                  ></div>
                </div>
              </div>

              <div className="card">
                <p className="text-sm text-gray-300 mb-2">Avg Win Rate</p>
                <p className="text-3xl font-bold text-white">{reportData.performance.avgWinRate}%</p>
                <div className="mt-3 w-full bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${reportData.performance.avgWinRate}%` }}
                  ></div>
                </div>
              </div>

              <div className="card">
                <p className="text-sm text-gray-300 mb-2">Avg Profit/Trader</p>
                <p className="text-3xl font-bold text-white">
                  ${reportData.performance.avgProfitPerTrader.toLocaleString()}
                </p>
                <p className="text-sm text-green-600 mt-2">+12.5% vs last period</p>
              </div>

              <div className="card">
                <p className="text-sm text-gray-300 mb-2">Funded Accounts</p>
                <p className="text-3xl font-bold text-white">{reportData.performance.fundedAccounts}</p>
                <p className="text-sm text-gray-300 mt-2">
                  {((reportData.performance.fundedAccounts / reportData.overview.activeTraders) * 100).toFixed(1)}% of active
                </p>
              </div>
            </div>
          </div>

          {/* Monthly Trend Chart */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-white mb-4">Monthly Trends</h2>
            <div className="card">
              <div className="overflow-x-auto">
                <div className="min-w-full">
                  {/* Simple bar chart visualization */}
                  <div className="space-y-4">
                    {reportData.monthlyData.map((data) => (
                      <div key={data.month}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-gray-200">{data.month}</span>
                          <div className="flex gap-4 text-sm text-gray-300">
                            <span>Traders: {data.traders}</span>
                            <span>Commissions: ${data.commissions}</span>
                            <span>Funded: {data.funded}</span>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <div className="flex-1 bg-slate-700 rounded-full h-6 overflow-hidden">
                            <div 
                              className="bg-blue-600 h-full flex items-center justify-end pr-2"
                              style={{ width: `${(data.traders / 20) * 100}%` }}
                            >
                              <span className="text-xs text-white font-medium">{data.traders}</span>
                            </div>
                          </div>
                          <div className="flex-1 bg-slate-700 rounded-full h-6 overflow-hidden">
                            <div 
                              className="bg-green-600 h-full flex items-center justify-end pr-2"
                              style={{ width: `${(data.commissions / 5000) * 100}%` }}
                            >
                              <span className="text-xs text-white font-medium">${data.commissions}</span>
                            </div>
                          </div>
                          <div className="flex-1 bg-slate-700 rounded-full h-6 overflow-hidden">
                            <div 
                              className="bg-yellow-600 h-full flex items-center justify-end pr-2"
                              style={{ width: `${(data.funded / 10) * 100}%` }}
                            >
                              <span className="text-xs text-white font-medium">{data.funded}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-center gap-6 mt-6 pt-4 border-t border-white/10">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-blue-600 rounded"></div>
                      <span className="text-sm text-gray-300">Traders</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-green-600 rounded"></div>
                      <span className="text-sm text-gray-300">Commissions</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-yellow-600 rounded"></div>
                      <span className="text-sm text-gray-300">Funded</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Top Traders */}
          <div>
            <h2 className="text-xl font-bold text-white mb-4">Top Performing Traders</h2>
            <div className="bg-slate-800/50 rounded-lg shadow-sm overflow-hidden">
              <table className="w-full">
                <thead className="bg-slate-900 border-b border-white/10">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Rank
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Trader
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Profit
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Win Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Total Trades
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-slate-800/50 divide-y divide-gray-200">
                  {reportData.topTraders.map((trader, index) => (
                    <tr key={index} className="hover:bg-slate-900">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${
                            index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : 'bg-orange-600'
                          }`}>
                            {index + 1}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-white">{trader.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-bold text-green-600">
                          +${trader.profit.toLocaleString()}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-white">{trader.winRate}%</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-white">{trader.trades}</div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </AffiliateLayout>
  );
}

