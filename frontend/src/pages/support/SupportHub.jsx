import { useState } from 'react';
import { Search, BookOpen, MessageCircle, FileText, Video, HelpCircle, ExternalLink, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import SEO from '../components/SEO';

export default function SupportHub() {
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    {
      title: 'Getting Started',
      icon: BookOpen,
      color: 'blue',
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
      color: 'purple',
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
      color: 'green',
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
      color: 'yellow',
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
      color: 'red',
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
      color: 'indigo',
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
    { title: 'Create Support Ticket', icon: MessageCircle, link: '/support/create-ticket', color: 'blue' },
    { title: 'Browse FAQ', icon: HelpCircle, link: '/support/faq', color: 'purple' },
    { title: 'My Tickets', icon: FileText, link: '/support/my-tickets', color: 'green' },
    { title: 'Join Discord Community', icon: ExternalLink, link: 'https://discord.gg/jKbmeSe7', color: 'indigo', external: true }
  ];

  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    green: 'bg-green-500/10 text-green-400 border-green-500/30',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    red: 'bg-red-500/10 text-red-400 border-red-500/30',
    indigo: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
  };

  return (
    <Layout>
      <SEO
        title="Support Hub - Help Center & Knowledge Base"
        description="Find answers, guides, and tutorials for MarketEdgePros. Learn how to pass challenges, get funded, and manage your trading account."
        keywords="support, help center, knowledge base, trading guides, tutorials, FAQ"
      />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            How Can We <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">Help You?</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Search our knowledge base for guides, tutorials, and answers to common questions
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search for help articles..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="py-12 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {quickLinks.map((link, index) => {
              const Icon = link.icon;
              return link.external ? (
                <a
                  key={index}
                  href={link.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`flex items-center gap-3 p-4 rounded-lg border transition-all hover:scale-105 ${colorClasses[link.color]}`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-semibold">{link.title}</span>
                </a>
              ) : (
                <Link
                  key={index}
                  to={link.link}
                  className={`flex items-center gap-3 p-4 rounded-lg border transition-all hover:scale-105 ${colorClasses[link.color]}`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-semibold">{link.title}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 bg-slate-900">
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
                  className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`p-3 rounded-lg ${colorClasses[category.color]}`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold text-white">{category.title}</h3>
                  </div>

                  <ul className="space-y-2">
                    {category.articles.map((article, articleIndex) => (
                      <li key={articleIndex}>
                        <Link
                          to={article.link}
                          className="flex items-center justify-between text-gray-300 hover:text-white transition-colors group"
                        >
                          <span className="text-sm">{article.title}</span>
                          <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </Link>
                      </li>
                    ))}
                  </ul>

                  <Link
                    to={`/support/category/${category.title.toLowerCase().replace(/\s+/g, '-')}`}
                    className="mt-4 inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 text-sm font-semibold"
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
      <section className="py-20 bg-gradient-to-br from-slate-900 to-blue-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
            Most Popular Articles
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {popularArticles.map((article, index) => (
              <Link
                key={index}
                to={article.link}
                className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all hover:transform hover:scale-105"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold text-white">{article.title}</h3>
                  <ChevronRight className="w-5 h-5 text-blue-400 flex-shrink-0" />
                </div>
                <p className="text-sm text-gray-400">{article.views} views</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Still Need Help */}
      <section className="py-20 bg-slate-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <MessageCircle className="w-16 h-16 text-blue-400 mx-auto mb-6" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Still Need Help?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Can't find what you're looking for? Our support team is here to help 24/7.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/contact"
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-bold hover:from-blue-600 hover:to-purple-700 transition"
            >
              Contact Support
            </Link>
            <a
              href="https://discord.gg/jKbmeSe7"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white font-bold hover:bg-white/20 transition"
            >
              Join Discord Community
            </a>
          </div>
        </div>
      </section>
    </Layout>
  );
}

