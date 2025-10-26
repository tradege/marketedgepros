import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  TrendingUp, TrendingDown, DollarSign, Calendar,
  Target, AlertCircle, CheckCircle, XCircle, Award,
  BarChart3, Activity, ArrowLeft
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../contexts/ToastContext';
import { SkeletonDashboard } from '../components/common/Skeleton';

export default function ChallengeDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [challenge, setChallenge] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadChallenge();
  }, [id]);

  const loadChallenge = async () => {
    try {
      setIsLoading(true);
      const response = await api.get(`/traders/challenges/${id}`);
      setChallenge(response.data.challenge);
    } catch (error) {
      // Show error message
      toast.error('Failed to load challenge details');
      navigate('/dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-600 mt-4">Loading challenge...</p>
        </div>
      </div>
    );
  }

  if (!challenge) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Challenge not found</h2>
          <button onClick={() => navigate('/dashboard')} className="btn btn-primary mt-4">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const profitProgress = (challenge.current_profit / challenge.profit_target) * 100;
  const isProfit = challenge.current_profit >= 0;

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'passed':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'funded':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{challenge.program_name}</h1>
              <p className="text-gray-600 mt-2">
                Phase {challenge.phase} of {challenge.total_phases} • {challenge.days_active} days active
              </p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-medium ${getStatusColor(challenge.status)}`}>
              {challenge.status}
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Current Balance</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  ${challenge.current_balance.toLocaleString()}
                </p>
                <p className={`text-sm mt-1 ${isProfit ? 'text-green-600' : 'text-red-600'}`}>
                  {isProfit ? '+' : ''}{challenge.current_profit.toLocaleString()} ({((challenge.current_profit / challenge.account_size) * 100).toFixed(2)}%)
                </p>
              </div>
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                isProfit ? 'bg-green-100' : 'bg-red-100'
              }`}>
                <DollarSign className={`w-6 h-6 ${isProfit ? 'text-green-600' : 'text-red-600'}`} />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Profit Target</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  ${challenge.profit_target.toLocaleString()}
                </p>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all" 
                    style={{ width: `${Math.min(profitProgress, 100)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-600 mt-1">{profitProgress.toFixed(1)}% achieved</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Win Rate</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{challenge.win_rate}%</p>
                <p className="text-sm text-gray-600 mt-1">
                  {challenge.winning_trades}W / {challenge.losing_trades}L
                </p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Trades</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{challenge.trades_count}</p>
                <p className="text-sm text-gray-600 mt-1">
                  Avg: {(challenge.trades_count / challenge.days_active).toFixed(1)}/day
                </p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Trading Stats */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Trading Statistics</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <span className="text-sm font-medium text-green-900">Best Trade</span>
                  </div>
                  <p className="text-2xl font-bold text-green-600">
                    +${challenge.best_trade}
                  </p>
                </div>

                <div className="p-4 bg-red-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingDown className="w-5 h-5 text-red-600" />
                    <span className="text-sm font-medium text-red-900">Worst Trade</span>
                  </div>
                  <p className="text-2xl font-bold text-red-600">
                    ${challenge.worst_trade}
                  </p>
                </div>

                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-blue-600" />
                    <span className="text-sm font-medium text-blue-900">Avg Win</span>
                  </div>
                  <p className="text-2xl font-bold text-blue-600">
                    +${challenge.average_win}
                  </p>
                </div>

                <div className="p-4 bg-orange-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <XCircle className="w-5 h-5 text-orange-600" />
                    <span className="text-sm font-medium text-orange-900">Avg Loss</span>
                  </div>
                  <p className="text-2xl font-bold text-orange-600">
                    ${challenge.average_loss}
                  </p>
                </div>
              </div>
            </div>

            {/* Recent Trades */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Trades</h2>
              <div className="space-y-3">
                {challenge.recent_trades.map((trade) => (
                  <div key={trade.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        trade.profit >= 0 ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        {trade.profit >= 0 ? (
                          <TrendingUp className="w-5 h-5 text-green-600" />
                        ) : (
                          <TrendingDown className="w-5 h-5 text-red-600" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{trade.symbol}</p>
                        <p className="text-sm text-gray-600 capitalize">{trade.type}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`font-bold ${trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {trade.profit >= 0 ? '+' : ''}${trade.profit}
                      </p>
                      <p className="text-xs text-gray-500">{trade.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Challenge Rules */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Challenge Rules</h2>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Target className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Profit Target</p>
                    <p className="text-sm text-gray-600">${challenge.rules.profit_target.toLocaleString()}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Max Daily Loss</p>
                    <p className="text-sm text-gray-600">${challenge.rules.max_daily_loss.toLocaleString()}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Max Total Loss</p>
                    <p className="text-sm text-gray-600">${challenge.rules.max_total_loss.toLocaleString()}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Trading Days</p>
                    <p className="text-sm text-gray-600">
                      Min: {challenge.rules.min_trading_days} • Max: {challenge.rules.max_trading_days}
                    </p>
                  </div>
                </div>

                {challenge.rules.consistency_rule && (
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Consistency Rule</p>
                      <p className="text-sm text-gray-600">No single day &gt; 40% of total profit</p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Profit Split */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Profit Split</h2>
              <div className="flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-24 h-24 bg-yellow-100 rounded-full mb-3">
                    <Award className="w-12 h-12 text-yellow-600" />
                  </div>
                  <p className="text-4xl font-bold text-gray-900">{challenge.profit_split}%</p>
                  <p className="text-sm text-gray-600 mt-1">Your profit share</p>
                </div>
              </div>
            </div>

            {/* MetaTrader Connection */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">MetaTrader</h2>
              <div className="p-4 bg-gray-50 rounded-lg text-center">
                <p className="text-sm text-gray-600 mb-3">Connect your MT4/MT5 account</p>
                <button className="btn btn-primary w-full">
                  Connect Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

