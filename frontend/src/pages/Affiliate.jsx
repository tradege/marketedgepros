import { useState } from 'react';
import { Link } from 'react-router-dom';
import { DollarSign, Users, TrendingUp, Gift, Copy, Check, ExternalLink, Calculator } from 'lucide-react';
import SEO from '../components/SEO';
import Layout from '../components/layout/Layout';

export default function Affiliate() {
  const [copied, setCopied] = useState(false);
  const [referrals, setReferrals] = useState(10);
  const [avgPurchase, setAvgPurchase] = useState(299);

  const affiliateLink = "https://marketedgepros.com/ref/YOUR_CODE";

  const handleCopy = () => {
    navigator.clipboard.writeText(affiliateLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const calculateEarnings = () => {
    const commission = 0.30; // 30%
    return (referrals * avgPurchase * commission).toFixed(2);
  };

  const benefits = [
    {
      icon: <DollarSign className="w-8 h-8" />,
      title: "30% Commission",
      description: "Earn 30% commission on every sale you refer. No limits, no caps."
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Lifetime Cookies",
      description: "Your referrals are tracked forever. Earn from their future purchases too."
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Recurring Revenue",
      description: "Earn from subscription renewals and account upgrades automatically."
    },
    {
      icon: <Gift className="w-8 h-8" />,
      title: "Bonus Rewards",
      description: "Hit milestones and unlock bonus payouts and exclusive perks."
    }
  ];

  const howItWorks = [
    {
      step: "1",
      title: "Sign Up Free",
      description: "Create your affiliate account in seconds. No fees, no commitments."
    },
    {
      step: "2",
      title: "Share Your Link",
      description: "Get your unique referral link and share it with your audience."
    },
    {
      step: "3",
      title: "Earn Commissions",
      description: "Get paid 30% for every trader who signs up through your link."
    },
    {
      step: "4",
      title: "Get Paid Weekly",
      description: "Receive your earnings every week via PayPal, Stripe, or bank transfer."
    }
  ];

  const commissionTiers = [
    { sales: "1-10", commission: "30%", color: "from-blue-600 to-cyan-600" },
    { sales: "11-50", commission: "35%", color: "from-purple-600 to-pink-600" },
    { sales: "51-100", commission: "40%", color: "from-orange-600 to-red-600" },
    { sales: "100+", commission: "45%", color: "from-green-600 to-emerald-600" }
  ];

  const faqs = [
    {
      question: "How much can I earn?",
      answer: "There's no limit! You earn 30-45% commission on every sale. Top affiliates earn $10,000+ per month."
    },
    {
      question: "When do I get paid?",
      answer: "Payouts are processed weekly, every Friday. Minimum payout is $50."
    },
    {
      question: "What can I promote?",
      answer: "All our challenges, courses, and services. You'll get access to marketing materials and creatives."
    },
    {
      question: "Do I need a website?",
      answer: "No! Share your link on social media, YouTube, Discord, or anywhere you have an audience."
    }
  ];

  return (
    <Layout>
      <SEO 
        title="Affiliate Program - Earn 30% Commission"
        description="Join our affiliate program and earn 30% commission on every referral. Promote the best prop trading platform and get paid weekly."
        keywords="affiliate program, trading affiliate, earn commission, referral program, passive income"
      />

      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-green-600 to-emerald-600 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <div className="inline-block px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white text-sm font-semibold mb-6">
                💰 EARN UP TO 45% COMMISSION
              </div>
              <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                Turn Your Audience Into <span className="text-yellow-400">Income</span>
              </h1>
              <p className="text-xl text-green-100 max-w-3xl mx-auto mb-8">
                Join thousands of affiliates earning passive income by promoting the most trader-friendly prop firm. 
                No experience needed, just share and earn.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/register"
                  className="px-8 py-4 bg-white text-green-600 rounded-lg hover:bg-gray-100 transition-all font-semibold text-lg"
                >
                  Join Affiliate Program
                </Link>
                <a
                  href="#calculator"
                  className="px-8 py-4 bg-green-700 text-white rounded-lg hover:bg-green-800 transition-all font-semibold text-lg"
                >
                  Calculate Earnings
                </a>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          {/* Benefits */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
              Why Join Our <span className="text-green-400">Affiliate Program?</span>
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {benefits.map((benefit, index) => (
                <div key={index} className="bg-slate-800 rounded-xl p-6 hover:shadow-xl hover:shadow-green-500/20 transition-all">
                  <div className="w-16 h-16 bg-gradient-to-r from-green-600 to-emerald-600 rounded-lg flex items-center justify-center text-white mb-4">
                    {benefit.icon}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">{benefit.title}</h3>
                  <p className="text-gray-300">{benefit.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* How It Works */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
              How It <span className="text-green-400">Works</span>
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {howItWorks.map((item, index) => (
                <div key={index} className="relative">
                  <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 h-full">
                    <div className="w-12 h-12 bg-gradient-to-r from-green-600 to-emerald-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                      {item.step}
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{item.title}</h3>
                    <p className="text-gray-300">{item.description}</p>
                  </div>
                  {index < howItWorks.length - 1 && (
                    <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <div className="w-8 h-0.5 bg-green-600"></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Commission Tiers */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-4">
              Commission <span className="text-green-400">Tiers</span>
            </h2>
            <p className="text-gray-300 text-center mb-12 max-w-2xl mx-auto">
              The more you sell, the more you earn. Unlock higher commission rates as you grow.
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {commissionTiers.map((tier, index) => (
                <div key={index} className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border-2 border-slate-700 hover:border-green-500 transition-all">
                  <div className={`text-sm font-semibold bg-gradient-to-r ${tier.color} text-white px-3 py-1 rounded-full inline-block mb-4`}>
                    {tier.sales} Sales/Month
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">{tier.commission}</div>
                  <p className="text-gray-400">Commission Rate</p>
                </div>
              ))}
            </div>
          </div>

          {/* Earnings Calculator */}
          <div id="calculator" className="mb-20">
            <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl p-1">
              <div className="bg-slate-900 rounded-2xl p-8">
                <div className="flex items-center justify-center gap-3 mb-6">
                  <Calculator className="w-8 h-8 text-green-400" />
                  <h2 className="text-3xl font-bold text-white">Earnings Calculator</h2>
                </div>
                <p className="text-gray-300 text-center mb-8">
                  See how much you could earn with our affiliate program
                </p>
                <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      Monthly Referrals
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="100"
                      value={referrals}
                      onChange={(e) => setReferrals(parseInt(e.target.value))}
                      className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="text-green-400 text-2xl font-bold mt-2">{referrals} referrals</div>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      Average Purchase Value
                    </label>
                    <input
                      type="range"
                      min="49"
                      max="1999"
                      step="50"
                      value={avgPurchase}
                      onChange={(e) => setAvgPurchase(parseInt(e.target.value))}
                      className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="text-green-400 text-2xl font-bold mt-2">${avgPurchase}</div>
                  </div>
                </div>
                <div className="mt-8 p-8 bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-xl text-center">
                  <p className="text-gray-300 mb-2">Your Estimated Monthly Earnings</p>
                  <div className="text-5xl font-bold text-green-400">${calculateEarnings()}</div>
                  <p className="text-sm text-gray-400 mt-2">Based on 30% commission rate</p>
                </div>
              </div>
            </div>
          </div>

          {/* Demo Affiliate Link */}
          <div className="mb-20">
            <div className="bg-slate-800 rounded-xl p-8">
              <h3 className="text-2xl font-bold text-white mb-4">Your Affiliate Link</h3>
              <p className="text-gray-300 mb-6">
                Share this link with your audience to start earning commissions
              </p>
              <div className="flex gap-4">
                <input
                  type="text"
                  value={affiliateLink}
                  readOnly
                  className="flex-1 px-6 py-4 bg-slate-700 border border-slate-600 rounded-lg text-white"
                />
                <button
                  onClick={handleCopy}
                  className="px-6 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/50 transition-all flex items-center gap-2"
                >
                  {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                  {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
            </div>
          </div>

          {/* FAQs */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
              Frequently Asked <span className="text-green-400">Questions</span>
            </h2>
            <div className="max-w-3xl mx-auto space-y-4">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-slate-800 rounded-xl p-6">
                  <h3 className="text-xl font-bold text-white mb-2">{faq.question}</h3>
                  <p className="text-gray-300">{faq.answer}</p>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl p-12 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Start Earning?
            </h2>
            <p className="text-xl text-green-100 mb-8 max-w-2xl mx-auto">
              Join thousands of affiliates already earning passive income with MarketEdgePros
            </p>
            <Link
              to="/register"
              className="inline-flex items-center gap-2 px-8 py-4 bg-white text-green-600 rounded-lg hover:bg-gray-100 transition-all font-semibold text-lg"
            >
              Join Now - It's Free <ExternalLink className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

