import { useState, useEffect } from 'react';
import { Wallet as WalletIcon, TrendingUp, TrendingDown, DollarSign, Clock, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

export default function Wallet() {
  const navigate = useNavigate();
  const [wallet, setWallet] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, credit, debit

  useEffect(() => {
    loadWalletData();
  }, []);

  const loadWalletData = async () => {
    try {
      setIsLoading(true);
      
      // Load wallet balance
      const walletResponse = await api.get('/api/v1/wallet/balance');
      setWallet(walletResponse.data.wallet);
      
      // Load transactions
      const transactionsResponse = await api.get('/api/v1/wallet/transactions');
      setTransactions(transactionsResponse.data.transactions || []);
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  const getTransactionIcon = (type) => {
    if (type === 'credit' || type === 'deposit' || type === 'commission') {
      return <ArrowDownRight className="w-5 h-5 text-green-600" />;
    }
    return <ArrowUpRight className="w-5 h-5 text-red-600" />;
  };

  const getTransactionColor = (type) => {
    if (type === 'credit' || type === 'deposit' || type === 'commission') {
      return 'text-green-600';
    }
    return 'text-red-600';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredTransactions = transactions.filter(t => {
    if (filter === 'all') return true;
    if (filter === 'credit') return ['credit', 'deposit', 'commission'].includes(t.transaction_type);
    if (filter === 'debit') return ['debit', 'withdrawal', 'fee'].includes(t.transaction_type);
    return true;
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading wallet...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <WalletIcon className="w-8 h-8 text-blue-600" />
            My Wallet
          </h1>
          <p className="mt-2 text-gray-600">Manage your balances and view transaction history</p>
        </div>

        {/* Balance Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Main Balance */}
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <DollarSign className="w-5 h-5" />
                <span className="text-sm font-medium opacity-90">Main Balance</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-2">
              ${wallet?.main_balance?.toFixed(2) || '0.00'}
            </div>
            <p className="text-sm opacity-75">Available for trading</p>
          </div>

          {/* Commission Balance */}
          <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                <span className="text-sm font-medium opacity-90">Commission Balance</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-2">
              ${wallet?.commission_balance?.toFixed(2) || '0.00'}
            </div>
            <p className="text-sm opacity-75">Earned commissions</p>
          </div>

          {/* Bonus Balance */}
          <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <TrendingDown className="w-5 h-5" />
                <span className="text-sm font-medium opacity-90">Bonus Balance</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-2">
              ${wallet?.bonus_balance?.toFixed(2) || '0.00'}
            </div>
            <p className="text-sm opacity-75">Promotional bonuses</p>
          </div>
        </div>

        {/* Total Balance Card */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Balance</p>
              <p className="text-4xl font-bold text-gray-900">
                ${wallet?.total_balance?.toFixed(2) || '0.00'}
              </p>
            </div>
            <button
              onClick={() => navigate('/withdrawals')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center gap-2"
            >
              <ArrowUpRight className="w-5 h-5" />
              Request Withdrawal
            </button>
          </div>
        </div>

        {/* Transaction History */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">Transaction History</h2>
              
              {/* Filter Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={() => setFilter('all')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filter === 'all'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setFilter('credit')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filter === 'credit'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Credits
                </button>
                <button
                  onClick={() => setFilter('debit')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filter === 'debit'
                      ? 'bg-red-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Debits
                </button>
              </div>
            </div>
          </div>

          {/* Transactions List */}
          <div className="divide-y divide-gray-200">
            {filteredTransactions.length === 0 ? (
              <div className="p-12 text-center">
                <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No transactions yet</p>
                <p className="text-sm text-gray-500 mt-2">Your transaction history will appear here</p>
              </div>
            ) : (
              filteredTransactions.map((transaction) => (
                <div key={transaction.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                        {getTransactionIcon(transaction.transaction_type)}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">
                          {transaction.description || transaction.transaction_type}
                        </p>
                        <p className="text-sm text-gray-500">
                          {formatDate(transaction.created_at)}
                        </p>
                        {transaction.balance_type && (
                          <span className="inline-block mt-1 px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded">
                            {transaction.balance_type}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`text-lg font-bold ${getTransactionColor(transaction.transaction_type)}`}>
                        {['credit', 'deposit', 'commission'].includes(transaction.transaction_type) ? '+' : '-'}
                        ${Math.abs(transaction.amount).toFixed(2)}
                      </p>
                      {transaction.reference_type && (
                        <p className="text-xs text-gray-500 mt-1">
                          Ref: {transaction.reference_type} #{transaction.reference_id}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

