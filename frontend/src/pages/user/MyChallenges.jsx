import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { programsAPI } from '../../services/api';
import { TrendingUp, Clock, CheckCircle, XCircle, ArrowRight, Loader } from 'lucide-react';
import UserLayout from '../../components/layout/UserLayout';

export default function MyChallenges() {
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await programsAPI.getMyChallenges();
      setChallenges(response.data.challenges || []);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'passed':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'pending':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <Clock className="w-4 h-4" />;
      case 'passed':
        return <CheckCircle className="w-4 h-4" />;
      case 'failed':
        return <XCircle className="w-4 h-4" />;
      default:
        return <TrendingUp className="w-4 h-4" />;
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Loader className="w-8 h-8 text-purple-500 animate-spin" />
      </div>
    );
  }

  return (
    <UserLayout>
      <div>
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-white">My Challenges</h1>
          <button
            onClick={() => navigate('/programs')}
            className="px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors"
          >
            Browse Programs
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/20 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-400 rounded-lg">
            {error}
          </div>
        )}

        {challenges.length === 0 ? (
          <div className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg p-12 text-center">
            <h3 className="text-xl text-gray-300 mb-4">
              You don't have any challenges yet
            </h3>
            <button
              onClick={() => navigate('/programs')}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors"
            >
              Start Your First Challenge
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {challenges.map((challenge) => (
              <div
                key={challenge.id}
                className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg p-6 transition-transform hover:-translate-y-1"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-white">
                    {challenge.program_name || 'Challenge'}
                  </h3>
                  <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-semibold rounded ${getStatusColor(challenge.status)}`}>
                    {getStatusIcon(challenge.status)}
                    {challenge.status}
                  </span>
                </div>

                <div className="mb-4 space-y-2">
                  <p className="text-sm text-gray-400">
                    Account Size: <span className="text-white font-semibold">${challenge.account_size?.toLocaleString()}</span>
                  </p>
                  <p className="text-sm text-gray-400">
                    Profit Target: <span className="text-green-400 font-semibold">{challenge.profit_target}%</span>
                  </p>
                  <p className="text-sm text-gray-400">
                    Max Drawdown: <span className="text-red-400 font-semibold">{challenge.max_drawdown}%</span>
                  </p>
                </div>

                <button
                  onClick={() => navigate(`/challenges/${challenge.id}`)}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2 border border-purple-600 text-purple-400 rounded-lg hover:bg-purple-600/10 transition-colors"
                >
                  View Details
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </UserLayout>
  );
}