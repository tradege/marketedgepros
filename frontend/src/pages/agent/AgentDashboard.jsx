import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Users, DollarSign, TrendingUp, Award,
  CheckCircle, Clock, XCircle, ArrowUpRight
} from 'lucide-react';
import AgentLayout from '../../components/agent/AgentLayout';
import api from '../../services/api';

export default function AgentDashboard() {
  const [stats, setStats] = useState({
    totalTraders: 0,
    activeTraders: 0,
    totalCommissions: 0,
    pendingCommissions: 0,
    activeChallenges: 0,
    passedChallenges: 0,
    failedChallenges: 0,
    fundedAccounts: 0,
  });

  const [recentTraders, setRecentTraders] = useState([]);
  const [recentCommissions, setRecentCommissions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch real data from API
      const [dashboardResponse, commissionsResponse] = await Promise.all([
        api.get('/reports/agent/dashboard'),
        api.get('/commissions')
      ]);

      const dashboardData = dashboardResponse.data;
      const commissionsData = commissionsResponse.data;

      // Set stats from API
      setStats({
        totalTraders: dashboardData.total_referrals || 0,
        activeTraders: dashboardData.active_traders || 0,
        totalCommissions: dashboardData.total_earned || 0,
        pendingCommissions: dashboardData.pending_balance || 0,
        activeChallenges: dashboardData.active_challenges || 0,
        passedChallenges: dashboardData.passed_challenges || 0,
        failedChallenges: dashboardData.failed_challenges || 0,
        fundedAccounts: dashboardData.funded_accounts || 0,
      });

      // Set recent traders
      if (dashboardData.recent_referrals) {
        setRecentTraders(dashboardData.recent_referrals.map(trader => ({
          id: trader.id,
          name: `${trader.first_name} ${trader.last_name}`,
          email: trader.email,
          status: trader.status || 'active',
          enrolled: new Date(trader.created_at).toLocaleDateString(),
          program: trader.program_name || 'N/A'
        })));
      }

      // Set recent commissions
      if (commissionsData.commissions) {
        setRecentCommissions(commissionsData.commissions.slice(0, 5).map(commission => ({
          id: commission.id,
          trader: commission.trader_name || 'N/A',
          amount: commission.amount,
          type: commission.type || 'enrollment',
          status: commission.status,
          date: new Date(commission.created_at).toLocaleDateString()
        })));
      }
    } catch (error) {
      // Keep default empty state on error
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <AgentLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="text-gray-300 mt-4">Loading dashboard...</p>
          </div>
        </div>
      </AgentLayout>
    );
  }

  return (
    <AgentLayout>
      <div className="min-h-screen bg-slate-900">
        {/* Header */}
        <div className="bg-slate-800/50 border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h1 className="text-3xl font-bold text-white">Agent Dashboard</h1>
            <p className="text-gray-300 mt-2">Overview of your traders and commissions</p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Total Traders */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Total Traders</p>
                  <p className="text-2xl font-bold text-white mt-1">{stats.totalTraders}</p>
                  <p className="text-xs text-green-600 mt-1">
                    {stats.activeTraders} active
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            {/* Total Commissions */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Total Commissions</p>
                  <p className="text-2xl font-bold text-white mt-1">
                    ${stats.totalCommissions.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-300 mt-1">
                    ${stats.pendingCommissions} pending
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>

            {/* Active Challenges */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Active Challenges</p>
                  <p className="text-2xl font-bold text-white mt-1">{stats.activeChallenges}</p>
                  <p className="text-xs text-gray-300 mt-1">
                    {stats.passedChallenges} passed
                  </p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </div>

            {/* Funded Accounts */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-300">Funded Accounts</p>
                  <p className="text-2xl font-bold text-white mt-1">{stats.fundedAccounts}</p>
                  <p className="text-xs text-green-600 mt-1">
                    {((stats.fundedAccounts / stats.passedChallenges) * 100).toFixed(1)}% success rate
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <Award className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </div>
          </div>

          {/* Challenge Performance */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="card">
              <div className="flex items-center gap-3 mb-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-gray-300">Passed</span>
              </div>
              <p className="text-3xl font-bold text-white">{stats.passedChallenges}</p>
              <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${(stats.passedChallenges / (stats.passedChallenges + stats.failedChallenges + stats.activeChallenges)) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3 mb-2">
                <Clock className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-gray-300">In Progress</span>
              </div>
              <p className="text-3xl font-bold text-white">{stats.activeChallenges}</p>
              <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${(stats.activeChallenges / (stats.passedChallenges + stats.failedChallenges + stats.activeChallenges)) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3 mb-2">
                <XCircle className="w-5 h-5 text-red-600" />
                <span className="text-sm font-medium text-gray-300">Failed</span>
              </div>
              <p className="text-3xl font-bold text-white">{stats.failedChallenges}</p>
              <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                <div 
                  className="bg-red-600 h-2 rounded-full" 
                  style={{ width: `${(stats.failedChallenges / (stats.passedChallenges + stats.failedChallenges + stats.activeChallenges)) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Traders */}
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Recent Traders</h2>
                <Link to="/agent/traders" className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1">
                  View All
                  <ArrowUpRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="space-y-4">
                {recentTraders.map((trader) => (
                  <div key={trader.id} className="flex items-center justify-between p-3 bg-slate-900 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <Users className="w-5 h-5 text-primary-600" />
                      </div>
                      <div>
                        <p className="font-medium text-white">{trader.name}</p>
                        <p className="text-sm text-gray-300">{trader.program}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        trader.status === 'funded' 
                          ? 'bg-yellow-100 text-yellow-800'
                          : trader.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-slate-700/50 text-gray-100'
                      }`}>
                        {trader.status}
                      </span>
                      <p className="text-xs text-gray-400 mt-1">{trader.enrolled}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Commissions */}
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Recent Commissions</h2>
                <Link to="/agent/commissions" className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1">
                  View All
                  <ArrowUpRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="space-y-4">
                {recentCommissions.map((commission) => (
                  <div key={commission.id} className="flex items-center justify-between p-3 bg-slate-900 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <DollarSign className="w-5 h-5 text-green-600" />
                      </div>
                      <div>
                        <p className="font-medium text-white">{commission.trader}</p>
                        <p className="text-sm text-gray-300 capitalize">{commission.type.replace('_', ' ')}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-white">${commission.amount}</p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        commission.status === 'paid' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {commission.status}
                      </span>
                      <p className="text-xs text-gray-400 mt-1">{commission.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link to="/agent/traders" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <Users className="w-8 h-8 text-primary-600" />
                <div>
                  <p className="font-medium text-white">Manage Traders</p>
                  <p className="text-sm text-gray-300">View and track your traders</p>
                </div>
              </div>
            </Link>

            <Link to="/agent/commissions" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <DollarSign className="w-8 h-8 text-green-600" />
                <div>
                  <p className="font-medium text-white">View Commissions</p>
                  <p className="text-sm text-gray-300">Track your earnings</p>
                </div>
              </div>
            </Link>

            <Link to="/agent/reports" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3">
                <TrendingUp className="w-8 h-8 text-purple-600" />
                <div>
                  <p className="font-medium text-white">View Reports</p>
                  <p className="text-sm text-gray-300">Analytics and insights</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </AgentLayout>
  );
}

