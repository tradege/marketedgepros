import { useEffect, useState } from 'react';
import { Search, Filter, Eye, Mail, Phone, TrendingUp, Award } from 'lucide-react';
import AffiliateLayout from '../../components/affiliate/AffiliateLayout';
import api from '../../services/api';

export default function TradersManagement() {
  const [traders, setTraders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedTrader, setSelectedTrader] = useState(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  useEffect(() => {
    loadTraders();
  }, []);

  const loadTraders = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/affiliate/traders');
      setTraders(response.data.traders || []);
    } catch (error) {
      // Mock data for development
      setTraders([
        {
          id: 1,
          name: 'John Trader',
          email: 'john@example.com',
          phone: '+1 234 567 8900',
          status: 'active',
          program: 'Two Phase $100K',
          enrolled_date: '2024-10-01',
          current_balance: 102450,
          profit_loss: 2450,
          total_trades: 47,
          win_rate: 68.5,
          challenge_phase: 'Phase 2',
        },
        {
          id: 2,
          name: 'Jane Smith',
          email: 'jane@example.com',
          phone: '+1 234 567 8901',
          status: 'active',
          program: 'One Phase $50K',
          enrolled_date: '2024-10-05',
          current_balance: 51230,
          profit_loss: 1230,
          total_trades: 32,
          win_rate: 71.2,
          challenge_phase: 'Phase 1',
        },
        {
          id: 3,
          name: 'Bob Wilson',
          email: 'bob@example.com',
          phone: '+1 234 567 8902',
          status: 'funded',
          program: 'Instant Funding $200K',
          enrolled_date: '2024-09-15',
          current_balance: 215890,
          profit_loss: 15890,
          total_trades: 124,
          win_rate: 74.3,
          challenge_phase: 'Funded',
        },
        {
          id: 4,
          name: 'Alice Brown',
          email: 'alice@example.com',
          phone: '+1 234 567 8903',
          status: 'failed',
          program: 'Two Phase $100K',
          enrolled_date: '2024-09-20',
          current_balance: 0,
          profit_loss: -10000,
          total_trades: 28,
          win_rate: 42.8,
          challenge_phase: 'Failed',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredTraders = traders.filter((trader) => {
    const matchesSearch =
      trader.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      trader.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || trader.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'funded':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'pending':
        return 'bg-slate-700/50 text-gray-100';
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
            <p className="text-gray-300 mt-4">Loading traders...</p>
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
            <h1 className="text-3xl font-bold text-white">My Traders</h1>
            <p className="text-gray-300 mt-2">Manage and monitor your traders' performance</p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="card">
              <p className="text-sm text-gray-300">Total Traders</p>
              <p className="text-2xl font-bold text-white mt-1">{traders.length}</p>
            </div>
            <div className="card">
              <p className="text-sm text-gray-300">Active</p>
              <p className="text-2xl font-bold text-green-600 mt-1">
                {traders.filter(t => t.status === 'active').length}
              </p>
            </div>
            <div className="card">
              <p className="text-sm text-gray-300">Funded</p>
              <p className="text-2xl font-bold text-yellow-600 mt-1">
                {traders.filter(t => t.status === 'funded').length}
              </p>
            </div>
            <div className="card">
              <p className="text-sm text-gray-300">Avg Win Rate</p>
              <p className="text-2xl font-bold text-white mt-1">
                {(traders.reduce((acc, t) => acc + t.win_rate, 0) / traders.length).toFixed(1)}%
              </p>
            </div>
          </div>

          {/* Filters */}
          <div className="bg-slate-800/50 rounded-lg shadow-sm p-4 mb-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search traders by name or email..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input pl-10 w-full"
                />
              </div>
              <div className="flex items-center gap-2">
                <Filter className="w-5 h-5 text-gray-400" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="input"
                >
                  <option value="all">All Status</option>
                  <option value="active">Active</option>
                  <option value="funded">Funded</option>
                  <option value="failed">Failed</option>
                  <option value="pending">Pending</option>
                </select>
              </div>
            </div>
          </div>

          {/* Traders Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredTraders.map((trader) => (
              <div key={trader.id} className="card">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                      <span className="text-primary-600 font-semibold text-lg">
                        {trader.name.charAt(0)}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">{trader.name}</h3>
                      <p className="text-sm text-gray-300">{trader.email}</p>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(trader.status)}`}>
                    {trader.status}
                  </span>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-300">Program</span>
                    <span className="text-sm font-medium text-white">{trader.program}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-300">Phase</span>
                    <span className="text-sm font-medium text-white">{trader.challenge_phase}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-300">Current Balance</span>
                    <span className="text-sm font-bold text-white">
                      ${trader.current_balance.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-300">P&L</span>
                    <span className={`text-sm font-bold ${trader.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {trader.profit_loss >= 0 ? '+' : ''}${trader.profit_loss.toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-slate-900 rounded-lg">
                  <div>
                    <p className="text-xs text-gray-300">Total Trades</p>
                    <p className="text-lg font-bold text-white">{trader.total_trades}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-300">Win Rate</p>
                    <p className="text-lg font-bold text-white">{trader.win_rate}%</p>
                  </div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setSelectedTrader(trader);
                      setShowDetailsModal(true);
                    }}
                    className="flex-1 btn btn-secondary text-sm flex items-center justify-center gap-2"
                  >
                    <Eye className="w-4 h-4" />
                    View Details
                  </button>
                  <button className="btn btn-secondary text-sm p-2">
                    <Mail className="w-4 h-4" />
                  </button>
                  <button className="btn btn-secondary text-sm p-2">
                    <Phone className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {filteredTraders.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-300">No traders found</p>
            </div>
          )}
        </div>
      </div>

      {/* Details Modal */}
      {showDetailsModal && selectedTrader && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800/50 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-primary-600 font-semibold text-lg">
                      {selectedTrader.name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-white">{selectedTrader.name}</h2>
                    <p className="text-gray-300">{selectedTrader.email}</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedTrader.status)}`}>
                  {selectedTrader.status}
                </span>
              </div>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-bold text-white mb-4">Account Information</h3>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-300">Program</p>
                      <p className="font-medium text-white">{selectedTrader.program}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-300">Challenge Phase</p>
                      <p className="font-medium text-white">{selectedTrader.challenge_phase}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-300">Enrolled Date</p>
                      <p className="font-medium text-white">
                        {new Date(selectedTrader.enrolled_date).toLocaleDateString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-300">Phone</p>
                      <p className="font-medium text-white">{selectedTrader.phone}</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-white mb-4">Performance Metrics</h3>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-300">Current Balance</p>
                      <p className="text-2xl font-bold text-white">
                        ${selectedTrader.current_balance.toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-300">Profit/Loss</p>
                      <p className={`text-2xl font-bold ${selectedTrader.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {selectedTrader.profit_loss >= 0 ? '+' : ''}${selectedTrader.profit_loss.toLocaleString()}
                      </p>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-300">Total Trades</p>
                        <p className="text-xl font-bold text-white">{selectedTrader.total_trades}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-300">Win Rate</p>
                        <p className="text-xl font-bold text-white">{selectedTrader.win_rate}%</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <div className="flex gap-3">
                  <button className="btn btn-primary flex-1 flex items-center justify-center gap-2">
                    <TrendingUp className="w-5 h-5" />
                    View Trading History
                  </button>
                  <button className="btn btn-secondary flex-1 flex items-center justify-center gap-2">
                    <Award className="w-5 h-5" />
                    View Commissions
                  </button>
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-white/10">
              <button
                onClick={() => setShowDetailsModal(false)}
                className="btn btn-secondary w-full"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </AffiliateLayout>
  );
}

