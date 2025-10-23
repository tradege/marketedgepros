import { useState, useEffect } from 'react';
import { X, User, Mail, Phone, Calendar, Shield, Activity, Users } from 'lucide-react';
import axios from 'axios';
import { getRoleConfig, getRoleBadge } from '../constants/roles';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

function UserDetailsModal({ userId, onClose }) {
  const [user, setUser] = useState(null);
  const [downline, setDownline] = useState(null);
  const [challenges, setChallenges] = useState(null);
  const [payments, setPayments] = useState(null);
  const [commissions, setCommissions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserDetails();
  }, [userId]);

  const fetchUserDetails = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      const response = await axios.get(
        `${API_BASE_URL}/admin/users/${userId}/full-details`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setUser(response.data.user);
      setDownline(response.data.downline);
      setChallenges(response.data.challenges);
      setPayments(response.data.payments);
      setCommissions(response.data.commissions);
      setError(null);
    } catch (err) {
      setError('Failed to load user details');
    } finally {
      setLoading(false);
    }
  };

  // getRoleBadge is now imported from constants/roles

  const getKYCBadge = (status) => {
    const badges = {
      approved: { color: 'bg-green-100 text-green-800', label: 'Approved' },
      pending: { color: 'bg-yellow-100 text-yellow-800', label: 'Pending' },
      rejected: { color: 'bg-red-100 text-red-800', label: 'Rejected' },
      not_submitted: { color: 'bg-gray-100 text-gray-800', label: 'Not Submitted' }
    };
    return badges[status] || badges.not_submitted;
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
          <div className="text-xl">Loading...</div>
        </div>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
          <div className="text-red-600">{error || 'User not found'}</div>
          <button
            onClick={onClose}
            className="mt-4 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  const roleBadge = getRoleBadge(user.role);
  const kycBadge = getKYCBadge(user.kyc_status);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center" style={{zIndex: 1400}}>
      <div className="bg-gray-800 rounded-lg w-full max-w-6xl m-4 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="sticky top-0 bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-white">
            User Details
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-200"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 overflow-y-auto flex-1">
          {/* Basic Info */}
          <div className="bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <User className="w-5 h-5" />
              Basic Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-400">Full Name</label>
                <p className="text-lg font-medium text-white">
                  {user.first_name} {user.last_name}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Email</label>
                <p className="text-lg font-medium text-white flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  {user.email}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Phone</label>
                <p className="text-lg font-medium text-white flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  {user.country_code} {user.phone || 'Not provided'}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Role</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${roleBadge.color}`}>
                    {roleBadge.label}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Account Status */}
          <div className="bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              Account Status
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm text-gray-400">Status</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Email Verified</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {user.is_verified ? 'Verified' : 'Not Verified'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">KYC Status</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${kycBadge.color}`}>
                    {kycBadge.label}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Activity */}
          <div className="bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Activity
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm text-gray-400">Created</label>
                <p className="text-sm font-medium text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Last Updated</label>
                <p className="text-sm font-medium text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {new Date(user.updated_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">Last Login</label>
                <p className="text-sm font-medium text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {user.last_login_at ? new Date(user.last_login_at).toLocaleDateString() : 'Never'}
                </p>
              </div>
            </div>
          </div>

          {/* Security */}
          <div className="bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Security</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-400">Two-Factor Authentication</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.two_factor_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.two_factor_enabled ? 'Enabled' : 'Disabled'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-400">User ID</label>
                <p className="text-sm font-mono text-white">
                  #{user.id}
                </p>
              </div>
            </div>
          </div>

          {/* Downline/Referrals */}
          {downline && downline.total_count > 0 && (
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Users className="w-5 h-5" />
                Downline ({downline.total_count} referrals)
              </h3>
              <div className="space-y-3">
                {downline.direct_referrals.map((ref) => (
                  <div key={ref.id} className="bg-gray-600 rounded p-3 flex justify-between items-center">
                    <div>
                      <p className="text-white font-medium">{ref.name}</p>
                      <p className="text-sm text-gray-400">{ref.email}</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 text-xs rounded ${ref.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {ref.is_active ? 'Active' : 'Inactive'}
                      </span>
                      <p className="text-xs text-gray-400 mt-1">{ref.children_count} referrals</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Trading Challenges */}
          {challenges && challenges.total_count > 0 && (
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">
                Trading Challenges ({challenges.total_count})
              </h3>
              <div className="space-y-3">
                {challenges.list.map((challenge) => (
                  <div key={challenge.id} className="bg-gray-600 rounded p-3">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="text-white font-medium">{challenge.program_name}</p>
                        <p className="text-sm text-gray-400">Account Size: ${challenge.account_size.toLocaleString()}</p>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded ${
                        challenge.status === 'active' ? 'bg-blue-100 text-blue-800' :
                        challenge.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {challenge.status}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="text-gray-400">Balance:</span>
                        <span className="text-white ml-2">${challenge.current_balance.toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-400">P/L:</span>
                        <span className={`ml-2 ${challenge.profit_loss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          ${challenge.profit_loss.toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Payments */}
          {payments && payments.total_count > 0 && (
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">
                Payments ({payments.total_count})
              </h3>
              <div className="mb-3">
                <p className="text-sm text-gray-400">Total Paid:</p>
                <p className="text-2xl font-bold text-white">${payments.total_amount.toLocaleString()}</p>
              </div>
              <div className="space-y-2">
                {payments.list.slice(0, 5).map((payment) => (
                  <div key={payment.id} className="bg-gray-600 rounded p-2 flex justify-between items-center">
                    <div>
                      <p className="text-white">${payment.amount.toLocaleString()}</p>
                      <p className="text-xs text-gray-400">{payment.payment_type}</p>
                    </div>
                    <span className={`px-2 py-1 text-xs rounded ${
                      payment.status === 'completed' ? 'bg-green-100 text-green-800' :
                      payment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {payment.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-700 border-t border-gray-600 px-6 py-4 flex-shrink-0">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default UserDetailsModal;

