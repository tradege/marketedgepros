import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  DollarSign,
  Trophy,
  CheckCircle,
  Clock,
  XCircle,
  ArrowRight,
  RefreshCw,
} from 'lucide-react';
import UserLayout from '../components/layout/UserLayout';
import useAuthStore from '../store/authStore';
import { programsAPI } from '../services/api';

export default function Dashboard() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState({
    totalChallenges: 0,
    activeChallenges: 0,
    passedChallenges: 0,
    totalProfit: 0,
  });

  useEffect(() => {
    loadChallenges();
  }, []);

  const loadChallenges = async () => {
    try {
      setIsLoading(true);
      const response = await programsAPI.getMyChallenges();
      const challengesData = response.data.challenges || [];
      setChallenges(challengesData);
      
      // Calculate stats
      setStats({
        totalChallenges: challengesData.length,
        activeChallenges: challengesData.filter(c => c.status === 'active').length,
        passedChallenges: challengesData.filter(c => c.status === 'passed').length,
        totalProfit: challengesData.reduce((sum, c) => sum + (c.profit || 0), 0),
      });
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'passed':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'failed':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
      case 'passed':
        return <CheckCircle className="w-4 h-4" />;
      case 'failed':
        return <XCircle className="w-4 h-4" />;
      case 'pending':
        return <Clock className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const statsCards = [
    {
      title: 'Total Challenges',
      value: stats.totalChallenges,
      icon: TrendingUp,
      gradient: 'from-indigo-500 to-purple-600',
    },
    {
      title: 'Active Challenges',
      value: stats.activeChallenges,
      icon: Trophy,
      gradient: 'from-green-400 to-cyan-400',
    },
    {
      title: 'Passed Challenges',
      value: stats.passedChallenges,
      icon: CheckCircle,
      gradient: 'from-blue-400 to-cyan-400',
    },
    {
      title: 'Total Profit',
      value: `$${stats.totalProfit.toLocaleString()}`,
      icon: DollarSign,
      gradient: 'from-pink-400 to-yellow-400',
    },
  ];

  return (
    <UserLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, {user?.full_name || user?.email}!
          </h1>
          <p className="text-gray-400">Here's your trading overview</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div
                key={index}
                className="bg-gray-800 rounded-xl border border-gray-700 p-6 hover:transform hover:-translate-y-1 hover:shadow-2xl transition-all duration-300"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.gradient} flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h3 className="text-3xl font-bold text-white mb-1">{stat.value}</h3>
                <p className="text-gray-400 text-sm">{stat.title}</p>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gradient-to-br from-indigo-500/10 to-purple-600/10 border border-indigo-500/30 rounded-xl p-8">
            <h3 className="text-2xl font-bold text-white mb-3">Start a New Challenge</h3>
            <p className="text-gray-400 mb-6">
              Choose from our trading programs and start your journey to get funded
            </p>
            <button
              onClick={() => navigate('/programs')}
              className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-2"
            >
              Browse Programs
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>

          <div className="bg-gradient-to-br from-green-400/10 to-cyan-400/10 border border-green-400/30 rounded-xl p-8">
            <h3 className="text-2xl font-bold text-white mb-3">Complete Your Profile</h3>
            <p className="text-gray-400 mb-6">
              Update your information and complete KYC verification
            </p>
            <button
              onClick={() => navigate('/profile')}
              className="bg-gradient-to-r from-green-400 to-cyan-400 hover:from-green-500 hover:to-cyan-500 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-2"
            >
              Go to Profile
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* My Challenges */}
        <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-700">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">My Challenges</h2>
              <button
                onClick={loadChallenges}
                className="text-gray-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-gray-700"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="p-6">
            {isLoading ? (
              <div className="py-8">
                <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 animate-pulse"></div>
                </div>
              </div>
            ) : challenges.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-400 mb-6">You don't have any challenges yet</p>
                <button
                  onClick={() => navigate('/programs')}
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200"
                >
                  Start Your First Challenge
                </button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-700/50">
                      <th className="text-left px-4 py-3 text-gray-400 font-semibold">Program</th>
                      <th className="text-left px-4 py-3 text-gray-400 font-semibold">Account Size</th>
                      <th className="text-left px-4 py-3 text-gray-400 font-semibold">Status</th>
                      <th className="text-left px-4 py-3 text-gray-400 font-semibold">Progress</th>
                      <th className="text-left px-4 py-3 text-gray-400 font-semibold">Profit</th>
                      <th className="text-right px-4 py-3 text-gray-400 font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {challenges.map((challenge) => (
                      <tr
                        key={challenge.id}
                        className="border-t border-gray-700 hover:bg-gray-700/30 transition-colors"
                      >
                        <td className="px-4 py-4 text-white font-semibold">
                          {challenge.program_name}
                        </td>
                        <td className="px-4 py-4 text-gray-300">
                          ${challenge.account_size?.toLocaleString()}
                        </td>
                        <td className="px-4 py-4">
                          <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(challenge.status)}`}>
                            {getStatusIcon(challenge.status)}
                            <span className="capitalize">{challenge.status}</span>
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          <div className="w-24">
                            <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-300"
                                style={{ width: `${challenge.progress || 0}%` }}
                              ></div>
                            </div>
                          </div>
                        </td>
                        <td className={`px-4 py-4 font-semibold ${challenge.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          ${challenge.profit?.toLocaleString() || 0}
                        </td>
                        <td className="px-4 py-4 text-right">
                          <button
                            onClick={() => navigate(`/challenges/${challenge.id}`)}
                            className="px-4 py-2 border border-indigo-500 text-indigo-400 hover:bg-indigo-500/10 rounded-lg transition-colors text-sm font-medium"
                          >
                            View Details
                          </button>
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
    </UserLayout>
  );
}

