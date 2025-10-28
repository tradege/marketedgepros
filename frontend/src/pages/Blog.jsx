import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, ArrowRight, Search, Tag, Loader } from 'lucide-react';
import Layout from '../components/layout/Layout';
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

  useEffect(() => {
    fetchPosts();
    fetchCategories();
    fetchFeaturedPosts();
  }, []);

  const fetchPosts = async (page = 1, category = 'all') => {
    try {
      setLoading(true);
      const params = { page, per_page: pagination.per_page, category };
      const response = await axios.get(`${API_URL}/blog/posts`, { params });
      setPosts(response.data.posts);
      setPagination(response.data.pagination);
    } catch (err) {
      setError('Failed to fetch posts');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/blog/categories`);
      setCategories(response.data);
    } catch (err) { /* Do nothing */ }
  };

  const fetchFeaturedPosts = async () => {
    try {
      const response = await axios.get(`${API_URL}/blog/featured`);
      setFeaturedPosts(response.data.posts || []);
    } catch (err) { 
      console.error('Failed to fetch featured posts:', err);
      setFeaturedPosts([]);
    }
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    fetchPosts(1, category);
  };

  const handlePageChange = (page) => {
    fetchPosts(page, selectedCategory);
  };

  const filteredPosts = posts.filter(post => 
    post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    post.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Layout>
      <div className="min-h-screen bg-black text-white">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 z-0">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0%,transparent_65%)]"></div>
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(168,85,247,0.15)_0%,transparent_50%)]"></div>
          </div>

          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-8">
              MarketEdge{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                Blog
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">
              Insights, tips, and news from the world of trading
            </p>
          </div>
        </section>

        {/* Main Content */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-12 gap-16">
              {/* Blog Posts */}
              <div className="md:col-span-8">
                {loading ? (
                  <div className="flex justify-center items-center h-96">
                    <Loader className="w-12 h-12 animate-spin text-cyan-400" />
                  </div>
                ) : error ? (
                  <p className="text-red-500">{error}</p>
                ) : (
                  <div className="grid gap-12">
                    {filteredPosts.map(post => (
                      <Link to={`/blog/${post.slug}`} key={post.id} className="group block">
                        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300">
                          <h2 className="text-3xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 group-hover:from-purple-400 group-hover:to-pink-400">
                            {post.title}
                          </h2>
                          <div className="flex items-center gap-4 text-gray-400 mb-4">
                            <div className="flex items-center gap-2"><Calendar size={16} /> {new Date(post.published_at).toLocaleDateString()}</div>
                            <div className="flex items-center gap-2"><Clock size={16} /> {post.reading_time || post.read_time || 5} min read</div>
                          </div>
                          <p className="text-lg text-gray-300 mb-6">{post.excerpt}</p>
                          <div className="flex items-center gap-2 text-cyan-400 font-semibold group-hover:text-purple-400">
                            Read More <ArrowRight size={16} />
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>

              {/* Sidebar */}
              <div className="md:col-span-4">
                <div className="sticky top-24 space-y-12">
                  {/* Search */}
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Search</h3>
                    <div className="relative">
                      <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                      <input
                        type="text"
                        placeholder="Search posts..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-12 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                      />
                    </div>
                  </div>

                  {/* Categories */}
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Categories</h3>
                    <div className="flex flex-wrap gap-2">
                      <button onClick={() => handleCategoryChange('all')} className={`px-4 py-2 rounded-full text-sm font-semibold ${selectedCategory === 'all' ? 'bg-cyan-500 text-white' : 'bg-white/10 text-gray-300 hover:bg-white/20'}`}>All</button>
                      {categories.map(cat => (
                        <button key={cat.id} onClick={() => handleCategoryChange(cat.slug)} className={`px-4 py-2 rounded-full text-sm font-semibold ${selectedCategory === cat.slug ? 'bg-cyan-500 text-white' : 'bg-white/10 text-gray-300 hover:bg-white/20'}`}>{cat.name}</button>
                      ))}
                    </div>
                  </div>

                  {/* Featured Posts */}
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Featured Posts</h3>
                    <div className="space-y-4">
                      {featuredPosts.map(post => (
                        <Link to={`/blog/${post.slug}`} key={post.id} className="block group">
                          <p className="text-lg font-semibold text-gray-300 group-hover:text-cyan-400">{post.title}</p>
                          <p className="text-sm text-gray-500">{new Date(post.published_at).toLocaleDateString()}</p>
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
}

