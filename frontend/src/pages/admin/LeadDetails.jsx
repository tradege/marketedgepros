import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  ArrowLeft, Mail, Phone, MapPin, Calendar, DollarSign, 
  User, Edit, Trash2, CheckCircle, XCircle, Clock,
  MessageSquare, Plus, Send
} from 'lucide-react';

const LeadDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [newNote, setNewNote] = useState('');
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    fetchLeadDetails();
    fetchNotes();
  }, [id]);

  const fetchLeadDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/api/v1/admin/crm/leads/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setLead(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching lead:', error);
      setLoading(false);
    }
  };

  const fetchNotes = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/api/v1/admin/crm/leads/${id}/notes`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setNotes(response.data.notes || []);
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  const handleAddNote = async () => {
    if (!newNote.trim()) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/v1/admin/crm/leads/${id}/notes`, 
        { content: newNote },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      setNewNote('');
      fetchNotes();
    } catch (error) {
      console.error('Error adding note:', error);
    }
  };

  const handleStatusChange = async (newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`/api/v1/admin/crm/leads/${id}`, 
        { status: newStatus },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      fetchLeadDetails();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this lead?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/v1/admin/crm/leads/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      navigate('/admin/crm');
    } catch (error) {
      console.error('Error deleting lead:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-500',
      contacted: 'bg-yellow-500',
      qualified: 'bg-purple-500',
      negotiation: 'bg-orange-500',
      converted: 'bg-green-500',
      lost: 'bg-red-500'
    };
    return colors[status] || 'bg-gray-500';
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-500';
    if (score >= 40) return 'text-yellow-500';
    return 'text-red-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <XCircle className="w-16 h-16 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Lead Not Found</h2>
        <p className="text-gray-400 mb-4">The lead you're looking for doesn't exist.</p>
        <button
          onClick={() => navigate('/admin/crm')}
          className="px-4 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600"
        >
          Back to CRM
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black p-6">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/admin/crm')}
          className="flex items-center text-gray-400 hover:text-white mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to CRM
        </button>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-4">
              <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                {lead.name?.charAt(0) || 'L'}
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">{lead.name || 'Unnamed Lead'}</h1>
                <p className="text-gray-400 mb-2">{lead.company || 'No company'}</p>
                <div className="flex items-center space-x-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${getStatusColor(lead.status)}`}>
                    {lead.status?.toUpperCase()}
                  </span>
                  <span className={`text-2xl font-bold ${getScoreColor(lead.score)}`}>
                    Score: {lead.score || 0}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={() => navigate(`/admin/crm/${id}/edit`)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center"
              >
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex space-x-4 border-b border-gray-700">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 font-semibold ${
              activeTab === 'overview'
                ? 'text-cyan-500 border-b-2 border-cyan-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            className={`px-4 py-2 font-semibold ${
              activeTab === 'notes'
                ? 'text-cyan-500 border-b-2 border-cyan-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Notes ({notes.length})
          </button>
          <button
            onClick={() => setActiveTab('activity')}
            className={`px-4 py-2 font-semibold ${
              activeTab === 'activity'
                ? 'text-cyan-500 border-b-2 border-cyan-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Activity
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {activeTab === 'overview' && (
            <>
              {/* Contact Information */}
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">Contact Information</h2>
                <div className="space-y-3">
                  <div className="flex items-center text-gray-300">
                    <Mail className="w-5 h-5 mr-3 text-cyan-500" />
                    <span>{lead.email || 'No email'}</span>
                  </div>
                  <div className="flex items-center text-gray-300">
                    <Phone className="w-5 h-5 mr-3 text-cyan-500" />
                    <span>{lead.phone || 'No phone'}</span>
                  </div>
                  <div className="flex items-center text-gray-300">
                    <MapPin className="w-5 h-5 mr-3 text-cyan-500" />
                    <span>{lead.location || 'No location'}</span>
                  </div>
                </div>
              </div>

              {/* Lead Details */}
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">Lead Details</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Source</p>
                    <p className="text-white font-semibold">{lead.source || 'Unknown'}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Budget</p>
                    <p className="text-white font-semibold flex items-center">
                      <DollarSign className="w-4 h-4 mr-1" />
                      {lead.budget || 'Not specified'}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Assigned To</p>
                    <p className="text-white font-semibold flex items-center">
                      <User className="w-4 h-4 mr-1" />
                      {lead.assigned_to || 'Unassigned'}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Next Follow-up</p>
                    <p className="text-white font-semibold flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {lead.next_followup || 'Not scheduled'}
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}

          {activeTab === 'notes' && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">Notes</h2>
              
              {/* Add Note */}
              <div className="mb-6">
                <textarea
                  value={newNote}
                  onChange={(e) => setNewNote(e.target.value)}
                  placeholder="Add a note..."
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500"
                  rows="3"
                />
                <button
                  onClick={handleAddNote}
                  className="mt-2 px-4 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 flex items-center"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Note
                </button>
              </div>

              {/* Notes List */}
              <div className="space-y-4">
                {notes.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">No notes yet</p>
                ) : (
                  notes.map((note, index) => (
                    <div key={index} className="bg-gray-700 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center">
                          <MessageSquare className="w-4 h-4 text-cyan-500 mr-2" />
                          <span className="text-white font-semibold">{note.created_by || 'Admin'}</span>
                        </div>
                        <span className="text-gray-400 text-sm">{note.created_at || 'Just now'}</span>
                      </div>
                      <p className="text-gray-300">{note.content}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {activeTab === 'activity' && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">Activity Timeline</h2>
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="w-8 h-8 bg-cyan-500 rounded-full flex items-center justify-center mr-4">
                    <Clock className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-semibold">Lead created</p>
                    <p className="text-gray-400 text-sm">{lead.created_at || 'Recently'}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">Quick Actions</h2>
            <div className="space-y-2">
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center justify-center">
                <Send className="w-4 h-4 mr-2" />
                Send Email
              </button>
              <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center justify-center">
                <Calendar className="w-4 h-4 mr-2" />
                Schedule Follow-up
              </button>
              <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 flex items-center justify-center">
                <CheckCircle className="w-4 h-4 mr-2" />
                Convert to Customer
              </button>
            </div>
          </div>

          {/* Change Status */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">Change Status</h2>
            <div className="space-y-2">
              {['new', 'contacted', 'qualified', 'negotiation', 'converted', 'lost'].map((status) => (
                <button
                  key={status}
                  onClick={() => handleStatusChange(status)}
                  className={`w-full px-4 py-2 rounded-lg text-white ${getStatusColor(status)} hover:opacity-80`}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeadDetails;
