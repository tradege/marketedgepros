import React, { useState } from 'react';
import { ChevronRight, ChevronDown, User, Users, Shield, UserCog } from 'lucide-react';

const UserTreeView = ({ users, onUserClick }) => {
  const [expandedNodes, setExpandedNodes] = useState(new Set());

  const toggleNode = (userId) => {
    console.log('toggleNode called with userId:', userId);
    setExpandedNodes(prev => {
      const newExpanded = new Set(prev);
      if (newExpanded.has(userId)) {
        newExpanded.delete(userId);
        console.log('Collapsed node:', userId);
      } else {
        newExpanded.add(userId);
        console.log('Expanded node:', userId);
      }
      console.log('New expanded nodes:', Array.from(newExpanded));
      return newExpanded;
    });
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'supermaster':
        return <Shield className="w-4 h-4 text-purple-400" />;
      case 'master':
        return <UserCog className="w-4 h-4 text-blue-400" />;
      case 'agent':
        return <Users className="w-4 h-4 text-green-400" />;
      case 'trader':
        return <User className="w-4 h-4 text-gray-400" />;
      default:
        return <User className="w-4 h-4 text-gray-400" />;
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'supermaster':
        return 'bg-purple-900/30 text-purple-300 border-purple-700';
      case 'master':
        return 'bg-blue-900/30 text-blue-300 border-blue-700';
      case 'agent':
        return 'bg-green-900/30 text-green-300 border-green-700';
      case 'trader':
        return 'bg-gray-800/30 text-gray-300 border-gray-700';
      default:
        return 'bg-gray-800/30 text-gray-300 border-gray-700';
    }
  };

  const UserNode = ({ user, level = 0 }) => {
    const hasChildren = user.children && user.children.length > 0;
    const isExpanded = expandedNodes.has(user.id);
    const paddingLeft = level * 24;

    const handleToggle = (e) => {
      e.stopPropagation();
      e.preventDefault();
      console.log('handleToggle called for user:', user.id, user.first_name, user.last_name);
      toggleNode(user.id);
    };

    return (
      <div className="border-l-2 border-gray-700/50">
        <div
          className="flex items-center gap-2 p-3 border-b border-gray-800/50 transition-colors"
          style={{ paddingLeft: `${paddingLeft + 12}px` }}
        >
          {/* Expand/Collapse button - using onMouseDown instead of onClick */}
          {hasChildren ? (
            <button
              type="button"
              onMouseDown={handleToggle}
              className="p-2 hover:bg-gray-700/70 rounded transition-colors cursor-pointer flex-shrink-0 bg-green-900/20"
              style={{
                minWidth: '36px',
                minHeight: '36px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 100,
                position: 'relative',
                border: '2px solid rgb(34, 197, 94)'
              }}
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
            >
              {isExpanded ? (
                <ChevronDown className="w-6 h-6 text-green-400" />
              ) : (
                <ChevronRight className="w-6 h-6 text-green-400" />
              )}
            </button>
          ) : (
            <div className="w-10" />
          )}

          {/* Role icon */}
          <div className="flex-shrink-0">
            {getRoleIcon(user.role)}
          </div>

          {/* User info */}
          <div
            className="flex-1 flex items-center gap-3 cursor-pointer hover:bg-gray-800/30 p-2 rounded"
            onClick={() => onUserClick && onUserClick(user)}
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-200 truncate">
                  {user.first_name} {user.last_name}
                </span>
                <span
                  className={`px-2 py-0.5 text-xs font-medium rounded border ${getRoleBadgeColor(
                    user.role
                  )}`}
                >
                  {user.role}
                </span>
              </div>
              <div className="text-xs text-gray-400 truncate">{user.email}</div>
            </div>

            {/* Children count */}
            {hasChildren && (
              <div className="flex-shrink-0 px-2 py-1 bg-gray-800 rounded text-xs text-gray-400">
                {user.children.length} {user.children.length === 1 ? 'user' : 'users'}
              </div>
            )}

            {/* Status badges */}
            <div className="flex items-center gap-2 flex-shrink-0">
              {user.is_verified && (
                <span className="px-2 py-0.5 text-xs bg-green-900/30 text-green-300 rounded border border-green-700">
                  Verified
                </span>
              )}
              {user.kyc_status === 'approved' && (
                <span className="px-2 py-0.5 text-xs bg-blue-900/30 text-blue-300 rounded border border-blue-700">
                  KYC
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Children */}
        {hasChildren && isExpanded && (
          <div className="bg-gray-900/30">
            {user.children.map((child) => (
              <UserNode key={child.id} user={child} level={level + 1} />
            ))}
          </div>
        )}
      </div>
    );
  };

  if (!users || users.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <Users className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No users found</p>
      </div>
    );
  }

  console.log('UserTreeView rendering with users:', users.length);

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
      {users.map((user) => (
        <UserNode key={user.id} user={user} level={0} />
      ))}
    </div>
  );
};

export default UserTreeView;
