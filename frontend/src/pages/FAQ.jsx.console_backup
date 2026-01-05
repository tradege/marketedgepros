import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Search, HelpCircle } from 'lucide-react';
import Layout from '../components/layout/Layout';
import StructuredData from '../components/seo/StructuredData';

export default function FAQ() {
  const [searchTerm, setSearchTerm] = useState('');
  const [openIndex, setOpenIndex] = useState(null);

  const categories = [
    {
      name: 'Getting Started',
      questions: [
        {
          q: 'What is MarketEdgePros?',
          a: 'MarketEdgePros is a proprietary trading firm that provides capital to skilled traders. We fund traders who demonstrate consistent profitability and proper risk management, allowing them to trade with our capital and keep up to 90% of the profits.'
        },
        {
          q: 'How do I get started?',
          a: "Simply sign up for an account, choose a challenge program that fits your trading style, complete the payment, and start trading immediately. You'll receive login credentials to your demo trading account within minutes."
        },
        {
          q: 'Do I need trading experience?',
          a: 'While we welcome traders of all levels, we recommend having at least 6 months of trading experience and a solid understanding of risk management before attempting our challenges.'
        },
        {
          q: 'What platforms do you support?',
          a: 'We currently support MetaTrader 4 (MT4) and MetaTrader 5 (MT5), the industry-standard trading platforms. TradingView integration is coming soon! Both platforms offer advanced charting, indicators, and automated trading capabilities.'
        }
      ]
    },
    {
      name: 'Challenge Programs',
      questions: [
        {
          q: 'What are the different challenge types?',
          a: 'We offer three types: One-Phase Challenge (single evaluation), Two-Phase Challenge (two evaluation stages), and Instant Funding (immediate funded account with stricter rules). Each has different profit targets and requirements.'
        },
        {
          q: 'What is the profit target?',
          a: 'Profit targets vary by program: One-Phase typically requires 10%, Two-Phase requires 8% in Phase 1 and 5% in Phase 2. Instant Funding has no profit target but stricter drawdown limits.'
        },
        {
          q: 'Is there a time limit?',
          a: "No! We don't impose time limits on our challenges. Take as long as you need to reach your profit target while maintaining proper risk management."
        },
        {
          q: 'What are the trading rules?',
          a: 'Main rules include: maximum daily drawdown (typically 5%), maximum total drawdown (typically 10%), minimum trading days (varies by program), and no prohibited strategies like high-frequency trading or arbitrage.'
        },
        {
          q: 'Can I use Expert Advisors (EAs)?',
          a: "Yes! You can use EAs and automated trading strategies as long as they comply with our trading rules and don't exploit platform latency or use prohibited strategies."
        }
      ]
    },
    {
      name: 'Funded Accounts',
      questions: [
        {
          q: 'How long does it take to get funded?',
          a: "Once you pass your challenge, you'll receive your funded account within 24 hours. We verify your trades and send you live account credentials via email."
        },
        {
          q: 'What is the profit split?',
          a: 'You keep 80% of profits initially. After your first withdrawal, this increases to 90% permanently. We believe in rewarding consistent performers.'
        },
        {
          q: 'Can I scale my account?',
          a: 'Yes! Based on your performance and consistency, you can scale your account up to $2M+. We review accounts every 3 months for scaling opportunities.'
        },
        {
          q: 'Are there any fees on funded accounts?',
          a: 'No monthly fees! You only pay the initial challenge fee. There are no platform fees, data fees, or monthly charges on funded accounts.'
        }
      ]
    },
    {
      name: 'Add-ons & Customization',
      questions: [
        {
          q: 'What are Add-ons?',
          a: 'Add-ons are optional upgrades you can purchase with your challenge to customize your trading experience. They include features like increased leverage, higher profit splits, bi-weekly payouts, and removal of minimum trading days.'
        },
        {
          q: 'How do Add-ons work?',
          a: 'When purchasing a challenge, you can select any Add-ons you want. The cost is added to your base challenge price, and the benefits apply immediately to your account. You can choose multiple Add-ons for maximum customization.'
        },
        {
          q: 'What Add-ons are available?',
          a: 'We offer: (1) Increased Leverage ($75) - Trade with 1:100 leverage instead of 1:30. (2) 90% Profit Split ($100) - Keep 90% of profits instead of 80%. (3) Bi-weekly Payouts ($50) - Get paid every 2 weeks instead of monthly. (4) No Minimum Trading Days ($30) - Remove the minimum trading days requirement.'
        },
        {
          q: 'Can I add Add-ons after purchasing?',
          a: 'Currently, Add-ons must be selected at the time of purchase. We recommend choosing all the Add-ons you want upfront to get the full benefits from day one.'
        }
      ]
    },
    {
      name: 'Payments & Withdrawals',
      questions: [
        {
          q: 'How do I request a withdrawal?',
          a: 'Log into your dashboard, navigate to Withdrawals, enter the amount you want to withdraw, and submit. We process withdrawals within 1-3 business days.'
        },
        {
          q: 'What payment methods do you accept?',
          a: 'We accept credit/debit cards, bank transfers, and cryptocurrency. For withdrawals, we support bank transfers, PayPal, Wise, and crypto.'
        },
        {
          q: 'Is there a minimum withdrawal amount?',
          a: 'Yes, the minimum withdrawal amount is $50. This helps us process withdrawals efficiently while keeping costs low for everyone.'
        },
        {
          q: 'How often can I withdraw?',
          a: 'You can request withdrawals as often as you like. Most traders withdraw bi-weekly or monthly, but daily withdrawals are also supported.'
        },
        {
          q: 'Are there withdrawal fees?',
          a: 'We cover all withdrawal fees up to $50. Any fees above that are deducted from your withdrawal amount.'
        }
      ]
    },
    {
      name: 'Technical & Support',
      questions: [
        {
          q: 'What if I have technical issues?',
          a: 'Contact our 24/7 support team via live chat, email, or phone. We typically respond within 15 minutes and resolve most issues within an hour.'
        },
        {
          q: 'Can I trade during news events?',
          a: 'Yes! We allow trading during news events. However, be aware of increased volatility and spreads during major economic announcements.'
        },
        {
          q: 'What happens if I violate a rule?',
          a: 'Rule violations result in challenge failure or funded account termination, depending on severity. However, you can always start a new challenge.'
        },
        {
          q: 'Do you offer refunds?',
          a: "Challenge fees are non-refundable once you start trading. However, if you pass and get funded, your challenge fee is refunded with your first profit withdrawal."
        },
        {
          q: 'Is my data secure?',
          a: 'Absolutely! We use bank-level encryption, secure servers, and comply with international data protection regulations. Your personal and financial data is completely safe.'
        }
      ]
    }
  ];

  const allQuestions = categories.flatMap((cat, catIndex) =>
    cat.questions.map((q, qIndex) => ({
      ...q,
      category: cat.name,
      index: `${catIndex}-${qIndex}`
    }))
  );

  const filteredQuestions = searchTerm
    ? allQuestions.filter(
        (item) =>
          item.q.toLowerCase().includes(searchTerm.toLowerCase()) ||
          item.a.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : allQuestions;

  const toggleQuestion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const faqData = {
    questions: allQuestions.map(q => ({
      question: q.q,
      answer: q.a
    }))
  };

  return (
    <Layout>
      <StructuredData type="faq" data={faqData} />
      <div className="min-h-screen bg-black text-white">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 z-0">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0%,transparent_65%)]"></div>
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(168,85,247,0.15)_0%,transparent_50%)]"></div>
          </div>

          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="flex justify-center mb-6">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-500 flex items-center justify-center">
                <HelpCircle className="w-10 h-10 text-white" />
              </div>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold mb-8">
              Frequently Asked{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                Questions
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-12">
              Find answers to common questions about MarketEdgePros, our challenges, and funded accounts
            </p>

            {/* Search Bar */}
            <div className="max-w-2xl mx-auto">
              <div className="relative">
                <Search className="absolute left-6 top-1/2 transform -translate-y-1/2 text-gray-400 w-6 h-6" />
                <input
                  type="text"
                  placeholder="Search for answers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-16 pr-6 py-5 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl text-white text-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Content */}
        <section className="relative py-32">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            {searchTerm ? (
              // Search Results
              <div className="space-y-4">
                <p className="text-gray-300 text-lg mb-8">
                  Found {filteredQuestions.length} result{filteredQuestions.length !== 1 ? 's' : ''}
                </p>
                {filteredQuestions.map((item) => (
                  <div
                    key={item.index}
                    className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden hover:bg-white/10 transition-all duration-300"
                  >
                    <button
                      onClick={() => toggleQuestion(item.index)}
                      className="w-full px-8 py-6 flex items-center justify-between text-left"
                    >
                      <div className="flex-1">
                        <span className="text-sm text-cyan-400 font-semibold">{item.category}</span>
                        <h3 className="text-xl font-semibold text-white mt-2">{item.q}</h3>
                      </div>
                      {openIndex === item.index ? (
                        <ChevronUp className="w-6 h-6 text-cyan-400 flex-shrink-0 ml-4" />
                      ) : (
                        <ChevronDown className="w-6 h-6 text-gray-400 flex-shrink-0 ml-4" />
                      )}
                    </button>
                    {openIndex === item.index && (
                      <div className="px-8 pb-6 border-t border-white/10">
                        <p className="text-gray-300 text-lg leading-relaxed pt-6">{item.a}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              // Categories
              <div className="space-y-16">
                {categories.map((category, catIndex) => (
                  <div key={catIndex}>
                    <h2 className="text-3xl font-bold mb-8">
                      <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                        {category.name}
                      </span>
                    </h2>
                    <div className="space-y-4">
                      {category.questions.map((item, qIndex) => {
                        const index = `${catIndex}-${qIndex}`;
                        return (
                          <div
                            key={index}
                            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden hover:bg-white/10 transition-all duration-300"
                          >
                            <button
                              onClick={() => toggleQuestion(index)}
                              className="w-full px-8 py-6 flex items-center justify-between text-left"
                            >
                              <h3 className="text-xl font-semibold text-white pr-4">{item.q}</h3>
                              {openIndex === index ? (
                                <ChevronUp className="w-6 h-6 text-cyan-400 flex-shrink-0" />
                              ) : (
                                <ChevronDown className="w-6 h-6 text-gray-400 flex-shrink-0" />
                              )}
                            </button>
                            {openIndex === index && (
                              <div className="px-8 pb-6 border-t border-white/10">
                                <p className="text-gray-300 text-lg leading-relaxed pt-6">{item.a}</p>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-32">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Still Have{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                Questions?
              </span>
            </h2>
            <p className="text-xl text-gray-300 mb-12">
              Our support team is available 24/7 to help you
            </p>
            <a
              href="/contact"
              className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-lg font-bold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50"
            >
              Contact Support
            </a>
          </div>
        </section>
      </div>
    </Layout>
  );
}

