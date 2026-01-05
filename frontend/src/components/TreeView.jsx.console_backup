import React, { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, Edit, Trash2, UserPlus, Eye } from 'lucide-react';
import api from '../services/api';

const TreeNode = ({ user, level = 0, onEdit, onDelete, onView, onAddChild }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [children, setChildren] = useState([]);
  const [childrenCount, setChildrenCount] = useState(0);
  const [loading, setLoading] = useState(false);

  // Load children when node is expanded
  useEffect(() => {
    if (isExpanded && children.length === 0) {
      loadChildren();
    }
  }, [isExpanded]);

  const loadChildren = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/users/${user.id}/children`);
      setChildren(response.data.children || []);
      setChildrenCount(response.data.total_count || 0);
    } catch (error) {
      console.error('Failed to load children:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const hasChildren = user.children_count > 0 || childrenCount > 0;

  // Role display mapping
  const getRoleDisplay = (role) => {
    const roleMap = {
      super_admin: 'Super Admin',
      admin: 'Admin',
      master: 'Master',
      affiliate: 'Affiliate',
      trader: 'Trader'
    };
    return roleMap[role] || role;
  };

  // Role icon
  const getRoleIcon = (role) => {
    switch (role) {
      case 'super_admin':
        return '👑';
      case 'admin':
        return '⚡';
      case 'master':
        return '📁';
      case 'affiliate':
        return '🤝';
      case 'trader':
        return '👤';
      default:
        return '👤';
    }
  };

  return (
    <div className="tree-node">
      <div 
        className="tree-node-content"
        style={{ 
          paddingLeft: `${level * 24}px`,
          display: 'flex',
          alignItems: 'center',
          padding: '8px 12px',
          borderBottom: '1px solid #2a2f3a',
          backgroundColor: level % 2 === 0 ? '#1a1f2e' : '#1e2433',
          transition: 'background-color 0.2s'
        }}
        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#252b3b'}
        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = level % 2 === 0 ? '#1a1f2e' : '#1e2433'}
      >
        {/* Expand/Collapse Button */}
        <div style={{ width: '24px', marginRight: '8px' }}>
          {hasChildren ? (
            <button
              onClick={toggleExpand}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                color: '#8b92a7',
                padding: 0,
                display: 'flex',
                alignItems: 'center'
              }}
            >
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          ) : (
            <span style={{ display: 'inline-block', width: '16px' }}></span>
          )}
        </div>

        {/* Role Icon */}
        <span style={{ marginRight: '8px', fontSize: '16px' }}>
          {getRoleIcon(user.role)}
        </span>

        {/* User Info */}
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ color: '#e8eaed', fontWeight: '500' }}>
            {user.first_name} {user.last_name}
          </span>
          <span style={{ color: '#8b92a7', fontSize: '13px' }}>
            {user.email}
          </span>
          <span 
            style={{ 
              color: '#60a5fa',
              fontSize: '12px',
              backgroundColor: '#1e3a5f',
              padding: '2px 8px',
              borderRadius: '4px'
            }}
          >
            {getRoleDisplay(user.role)}
          </span>
          {hasChildren && (
            <span 
              style={{ 
                color: '#8b92a7',
                fontSize: '12px',
                backgroundColor: '#2a2f3a',
                padding: '2px 8px',
                borderRadius: '4px'
              }}
            >
              [{user.children_count || childrenCount} users]
            </span>
          )}
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '8px', marginLeft: '12px' }}>
          <button
            onClick={() => onView(user)}
            style={{
              background: '#2563eb',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
            title="View"
          >
            <Eye size={14} />
            View
          </button>
          <button
            onClick={() => onEdit(user)}
            style={{
              background: '#059669',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
            title="Edit"
          >
            <Edit size={14} />
            Edit
          </button>
          <button
            onClick={() => onAddChild(user)}
            style={{
              background: '#7c3aed',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
            title="Add Child"
          >
            <UserPlus size={14} />
            Add
          </button>
          <button
            onClick={() => onDelete(user)}
            style={{
              background: '#dc2626',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
            title="Delete"
          >
            <Trash2 size={14} />
            Delete
          </button>
        </div>
      </div>

      {/* Children */}
      {isExpanded && (
        <div className="tree-node-children">
          {loading ? (
            <div style={{ paddingLeft: `${(level + 1) * 24}px`, padding: '12px', color: '#8b92a7' }}>
              Loading...
            </div>
          ) : (
            children.map((child) => (
              <TreeNode
                key={child.id}
                user={child}
                level={level + 1}
                onEdit={onEdit}
                onDelete={onDelete}
                onView={onView}
                onAddChild={onAddChild}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};

const TreeView = ({ onEdit, onDelete, onView, onAddUser }) => {
  const [rootUsers, setRootUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTreeData();
  }, []);

  const loadTreeData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/users/tree');
      setRootUsers(response.data.tree || []);
    } catch (error) {
      console.error('Failed to load tree data:', error);
      setError('Failed to load user hierarchy');
    } finally {
      setLoading(false);
    }
  };

  const handleAddChild = (parentUser) => {
    // Call onAddUser with parent context
    onAddUser(parentUser);
  };

  if (loading) {
    return (
      <div style={{ padding: '24px', textAlign: 'center', color: '#8b92a7' }}>
        Loading user hierarchy...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '24px', textAlign: 'center', color: '#dc2626' }}>
        {error}
      </div>
    );
  }

  if (rootUsers.length === 0) {
    return (
      <div style={{ padding: '24px', textAlign: 'center', color: '#8b92a7' }}>
        No users found
      </div>
    );
  }

  return (
    <div className="tree-view" style={{ 
      backgroundColor: '#1a1f2e',
      borderRadius: '8px',
      overflow: 'hidden',
      border: '1px solid #2a2f3a'
    }}>
      {rootUsers.map((user) => (
        <TreeNode
          key={user.id}
          user={user}
          level={0}
          onEdit={onEdit}
          onDelete={onDelete}
          onView={onView}
          onAddChild={handleAddChild}
        />
      ))}
    </div>
  );
};

export default TreeView;

