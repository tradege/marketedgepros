import React from 'react';
import Layout from '../components/layout/Layout';
import { Briefcase, Users, TrendingUp, Globe, DollarSign, Clock } from 'lucide-react';

function Careers() {
  const benefits = [
    {
      icon: Users,
      title: "Talented Team",
      description: "Work with passionate and skilled professionals",
      color: "from-cyan-500 to-blue-600"
    },
    {
      icon: TrendingUp,
      title: "Shape the Future",
      description: "Build the future of prop trading industry",
      color: "from-purple-500 to-pink-600"
    },
    {
      icon: DollarSign,
      title: "Competitive Pay",
      description: "Attractive salary and benefits package",
      color: "from-green-500 to-emerald-600"
    },
    {
      icon: Clock,
      title: "Flexible Work",
      description: "Work from anywhere with flexible hours",
      color: "from-orange-500 to-red-600"
    },
    {
      icon: Globe,
      title: "Global Impact",
      description: "Reach traders in 200+ countries",
      color: "from-blue-500 to-indigo-600"
    }
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Hero Section */}
        <div className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-blue-900/20 to-purple-900/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-24 relative">
            <div className="text-center max-w-4xl mx-auto">
              <div className="flex justify-center mb-6">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                  <Briefcase className="w-10 h-10 text-white" />
                </div>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                Join Our <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Team</span>
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Help us build the future of prop trading and empower traders worldwide
              </p>
            </div>
          </div>
        </div>

        {/* Benefits Grid */}
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-12">
              Why <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Join Us?</span>
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
              {benefits.map((benefit, index) => {
                const Icon = benefit.icon;
                return (
                  <div key={index} className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${benefit.color} flex items-center justify-center mb-4`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                    <p className="text-gray-400">{benefit.description}</p>
                  </div>
                );
              })}
            </div>

            {/* Open Positions */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50 mb-8">
              <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
                Open Positions
              </h2>
              <p className="text-gray-300 text-lg mb-6">
                We do not have any open positions at the moment, but we are always interested in hearing from talented people.
              </p>
              <p className="text-gray-300 text-lg">
                If you believe you have what it takes to be a part of our team, please send your resume and a cover letter to{' '}
                <a href="mailto:careers@marketedgepros.com" className="text-cyan-400 hover:text-cyan-300 transition-colors font-semibold">
                  careers@marketedgepros.com
                </a>
              </p>
            </div>

            {/* CTA */}
            <div className="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 rounded-2xl p-12 border border-cyan-500/30 text-center">
              <h2 className="text-3xl font-bold mb-4">Ready to Make an Impact?</h2>
              <p className="text-gray-300 text-lg mb-8">
                Join us in revolutionizing the prop trading industry
              </p>
              <a
                href="mailto:careers@marketedgepros.com"
                className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 hover:scale-105"
              >
                <Briefcase className="w-5 h-5" />
                Apply Now
              </a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Careers;

