import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  Search,
  Filter,
  Eye,
  CheckCircle,
  XCircle,
  DollarSign,
  Calendar,
  User,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export default function ChallengesManagement() {
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchChallenges();
  }, [currentPage, statusFilter]);

  const fetchChallenges = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      const params = new URLSearchParams({
        page: currentPage,
        per_page: 20,
      });
      
      if (statusFilter !== 'all') {
        params.append('status', statusFilter);
      }

      const response = await axios.get(
        `${API_BASE_URL}/admin/challenges?${params.toString()}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setChallenges(response.data.challenges || []);
      setTotalPages(response.data.total_pages || 1);
      setError(null);
    } catch (err) {
      console.error('Failed to load challenges:', err);
      setError('Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      passed: 'bg-green-500/20 text-green-400 border-green-500/30',
      failed: 'bg-red-500/20 text-red-400 border-red-500/30',
      funded: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
      pending: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    };
    return colors[status] || 'bg-gray-500/20 text-gray-400 border-gray-500/30';
  };

  const getPhaseColor = (phase) => {
    const colors = {
      1: 'text-cyan-400',
      2: 'text-teal-400',
      funded: 'text-purple-400',
    };
    return colors[phase] || 'text-gray-400';
  };

  const filteredChallenges = challenges.filter(challenge =>
    searchTerm === '' ||
    challenge.user_email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    challenge.program_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    challenge.id?.toString().includes(searchTerm)
  );

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(amount);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const calculateProfit = (challenge) => {
    const initial = parseFloat(challenge.initial_balance || 0);
    const current = parseFloat(challenge.current_balance || 0);
    const profit = current - initial;
    const percentage = initial > 0 ? ((profit / initial) * 100).toFixed(2) : 0;
    return { profit, percentage };
  };

  if (loading && challenges.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-cyan-500 border-t-transparent mb-4"></div>
          <p className="text-gray-300 text-lg">Loading challenges...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                Challenges Management
              </h1>
              <p className="text-gray-400">
                Monitor and manage all trading challenges
              </p>
            </div>
            <button
              onClick={fetchChallenges}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300"
            >
              <RefreshCw className="w-5 h-5" />
              Refresh
            </button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Challenges</p>
                  <p className="text-2xl font-bold text-white">{challenges.length}</p>
                </div>
                <TrendingUp className="w-8 h-8 text-cyan-400" />
              </div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Active</p>
                  <p className="text-2xl font-bold text-blue-400">
                    {challenges.filter(c => c.status === 'active').length}
                  </p>
                </div>
                <CheckCircle className="w-8 h-8 text-blue-400" />
              </div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Passed</p>
                  <p className="text-2xl font-bold text-green-400">
                    {challenges.filter(c => c.status === 'passed').length}
                  </p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-400" />
              </div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Funded</p>
                  <p className="text-2xl font-bold text-purple-400">
                    {challenges.filter(c => c.status === 'funded').length}
                  </p>
                </div>
                <DollarSign className="w-8 h-8 text-purple-400" />
              </div>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search by user email, program name, or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500/50 transition-colors"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="text-gray-400 w-5 h-5" />
              <select
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white focus:outline-none focus:border-cyan-500/50 transition-colors"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="passed">Passed</option>
                <option value="failed">Failed</option>
                <option value="funded">Funded</option>
                <option value="pending">Pending</option>
              </select>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-400" />
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Challenges Table */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50">
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">ID</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">User</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Program</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Phase</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Balance</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Profit/Loss</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Created</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredChallenges.length === 0 ? (
                  <tr>
                    <td colSpan="9" className="px-6 py-12 text-center">
                      <div className="flex flex-col items-center gap-3">
                        <AlertCircle className="w-12 h-12 text-gray-500" />
                        <p className="text-gray-400">No challenges found</p>
                      </div>
                    </td>
                  </tr>
                ) : (
                  filteredChallenges.map((challenge) => {
                    const { profit, percentage } = calculateProfit(challenge);
                    const isProfitable = profit >= 0;

                    return (
                      <tr
                        key={challenge.id}
                        className="border-b border-slate-700/30 hover:bg-slate-700/30 transition-colors"
                      >
                        <td className="px-6 py-4">
                          <span className="text-cyan-400 font-mono">#{challenge.id}</span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <User className="w-4 h-4 text-gray-400" />
                            <span className="text-white">{challenge.user_email || 'N/A'}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-gray-300">{challenge.program_name || 'N/A'}</span>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`font-semibold ${getPhaseColor(challenge.phase)}`}>
                            Phase {challenge.phase}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-white font-semibold">
                            {formatCurrency(challenge.current_balance || 0)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex flex-col">
                            <span className={`font-semibold ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
                              {isProfitable ? '+' : ''}{formatCurrency(profit)}
                            </span>
                            <span className={`text-sm ${isProfitable ? 'text-green-400/70' : 'text-red-400/70'}`}>
                              {isProfitable ? '+' : ''}{percentage}%
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getStatusColor(challenge.status)}`}>
                            {challenge.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2 text-gray-400">
                            <Calendar className="w-4 h-4" />
                            <span className="text-sm">{formatDate(challenge.created_at)}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <button
                            onClick={() => navigate(`/admin/challenges/${challenge.id}`)}
                            className="flex items-center gap-2 px-3 py-1.5 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors"
                          >
                            <Eye className="w-4 h-4" />
                            View
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-6 py-4 border-t border-slate-700/50">
              <p className="text-gray-400 text-sm">
                Page {currentPage} of {totalPages}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 bg-slate-700/50 text-white rounded-lg hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Previous
                </button>
                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-lg hover:shadow-lg hover:shadow-cyan-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

