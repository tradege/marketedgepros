import React from 'react';
import { Award, Target, Users, TrendingUp, Shield, Globe, CheckCircle, Calendar, MapPin, Linkedin } from 'lucide-react';
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

  const timeline = [
    {
      year: "2020",
      title: "Company Founded",
      description: "MarketEdgePros was established with a vision to democratize access to trading capital."
    },
    {
      year: "2021",
      title: "First 1,000 Traders",
      description: "Reached our first milestone of 1,000 funded traders across 50 countries."
    },
    {
      year: "2022",
      title: "Platform Expansion",
      description: "Launched instant funding and expanded to support multiple asset classes."
    },
    {
      year: "2023",
      title: "$10M Capital Deployed",
      description: "Surpassed $10 million in total capital deployed to successful traders."
    },
    {
      year: "2024",
      title: "Global Recognition",
      description: "Recognized as one of the top prop trading firms worldwide with 5,000+ active traders."
    }
  ];

  const team = [
    {
      name: "David Chen",
      role: "CEO & Founder",
      image: "DC",
      description: "Former institutional trader with 15+ years of experience in prop trading."
    },
    {
      name: "Sarah Williams",
      role: "CTO",
      image: "SW",
      description: "Technology leader specializing in trading platforms and risk management systems."
    },
    {
      name: "Michael Rodriguez",
      role: "Head of Trading",
      image: "MR",
      description: "Expert trader and educator with a track record of training successful traders."
    },
    {
      name: "Emma Thompson",
      role: "Head of Support",
      image: "ET",
      description: "Dedicated to ensuring every trader receives world-class support and guidance."
    }
  ];

  const achievements = [
    {
      icon: Award,
      title: "Industry Leader",
      description: "Ranked among top 5 prop trading firms globally"
    },
    {
      icon: Users,
      title: "Trader Success",
      description: "85% of funded traders remain profitable after 6 months"
    },
    {
      icon: Globe,
      title: "Global Reach",
      description: "Active traders in over 120 countries worldwide"
    },
    {
      icon: TrendingUp,
      title: "Fast Growth",
      description: "300% year-over-year growth in funded accounts"
    }
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

        {/* Timeline Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Our{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                  Journey
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                From startup to industry leader - our growth story
              </p>
            </div>

            <div className="relative">
              {/* Timeline Line */}
              <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-gradient-to-b from-cyan-500 via-purple-500 to-pink-500 hidden md:block"></div>

              <div className="space-y-12">
                {timeline.map((item, index) => (
                  <div key={index} className={`flex items-center gap-8 ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                    <div className={`flex-1 ${index % 2 === 0 ? 'md:text-right' : 'md:text-left'}`}>
                      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
                        <div className="flex items-center gap-3 mb-3">
                          <Calendar className="w-5 h-5 text-cyan-400" />
                          <span className="text-2xl font-bold text-cyan-400">{item.year}</span>
                        </div>
                        <h3 className="text-2xl font-bold text-white mb-2">{item.title}</h3>
                        <p className="text-gray-400">{item.description}</p>
                      </div>
                    </div>
                    <div className="hidden md:block w-4 h-4 bg-cyan-500 rounded-full border-4 border-black z-10"></div>
                    <div className="flex-1"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Meet Our{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                  Team
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Experienced professionals dedicated to your trading success
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {team.map((member, index) => (
                <div key={index} className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:border-cyan-500/50 transition-all hover:scale-105">
                  <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                    {member.image}
                  </div>
                  <h3 className="text-xl font-bold text-white text-center mb-1">{member.name}</h3>
                  <p className="text-cyan-400 text-center mb-4">{member.role}</p>
                  <p className="text-gray-400 text-center text-sm">{member.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Achievements Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-20">
              <h2 className="text-5xl md:text-6xl font-bold mb-6">
                Our{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                  Achievements
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Milestones that define our commitment to excellence
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {achievements.map((achievement, index) => {
                const Icon = achievement.icon;
                return (
                  <div key={index} className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:border-cyan-500/50 transition-all text-center">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{achievement.title}</h3>
                    <p className="text-gray-400">{achievement.description}</p>
                  </div>
                );
              })}
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

