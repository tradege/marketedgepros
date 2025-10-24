import { useState, useEffect } from 'react';
import { DollarSign, CheckCircle, XCircle, Clock, Eye, Download } from 'lucide-react';
import AdminLayout from '../../components/admin/AdminLayout';
import DataTable from '../../components/common/DataTable';
import api from '../../services/api';

export default function WithdrawalManagement() {
  const [withdrawals, setWithdrawals] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedWithdrawal, setSelectedWithdrawal] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadWithdrawals();
  }, [selectedStatus]);

  const loadWithdrawals = async () => {
    try {
      setIsLoading(true);
      const params = selectedStatus !== 'all' ? { status: selectedStatus } : {};
      const response = await api.get('/wallet/admin/withdrawals', { params });
      setWithdrawals(response.data.withdrawals || []);
    } catch (error) {
      console.error('Failed to load withdrawals:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (withdrawalId) => {
    if (!confirm('Are you sure you want to approve this withdrawal?')) return;

    try {
      setActionLoading(true);
      await api.post(`/wallet/admin/withdrawals/${withdrawalId}/approve`);
      alert('Withdrawal approved successfully');
      loadWithdrawals();
      setShowDetailsModal(false);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to approve withdrawal');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async (withdrawalId) => {
    const reason = prompt('Please provide a reason for rejection:');
    if (!reason) return;

    try {
      setActionLoading(true);
      await api.post(`/wallet/admin/withdrawals/${withdrawalId}/reject`, { reason });
      alert('Withdrawal rejected successfully');
      loadWithdrawals();
      setShowDetailsModal(false);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to reject withdrawal');
    } finally {
      setActionLoading(false);
    }
  };

  const handleComplete = async (withdrawalId) => {
    const transactionId = prompt('Please enter the transaction ID:');
    if (!transactionId) return;

    try {
      setActionLoading(true);
      await api.post(`/wallet/admin/withdrawals/${withdrawalId}/complete`, { transaction_id: transactionId });
      alert('Withdrawal marked as completed');
      loadWithdrawals();
      setShowDetailsModal(false);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to complete withdrawal');
    } finally {
      setActionLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const styles = {
      pending: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-blue-100 text-blue-800',
      processing: 'bg-purple-100 text-purple-800',
      completed: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const columns = [
    {
      key: 'id',
      label: 'ID',
      render: (row) => `#${row.id}`,
    },
    {
      key: 'user',
      label: 'User',
      render: (row) => (
        <div>
          <div className="font-medium">{row.user?.name || 'N/A'}</div>
          <div className="text-sm text-gray-500">{row.user?.email || 'N/A'}</div>
        </div>
      ),
    },
    {
      key: 'amount',
      label: 'Amount',
      render: (row) => (
        <div>
          <div className="font-semibold">${parseFloat(row.amount).toFixed(2)}</div>
          {row.fee > 0 && (
            <div className="text-xs text-gray-500">
              Fee: ${parseFloat(row.fee).toFixed(2)}
            </div>
          )}
        </div>
      ),
    },
    {
      key: 'payment_method',
      label: 'Method',
      render: (row) => (
        <span className="capitalize">{row.payment_method?.replace('_', ' ')}</span>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      render: (row) => getStatusBadge(row.status),
    },
    {
      key: 'created_at',
      label: 'Requested',
      render: (row) => new Date(row.created_at).toLocaleDateString(),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <button
          onClick={() => {
            setSelectedWithdrawal(row);
            setShowDetailsModal(true);
          }}
          className="text-blue-600 hover:text-blue-800 font-medium"
        >
          <Eye className="w-5 h-5" />
        </button>
      ),
    },
  ];

  const stats = [
    {
      label: 'Total Pending',
      value: withdrawals.filter((w) => w.status === 'pending').length,
      icon: Clock,
      color: 'yellow',
    },
    {
      label: 'Total Amount Pending',
      value: `$${withdrawals
        .filter((w) => w.status === 'pending')
        .reduce((sum, w) => sum + parseFloat(w.amount), 0)
        .toFixed(2)}`,
      icon: DollarSign,
      color: 'blue',
    },
    {
      label: 'Completed Today',
      value: withdrawals.filter(
        (w) =>
          w.status === 'completed' &&
          new Date(w.completed_at).toDateString() === new Date().toDateString()
      ).length,
      icon: CheckCircle,
      color: 'green',
    },
    {
      label: 'Rejected',
      value: withdrawals.filter((w) => w.status === 'rejected').length,
      icon: XCircle,
      color: 'red',
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Withdrawal Management</h1>
          <p className="mt-2 text-gray-600">Manage and process withdrawal requests</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            const colorClasses = {
              yellow: 'bg-yellow-100 text-yellow-600',
              blue: 'bg-blue-100 text-blue-600',
              green: 'bg-green-100 text-green-600',
              red: 'bg-red-100 text-red-600',
            };

            return (
              <div key={index} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.label}</p>
                    <p className="text-2xl font-bold mt-1">{stat.value}</p>
                  </div>
                  <div className={`p-3 rounded-lg ${colorClasses[stat.color]}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex gap-2">
            {['all', 'pending', 'approved', 'processing', 'completed', 'rejected'].map((status) => (
              <button
                key={status}
                onClick={() => setSelectedStatus(status)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedStatus === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow">
          <DataTable
            columns={columns}
            data={withdrawals}
            isLoading={isLoading}
            emptyMessage="No withdrawals found"
          />
        </div>

        {/* Details Modal */}
        {showDetailsModal && selectedWithdrawal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-2xl font-bold">Withdrawal Details</h2>
                  <button
                    onClick={() => setShowDetailsModal(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-4">
                  {/* User Info */}
                  <div className="border-b pb-4">
                    <h3 className="font-semibold mb-2">User Information</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Name:</span>
                        <span className="ml-2 font-medium">{selectedWithdrawal.user?.name || 'N/A'}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Email:</span>
                        <span className="ml-2 font-medium">{selectedWithdrawal.user?.email || 'N/A'}</span>
                      </div>
                    </div>
                  </div>

                  {/* Amount Info */}
                  <div className="border-b pb-4">
                    <h3 className="font-semibold mb-2">Amount Details</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Gross Amount:</span>
                        <span className="ml-2 font-medium">${parseFloat(selectedWithdrawal.amount).toFixed(2)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Fee:</span>
                        <span className="ml-2 font-medium">${parseFloat(selectedWithdrawal.fee || 0).toFixed(2)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Net Amount:</span>
                        <span className="ml-2 font-medium text-green-600">
                          ${parseFloat(selectedWithdrawal.net_amount || selectedWithdrawal.amount).toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Payment Info */}
                  <div className="border-b pb-4">
                    <h3 className="font-semibold mb-2">Payment Information</h3>
                    <div className="text-sm space-y-2">
                      <div>
                        <span className="text-gray-600">Method:</span>
                        <span className="ml-2 font-medium capitalize">
                          {selectedWithdrawal.payment_method?.replace('_', ' ')}
                        </span>
                      </div>
                      {selectedWithdrawal.payment_details && (
                        <div>
                          <span className="text-gray-600">Details:</span>
                          <pre className="ml-2 mt-1 p-2 bg-gray-50 rounded text-xs">
                            {JSON.stringify(selectedWithdrawal.payment_details, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Status Info */}
                  <div className="border-b pb-4">
                    <h3 className="font-semibold mb-2">Status</h3>
                    <div className="flex items-center gap-2">
                      {getStatusBadge(selectedWithdrawal.status)}
                      <span className="text-sm text-gray-600">
                        Requested: {new Date(selectedWithdrawal.created_at).toLocaleString()}
                      </span>
                    </div>
                    {selectedWithdrawal.rejection_reason && (
                      <div className="mt-2 p-3 bg-red-50 rounded">
                        <span className="text-sm font-medium text-red-800">Rejection Reason:</span>
                        <p className="text-sm text-red-700 mt-1">{selectedWithdrawal.rejection_reason}</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-3 pt-4">
                    {selectedWithdrawal.status === 'pending' && (
                      <>
                        <button
                          onClick={() => handleApprove(selectedWithdrawal.id)}
                          disabled={actionLoading}
                          className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 font-medium"
                        >
                          <CheckCircle className="w-5 h-5 inline mr-2" />
                          Approve
                        </button>
                        <button
                          onClick={() => handleReject(selectedWithdrawal.id)}
                          disabled={actionLoading}
                          className="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 font-medium"
                        >
                          <XCircle className="w-5 h-5 inline mr-2" />
                          Reject
                        </button>
                      </>
                    )}
                    {(selectedWithdrawal.status === 'approved' || selectedWithdrawal.status === 'processing') && (
                      <button
                        onClick={() => handleComplete(selectedWithdrawal.id)}
                        disabled={actionLoading}
                        className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
                      >
                        <Download className="w-5 h-5 inline mr-2" />
                        Mark as Completed
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </AdminLayout>
  );
}

