import { useState, useEffect } from 'react';
import { useToast } from '../../contexts/ToastContext';
import { useNavigate } from 'react-router-dom';
import AdminLayout from '../../components/admin/AdminLayout';
import { 
  Users, 
  Plus, 
  Filter, 
  Search, 
  Mail, 
  Phone, 
  Calendar,
  TrendingUp,
  DollarSign,
  Target,
  Activity,
  X
} from 'lucide-react';
import { crmAPI } from '../../services/api';

export default function CRM() {
  const toast = useToast();
  const navigate = useNavigate();
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('table'); // 'table' or 'pipeline'
  const [filters, setFilters] = useState({
    status: 'all',
    source: 'all',
    search: ''
  });
  const [stats, setStats] = useState({
    total: 0,
    new: 0,
    contacted: 0,
    qualified: 0,
    converted: 0
  });
  const [showAddModal, setShowAddModal] = useState(false);
  const [newLead, setNewLead] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    company: '',
    status: 'new',
    source: 'website',
    score: 50,
    budget: ''
  });

  useEffect(() => {
    fetchLeads();
    fetchStats();
  }, [filters]);

  const fetchLeads = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.status !== 'all') params.status = filters.status;
      if (filters.source !== 'all') params.source = filters.source;
      if (filters.search) params.search = filters.search;
      
      const response = await crmAPI.getLeads(params);
      setLeads(response.data.leads || []);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await crmAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleCreateLead = async (e) => {
    e.preventDefault();
    try {
      const response = await crmAPI.createLead(newLead);
      setShowAddModal(false);
      setNewLead({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        company: '',
        status: 'new',
        source: 'website',
        score: 50,
        budget: ''
      });
      fetchLeads();
      fetchStats();
    } catch (error) {
      console.error('Error creating lead:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      toast.error('Error creating lead: ' + (error.response?.data?.error || error.message));
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      contacted: 'bg-yellow-100 text-yellow-800',
      qualified: 'bg-purple-100 text-purple-800',
      negotiation: 'bg-orange-100 text-orange-800',
      converted: 'bg-green-100 text-green-800',
      lost: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getSourceColor = (source) => {
    const colors = {
      website: 'bg-indigo-100 text-indigo-800',
      referral: 'bg-pink-100 text-pink-800',
      affiliate: 'bg-cyan-100 text-cyan-800',
      social_media: 'bg-purple-100 text-purple-800'
    };
    return colors[source] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const pipeline = {
    new: leads.filter(l => l.status === 'new'),
    contacted: leads.filter(l => l.status === 'contacted'),
    qualified: leads.filter(l => l.status === 'qualified'),
    negotiation: leads.filter(l => l.status === 'negotiation'),
    converted: leads.filter(l => l.status === 'converted')
  };

  const renderPipelineColumn = (stage, stageLeads) => (
    <div key={stage} className="flex-shrink-0 w-80">
      <div className="bg-slate-700/30 rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-white capitalize">{stage}</h3>
          <span className="bg-slate-600 text-white text-xs px-2 py-1 rounded-full">
            {stageLeads.length}
          </span>
        </div>
        <div className="space-y-3">
          {stageLeads.map(lead => (
            <div 
              key={lead.id}
              className="bg-slate-800 border border-slate-600 rounded-lg p-4 cursor-pointer hover:border-blue-500 transition-colors"
            >
              <div className="font-medium text-white mb-2">
                {lead.first_name} {lead.last_name}
              </div>
              {lead.company && (
                <div className="text-sm text-gray-400 mb-2">{lead.company}</div>
              )}
              <div className="flex items-center gap-2 text-sm text-gray-300 mb-2">
                <Mail size={14} />
                {lead.email}
              </div>
              {lead.phone && (
                <div className="flex items-center gap-2 text-sm text-gray-300 mb-2">
                  <Phone size={14} />
                  {lead.phone}
                </div>
              )}
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-600">
                <span className={`text-sm font-semibold ${getScoreColor(lead.score)}`}>
                  Score: {lead.score}
                </span>
                {lead.budget && (
                  <span className="text-sm text-gray-300">
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

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">CRM</h1>
            <p className="text-slate-400 mt-1">Manage your leads and customer relationships</p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
          >
            <Plus size={20} />
            Add Lead
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Total Leads</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.total}</p>
              </div>
              <div className="bg-blue-500/10 p-3 rounded-lg">
                <Users className="text-blue-500" size={24} />
              </div>
            </div>
          </div>
          
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">New</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.new}</p>
              </div>
              <div className="bg-green-500/10 p-3 rounded-lg">
                <TrendingUp className="text-green-500" size={24} />
              </div>
            </div>
          </div>
          
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Contacted</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.contacted}</p>
              </div>
              <div className="bg-yellow-500/10 p-3 rounded-lg">
                <Activity className="text-yellow-500" size={24} />
              </div>
            </div>
          </div>
          
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Qualified</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.qualified}</p>
              </div>
              <div className="bg-purple-500/10 p-3 rounded-lg">
                <Target className="text-purple-500" size={24} />
              </div>
            </div>
          </div>
          
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Converted</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.converted}</p>
              </div>
              <div className="bg-emerald-500/10 p-3 rounded-lg">
                <DollarSign className="text-emerald-500" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* View Toggle & Filters */}
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <button
              onClick={() => setView('table')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                view === 'table' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              Table View
            </button>
            <button
              onClick={() => setView('pipeline')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                view === 'pipeline' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              Pipeline View
            </button>
          </div>
          
          <div className="flex gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search leads..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="pl-10 pr-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />
            </div>
            
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="all">All Status</option>
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="qualified">Qualified</option>
              <option value="negotiation">Negotiation</option>
              <option value="converted">Converted</option>
              <option value="lost">Lost</option>
            </select>
            
            <select
              value={filters.source}
              onChange={(e) => setFilters({ ...filters, source: e.target.value })}
              className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="all">All Sources</option>
              <option value="website">Website</option>
              <option value="referral">Referral</option>
              <option value="affiliate">Affiliate</option>
              <option value="social_media">Social Media</option>
            </select>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        )}

        {/* Table View */}
        {!loading && view === 'table' && (
          <div className="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-700/50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Lead</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Contact</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Source</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Score</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Budget</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Assigned To</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Next Follow-up</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {leads.map((lead) => (
                    <tr 
                      key={lead.id} 
                      onClick={() => navigate(`/admin/crm/${lead.id}`)}
                      className="hover:bg-slate-700/50 cursor-pointer transition-colors"
                    >
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-medium text-white">
                            {lead.first_name} {lead.last_name}
                          </div>
                          {lead.company && (
                            <div className="text-sm text-gray-400">{lead.company}</div>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2 text-sm text-gray-300">
                            <Mail size={14} />
                            {lead.email}
                          </div>
                          {lead.phone && (
                            <div className="flex items-center gap-2 text-sm text-gray-300">
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
                      <td className="px-6 py-4 text-sm text-white">
                        {lead.budget ? `$${lead.budget.toLocaleString()}` : '-'}
                      </td>
                      <td className="px-6 py-4 text-sm text-white">
                        {lead.assigned_user ? lead.assigned_user.name : 'Unassigned'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-300">
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
        {!loading && view === 'pipeline' && (
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex gap-4 overflow-x-auto">
              {Object.entries(pipeline).map(([stage, stageLeads]) => 
                renderPipelineColumn(stage, stageLeads)
              )}
            </div>
          </div>
        )}
      </div>

      {/* Add Lead Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Add New Lead</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
              >
                <X className="text-gray-400" size={20} />
              </button>
            </div>

            <form onSubmit={handleCreateLead} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">First Name *</label>
                  <input
                    type="text"
                    required
                    value={newLead.first_name}
                    onChange={(e) => setNewLead({ ...newLead, first_name: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Last Name *</label>
                  <input
                    type="text"
                    required
                    value={newLead.last_name}
                    onChange={(e) => setNewLead({ ...newLead, last_name: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email *</label>
                <input
                  type="email"
                  required
                  value={newLead.email}
                  onChange={(e) => setNewLead({ ...newLead, email: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Phone</label>
                <input
                  type="tel"
                  value={newLead.phone}
                  onChange={(e) => setNewLead({ ...newLead, phone: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Company</label>
                <input
                  type="text"
                  value={newLead.company}
                  onChange={(e) => setNewLead({ ...newLead, company: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
                  <select
                    value={newLead.status}
                    onChange={(e) => setNewLead({ ...newLead, status: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="new">New</option>
                    <option value="contacted">Contacted</option>
                    <option value="qualified">Qualified</option>
                    <option value="negotiation">Negotiation</option>
                    <option value="converted">Converted</option>
                    <option value="lost">Lost</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Source</label>
                  <select
                    value={newLead.source}
                    onChange={(e) => setNewLead({ ...newLead, source: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="website">Website</option>
                    <option value="referral">Referral</option>
                    <option value="affiliate">Affiliate</option>
                    <option value="social_media">Social Media</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Score (0-100)</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={newLead.score}
                    onChange={(e) => setNewLead({ ...newLead, score: parseInt(e.target.value) })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Budget ($)</label>
                  <input
                    type="number"
                    value={newLead.budget}
                    onChange={(e) => setNewLead({ ...newLead, budget: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-6 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
                >
                  Create Lead
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
