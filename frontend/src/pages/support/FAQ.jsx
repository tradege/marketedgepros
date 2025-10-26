import { useState, useEffect } from 'react';
import { Search, ChevronDown, ChevronUp, ThumbsUp, ThumbsDown, Loader } from 'lucide-react';
import { Link } from 'react-router-dom';
import Layout from '../../components/layout/Layout';
import SEO from '../../components/SEO';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://marketedgepros.com/api/v1';

export default function FAQ() {
  const [faqs, setFaqs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [expandedFaq, setExpandedFaq] = useState(null);
  const [feedbackGiven, setFeedbackGiven] = useState({});

  useEffect(() => {
    fetchFAQs();
    fetchCategories();
  }, [selectedCategory]);

  const fetchFAQs = async () => {
    try {
      setLoading(true);
      const params = selectedCategory !== 'all' ? { category: selectedCategory } : {};
      const response = await axios.get(`${API_URL}/support/faq/`, { params });
      setFaqs(response.data.faqs);
    } catch (error) {
      console.error('Error fetching FAQs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/support/faq/categories`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleFeedback = async (faqId, isHelpful) => {
    try {
      await axios.post(`${API_URL}/support/faq/${faqId}/helpful`, {
        helpful: isHelpful
      });
      setFeedbackGiven({ ...feedbackGiven, [faqId]: true });
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const categoryColors = {
    getting_started: 'blue',
    account: 'purple',
    trading: 'green',
    payments: 'yellow',
    technical: 'red'
  };

  const getCategoryColor = (category) => {
    const color = categoryColors[category] || 'gray';
    return {
      blue: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
      purple: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
      green: 'bg-green-500/10 text-green-400 border-green-500/30',
      yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
      red: 'bg-red-500/10 text-red-400 border-red-500/30',
      gray: 'bg-gray-500/10 text-gray-400 border-gray-500/30'
    }[color];
  };

  const formatCategoryName = (category) => {
    return category.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <Layout>
      <SEO
        title="Frequently Asked Questions (FAQ)"
        description="Find answers to common questions about MarketEdgePros, trading challenges, payments, and more."
        keywords="FAQ, frequently asked questions, help, support, trading questions"
      />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Frequently Asked <span className="bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">Questions</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Quick answers to common questions about our platform and services
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search FAQs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-12 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap gap-3 justify-center mb-8">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-6 py-2 rounded-lg font-medium transition-all ${
                selectedCategory === 'all'
                  ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              All ({faqs.length})
            </button>
            {categories.map((cat) => (
              <button
                key={cat.name}
                onClick={() => setSelectedCategory(cat.name)}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  selectedCategory === cat.name
                    ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                    : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                }`}
              >
                {formatCategoryName(cat.name)} ({cat.count})
              </button>
            ))}
          </div>

          {/* FAQs List */}
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <Loader className="w-8 h-8 text-purple-500 animate-spin" />
            </div>
          ) : filteredFaqs.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">No FAQs found matching your search.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredFaqs.map((faq) => (
                <div
                  key={faq.id}
                  className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden hover:border-purple-500/50 transition-all"
                >
                  <button
                    onClick={() => setExpandedFaq(expandedFaq === faq.id ? null : faq.id)}
                    className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-700/30 transition-all"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getCategoryColor(faq.category)}`}>
                          {formatCategoryName(faq.category)}
                        </span>
                        {faq.is_featured && (
                          <span className="px-3 py-1 rounded-full text-xs font-medium bg-yellow-500/10 text-yellow-400 border border-yellow-500/30">
                            Popular
                          </span>
                        )}
                      </div>
                      <h3 className="text-lg font-semibold text-white">{faq.question}</h3>
                    </div>
                    {expandedFaq === faq.id ? (
                      <ChevronUp className="w-5 h-5 text-purple-400 flex-shrink-0" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-gray-400 flex-shrink-0" />
                    )}
                  </button>

                  {expandedFaq === faq.id && (
                    <div className="px-6 pb-6 border-t border-slate-700">
                      <div className="pt-4 text-gray-300 prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: faq.answer }} />
                      
                      {/* Feedback */}
                      <div className="mt-6 pt-4 border-t border-slate-700">
                        {feedbackGiven[faq.id] ? (
                          <p className="text-green-400 text-sm">Thank you for your feedback!</p>
                        ) : (
                          <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-400">Was this helpful?</span>
                            <button
                              onClick={() => handleFeedback(faq.id, true)}
                              className="flex items-center gap-2 px-4 py-2 bg-green-500/10 text-green-400 rounded-lg hover:bg-green-500/20 transition-all"
                            >
                              <ThumbsUp className="w-4 h-4" />
                              Yes
                            </button>
                            <button
                              onClick={() => handleFeedback(faq.id, false)}
                              className="flex items-center gap-2 px-4 py-2 bg-red-500/10 text-red-400 rounded-lg hover:bg-red-500/20 transition-all"
                            >
                              <ThumbsDown className="w-4 h-4" />
                              No
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-900 to-blue-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Still Have Questions?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Can't find what you're looking for? Our support team is here to help!
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              to="/support/create-ticket"
              className="px-8 py-4 bg-white text-purple-900 rounded-xl font-semibold hover:bg-gray-100 transition-all"
            >
              Create Support Ticket
            </Link>
            <Link
              to="/support"
              className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-xl font-semibold hover:bg-white/20 transition-all"
            >
              Browse Support Hub
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}

