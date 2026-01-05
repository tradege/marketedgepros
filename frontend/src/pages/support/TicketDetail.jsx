import { useState, useEffect } from 'react';
import { useToast } from '../../contexts/ToastContext';
import { useParams, useSearchParams, Link } from 'react-router-dom';
import { ArrowLeft, Send, Clock, CheckCircle, User, Calendar, Tag, AlertTriangle, Loader, MessageCircle } from 'lucide-react';
import Layout from '../../components/layout/Layout';
import SEO from '../../components/SEO';
import api from "../../services/api";

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function TicketDetail() {
  const { ticketNumber } = useParams();
  const [searchParams] = useSearchParams();
  const email = searchParams.get('email');

  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newMessage, setNewMessage] = useState('');
  const [sendingMessage, setSendingMessage] = useState(false);

  useEffect(() => {
    if (ticketNumber && email) {
      fetchTicket();
    }
  }, [ticketNumber, email]);

  const fetchTicket = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/support/tickets/${ticketNumber}`, {
        params: { email }
      });
      setTicket(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load ticket');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      setSendingMessage(true);
      await axios.post(`${API_URL}/support/tickets/${ticketNumber}/messages`, {
        email,
        message: newMessage,
        name: ticket.name
      });
      
      setNewMessage('');
      await fetchTicket(); // Reload ticket to show new message
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to send message');
    } finally {
      setSendingMessage(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      open: { color: 'bg-blue-500/10 text-blue-400 border-blue-500/30', icon: Clock, label: 'Open' },
      in_progress: { color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30', icon: MessageCircle, label: 'In Progress' },
      waiting_customer: { color: 'bg-purple-500/10 text-purple-400 border-purple-500/30', icon: AlertTriangle, label: 'Waiting for You' },
      resolved: { color: 'bg-green-500/10 text-green-400 border-green-500/30', icon: CheckCircle, label: 'Resolved' },
      closed: { color: 'bg-gray-500/10 text-gray-400 border-gray-500/30', icon: CheckCircle, label: 'Closed' }
    };
    return badges[status] || badges.open;
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: 'text-green-400',
      medium: 'text-yellow-400',
      high: 'text-orange-400',
      urgent: 'text-red-400'
    };
    return colors[priority] || colors.medium;
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

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-slate-900 flex items-center justify-center">
          <Loader className="w-8 h-8 text-blue-500 animate-spin" />
        </div>
      </Layout>
    );
  }

  if (error || !ticket) {
    return (
      <Layout>
        <div className="min-h-screen bg-slate-900 flex items-center justify-center">
          <div className="text-center">
            <AlertTriangle className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">Ticket Not Found</h2>
            <p className="text-gray-400 mb-6">{error || 'The ticket you are looking for does not exist.'}</p>
            <Link
              to="/support"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-xl font-semibold hover:bg-blue-600 transition-all"
            >
              <ArrowLeft className="w-5 h-5" />
              Back to Support
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  const statusBadge = getStatusBadge(ticket.status);
  const StatusIcon = statusBadge.icon;

  return (
    <Layout>
      <SEO
        title={`Ticket #${ticket.ticket_number} - ${ticket.subject}`}
        description={ticket.description}
      />

      {/* Header */}
      <section className="relative pt-32 pb-12 overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            to="/support"
            className="inline-flex items-center gap-2 text-gray-300 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Support
          </Link>

          <div className="flex items-start justify-between gap-4 mb-6">
            <div>
              <div className="flex items-center gap-3 mb-3">
                <span className="font-mono text-lg text-gray-400">#{ticket.ticket_number}</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium border ${statusBadge.color} flex items-center gap-1.5`}>
                  <StatusIcon className="w-4 h-4" />
                  {statusBadge.label}
                </span>
              </div>
              <h1 className="text-4xl font-bold text-white mb-2">{ticket.subject}</h1>
              <div className="flex items-center gap-6 text-gray-400">
                <span className="flex items-center gap-2">
                  <User className="w-4 h-4" />
                  {ticket.name}
                </span>
                <span className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {formatDate(ticket.created_at)}
                </span>
                <span className="flex items-center gap-2">
                  <Tag className="w-4 h-4" />
                  {ticket.category}
                </span>
                <span className={`flex items-center gap-2 ${getPriorityColor(ticket.priority)}`}>
                  <AlertTriangle className="w-4 h-4" />
                  {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)} Priority
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-12 bg-slate-900">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Original Message */}
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                <User className="w-5 h-5 text-blue-400" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="font-semibold text-white">{ticket.name}</span>
                  <span className="text-sm text-gray-500">{formatDate(ticket.created_at)}</span>
                </div>
                <div className="text-gray-300 whitespace-pre-wrap">{ticket.description}</div>
              </div>
            </div>
          </div>

          {/* Messages */}
          {ticket.messages && ticket.messages.length > 0 && (
            <div className="space-y-4 mb-6">
              {ticket.messages.map((message) => (
                <div
                  key={message.id}
                  className={`bg-slate-800/50 backdrop-blur-sm border rounded-xl p-6 ${
                    message.is_staff
                      ? 'border-green-500/30 bg-green-500/5'
                      : 'border-slate-700'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.is_staff
                        ? 'bg-green-500/20'
                        : 'bg-blue-500/20'
                    }`}>
                      <User className={`w-5 h-5 ${
                        message.is_staff ? 'text-green-400' : 'text-blue-400'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="font-semibold text-white">
                          {message.is_staff ? 'Support Team' : message.name || ticket.name}
                        </span>
                        {message.is_staff && (
                          <span className="px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/30">
                            Staff
                          </span>
                        )}
                        <span className="text-sm text-gray-500">{formatDate(message.created_at)}</span>
                      </div>
                      <div className="text-gray-300 whitespace-pre-wrap">{message.message}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Reply Form */}
          {ticket.status !== 'closed' && (
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Add a Reply</h3>
              <form onSubmit={handleSendMessage}>
                <textarea
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type your message here..."
                  rows={6}
                  className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none mb-4"
                  disabled={sendingMessage}
                />
                <button
                  type="submit"
                  disabled={sendingMessage || !newMessage.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-blue-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {sendingMessage ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      Send Reply
                    </>
                  )}
                </button>
              </form>
            </div>
          )}

          {ticket.status === 'closed' && (
            <div className="bg-gray-500/10 border border-gray-500/30 rounded-xl p-6 text-center">
              <CheckCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-white mb-2">This ticket is closed</h3>
              <p className="text-gray-400">
                If you need further assistance, please create a new support ticket.
              </p>
            </div>
          )}
        </div>
      </section>
    </Layout>
  );
}

