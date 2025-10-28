import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Eye, DollarSign, Gift } from 'lucide-react';
import axios from 'axios';
// AdminLayout removed - wrapped in App.jsx
// // AdminLayout removed - wrapped in App.jsx
// import AdminLayout from '../../components/admin/AdminLayout';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const PaymentApprovals = () => {
  const [pendingRequests, setPendingRequests] = useState([]);
  const [allRequests, setAllRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [actionType, setActionType] = useState(null); // 'approve' or 'reject'
  const [adminNotes, setAdminNotes] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [processing, setProcessing] = useState(false);
  const [stats, setStats] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const pendingRes = await axios.get(`${API_BASE_URL}/payment-approvals/pending`, { headers });
      setPendingRequests(pendingRes.data.data || []);

      const statsRes = await axios.get(`${API_BASE_URL}/payment-approvals/stats`, { headers });
      setStats(statsRes.data.data || {});

      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load approval requests');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (request, action) => {
    setSelectedRequest(request);
    setActionType(action);
    setDialogOpen(true);
    setAdminNotes('');
    setRejectionReason('');
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedRequest(null);
    setActionType(null);
    setAdminNotes('');
    setRejectionReason('');
  };

  const handleApprove = async () => {
    if (!selectedRequest) return;

    try {
      setProcessing(true);
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(
        `${API_BASE_URL}/payment-approvals/${selectedRequest.id}/approve`,
        { admin_notes: adminNotes },
        { headers }
      );

      await fetchData();
      handleCloseDialog();
      alert('Payment approved successfully!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to approve request');
    } finally {
      setProcessing(false);
    }
  };

  const handleReject = async () => {
    if (!selectedRequest || !rejectionReason.trim()) {
      alert('Please provide a rejection reason');
      return;
    }

    try {
      setProcessing(true);
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(
        `${API_BASE_URL}/payment-approvals/${selectedRequest.id}/reject`,
        {
          rejection_reason: rejectionReason,
          admin_notes: adminNotes
        },
        { headers }
      );

      await fetchData();
      handleCloseDialog();
      alert('Payment rejected');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to reject request');
    } finally {
      setProcessing(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'warning';
      case 'approved':
        return 'success';
      case 'rejected':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPaymentTypeIcon = (type) => {
    return type === 'cash' ? <DollarSign className="h-4 w-4" /> : <Gift className="h-4 w-4" />;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const formatAmount = (amount) => {
    return `$${parseFloat(amount).toFixed(2)}`;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-transparent dark:border-neutral-700 dark:border-t-transparent" />
      </div>
    );
  }

  return (
    
    <div className="p-4 md:p-6">
      <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
        Payment Approvals
      </h1>

      {error && (
        <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-red-800 dark:border-red-800/50 dark:bg-red-900/30 dark:text-red-300">
          {error}
        </div>
      )}

      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-4">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Pending</p>
            <p className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
              {stats.pending || 0}
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-4">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Approved</p>
            <p className="text-2xl font-semibold text-green-600 dark:text-green-400">
              {stats.approved || 0}
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-4">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Rejected</p>
            <p className="text-2xl font-semibold text-red-600 dark:text-red-400">
              {stats.rejected || 0}
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-4">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Total</p>
            <p className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
              {stats.total || 0}
            </p>
          </div>
        </div>
      )}

      <div className="rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 overflow-hidden">
        <div className="px-4 py-3 border-b border-gray-200 dark:border-neutral-800">
          <h2 className="text-lg font-medium text-gray-900 dark:text-gray-100">
            Pending Approval Requests
          </h2>
        </div>
        <div className="p-4">
          {pendingRequests.length === 0 ? (
            <div className="rounded-md border border-blue-200 bg-blue-50 px-4 py-3 text-blue-800 dark:border-blue-800/50 dark:bg-blue-900/30 dark:text-blue-300">
              No pending approval requests
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 dark:bg-neutral-800/50">
                  <tr>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">ID</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Requester</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Trader</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Amount</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Type</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Date</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-neutral-800">
                  {pendingRequests.map((request) => (
                    <tr key={request.id} className="hover:bg-gray-50 dark:hover:bg-neutral-800/60">
                      <td className="px-4 py-3 align-top text-gray-900 dark:text-gray-100">{request.id}</td>
                      <td className="px-4 py-3 align-top">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {request.requester?.name || 'N/A'}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {request.requester?.email || ''}
                        </div>
                        <div className="mt-1 inline-flex items-center rounded-full border border-gray-300 dark:border-neutral-700 px-2 py-0.5 text-xs text-gray-700 dark:text-gray-300">
                          {request.requester?.role || 'N/A'}
                        </div>
                      </td>
                      <td className="px-4 py-3 align-top">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {request.trader?.name || 'N/A'}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {request.trader?.email || ''}
                        </div>
                      </td>
                      <td className="px-4 py-3 align-top">
                        <div className="font-semibold text-gray-900 dark:text-gray-100">
                          {formatAmount(request.amount)}
                        </div>
                      </td>
                      <td className="px-4 py-3 align-top">
                        <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${
                          request.payment_type === 'cash'
                            ? 'text-blue-700 bg-blue-50 ring-blue-200 dark:text-blue-300 dark:bg-blue-950/40 dark:ring-blue-900/50'
                            : 'text-purple-700 bg-purple-50 ring-purple-200 dark:text-purple-300 dark:bg-purple-950/40 dark:ring-purple-900/50'
                        }`}>
                          {getPaymentTypeIcon(request.payment_type)}
                          {request.payment_type.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-4 py-3 align-top">
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {formatDate(request.created_at)}
                        </div>
                      </td>
                      <td className="px-4 py-3 align-top">
                        <div className="flex gap-2">
                          <button
                            className="inline-flex items-center gap-1.5 rounded-md bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-green-500/50 disabled:opacity-50"
                            onClick={() => handleOpenDialog(request, 'approve')}
                          >
                            <CheckCircle className="h-4 w-4" />
                            Approve
                          </button>
                          <button
                            className="inline-flex items-center gap-1.5 rounded-md bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-red-500/50 disabled:opacity-50"
                            onClick={() => handleOpenDialog(request, 'reject')}
                          >
                            <XCircle className="h-4 w-4" />
                            Reject
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {dialogOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/50" onClick={handleCloseDialog} />
          <div
            className="relative w-full max-w-lg mx-4 rounded-lg border border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="px-4 py-3 border-b border-gray-200 dark:border-neutral-800">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                {actionType === 'approve' ? 'Approve Payment' : 'Reject Payment'}
              </h3>
            </div>
            <div className="p-4">
              {selectedRequest && (
                <div className="space-y-2">
                  <p className="text-sm text-gray-800 dark:text-gray-200">
                    <strong>Requester:</strong> {selectedRequest.requester?.name}
                  </p>
                  <p className="text-sm text-gray-800 dark:text-gray-200">
                    <strong>Trader:</strong> {selectedRequest.trader?.name}
                  </p>
                  <p className="text-sm text-gray-800 dark:text-gray-200">
                    <strong>Amount:</strong> {formatAmount(selectedRequest.amount)}
                  </p>
                  <p className="text-sm text-gray-800 dark:text-gray-200">
                    <strong>Payment Type:</strong> {selectedRequest.payment_type.toUpperCase()}
                  </p>

                  {actionType === 'reject' && (
                    <div className="pt-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Rejection Reason *
                      </label>
                      <textarea
                        className="w-full rounded-md border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-gray-900 dark:text-gray-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows={3}
                        value={rejectionReason}
                        onChange={(e) => setRejectionReason(e.target.value)}
                        required
                      />
                    </div>
                  )}

                  <div className="pt-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Admin Notes (Optional)
                    </label>
                    <textarea
                      className="w-full rounded-md border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-gray-900 dark:text-gray-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      value={adminNotes}
                      onChange={(e) => setAdminNotes(e.target.value)}
                    />
                  </div>
                </div>
              )}
            </div>
            <div className="px-4 py-3 border-t border-gray-200 dark:border-neutral-800 flex justify-end gap-2">
              <button
                className="inline-flex items-center rounded-md border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                onClick={handleCloseDialog}
                disabled={processing}
              >
                Cancel
              </button>
              <button
                onClick={actionType === 'approve' ? handleApprove : handleReject}
                className={`inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium text-white focus:outline-none focus:ring-2 disabled:opacity-50 ${
                  actionType === 'approve'
                    ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500/50'
                    : 'bg-red-600 hover:bg-red-700 focus:ring-red-500/50'
                }`}
                disabled={processing || (actionType === 'reject' && !rejectionReason.trim())}
              >
                {processing ? (
                  <span className="h-5 w-5 animate-spin rounded-full border-2 border-white/60 border-t-transparent" />
                ) : actionType === 'approve' ? (
                  'Approve'
                ) : (
                  'Reject'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
    
  );
};

export default PaymentApprovals;