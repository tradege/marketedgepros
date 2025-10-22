import { useState, useEffect } from 'react';
import { X, User, Mail, Phone, Calendar, Shield, Activity } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

function UserDetailsModal({ userId, onClose }) {
  const [user, setUser] = useState(null);
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
        `${API_BASE_URL}/admin/users/${userId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setUser(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load user details');
    } finally {
      setLoading(false);
    }
  };

  const getRoleBadge = (role) => {
    const badges = {
      supermaster: { color: 'bg-purple-100 text-purple-800', label: 'Super Master' },
      admin: { color: 'bg-blue-100 text-blue-800', label: 'Master' },
      agent: { color: 'bg-green-100 text-green-800', label: 'Agent' },
      trader: { color: 'bg-gray-100 text-gray-800', label: 'Trader' }
    };
    return badges[role] || badges.trader;
  };

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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg w-full max-w-4xl m-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            User Details
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Basic Info */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <User className="w-5 h-5" />
              Basic Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Full Name</label>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {user.first_name} {user.last_name}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Email</label>
                <p className="text-lg font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  {user.email}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Phone</label>
                <p className="text-lg font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  {user.country_code} {user.phone || 'Not provided'}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Role</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${roleBadge.color}`}>
                    {roleBadge.label}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Account Status */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              Account Status
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Status</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Email Verified</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {user.is_verified ? 'Verified' : 'Not Verified'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">KYC Status</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${kycBadge.color}`}>
                    {kycBadge.label}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Activity */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Activity
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Created</label>
                <p className="text-sm font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Last Updated</label>
                <p className="text-sm font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {new Date(user.updated_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Last Login</label>
                <p className="text-sm font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {user.last_login_at ? new Date(user.last_login_at).toLocaleDateString() : 'Never'}
                </p>
              </div>
            </div>
          </div>

          {/* Security */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Security</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Two-Factor Authentication</label>
                <p>
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    user.two_factor_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.two_factor_enabled ? 'Enabled' : 'Disabled'}
                  </span>
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">User ID</label>
                <p className="text-sm font-mono text-gray-900 dark:text-white">
                  #{user.id}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600 px-6 py-4">
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

