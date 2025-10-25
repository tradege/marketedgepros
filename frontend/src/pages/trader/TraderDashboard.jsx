import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  TrendingUp, TrendingDown, DollarSign, Activity,
  AlertTriangle, CheckCircle, Clock, Award, ArrowUpRight
} from 'lucide-react';
import TraderLayout from '../../components/trader/TraderLayout';
import api from '../../services/api';

export default function TraderDashboard() {
  const [accountData, setAccountData] = useState({
    balance: 102450,
    equity: 103200,
    profitLoss: 2450,
    profitLossPercent: 2.45,
    dailyProfitLoss: 450,
    drawdown: 1.2,
    maxDrawdown: 5.0,
    challengePhase: 'Phase 2',
    daysTraded: 12,
    minDaysRequired: 15,
    profitTarget: 5000,
    profitAchieved: 2450,
  });

  const [recentTrades, setRecentTrades] = useState([]);
  const [stats, setStats] = useState({
    totalTrades: 47,
    winningTrades: 32,
    losingTrades: 15,
    winRate: 68.1,
    avgWin: 245,
    avgLoss: 120,
    profitFactor: 2.04,
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch real data from API
      const response = await api.get('/traders/dashboard');
      const data = response.data;
      
      if (!data.has_challenge) {
        // No active challenge
        setAccountData({
          balance: 0,
          equity: 0,
          profitLoss: 0,
          profitLossPercent: 0,
          dailyProfitLoss: 0,
          drawdown: 0,
          maxDrawdown: 0,
          challengePhase: 'No Active Challenge',
          daysTraded: 0,
          minDaysRequired: 0,
          profitTarget: 0,
          profitAchieved: 0,
        });
        setStats({
          totalTrades: 0,
          winningTrades: 0,
          losingTrades: 0,
          winRate: 0,
          avgWin: 0,
          avgLoss: 0,
          profitFactor: 0,
        });
        setRecentTrades([]);
        return;
      }
      
      // Set account data from API
      setAccountData({
        balance: data.account.balance,
        equity: data.account.equity,
        profitLoss: data.account.total_pnl,
        profitLossPercent: data.account.total_pnl_percentage,
        dailyProfitLoss: 0, // Not provided by API
        drawdown: data.drawdown.current,
        maxDrawdown: data.drawdown.max_allowed,
        challengePhase: data.challenge.phase || 'Phase 1',
        daysTraded: data.progress.days.completed,
        minDaysRequired: data.progress.days.required,
        profitTarget: data.progress.profit.target,
        profitAchieved: data.progress.profit.achieved,
      });
      
      // Set statistics from API
      setStats({
        totalTrades: data.statistics.total_trades,
        winningTrades: data.statistics.winning_trades,
        losingTrades: data.statistics.losing_trades,
        winRate: data.statistics.win_rate,
        avgWin: data.statistics.average_win,
        avgLoss: Math.abs(data.statistics.average_loss),
        profitFactor: data.statistics.profit_factor,
      });
      
      // Set recent trades from API
      if (data.recent_trades) {
        setRecentTrades(data.recent_trades.map(trade => ({
          id: trade.id,
          symbol: trade.symbol,
          type: trade.type,
          openTime: new Date(trade.open_time).toLocaleString(),
          closeTime: trade.close_time ? new Date(trade.close_time).toLocaleString() : 'Open',
          lots: trade.lots,
          profit: trade.profit,
          pips: trade.pips,
        })));
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      // Keep default mock data on error
    } finally {
      setIsLoading(false);
    }
  };

  const profitTargetPercent = (accountData.profitAchieved / accountData.profitTarget) * 100;
  const daysProgress = (accountData.daysTraded / accountData.minDaysRequired) * 100;

  if (isLoading) {
    return (
      <TraderLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="text-gray-600 mt-4">Loading dashboard...</p>
          </div>
        </div>
      </TraderLayout>
    );
  }

  return (
    <TraderLayout>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Trader Dashboard</h1>
                <p className="text-gray-600 mt-2">Monitor your trading performance</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg font-medium">
                  {accountData.challengePhase}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Account Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Balance</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    ${accountData.balance.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Equity</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    ${accountData.equity.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Activity className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total P&L</p>
                  <p className={`text-2xl font-bold mt-1 ${accountData.profitLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {accountData.profitLoss >= 0 ? '+' : ''}${accountData.profitLoss.toLocaleString()}
                  </p>
                  <p className={`text-xs mt-1 ${accountData.profitLossPercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {accountData.profitLossPercent >= 0 ? '+' : ''}{accountData.profitLossPercent}%
                  </p>
                </div>
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                  accountData.profitLoss >= 0 ? 'bg-green-100' : 'bg-red-100'
                }`}>
                  {accountData.profitLoss >= 0 ? (
                    <TrendingUp className="w-6 h-6 text-green-600" />
                  ) : (
                    <TrendingDown className="w-6 h-6 text-red-600" />
                  )}
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Drawdown</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    {accountData.drawdown}%
                  </p>
                  <p className="text-xs text-gray-600 mt-1">
                    Max: {accountData.maxDrawdown}%
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </div>
          </div>

          {/* Challenge Progress */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div className="card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Profit Target Progress</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Target</span>
                  <span className="text-sm font-medium text-gray-900">${accountData.profitTarget.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Achieved</span>
                  <span className="text-sm font-bold text-green-600">${accountData.profitAchieved.toLocaleString()}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    className="bg-green-600 h-4 rounded-full flex items-center justify-end pr-2"
                    style={{ width: `${Math.min(profitTargetPercent, 100)}%` }}
                  >
                    <span className="text-xs text-white font-medium">{profitTargetPercent.toFixed(1)}%</span>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  ${(accountData.profitTarget - accountData.profitAchieved).toLocaleString()} remaining
                </p>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Trading Days Progress</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Required</span>
                  <span className="text-sm font-medium text-gray-900">{accountData.minDaysRequired} days</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Completed</span>
                  <span className="text-sm font-bold text-blue-600">{accountData.daysTraded} days</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    className="bg-blue-600 h-4 rounded-full flex items-center justify-end pr-2"
                    style={{ width: `${Math.min(daysProgress, 100)}%` }}
                  >
                    <span className="text-xs text-white font-medium">{daysProgress.toFixed(1)}%</span>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  {accountData.minDaysRequired - accountData.daysTraded} days remaining
                </p>
              </div>
            </div>
          </div>

          {/* Trading Statistics */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Trading Statistics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Total Trades</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalTrades}</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Winning</p>
                <p className="text-2xl font-bold text-green-600">{stats.winningTrades}</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Losing</p>
                <p className="text-2xl font-bold text-red-600">{stats.losingTrades}</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Win Rate</p>
                <p className="text-2xl font-bold text-gray-900">{stats.winRate}%</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Avg Win</p>
                <p className="text-2xl font-bold text-green-600">${stats.avgWin}</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Avg Loss</p>
                <p className="text-2xl font-bold text-red-600">${stats.avgLoss}</p>
              </div>
              <div className="card text-center">
                <p className="text-sm text-gray-600 mb-1">Profit Factor</p>
                <p className="text-2xl font-bold text-gray-900">{stats.profitFactor}</p>
              </div>
            </div>
          </div>

          {/* Recent Trades */}
          <div className="card mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">Recent Trades</h2>
              <Link to="/trader/history" className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1">
                View All
                <ArrowUpRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Symbol</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Lots</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Open Time</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Close Time</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pips</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Profit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {recentTrades.map((trade) => (
                    <tr key={trade.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{trade.symbol}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.type === 'buy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {trade.type.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">{trade.lots}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{trade.openTime}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{trade.closeTime}</td>
                      <td className={`px-4 py-3 text-sm font-medium ${trade.pips >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {trade.pips >= 0 ? '+' : ''}{trade.pips}
                      </td>
                      <td className={`px-4 py-3 text-sm font-bold ${trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {trade.profit >= 0 ? '+' : ''}${trade.profit}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link to="/trader/history" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <TrendingUp className="w-8 h-8 text-primary-600" />
                <div>
                  <p className="font-medium text-gray-900">Trading History</p>
                  <p className="text-sm text-gray-600">View all your trades</p>
                </div>
              </div>
            </Link>

            <Link to="/trader/withdrawals" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <DollarSign className="w-8 h-8 text-green-600" />
                <div>
                  <p className="font-medium text-gray-900">Withdrawals</p>
                  <p className="text-sm text-gray-600">Request payout</p>
                </div>
              </div>
            </Link>

            <Link to="/trader/documents" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <Award className="w-8 h-8 text-yellow-600" />
                <div>
                  <p className="font-medium text-gray-900">Documents</p>
                  <p className="text-sm text-gray-600">Upload KYC documents</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </TraderLayout>
  );
}

