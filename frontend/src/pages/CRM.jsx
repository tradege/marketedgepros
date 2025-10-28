import { useState, useEffect } from 'react';
import { Users, TrendingUp, UserPlus, Phone, Mail, Calendar, DollarSign, Filter, Search, X, Check, AlertCircle } from 'lucide-react';

export default function CRM() {
  const [view, setView] = useState('list'); // 'list' or 'pipeline'
  const [stats, setStats] = useState({
    total_leads: 0,
    by_status: {},
    by_source: {},
    this_month: 0,
    converted_this_month: 0,
    conversion_rate: 0
  });
  
  const [leads, setLeads] = useState([]);
  const [pipeline, setPipeline] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  
  const [filters, setFilters] = useState({
    status: '',
    source: '',
    search: ''
  });

  useEffect(() => {
    fetchStats();
    fetchLeads();
    fetchPipeline();
  }, [filters]);

  const fetchStats = async () => {
    // Mock data
    setStats({
      total_leads: 156,
      by_status: {
        new: 23,
        contacted: 45,
        qualified: 32,
        negotiating: 18,
        converted: 28,
        lost: 10
      },
      by_source: {
        website: 67,
        referral: 45,
        agent: 23,
        social_media: 21
      },
      this_month: 34,
      converted_this_month: 12,
      conversion_rate: 17.95
    });
  };

  const fetchLeads = async () => {
    // Mock data
    setLeads([
      {
        id: 1,
        first_name: 'John',
        last_name: 'Doe',
        email: 'john@example.com',
        phone: '+1234567890',
        status: 'qualified',
        source: 'website',
        score: 85,
        budget: 10000,
        company: 'Tech Corp',
        assigned_user: { id: 1, name: 'Agent Smith' },
        created_at: '2024-03-15T10:00:00',
        last_contacted_at: '2024-03-18T14:30:00',
        next_follow_up: '2024-03-20T10:00:00'
      },
      {
        id: 2,
        first_name: 'Jane',
        last_name: 'Smith',
        email: 'jane@example.com',
        phone: '+1234567891',
        status: 'contacted',
        source: 'referral',
        score: 72,
        budget: 5000,
        company: 'Business Inc',
        assigned_user: { id: 2, name: 'Agent Johnson' },
        created_at: '2024-03-16T11:00:00',
        last_contacted_at: '2024-03-17T09:15:00',
        next_follow_up: '2024-03-19T15:00:00'
      },
      {
        id: 3,
        first_name: 'Mike',
        last_name: 'Johnson',
        email: 'mike@example.com',
        phone: '+1234567892',
        status: 'new',
        source: 'social_media',
        score: 45,
        budget: null,
        company: null,
        assigned_user: null,
        created_at: '2024-03-18T16:00:00',
        last_contacted_at: null,
        next_follow_up: null
      }
    ]);
    setLoading(false);
  };

  const fetchPipeline = async () => {
    // Mock pipeline data
    setPipeline({
      new: [
        { id: 3, first_name: 'Mike', last_name: 'Johnson', score: 45, budget: null }
      ],
      contacted: [
        { id: 2, first_name: 'Jane', last_name: 'Smith', score: 72, budget: 5000 }
      ],
      qualified: [
        { id: 1, first_name: 'John', last_name: 'Doe', score: 85, budget: 10000 }
      ],
      negotiating: []
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      contacted: 'bg-yellow-100 text-yellow-800',
      qualified: 'bg-green-100 text-green-800',
      negotiating: 'bg-purple-100 text-purple-800',
      converted: 'bg-emerald-100 text-emerald-800',
      lost: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getSourceColor = (source) => {
    const colors = {
      website: 'bg-blue-100 text-blue-800',
      referral: 'bg-green-100 text-green-800',
      agent: 'bg-purple-100 text-purple-800',
      social_media: 'bg-pink-100 text-pink-800',
      paid_ads: 'bg-orange-100 text-orange-800',
      organic: 'bg-teal-100 text-teal-800'
    };
    return colors[source] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const renderPipelineColumn = (stage, stageLeads) => {
    const stageNames = {
      new: 'New',
      contacted: 'Contacted',
      qualified: 'Qualified',
      negotiating: 'Negotiating'
    };

    const stageColors = {
      new: 'border-blue-500',
      contacted: 'border-yellow-500',
      qualified: 'border-green-500',
      negotiating: 'border-purple-500'
    };

    return (
      <div key={stage} className="flex-1 min-w-[280px]">
        <div className={`bg-white rounded-lg border-t-4 ${stageColors[stage]} p-4`}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">{stageNames[stage]}</h3>
            <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
              {stageLeads.length}
            </span>
          </div>

          <div className="space-y-3">
            {stageLeads.map((lead) => (
              <div
                key={lead.id}
                onClick={() => {
                  setSelectedLead(lead);
                  setShowDetailsModal(true);
                }}
                className="bg-gray-50 rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow"
              >
                <div className="font-medium text-gray-900">
                  {lead.first_name} {lead.last_name}
                </div>
                <div className="flex items-center justify-between mt-2">
                  <span className={`text-sm font-semibold ${getScoreColor(lead.score)}`}>
                    Score: {lead.score}
                  </span>
                  {lead.budget && (
                    <span className="text-sm text-gray-600">
                      ${lead.budget.toLocaleString()}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-xl md:text-2xl font-bold text-gray-900">CRM - Lead Management</h1>
          <p className="text-gray-600 mt-1">Manage and convert your leads</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <UserPlus size={20} />
          Add Lead
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Leads</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.total_leads}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="text-blue-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">This Month</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.this_month}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="text-green-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Converted</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.converted_this_month}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Check className="text-purple-600" size={24} />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Conversion Rate</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.conversion_rate}%</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <DollarSign className="text-orange-600" size={24} />
            </div>
          </div>
        </div>
      </div>

      {/* Status Distribution */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Leads by Status</h3>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
          {Object.entries(stats.by_status).map(([status, count]) => (
            <div key={status} className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-gray-900">{count}</p>
              <p className="text-sm text-gray-600 mt-1 capitalize">{status}</p>
            </div>
          ))}
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex flex-wrap gap-2 bg-white rounded-lg shadow p-2 w-fit">
        <button
          onClick={() => setView('list')}
          className={`px-4 py-2 rounded-lg ${
            view === 'list' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          List View
        </button>
        <button
          onClick={() => setView('pipeline')}
          className={`px-4 py-2 rounded-lg ${
            view === 'pipeline' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          Pipeline View
        </button>
      </div>

      {/* List View */}
      {view === 'list' && (
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Search leads..."
                    value={filters.search}
                    onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Status</option>
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="qualified">Qualified</option>
                <option value="negotiating">Negotiating</option>
                <option value="converted">Converted</option>
                <option value="lost">Lost</option>
              </select>
              <select
                value={filters.source}
                onChange={(e) => setFilters({ ...filters, source: e.target.value })}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Sources</option>
                <option value="website">Website</option>
                <option value="referral">Referral</option>
                <option value="agent">Agent</option>
                <option value="social_media">Social Media</option>
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Lead</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Budget</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Assigned To</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Next Follow-up</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {leads.map((lead) => (
                  <tr 
                    key={lead.id} 
                    onClick={() => {
                      setSelectedLead(lead);
                      setShowDetailsModal(true);
                    }}
                    className="hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-6 py-4">
                      <div>
                        <div className="font-medium text-gray-900">
                          {lead.first_name} {lead.last_name}
                        </div>
                        {lead.company && (
                          <div className="text-sm text-gray-500">{lead.company}</div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <Mail size={14} />
                          {lead.email}
                        </div>
                        {lead.phone && (
                          <div className="flex items-center gap-2 text-sm text-gray-600">
                            <Phone size={14} />
                            {lead.phone}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(lead.status)}`}>
                        {lead.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${getSourceColor(lead.source)}`}>
                        {lead.source}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`font-semibold ${getScoreColor(lead.score)}`}>
                        {lead.score}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {lead.budget ? `$${lead.budget.toLocaleString()}` : '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {lead.assigned_user ? lead.assigned_user.name : 'Unassigned'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {lead.next_follow_up ? (
                        <div className="flex items-center gap-2">
                          <Calendar size={14} />
                          {new Date(lead.next_follow_up).toLocaleDateString()}
                        </div>
                      ) : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pipeline View */}
      {view === 'pipeline' && (
        <div className="bg-gray-50 rounded-lg p-6">
          <div className="flex gap-4 overflow-x-auto">
            {Object.entries(pipeline).map(([stage, stageLeads]) => 
              renderPipelineColumn(stage, stageLeads)
            )}
          </div>
        </div>
      )}
    </div>
  );
}

