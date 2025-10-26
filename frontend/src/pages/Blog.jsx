import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, ArrowRight, Search, Tag } from 'lucide-react';
import SEO from '../components/SEO';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

export default function Blog() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [featuredPosts, setFeaturedPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 9,
    total_posts: 0,
    total_pages: 0
  });

  // Fetch blog posts
  useEffect(() => {
    fetchPosts();
  }, [selectedCategory, pagination.page]);

  // Fetch categories
  useEffect(() => {
    fetchCategories();
  }, []);

  // Fetch featured posts
  useEffect(() => {
    fetchFeaturedPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        per_page: pagination.per_page
      };
      
      if (selectedCategory !== 'all') {
        params.category = selectedCategory;
      }

      const response = await axios.get(`${API_URL}/blog/posts`, { params });
      setPosts(response.data.posts);
      setPagination(response.data.pagination);
      setError('');
    } catch (err) {
      console.error('Error fetching posts:', err);
      setError('Failed to load blog posts');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/blog/categories`);
      const cats = response.data.categories;
      
      // Add "All Posts" category
      const allCount = cats.reduce((sum, cat) => sum + cat.count, 0);
      setCategories([
        { name: 'all', count: allCount },
        ...cats.map(cat => ({ name: cat.name, count: cat.count }))
      ]);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  const fetchFeaturedPosts = async () => {
    try {
      const response = await axios.get(`${API_URL}/blog/featured?limit=1`);
      setFeaturedPosts(response.data.posts);
    } catch (err) {
      console.error('Error fetching featured posts:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      fetchPosts();
      return;
    }

    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/blog/search`, {
        params: { q: searchQuery, per_page: pagination.per_page }
      });
      setPosts(response.data.posts);
      setPagination(response.data.pagination);
      setError('');
    } catch (err) {
      console.error('Error searching posts:', err);
      setError('Failed to search blog posts');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'long', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  const formatDateShort = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getCategoryDisplayName = (category) => {
    const categoryMap = {
      'trading_strategies': 'Trading Strategies',
      'risk_management': 'Risk Management',
      'market_analysis': 'Market Analysis',
      'prop_trading': 'Prop Trading',
      'education': 'Education',
      'news': 'News'
    };
    return categoryMap[category] || category;
  };

  const featuredPost = featuredPosts[0];

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
              <form onSubmit={handleSearch} className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search articles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </form>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Categories */}
          {categories.length > 0 && (
            <div className="flex flex-wrap gap-3 mb-12">
              {categories.map((category) => (
                <button
                  key={category.name}
                  onClick={() => {
                    setSelectedCategory(category.name);
                    setPagination(prev => ({ ...prev, page: 1 }));
                  }}
                  className={`px-6 py-2 rounded-full transition-all ${
                    selectedCategory === category.name
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                  }`}
                >
                  {category.name === 'all' ? 'All Posts' : getCategoryDisplayName(category.name)} ({category.count})
                </button>
              ))}
            </div>
          )}

          {/* Featured Post */}
          {selectedCategory === 'all' && !searchQuery && featuredPost && (
            <div className="mb-16">
              <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-2xl p-1">
                <div className="bg-slate-900 rounded-2xl overflow-hidden">
                  <div className="grid md:grid-cols-2 gap-8">
                    <div className="relative h-64 md:h-full">
                      {featuredPost.featured_image ? (
                        <img
                          src={featuredPost.featured_image}
                          alt={featuredPost.featured_image_alt || featuredPost.title}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                          <span className="text-white text-6xl font-bold opacity-20">
                            {featuredPost.title.charAt(0)}
                          </span>
                        </div>
                      )}
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
                          {formatDate(featuredPost.published_at)}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {featuredPost.reading_time} min read
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
                          {featuredPost.author && (
                            <>
                              <p className="text-white font-semibold">{featuredPost.author.name}</p>
                              <p className="text-sm text-gray-400">{getCategoryDisplayName(featuredPost.category)}</p>
                            </>
                          )}
                        </div>
                        <Link
                          to={`/blog/${featuredPost.slug}`}
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

          {/* Loading State */}
          {loading && (
            <div className="text-center py-16">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
              <p className="text-gray-400 mt-4">Loading articles...</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="text-center py-16">
              <p className="text-red-400 text-lg">{error}</p>
            </div>
          )}

          {/* Blog Grid */}
          {!loading && !error && posts.length > 0 && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {posts.map((post) => (
                <div key={post.id} className="bg-slate-800 rounded-xl overflow-hidden hover:shadow-xl hover:shadow-blue-500/20 transition-all group">
                  <div className="relative h-48 overflow-hidden">
                    {post.featured_image ? (
                      <img
                        src={post.featured_image}
                        alt={post.featured_image_alt || post.title}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                        <span className="text-white text-4xl font-bold opacity-30">
                          {post.title.charAt(0)}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex items-center gap-4 text-sm text-gray-400 mb-3">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {formatDateShort(post.published_at)}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {post.reading_time} min
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
                        {post.author && (
                          <>
                            <p className="text-sm text-white font-semibold">{post.author.name}</p>
                            <p className="text-xs text-gray-400">{getCategoryDisplayName(post.category)}</p>
                          </>
                        )}
                      </div>
                      <Link
                        to={`/blog/${post.slug}`}
                        className="text-blue-400 hover:text-blue-300 transition-colors"
                      >
                        <ArrowRight className="w-5 h-5" />
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* No Results */}
          {!loading && !error && posts.length === 0 && (
            <div className="text-center py-16">
              <p className="text-gray-400 text-lg">No articles found matching your search.</p>
            </div>
          )}

          {/* Pagination */}
          {!loading && !error && pagination.total_pages > 1 && (
            <div className="flex justify-center gap-2 mt-12">
              <button
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                disabled={!pagination.has_prev}
                className="px-4 py-2 bg-slate-800 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-700 transition-colors"
              >
                Previous
              </button>
              <span className="px-4 py-2 text-gray-300">
                Page {pagination.page} of {pagination.total_pages}
              </span>
              <button
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                disabled={!pagination.has_next}
                className="px-4 py-2 bg-slate-800 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-700 transition-colors"
              >
                Next
              </button>
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

