import { useState, useEffect } from 'react';
import AdminLayout from '../../components/admin/AdminLayout';
import { FileCheck, CheckCircle, XCircle, Clock } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

function KYCApproval() {
  const [pendingKYC, setPendingKYC] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [allUsers, setAllUsers] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      // Fetch pending KYC
      const kycResponse = await axios.get(
        `${API_BASE_URL}/admin/kyc/pending`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setPendingKYC(kycResponse.data.pending_kyc);

      // Fetch all users to get stats
      const usersResponse = await axios.get(
        `${API_BASE_URL}/admin/users?per_page=1000`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setAllUsers(usersResponse.data.users);
      setError(null);
    } catch (err) {
      setError('Failed to load KYC data');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (userId) => {
    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        `${API_BASE_URL}/admin/kyc/${userId}/approve`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Refresh data
      fetchData();
      alert('KYC approved successfully');
    } catch (err) {
      alert('Failed to approve KYC');
    }
  };

  const handleReject = async (userId) => {
    try {
      const token = localStorage.getItem('access_token');
      const reason = prompt('Please enter rejection reason:');
      if (!reason) return;

      await axios.post(
        `${API_BASE_URL}/admin/kyc/${userId}/reject`,
        { reason },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Refresh data
      fetchData();
      alert('KYC rejected successfully');
    } catch (err) {
      alert('Failed to reject KYC');
    }
  };

  // Calculate stats
  const stats = {
    pending: allUsers.filter(u => u.kyc_status === 'pending').length,
    approved: allUsers.filter(u => u.kyc_status === 'approved').length,
    rejected: allUsers.filter(u => u.kyc_status === 'rejected').length,
    total: allUsers.filter(u => u.kyc_status !== 'not_submitted').length,
  };

  const verificationRate = stats.total > 0 
    ? Math.round((stats.approved / stats.total) * 100) 
    : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white dark:text-white">
          KYC Approval
        </h1>
        <p className="mt-2 text-sm text-gray-300 dark:text-gray-400">
          Review and approve user identity verification
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-600 dark:text-yellow-400">Pending KYC</p>
              <p className="text-2xl font-bold text-yellow-900 dark:text-yellow-100">
                {stats.pending}
              </p>
              <p className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">Requires review</p>
            </div>
            <Clock className="w-12 h-12 text-yellow-600 dark:text-yellow-400" />
          </div>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 dark:text-green-400">Approved</p>
              <p className="text-2xl font-bold text-green-900 dark:text-green-100">
                {stats.approved}
              </p>
              <p className="text-xs text-green-600 dark:text-green-400 mt-1">Verified users</p>
            </div>
            <CheckCircle className="w-12 h-12 text-green-600 dark:text-green-400" />
          </div>
        </div>

        <div className="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600 dark:text-red-400">Rejected</p>
              <p className="text-2xl font-bold text-red-900 dark:text-red-100">
                {stats.rejected}
              </p>
              <p className="text-xs text-red-600 dark:text-red-400 mt-1">Failed verification</p>
            </div>
            <XCircle className="w-12 h-12 text-red-600 dark:text-red-400" />
          </div>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 dark:text-blue-400">Verification Rate</p>
              <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                {verificationRate}%
              </p>
              <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">Success rate</p>
            </div>
            <FileCheck className="w-12 h-12 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
      </div>

      {/* Pending KYC Table */}
      <div className="bg-slate-800/50 dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-white/10 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-white dark:text-white">
            Pending KYC Submissions
          </h2>
        </div>

        {pendingKYC.length === 0 ? (
          <div className="p-8 text-center text-gray-400 dark:text-gray-400">
            <FileCheck className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium">No pending KYC submissions</p>
            <p className="text-sm mt-2">All KYC requests have been processed</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-900 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                    Submitted Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                    Documents
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-slate-800/50 dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {pendingKYC.map((kyc) => (
                  <tr key={kyc.id} className="hover:bg-slate-900 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-white dark:text-white">
                        {kyc.first_name} {kyc.last_name}
                      </div>
                      <div className="text-sm text-gray-400 dark:text-gray-400">
                        ID: #{kyc.id}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 dark:text-gray-400">
                      {kyc.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 dark:text-gray-400">
                      {kyc.kyc_submitted_at ? new Date(kyc.kyc_submitted_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex gap-2">
                        {kyc.kyc_id_url && (
                          <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">ID</span>
                        )}
                        {kyc.kyc_address_url && (
                          <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Address</span>
                        )}
                        {kyc.kyc_selfie_url && (
                          <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">Selfie</span>
                        )}
                        {kyc.kyc_bank_url && (
                          <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">Bank</span>
                        )}
                        {!kyc.kyc_id_url && !kyc.kyc_address_url && !kyc.kyc_selfie_url && !kyc.kyc_bank_url && (
                          <span className="px-2 py-1 text-xs bg-slate-700/50 text-gray-100 rounded">No documents</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <div className="flex gap-2">
                        <button 
                          onClick={() => handleApprove(kyc.id)}
                          className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                        >
                          Approve
                        </button>
                        <button 
                          onClick={() => handleReject(kyc.id)}
                          className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                        >
                          Reject
                        </button>
                        <button className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
                          View
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
    </AdminLayout>
  );
}

export default KYCApproval;

