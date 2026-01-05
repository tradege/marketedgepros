import { useState } from 'react';
import { CheckCircle, BookOpen, Video, FileText, Award, Mail, ArrowRight } from 'lucide-react';
import Layout from '../components/layout/Layout';
import SEO from '../components/SEO';
import StructuredData from '../components/seo/StructuredData';
import api from "../services/api";



export default function FreeCourse() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const courseModules = [
    {
      title: 'Module 1: Trading Fundamentals',
      duration: '45 min',
      lessons: [
        'Understanding Financial Markets',
        'Market Participants and Structure',
        'Types of Trading Instruments',
        'Reading Price Charts',
        'Timeframes and Their Importance'
      ],
      icon: BookOpen
    },
    {
      title: 'Module 2: Technical Analysis',
      duration: '60 min',
      lessons: [
        'Support and Resistance Levels',
        'Trend Lines and Channels',
        'Chart Patterns (Head & Shoulders, Triangles)',
        'Candlestick Patterns',
        'Moving Averages and Indicators'
      ],
      icon: Video
    },
    {
      title: 'Module 3: Risk Management',
      duration: '50 min',
      lessons: [
        'Position Sizing Strategies',
        'Stop Loss and Take Profit',
        'Risk-Reward Ratios',
        'Managing Drawdowns',
        'Psychology of Risk'
      ],
      icon: FileText
    },
    {
      title: 'Module 4: Trading Strategy',
      duration: '55 min',
      lessons: [
        'Developing Your Trading Plan',
        'Entry and Exit Strategies',
        'Backtesting Your Strategy',
        'Adapting to Market Conditions',
        'Building a Trading Journal'
      ],
      icon: Award
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await api.post('/free-course/register', {
        name,
        email
      });
      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to register. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const courseData = {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "Free Trading Course - MarketEdgePros",
    "description": "Learn professional trading strategies with our comprehensive free course. Master technical analysis, risk management, and trading psychology.",
    "provider": {
      "@type": "Organization",
      "name": "MarketEdgePros",
      "sameAs": "https://marketedgepros.com"
    },
    "educationalLevel": "Beginner to Intermediate",
    "coursePrerequisites": "None",
    "hasCourseInstance": {
      "@type": "CourseInstance",
      "courseMode": "online",
      "courseWorkload": "PT3H30M"
    }
  };

  return (
    <Layout>
      <SEO
        title="Free Trading Course | Learn Professional Trading"
        description="Master trading with our comprehensive free course. Learn technical analysis, risk management, and proven strategies from professional traders."
        keywords="free trading course, learn trading, trading education, technical analysis, risk management"
        canonical="https://marketedgepros.com/free-course"
      />
      <StructuredData data={courseData} />

      <div className="min-h-screen bg-black py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Hero Section */}
          <div className="text-center mb-20">
            <div className="inline-flex items-center gap-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full px-6 py-2 mb-6">
              <Award className="w-5 h-5 text-cyan-400" />
              <span className="text-cyan-400 font-semibold">100% Free • No Credit Card Required</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Master <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Professional Trading</span>
            </h1>
            
            <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-12">
              Learn the strategies and techniques used by successful prop traders. Our comprehensive free course covers everything from fundamentals to advanced risk management.
            </p>

            {/* Registration Form */}
            {!submitted ? (
              <div className="max-w-md mx-auto bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
                <h3 className="text-2xl font-bold text-white mb-6">Get Instant Access</h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <input
                      type="text"
                      placeholder="Your Name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                      className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500 transition-colors"
                    />
                  </div>
                  <div>
                    <input
                      type="email"
                      placeholder="Your Email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500 transition-colors"
                    />
                  </div>
                  {error && (
                    <p className="text-red-400 text-sm">{error}</p>
                  )}
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    {loading ? 'Sending...' : 'Start Learning Now'}
                    <ArrowRight className="w-5 h-5" />
                  </button>
                </form>
                <p className="text-xs text-gray-400 mt-4">
                  By signing up, you agree to receive course materials via email.
                </p>
              </div>
            ) : (
              <div className="max-w-md mx-auto bg-cyan-500/10 border border-cyan-500/30 rounded-2xl p-8">
                <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Check Your Email!</h3>
                <p className="text-gray-300">
                  We've sent you the course materials and access instructions. Start learning right away!
                </p>
              </div>
            )}
          </div>

          {/* Course Modules */}
          <div className="mb-20">
            <h2 className="text-4xl font-bold text-center text-white mb-4">
              What You'll <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">Learn</span>
            </h2>
            <p className="text-gray-300 text-center max-w-2xl mx-auto mb-12">
              4 comprehensive modules covering everything you need to become a successful trader
            </p>

            <div className="grid md:grid-cols-2 gap-8">
              {courseModules.map((module, index) => {
                const Icon = module.icon;
                return (
                  <div
                    key={index}
                    className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105"
                  >
                    <div className="flex items-center gap-4 mb-6">
                      <div className="w-14 h-14 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
                        <Icon className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-white">{module.title}</h3>
                        <p className="text-cyan-400 text-sm">{module.duration}</p>
                      </div>
                    </div>
                    <ul className="space-y-3">
                      {module.lessons.map((lesson, lessonIndex) => (
                        <li key={lessonIndex} className="flex items-start gap-3">
                          <CheckCircle className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-300">{lesson}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Benefits */}
          <div className="grid md:grid-cols-3 gap-8 mb-20">
            <div className="text-center p-8 bg-white/5 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                <Video className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Video Lessons</h3>
              <p className="text-gray-400">High-quality video content with real trading examples</p>
            </div>
            <div className="text-center p-8 bg-white/5 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Downloadable Resources</h3>
              <p className="text-gray-400">PDFs, checklists, and trading templates</p>
            </div>
            <div className="text-center p-8 bg-white/5 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-all duration-300">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full flex items-center justify-center">
                <Award className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Lifetime Access</h3>
              <p className="text-gray-400">Learn at your own pace, revisit anytime</p>
            </div>
          </div>

          {/* CTA */}
          {!submitted && (
            <div className="text-center bg-gradient-to-r from-cyan-500/10 to-teal-500/10 border border-cyan-500/30 rounded-2xl p-12">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Ready to Start Your Trading Journey?
              </h2>
              <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
                Join thousands of traders who have learned with our free course. No credit card required.
              </p>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5" />
              </a>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

