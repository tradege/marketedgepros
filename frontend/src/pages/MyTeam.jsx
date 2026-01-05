import { useState, useEffect } from 'react';
import { Users, TrendingUp, UserPlus, Search, Filter, ChevronDown, ChevronRight } from 'lucide-react';
import { getRoleConfig } from '../constants/roles';
import UserLayout from '../components/layout/UserLayout';
import { hierarchyAPI } from '../services/api';

export default function MyTeam() {
  const [stats, setStats] = useState({
    total_downline: 0,
    direct_children: 0,
    by_role: {},
    active: 0,
    inactive: 0,
    max_depth: 0
  });
  
  const [directTeam, setDirectTeam] = useState([]);
  const [tree, setTree] = useState(null);
  const [view, setView] = useState('list'); // 'list' or 'tree'
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [expandedNodes, setExpandedNodes] = useState(new Set());

  useEffect(() => {
    fetchStats();
    fetchDirectTeam();
    fetchTree();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await hierarchyAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
      // Fallback to empty stats
      setStats({
        total_downline: 0,
        direct_children: 0,
        by_role: {},
        active: 0,
        inactive: 0,
        max_depth: 0
      });
    }
  };

const fetchDirectTeam = async () => {
    try {
      const response = await hierarchyAPI.getMyDirectTeam();
      setDirectTeam(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch direct team:', error);
      setDirectTeam([]);
      setLoading(false);
    }
  };

  const fetchTree = async () => {
    try {
      const response = await hierarchyAPI.getTree();
      setTree(response.data);
    } catch (error) {
      console.error('Failed to fetch tree:', error);
      setTree(null);
    }
  };

  const toggleNode = (nodeId) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId);
    } else {
      newExpanded.add(nodeId);
    }
    setExpandedNodes(newExpanded);
  };

  const renderTreeNode = (node, depth = 0) => {
    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = expandedNodes.has(node.id);
    const roleConfig = getRoleConfig(node.role);

    return (
      <div key={node.id} className="mb-2">
        <div 
          className={`flex items-center gap-3 p-3 rounded-lg border ${
            node.is_active ? 'bg-white border-gray-200' : 'bg-gray-50 border-gray-300'
          }`}
          style={{ marginLeft: `${depth * 40}px` }}
        >
          {hasChildren && (
            <button
              onClick={() => toggleNode(node.id)}
              className="text-gray-500 hover:text-gray-700"
            >
              {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
            </button>
          )}
          
          {!hasChildren && <div className="w-5" />}
          
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-900">{node.name}</span>
              <span className={`px-2 py-1 text-xs rounded-full ${roleConfig.color}`}>
                {roleConfig.label}
              </span>
              {!node.is_active && (
                <span className="px-2 py-1 text-xs rounded-full bg-red-100 text-red-800">
                  Inactive
                </span>
              )}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              Level {node.level} • {node.children_count} direct • {node.email || ''}
            </div>
          </div>
        </div>

        {hasChildren && isExpanded && (
          <div className="mt-2">
            {node.children.map(child => renderTreeNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  // getRoleBadgeColor removed - using getRoleConfig from constants/roles.js instead

  const getKYCBadgeColor = (status) => {
    const colors = {
      approved: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      rejected: 'bg-red-100 text-red-800',
      not_submitted: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <UserLayout>
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-xl md:text-2xl font-bold text-gray-900">My Team</h1>
          <p className="text-gray-600 mt-1">Manage your downline and team members</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <UserPlus size={20} />
          Create User
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Downline</p>
              <p className="text-xl md:text-2xl font-bold text-gray-900 mt-1">{stats.total_downline}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="text-blue-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Direct Team</p>
              <p className="text-xl md:text-2xl font-bold text-gray-900 mt-1">{stats.direct_children}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <UserPlus className="text-green-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Members</p>
              <p className="text-xl md:text-2xl font-bold text-gray-900 mt-1">{stats.active}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <TrendingUp className="text-purple-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Max Depth</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.max_depth} Levels</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Filter className="text-orange-600" size={24} />
            </div>
          </div>
        </div>
      </div>

      {/* Role Distribution */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Team by Role</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(stats.by_role).map(([role, count]) => (
            <div key={role} className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-gray-900">{count}</p>
              <p className="text-sm text-gray-600 mt-1 capitalize">{role}s</p>
            </div>
          ))}
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex gap-2 bg-white rounded-lg shadow p-2 w-fit">
        <button
          onClick={() => setView('list')}
          className={`px-4 py-2 rounded-lg ${
            view === 'list' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          List View
        </button>
        <button
          onClick={() => setView('tree')}
          className={`px-4 py-2 rounded-lg ${
            view === 'tree' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          Tree View
        </button>
      </div>

      {/* List View */}
      {view === 'list' && (
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Direct Team Members</h3>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">KYC Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Direct</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Downline</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Joined</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {directTeam.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <div className="font-medium text-gray-900">
                          {user.first_name} {user.last_name}
                        </div>
                        <div className="text-sm text-gray-500">{user.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${getRoleConfig(user.role).color}`}>
                        {getRoleConfig(user.role).label}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${getKYCBadgeColor(user.kyc_status)}`}>
                        {user.kyc_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{user.children_count}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{user.downline_count}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tree View */}
      {view === 'tree' && tree && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Organization Tree</h3>
          <div className="space-y-2">
            {renderTreeNode(tree)}
          </div>
        </div>
      )}
    </div>
    </UserLayout>
  );
}

