import React from 'react';
import { UserPlus, Target, TrendingUp, DollarSign, CheckCircle, ArrowRight } from 'lucide-react';
import Layout from '../components/layout/Layout';

export default function HowItWorks() {
  const steps = [
    {
      number: 1,
      icon: UserPlus,
      title: 'Sign Up & Choose Your Challenge',
      description: 'Create your account and select a challenge that matches your trading style and capital goals.',
      details: [
        'Choose from One-Phase, Two-Phase, or Instant Funding',
        'Select your preferred account size ($10K - $200K)',
        'Review the trading objectives and rules',
        'Complete your registration and payment'
      ]
    },
    {
      number: 2,
      icon: Target,
      title: 'Pass Your Evaluation',
      description: 'Demonstrate your trading skills by meeting the profit targets while following risk management rules.',
      details: [
        'Trade on a demo account with real market conditions',
        'Meet the profit target (typically 8-10%)',
        'Stay within daily and overall drawdown limits',
        'Trade for minimum required days',
        'No prohibited trading strategies'
      ]
    },
    {
      number: 3,
      icon: CheckCircle,
      title: 'Get Funded',
      description: 'Once you pass, receive your funded account and start trading with our capital.',
      details: [
        'Receive your funded account within 24 hours',
        'Get access to live MT5 trading account',
        'Start trading with real capital',
        'Keep up to 90% of your profits',
        'Scale your account based on performance'
      ]
    },
    {
      number: 4,
      icon: DollarSign,
      title: 'Withdraw Your Profits',
      description: 'Request withdrawals anytime and receive your profits quickly and securely.',
      details: [
        'Request withdrawals on-demand',
        'Receive profits within 1-3 business days',
        'Multiple payment methods available',
        'No minimum withdrawal amount',
        'Keep trading and earning continuously'
      ]
    }
  ];

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
              How It{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                Works
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">
              Your journey from trader to funded professional in 4 simple steps
            </p>
          </div>
        </section>

        {/* Steps Section */}
        <section className="relative py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="space-y-32">
              {steps.map((step, index) => {
                const Icon = step.icon;
                const isEven = index % 2 === 0;
                
                return (
                  <div key={index} className={`grid md:grid-cols-2 gap-16 items-center ${isEven ? '' : 'md:flex-row-reverse'}`}>
                    {/* Content */}
                    <div className={isEven ? '' : 'md:order-2'}>
                      <div className="inline-flex items-center gap-3 mb-6">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-500 flex items-center justify-center text-2xl font-bold">
                          {step.number}
                        </div>
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-500 flex items-center justify-center">
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                      </div>
                      
                      <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                          {step.title}
                        </span>
                      </h2>
                      
                      <p className="text-xl text-gray-300 mb-8">
                        {step.description}
                      </p>
                      
                      <ul className="space-y-4">
                        {step.details.map((detail, idx) => (
                          <li key={idx} className="flex items-start gap-3">
                            <CheckCircle className="w-6 h-6 text-cyan-400 flex-shrink-0 mt-1" />
                            <span className="text-gray-300 text-lg">{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    {/* Visual */}
                    <div className={isEven ? '' : 'md:order-1'}>
                      <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-teal-500/20 blur-3xl"></div>
                        <div className="relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-12 text-center">
                          <div className="w-32 h-32 mx-auto rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-500 flex items-center justify-center mb-6">
                            <Icon className="w-16 h-16 text-white" />
                          </div>
                          <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-4">
                            Step {step.number}
                          </div>
                          <div className="text-2xl font-semibold text-gray-300">
                            {step.title}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Arrow (except last step) */}
                    {index < steps.length - 1 && (
                      <div className="col-span-2 flex justify-center my-8">
                        <ArrowRight className="w-12 h-12 text-cyan-400 transform rotate-90 md:rotate-0" />
                      </div>
                    )}
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
              Join thousands of traders and start your funded trading journey today
            </p>
            <a
              href="/programs"
              className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-lg font-bold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50"
            >
              View Programs
            </a>
          </div>
        </section>
      </div>
    </Layout>
  );
}

