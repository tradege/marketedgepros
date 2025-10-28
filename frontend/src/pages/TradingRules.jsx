import React from 'react';
import Layout from '../components/layout/Layout';
import { Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

function TradingRules() {
  const rules = [
    {
      title: "General Rules",
      icon: Shield,
      items: [
        "One account per person. Multiple accounts are not allowed.",
        "No use of prohibited trading strategies including martingale, grid trading, or high-frequency trading bots.",
        "All trading must be performed manually by the account holder. No account sharing or third-party trading.",
        "Respect our risk management parameters at all times."
      ]
    },
    {
      title: "Risk Management",
      icon: AlertTriangle,
      items: [
        "Daily Loss Limit: You may not lose more than 5% of your initial account balance in a single day.",
        "Maximum Drawdown: Your account balance may not fall below 10% of your initial account balance at any time.",
        "Stop-Loss Required: All trades must have a valid stop-loss order."
      ]
    }
  ];

  const prohibited = [
    "Martingale/Grid Trading: Averaging down or increasing position size after a losing trade.",
    "High-Frequency Trading (HFT): Using automated systems to execute a large number of orders in fractions of a second.",
    "Latency Arbitrage: Exploiting delays in price feeds.",
    "Copy Trading: Copying trades from other traders or signals."
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Hero Section */}
        <div className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-blue-900/20 to-purple-900/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-24 relative">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                Trading <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Rules</span>
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Fair and transparent guidelines to ensure a level playing field for all traders
              </p>
            </div>
          </div>
        </div>

        {/* Rules Sections */}
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {rules.map((section, index) => {
              const Icon = section.icon;
              return (
                <div key={index} className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50 hover:border-cyan-500/50 transition-all duration-300">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold">{section.title}</h2>
                  </div>
                  <ul className="space-y-4">
                    {section.items.map((item, i) => (
                      <li key={i} className="flex items-start gap-3">
                        <CheckCircle className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          {/* Prohibited Strategies */}
          <div className="bg-gradient-to-br from-red-900/20 to-orange-900/20 rounded-2xl p-8 border border-red-500/30 mb-16">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-orange-600 flex items-center justify-center">
                <XCircle className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold">Prohibited Strategies</h2>
            </div>
            <p className="text-gray-300 mb-6">The following strategies are strictly prohibited:</p>
            <ul className="space-y-4">
              {prohibited.map((item, i) => (
                <li key={i} className="flex items-start gap-3">
                  <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-300">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Violation Warning */}
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-yellow-500/30">
            <h2 className="text-2xl font-bold mb-4 text-yellow-400">Violation of Rules</h2>
            <p className="text-gray-300 mb-4">
              Any violation of these rules will result in an immediate termination of your trading account, and any profits will be forfeited. We reserve the right to update these rules at any time.
            </p>
            <p className="text-gray-300">
              If you have any questions about these rules, please contact our support team at{' '}
              <a href="mailto:support@marketedgepros.com" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                support@marketedgepros.com
              </a>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default TradingRules;

