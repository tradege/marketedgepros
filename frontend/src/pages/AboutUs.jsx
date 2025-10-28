import React from 'react';
import { Award, Target, Users, TrendingUp, Shield, Globe, CheckCircle } from 'lucide-react';
import Layout from '../components/layout/Layout';

export default function AboutUs() {
  const values = [
    {
      icon: Shield,
      title: "Transparency",
      description: "Clear rules, fair evaluation, and honest communication at every step."
    },
    {
      icon: Users,
      title: "Community",
      description: "Building a global network of successful traders supporting each other."
    },
    {
      icon: Target,
      title: "Excellence",
      description: "Providing world-class technology and support to help traders succeed."
    },
    {
      icon: TrendingUp,
      title: "Growth",
      description: "Continuously improving our platform and expanding opportunities for traders."
    }
  ];

  const stats = [
    { value: "$10M+", label: "Capital Deployed", gradient: "from-cyan-400 to-teal-400" },
    { value: "5,000+", label: "Active Traders", gradient: "from-purple-400 to-pink-400" },
    { value: "120+", label: "Countries", gradient: "from-orange-400 to-red-400" },
    { value: "90%", label: "Profit Split", gradient: "from-blue-400 to-indigo-400" }
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-black text-white">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 z-0">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0%,transparent_65%)]"></div>
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(168,85,247,0.15)_0%,transparent_50%)]"></div>
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(14,165,233,0.15)_0%,transparent_50%)]"></div>
          </div>

          {/* Content */}
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-8">
              About{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                MarketEdgePros
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">
              Empowering traders worldwide with capital, technology, and support to achieve their trading goals.
            </p>
          </div>
        </section>

        {/* Stats Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className={`text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${stat.gradient} mb-2`}>
                    {stat.value}
                  </div>
                  <div className="text-gray-400 text-lg">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Mission Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="text-5xl md:text-6xl font-bold mb-8">
                  Our{' '}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                    Mission
                  </span>
                </h2>
                <p className="text-xl text-gray-300 mb-6">
                  At MarketEdgePros, we believe that talented traders deserve access to substantial capital to maximize their potential.
                </p>
                <p className="text-xl text-gray-300 mb-6">
                  Our mission is to identify, fund, and support skilled traders who demonstrate consistent profitability and risk management.
                </p>
                <p className="text-xl text-gray-300">
                  We provide a transparent, fair, and technology-driven platform that removes traditional barriers to professional trading.
                </p>
              </div>
              
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 blur-3xl"></div>
                <div className="relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-12">
                  <div className="space-y-6">
                    {[
                      "Access to substantial trading capital",
                      "Keep up to 90% of your profits",
                      "No time limits on challenges",
                      "Instant payout processing",
                      "Professional trading tools",
                      "Dedicated support team"
                    ].map((item, index) => (
                      <div key={index} className="flex items-center gap-4">
                        <CheckCircle className="w-6 h-6 text-cyan-400 flex-shrink-0" />
                        <span className="text-gray-300 text-lg">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Our{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                  Values
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                The principles that guide everything we do
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {values.map((value, index) => {
                const Icon = value.icon;
                return (
                  <div
                    key={index}
                    className="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300 hover:scale-105"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    <div className="relative">
                      <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-500 flex items-center justify-center mb-6">
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-2xl font-bold mb-4">{value.title}</h3>
                      <p className="text-gray-400">{value.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-32">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-5xl md:text-6xl font-bold mb-8">
              Ready to{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                Get Started?
              </span>
            </h2>
            <p className="text-xl text-gray-300 mb-12">
              Join thousands of traders worldwide and start your funded trading journey today
            </p>
            <a
              href="/programs"
              className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-lg font-bold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50"
            >
              Get Funded Now
            </a>
          </div>
        </section>
      </div>
    </Layout>
  );
}

