import { useState, useEffect } from 'react';
import { Ticket, Clock, CheckCircle, AlertCircle, MessageCircle, Loader, Filter } from 'lucide-react';
import { Link } from 'react-router-dom';
import Layout from '../../components/layout/Layout';
import SEO from '../../components/SEO';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function MyTickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchTickets();
  }, [statusFilter]);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const params = statusFilter !== 'all' ? { status: statusFilter } : {};
      
      const response = await axios.get(`${API_URL}/support/tickets/my`, {
        headers: { Authorization: `Bearer ${token}` },
        params
      });
      
      setTickets(response.data.tickets);
    } catch (error) {
      console.error('Error fetching tickets:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      open: { color: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30', icon: Clock, label: 'Open' },
      in_progress: { color: 'bg-teal-500/10 text-teal-400 border-teal-500/30', icon: MessageCircle, label: 'In Progress' },
      waiting_customer: { color: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30', icon: AlertCircle, label: 'Waiting for You' },
      resolved: { color: 'bg-teal-500/10 text-teal-400 border-teal-500/30', icon: CheckCircle, label: 'Resolved' },
      closed: { color: 'bg-gray-500/10 text-gray-400 border-gray-500/30', icon: CheckCircle, label: 'Closed' }
    };
    return badges[status] || badges.open;
  };

  const getPriorityBadge = (priority) => {
    const badges = {
      low: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
      medium: 'bg-teal-500/10 text-teal-400 border-teal-500/30',
      high: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
      urgent: 'bg-teal-500/10 text-teal-400 border-teal-500/30'
    };
    return badges[priority] || badges.medium;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const stats = {
    total: tickets.length,
    open: tickets.filter(t => t.status === 'open').length,
    in_progress: tickets.filter(t => t.status === 'in_progress' || t.status === 'waiting_customer').length,
    resolved: tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
  };

  return (
    <Layout>
      <SEO
        title="My Support Tickets"
        description="View and manage your support tickets"
        keywords="support tickets, help, customer service"
      />

      {/* Hero Section */}
      <section className="relative pt-32 pb-12 overflow-hidden bg-black">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
                My Support <span className="bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text text-transparent">Tickets</span>
              </h1>
              <p className="text-xl text-gray-300">
                Track and manage all your support requests
              </p>
            </div>
            <Link
              to="/support/create-ticket"
              className="hidden md:flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition-all"
            >
              <Ticket className="w-5 h-5" />
              New Ticket
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
              <p className="text-gray-400 text-sm mb-2">Total Tickets</p>
              <p className="text-3xl font-bold text-white">{stats.total}</p>
            </div>
            <div className="bg-slate-900/50 backdrop-blur-sm border border-cyan-500/30 rounded-xl p-6">
              <p className="text-gray-400 text-sm mb-2">Open</p>
              <p className="text-3xl font-bold text-cyan-400">{stats.open}</p>
            </div>
            <div className="bg-slate-900/50 backdrop-blur-sm border border-teal-500/30 rounded-xl p-6">
              <p className="text-gray-400 text-sm mb-2">In Progress</p>
              <p className="text-3xl font-bold text-teal-400">{stats.in_progress}</p>
            </div>
            <div className="bg-slate-900/50 backdrop-blur-sm border border-cyan-500/30 rounded-xl p-6">
              <p className="text-gray-400 text-sm mb-2">Resolved</p>
              <p className="text-3xl font-bold text-cyan-400">{stats.resolved}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Tickets List */}
      <section className="py-12 bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Filters */}
          <div className="flex items-center gap-3 mb-6">
            <Filter className="w-5 h-5 text-gray-400" />
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                statusFilter === 'all'
                  ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setStatusFilter('open')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                statusFilter === 'open'
                  ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              Open
            </button>
            <button
              onClick={() => setStatusFilter('in_progress')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                statusFilter === 'in_progress'
                  ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              In Progress
            </button>
            <button
              onClick={() => setStatusFilter('resolved')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                statusFilter === 'resolved'
                  ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              Resolved
            </button>
          </div>

          {/* Tickets */}
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <Loader className="w-8 h-8 text-cyan-500 animate-spin" />
            </div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-6">
                <Ticket className="w-10 h-10 text-gray-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">No tickets found</h3>
              <p className="text-gray-400 mb-6">You haven't created any support tickets yet.</p>
              <Link
                to="/support/create-ticket"
                className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition-all"
              >
                <Ticket className="w-5 h-5" />
                Create Your First Ticket
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {tickets.map((ticket) => {
                const statusBadge = getStatusBadge(ticket.status);
                const StatusIcon = statusBadge.icon;

                return (
                  <Link
                    key={ticket.id}
                    to={`/support/ticket/${ticket.ticket_number}?email=${ticket.email}`}
                    className="block bg-slate-900/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-cyan-500/50 transition-all"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-cyan-400 font-mono font-semibold">
                            #{ticket.ticket_number}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${statusBadge.color} flex items-center gap-1.5`}>
                            <StatusIcon className="w-3.5 h-3.5" />
                            {statusBadge.label}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityBadge(ticket.priority)}`}>
                            {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
                          </span>
                        </div>
                        <h3 className="text-xl font-semibold text-white mb-2">{ticket.subject}</h3>
                        <p className="text-gray-400 text-sm line-clamp-2">{ticket.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-400">
                      <span>Created {formatDate(ticket.created_at)}</span>
                      {ticket.last_response_at && (
                        <span>Last response {formatDate(ticket.last_response_at)}</span>
                      )}
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      </section>
    </Layout>
  );
}
