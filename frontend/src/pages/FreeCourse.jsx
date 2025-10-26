import { useState } from 'react';
import { CheckCircle, BookOpen, Video, FileText, Award, Mail, ArrowRight } from 'lucide-react';
import Layout from '../components/layout/Layout';
import SEO from '../components/SEO';
import StructuredData from '../components/seo/StructuredData';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

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
      title: 'Module 4: Trading Strategies',
      duration: '70 min',
      lessons: [
        'Trend Following Strategies',
        'Range Trading Techniques',
        'Breakout Trading',
        'News Trading Fundamentals',
        'Scalping vs Swing Trading'
      ],
      icon: Award
    },
    {
      title: 'Module 5: Prop Trading Success',
      duration: '40 min',
      lessons: [
        'Understanding Prop Firm Rules',
        'Passing Evaluation Challenges',
        'Consistency and Discipline',
        'Scaling Your Funded Account',
        'Common Mistakes to Avoid'
      ],
      icon: CheckCircle
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await axios.post(`${API_URL}/leads/course-signup`, {
        email,
        name,
        source: 'free_course'
      });
      
      setSubmitted(true);
      setEmail('');
      setName('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to sign up. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const courseData = {
    title: 'Free Trading Course - Master Prop Trading',
    description: 'Learn professional trading strategies, risk management, and how to pass prop firm challenges. 100% free comprehensive course.',
    datePublished: '2025-10-26',
    dateModified: '2025-10-26'
  };

  return (
    <Layout>
      <SEO
        title="Free Trading Course - Master Prop Trading"
        description="Learn professional trading strategies, risk management, and how to pass prop firm challenges. 100% free comprehensive course for aspiring funded traders."
        keywords="free trading course, prop trading education, trading strategies, risk management, funded trader training"
      />
      <StructuredData type="article" data={courseData} />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Content */}
            <div>
              <div className="inline-block mb-4 px-4 py-2 bg-green-500/10 border border-green-500/30 rounded-full">
                <span className="text-green-400 text-sm font-semibold">100% FREE COURSE</span>
              </div>

              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                <span className="text-white">Master </span>
                <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  Prop Trading
                </span>
                <br />
                <span className="text-white">in 5 Modules</span>
              </h1>

              <p className="text-xl text-gray-300 mb-8">
                Learn everything you need to become a successful funded trader. From trading fundamentals to passing prop firm challenges.
              </p>

              <div className="space-y-4 mb-8">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <span className="text-gray-300">5 comprehensive modules (265+ minutes)</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <span className="text-gray-300">Video lessons + downloadable resources</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <span className="text-gray-300">Lifetime access - learn at your own pace</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <span className="text-gray-300">Certificate of completion</span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <Award className="w-12 h-12 text-yellow-400" />
                <div>
                  <div className="text-2xl font-bold text-white">4,500+</div>
                  <div className="text-gray-400">Students enrolled</div>
                </div>
              </div>
            </div>

            {/* Right Column - Signup Form */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8">
              {!submitted ? (
                <>
                  <div className="text-center mb-6">
                    <Mail className="w-16 h-16 text-blue-400 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-white mb-2">
                      Get Instant Access
                    </h2>
                    <p className="text-gray-400">
                      Enter your details to start learning today
                    </p>
                  </div>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                        Full Name
                      </label>
                      <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="John Doe"
                      />
                    </div>

                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                        Email Address
                      </label>
                      <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="john@example.com"
                      />
                    </div>

                    {error && (
                      <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                        {error}
                      </div>
                    )}

                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full px-6 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-bold text-lg hover:from-blue-600 hover:to-purple-700 transition transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        'Sending...'
                      ) : (
                        <>
                          Get Free Access
                          <ArrowRight className="w-5 h-5" />
                        </>
                      )}
                    </button>

                    <p className="text-xs text-gray-400 text-center">
                      By signing up, you agree to receive educational emails from MarketEdgePros.
                      Unsubscribe anytime.
                    </p>
                  </form>
                </>
              ) : (
                <div className="text-center py-8">
                  <CheckCircle className="w-20 h-20 text-green-400 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-white mb-2">
                    Check Your Email!
                  </h3>
                  <p className="text-gray-300 mb-6">
                    We've sent you the course access link. Check your inbox (and spam folder) for the email.
                  </p>
                  <button
                    onClick={() => setSubmitted(false)}
                    className="text-blue-400 hover:text-blue-300 font-semibold"
                  >
                    Sign up another email
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Course Modules */}
      <section className="py-20 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              What You'll <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">Learn</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              5 comprehensive modules covering everything from trading basics to advanced prop firm strategies
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {courseModules.map((module, index) => {
              const Icon = module.icon;
              return (
                <div
                  key={index}
                  className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 hover:transform hover:scale-105"
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div className="p-3 bg-blue-500/10 rounded-lg">
                      <Icon className="w-6 h-6 text-blue-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-white mb-1">
                        {module.title}
                      </h3>
                      <p className="text-sm text-gray-400">{module.duration}</p>
                    </div>
                  </div>

                  <ul className="space-y-2">
                    {module.lessons.map((lesson, lessonIndex) => (
                      <li key={lessonIndex} className="flex items-start gap-2 text-gray-300 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                        <span>{lesson}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Start Your Trading Journey?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of traders who have transformed their trading with our free course.
          </p>
          <a
            href="#signup"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg font-bold text-lg hover:bg-gray-100 transition transform hover:scale-105"
          >
            Get Free Access Now
          </a>
        </div>
      </section>
    </Layout>
  );
}

