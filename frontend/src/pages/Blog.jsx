import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, ArrowRight, Search, Tag } from 'lucide-react';
import SEO from '../components/SEO';

export default function Blog() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    { id: 'all', name: 'All Posts', count: 12 },
    { id: 'trading-strategies', name: 'Trading Strategies', count: 5 },
    { id: 'risk-management', name: 'Risk Management', count: 3 },
    { id: 'market-analysis', name: 'Market Analysis', count: 2 },
    { id: 'prop-trading', name: 'Prop Trading', count: 2 }
  ];

  const blogPosts = [
    {
      id: 1,
      title: '10 Essential Risk Management Rules for Prop Traders',
      excerpt: 'Master these fundamental risk management principles to protect your funded account and maximize long-term profitability.',
      author: 'Michael Chen',
      authorRole: 'Senior Trader',
      date: '2025-10-20',
      readTime: '8 min read',
      category: 'risk-management',
      image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop',
      tags: ['Risk Management', 'Trading Psychology', 'Prop Trading']
    },
    {
      id: 2,
      title: 'How to Pass Your Prop Firm Challenge on First Attempt',
      excerpt: 'Proven strategies and tips from traders who successfully passed their evaluation challenges on the first try.',
      author: 'Sarah Johnson',
      authorRole: 'Trading Coach',
      date: '2025-10-18',
      readTime: '12 min read',
      category: 'prop-trading',
      image: 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&h=400&fit=crop',
      tags: ['Challenge Tips', 'Evaluation', 'Success Stories']
    },
    {
      id: 3,
      title: 'Top 5 Trading Strategies for Volatile Markets',
      excerpt: 'Learn how to adapt your trading approach during high volatility periods and capitalize on market movements.',
      author: 'David Martinez',
      authorRole: 'Market Analyst',
      date: '2025-10-15',
      readTime: '10 min read',
      category: 'trading-strategies',
      image: 'https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800&h=400&fit=crop',
      tags: ['Volatility', 'Strategies', 'Market Conditions']
    },
    {
      id: 4,
      title: 'Understanding Drawdown: The Key to Prop Trading Success',
      excerpt: 'Deep dive into drawdown management and why it\'s the most critical metric in proprietary trading.',
      author: 'Emma Wilson',
      authorRole: 'Risk Manager',
      date: '2025-10-12',
      readTime: '7 min read',
      category: 'risk-management',
      image: 'https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=800&h=400&fit=crop',
      tags: ['Drawdown', 'Risk', 'Account Management']
    },
    {
      id: 5,
      title: 'Weekly Market Analysis: EUR/USD Outlook',
      excerpt: 'Technical and fundamental analysis of the EUR/USD pair with key levels to watch this week.',
      author: 'James Thompson',
      authorRole: 'Forex Analyst',
      date: '2025-10-10',
      readTime: '6 min read',
      category: 'market-analysis',
      image: 'https://images.unsplash.com/photo-1642790551116-18e150f248e8?w=800&h=400&fit=crop',
      tags: ['EUR/USD', 'Forex', 'Technical Analysis']
    },
    {
      id: 6,
      title: 'Scalping vs Swing Trading: Which Suits Your Prop Account?',
      excerpt: 'Compare different trading styles and discover which approach aligns best with prop firm rules.',
      author: 'Michael Chen',
      authorRole: 'Senior Trader',
      date: '2025-10-08',
      readTime: '9 min read',
      category: 'trading-strategies',
      image: 'https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800&h=400&fit=crop',
      tags: ['Scalping', 'Swing Trading', 'Trading Styles']
    }
  ];

  const filteredPosts = blogPosts.filter(post => {
    const matchesCategory = selectedCategory === 'all' || post.category === selectedCategory;
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const featuredPost = blogPosts[0];

  return (
    <>
      <SEO 
        title="Trading Blog - Tips, Strategies & Market Analysis"
        description="Expert trading insights, prop firm strategies, risk management tips, and market analysis from professional traders."
        keywords="trading blog, forex strategies, prop trading tips, market analysis, risk management"
      />

      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                Trading <span className="text-yellow-400">Insights</span>
              </h1>
              <p className="text-xl text-blue-100 max-w-2xl mx-auto">
                Expert tips, strategies, and market analysis to help you succeed as a funded trader
              </p>
            </div>

            {/* Search Bar */}
            <div className="mt-8 max-w-2xl mx-auto">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search articles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Categories */}
          <div className="flex flex-wrap gap-3 mb-12">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-2 rounded-full transition-all ${
                  selectedCategory === category.id
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>

          {/* Featured Post */}
          {selectedCategory === 'all' && !searchQuery && (
            <div className="mb-16">
              <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-2xl p-1">
                <div className="bg-slate-900 rounded-2xl overflow-hidden">
                  <div className="grid md:grid-cols-2 gap-8">
                    <div className="relative h-64 md:h-full">
                      <img
                        src={featuredPost.image}
                        alt={featuredPost.title}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute top-4 left-4">
                        <span className="px-4 py-2 bg-yellow-400 text-slate-900 rounded-full text-sm font-semibold">
                          Featured
                        </span>
                      </div>
                    </div>
                    <div className="p-8 flex flex-col justify-center">
                      <div className="flex items-center gap-4 text-sm text-gray-400 mb-4">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {new Date(featuredPost.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {featuredPost.readTime}
                        </span>
                      </div>
                      <h2 className="text-3xl font-bold text-white mb-4">
                        {featuredPost.title}
                      </h2>
                      <p className="text-gray-300 mb-6">
                        {featuredPost.excerpt}
                      </p>
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white font-semibold">{featuredPost.author}</p>
                          <p className="text-sm text-gray-400">{featuredPost.authorRole}</p>
                        </div>
                        <Link
                          to={`/blog/${featuredPost.id}`}
                          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all"
                        >
                          Read More <ArrowRight className="w-4 h-4" />
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Blog Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredPosts.map((post) => (
              <div key={post.id} className="bg-slate-800 rounded-xl overflow-hidden hover:shadow-xl hover:shadow-blue-500/20 transition-all group">
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={post.image}
                    alt={post.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-4 text-sm text-gray-400 mb-3">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date(post.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {post.readTime}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-gray-300 mb-4 line-clamp-2">
                    {post.excerpt}
                  </p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tags.slice(0, 2).map((tag, index) => (
                      <span key={index} className="flex items-center gap-1 px-3 py-1 bg-slate-700 text-gray-300 rounded-full text-xs">
                        <Tag className="w-3 h-3" />
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                    <div>
                      <p className="text-sm text-white font-semibold">{post.author}</p>
                      <p className="text-xs text-gray-400">{post.authorRole}</p>
                    </div>
                    <Link
                      to={`/blog/${post.id}`}
                      className="text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      <ArrowRight className="w-5 h-5" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* No Results */}
          {filteredPosts.length === 0 && (
            <div className="text-center py-16">
              <p className="text-gray-400 text-lg">No articles found matching your search.</p>
            </div>
          )}

          {/* Newsletter CTA */}
          <div className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-1">
            <div className="bg-slate-900 rounded-2xl p-12 text-center">
              <h2 className="text-3xl font-bold text-white mb-4">
                Never Miss a Trading Insight
              </h2>
              <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
                Subscribe to our newsletter and get the latest trading strategies, market analysis, and prop trading tips delivered to your inbox weekly.
              </p>
              <div className="flex gap-4 max-w-md mx-auto">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-6 py-4 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all font-semibold">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

