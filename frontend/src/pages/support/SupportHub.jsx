import { useState } from 'react';
import { Search, BookOpen, MessageCircle, FileText, Video, HelpCircle, ExternalLink, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import Layout from '../../components/layout/Layout';
import SEO from '../../components/SEO';

export default function SupportHub() {
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    {
      title: 'Getting Started',
      icon: BookOpen,
      articles: [
        { title: 'How to Create an Account', link: '/support/create-account' },
        { title: 'Choosing the Right Challenge', link: '/support/choose-challenge' },
        { title: 'Making Your First Payment', link: '/support/first-payment' },
        { title: 'Setting Up MT5', link: '/support/setup-mt5' },
        { title: 'Understanding Trading Rules', link: '/support/trading-rules' }
      ]
    },
    {
      title: 'Challenges & Evaluation',
      icon: FileText,
      articles: [
        { title: 'Challenge Rules Explained', link: '/support/challenge-rules' },
        { title: 'How to Pass Your Challenge', link: '/support/pass-challenge' },
        { title: 'Daily Drawdown Calculation', link: '/support/daily-drawdown' },
        { title: 'Total Drawdown Limits', link: '/support/total-drawdown' },
        { title: 'Minimum Trading Days', link: '/support/min-trading-days' }
      ]
    },
    {
      title: 'Funded Accounts',
      icon: Video,
      articles: [
        { title: 'Getting Your Funded Account', link: '/support/get-funded' },
        { title: 'Profit Split Explained', link: '/support/profit-split' },
        { title: 'Scaling Your Account', link: '/support/scaling' },
        { title: 'Trading on Funded Account', link: '/support/trading-funded' },
        { title: 'Account Consistency Requirements', link: '/support/consistency' }
      ]
    },
    {
      title: 'Payments & Withdrawals',
      icon: MessageCircle,
      articles: [
        { title: 'How to Request a Withdrawal', link: '/support/request-withdrawal' },
        { title: 'Payment Methods Accepted', link: '/support/payment-methods' },
        { title: 'Withdrawal Processing Times', link: '/support/withdrawal-times' },
        { title: 'Minimum Withdrawal Amount', link: '/support/min-withdrawal' },
        { title: 'Payout Schedule', link: '/support/payout-schedule' }
      ]
    },
    {
      title: 'Platform & Technical',
      icon: HelpCircle,
      articles: [
        { title: 'MT5 Installation Guide', link: '/support/mt5-install' },
        { title: 'Connecting to Trading Server', link: '/support/connect-server' },
        { title: 'Using Expert Advisors (EAs)', link: '/support/using-eas' },
        { title: 'Troubleshooting Connection Issues', link: '/support/connection-issues' },
        { title: 'Platform Requirements', link: '/support/requirements' }
      ]
    },
    {
      title: 'Account Management',
      icon: FileText,
      articles: [
        { title: 'Updating Your Profile', link: '/support/update-profile' },
        { title: 'KYC Verification Process', link: '/support/kyc-process' },
        { title: 'Changing Your Password', link: '/support/change-password' },
        { title: 'Two-Factor Authentication', link: '/support/2fa' },
        { title: 'Account Security Best Practices', link: '/support/security' }
      ]
    }
  ];

  const popularArticles = [
    { title: 'How to Pass Your First Challenge', views: '12.5K', link: '/support/pass-challenge' },
    { title: 'Understanding Daily Drawdown', views: '8.3K', link: '/support/daily-drawdown' },
    { title: 'MT5 Setup Guide', views: '7.1K', link: '/support/mt5-install' },
    { title: 'Withdrawal Process Explained', views: '6.8K', link: '/support/request-withdrawal' },
    { title: 'Profit Split & Scaling', views: '5.9K', link: '/support/profit-split' }
  ];

  const quickLinks = [
    { title: 'Create Support Ticket', icon: MessageCircle, link: '/support/create-ticket' },
    { title: 'Browse FAQ', icon: HelpCircle, link: '/support/faq' },
    { title: 'My Tickets', icon: FileText, link: '/support/my-tickets' },
    { title: 'Join Discord Community', icon: ExternalLink, link: 'https://discord.gg/jKbmeSe7', external: true }
  ];

  return (
    <Layout>
      <SEO 
        title="Support Hub - Help Center & Knowledge Base"
        description="Find answers to common questions, browse our knowledge base, and get help from our support team."
      />

      {/* Hero Section */}
      <section className="relative py-20 bg-black">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-teal-500/10"></div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
            How Can We <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Help You?</span>
          </h1>
          <p className="text-xl text-gray-400 mb-8">
            Search our knowledge base for guides, tutorials, and answers to common questions
          </p>
          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search for help articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50"
            />
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="py-12 bg-black border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickLinks.map((link, index) => {
              const Icon = link.icon;
              if (link.external) {
                return (
                  <a
                    key={index}
                    href={link.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-4 bg-white/5 border border-white/10 rounded-lg hover:bg-gradient-to-r hover:from-cyan-500/20 hover:to-teal-500/20 hover:border-cyan-500/50 transition-all group"
                  >
                    <Icon className="w-5 h-5 text-cyan-400" />
                    <span className="font-semibold text-white group-hover:text-cyan-300">{link.title}</span>
                  </a>
                );
              }
              return (
                <Link
                  key={index}
                  to={link.link}
                  className="flex items-center gap-3 p-4 bg-white/5 border border-white/10 rounded-lg hover:bg-gradient-to-r hover:from-cyan-500/20 hover:to-teal-500/20 hover:border-cyan-500/50 transition-all group"
                >
                  <Icon className="w-5 h-5 text-cyan-400" />
                  <span className="font-semibold text-white group-hover:text-cyan-300">{link.title}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
            Browse by Category
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {categories.map((category, index) => {
              const Icon = category.icon;
              return (
                <div
                  key={index}
                  className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 hover:border-cyan-500/30 transition-all group"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 rounded-lg bg-gradient-to-r from-cyan-500/20 to-teal-500/20 border border-cyan-500/30 group-hover:from-cyan-500/30 group-hover:to-teal-500/30 transition-all">
                      <Icon className="w-6 h-6 text-cyan-400" />
                    </div>
                    <h3 className="text-xl font-bold text-white">{category.title}</h3>
                  </div>
                  <ul className="space-y-2">
                    {category.articles.map((article, articleIndex) => (
                      <li key={articleIndex}>
                        <Link
                          to={article.link}
                          className="flex items-center justify-between text-gray-400 hover:text-cyan-300 transition-colors group/item"
                        >
                          <span className="text-sm">{article.title}</span>
                          <ChevronRight className="w-4 h-4 opacity-0 group-hover/item:opacity-100 transition-opacity text-cyan-400" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                  <Link
                    to={`/support/category/${category.title.toLowerCase().replace(/\s+/g, '-')}`}
                    className="mt-4 inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 text-sm font-semibold"
                  >
                    View All Articles
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Popular Articles */}
      <section className="py-20 bg-gradient-to-br from-black via-cyan-950/20 to-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
            Most Popular Articles
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {popularArticles.map((article, index) => (
              <Link
                key={index}
                to={article.link}
                className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-gradient-to-r hover:from-cyan-500/10 hover:to-teal-500/10 hover:border-cyan-500/50 transition-all hover:transform hover:scale-105"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold text-white">{article.title}</h3>
                  <ChevronRight className="w-5 h-5 text-cyan-400 flex-shrink-0" />
                </div>
                <p className="text-sm text-gray-400">{article.views} views</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Still Need Help */}
      <section className="py-20 bg-black border-t border-white/10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <MessageCircle className="w-16 h-16 text-cyan-400 mx-auto mb-6" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Still Need Help?
          </h2>
          <p className="text-xl text-gray-400 mb-8">
            Can't find what you're looking for? Our support team is here to help 24/7.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/contact"
              className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-lg text-white font-bold hover:from-cyan-600 hover:to-teal-600 transition shadow-lg shadow-cyan-500/50"
            >
              Contact Support
            </Link>
            <a
              href="https://discord.gg/jKbmeSe7"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white font-bold hover:bg-white/20 hover:border-cyan-500/50 transition"
            >
              Join Discord Community
            </a>
          </div>
        </div>
      </section>
    </Layout>
  );
}
