import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { supportArticles } from '../../data/articles';
import Layout from '../../components/layout/Layout';
import ReactMarkdown from 'react-markdown';

const Article = () => {
  const { slug } = useParams();
  const [article, setArticle] = useState(null);
  const [content, setContent] = useState('');
  const [relatedArticles, setRelatedArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Find article in all categories
    let foundArticle = null;
    let categoryKey = null;

    for (const [key, category] of Object.entries(supportArticles)) {
      const found = category.articles.find((a) => a.slug === slug);
      if (found) {
        foundArticle = found;
        categoryKey = key;
        break;
      }
    }

    if (foundArticle) {
      setArticle(foundArticle);
      
      // Load markdown content from file
      const loadContent = async () => {
        try {
          // Map category keys to folder names
          const folderMap = {
            'getting-started': 'getting-started',
            'challenges-evaluation': 'challenges-and-evaluation',
            'funded-accounts': 'funded-accounts',
            'payments-withdrawals': 'payments-and-withdrawals',
            'platform-technical': 'platform-and-technical',
            'account-management': 'account-management',
          };
          
          const folder = folderMap[categoryKey];
          const response = await fetch(`/support_articles/${folder}/${slug}.md`);
          
          if (response.ok) {
            const text = await response.text();
            setContent(text);
          } else {
            setContent(`# ${foundArticle.title}

## Overview

This article covers important information about ${foundArticle.title.toLowerCase()}. We're currently updating our support documentation to provide you with the most comprehensive and up-to-date information.

## Key Points

### Understanding the Basics

${foundArticle.title} is an essential aspect of your trading journey with MarketEdgePros. Whether you're just getting started or looking to optimize your trading strategy, understanding this topic is crucial for your success.

### Important Considerations

When dealing with ${foundArticle.title.toLowerCase()}, keep these important factors in mind:

1. **Follow the Rules** - Always adhere to the trading rules and guidelines
2. **Risk Management** - Proper risk management is key to long-term success
3. **Stay Informed** - Keep up with platform updates and announcements
4. **Ask Questions** - Don't hesitate to reach out to support if you need clarification

### Best Practices

To make the most of your experience:

- Review all relevant documentation thoroughly
- Test your understanding with small positions first
- Keep detailed records of your trading activity
- Regularly check your account status and metrics
- Stay within all defined limits and parameters

## Need More Information?

### Contact Support

If you need specific information about ${foundArticle.title.toLowerCase()}, please don't hesitate to contact our support team:

- **Email:** support@marketedgepros.com
- **Live Chat:** Available 24/7 via the chat widget
- **Discord:** Join our community for peer support

### Related Resources

- Check our FAQ section for quick answers
- Browse other articles in the ${foundArticle.category.replace('-', ' ')} category
- Join our Discord community for discussions with other traders
- Review your dashboard for personalized information

## Additional Help

Our support team is always here to help you succeed. We're committed to providing you with the resources and assistance you need to achieve your trading goals.

### Quick Tips

- **Be Patient** - Success in prop trading takes time and discipline
- **Stay Consistent** - Follow your trading plan consistently
- **Learn Continuously** - Always look for ways to improve your skills
- **Manage Risk** - Never risk more than you can afford to lose

## Conclusion

Understanding ${foundArticle.title.toLowerCase()} is an important part of your journey with MarketEdgePros. If you have any questions or need further clarification, our support team is ready to assist you.

---

*Last Updated: November 2025*
*Article Status: Under Review*

For the most current information, please contact our support team or check your account dashboard.`);
          }
        } catch (error) {
          console.error('Error loading article:', error);
          setContent(`# ${foundArticle.title}

## Overview

This article covers important information about ${foundArticle.title.toLowerCase()}. We're currently updating our support documentation.

## Contact Support

For specific information, please contact support@marketedgepros.com`);
        } finally {
          setLoading(false);
        }
      };

      loadContent();

      // Get related articles from the same category
      const related = supportArticles[categoryKey].articles
        .filter((a) => a.slug !== slug)
        .slice(0, 3);
      setRelatedArticles(related);
    } else {
      setArticle(null);
      setLoading(false);
    }
  }, [slug]);

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-black text-white flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading article...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!article) {
    return (
      <Layout>
        <div className="min-h-screen bg-black text-white flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Article Not Found</h1>
            <p className="text-gray-400 mb-8">The article you're looking for doesn't exist.</p>
            <Link
              to="/support"
              className="inline-block bg-gradient-to-r from-cyan-500 to-teal-500 text-white font-bold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity"
            >
              Back to Support Hub
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <Helmet>
        <title>{`${article.title} | MarketEdgePros Support`}</title>
        <meta name="description" content={article.description} />
      </Helmet>

      <div className="min-h-screen bg-black text-white">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-4xl mx-auto">
            {/* Breadcrumbs */}
            <div className="text-sm text-gray-400 mb-6">
              <Link to="/support" className="hover:text-cyan-400 transition-colors">
                Support Hub
              </Link>
              <span className="mx-2">/</span>
              <span className="capitalize">{article.category.replace('-', ' ')}</span>
              <span className="mx-2">/</span>
              <span className="text-gray-200">{article.title}</span>
            </div>

            {/* Article Header */}
            <div className="bg-gradient-to-br from-gray-900 to-black border border-cyan-500/20 rounded-lg p-8 mb-8">
              <span className="inline-block bg-gradient-to-r from-cyan-500 to-teal-500 text-black text-xs font-semibold px-3 py-1 rounded-full mb-4">
                {article.category.replace('-', ' ').toUpperCase()}
              </span>
              <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-teal-400">
                {article.title}
              </h1>
              <p className="text-lg text-gray-300 mb-4">{article.description}</p>
              <div className="flex items-center text-sm text-gray-400">
                <span>📖 {article.readTime} read</span>
                <span className="mx-2">|</span>
                <span>📅 Last updated: Nov 4, 2025</span>
              </div>
            </div>

            {/* Article Content */}
            <div className="prose prose-invert prose-cyan max-w-none">
              <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8">
                <ReactMarkdown
                  components={{
                    h1: ({ node, ...props }) => <h1 className="text-3xl font-bold text-white mb-4 mt-8" {...props} />,
                    h2: ({ node, ...props }) => <h2 className="text-2xl font-bold text-white mb-3 mt-6" {...props} />,
                    h3: ({ node, ...props }) => <h3 className="text-xl font-bold text-cyan-400 mb-2 mt-4" {...props} />,
                    p: ({ node, ...props }) => <p className="text-gray-300 mb-4 leading-relaxed" {...props} />,
                    a: ({ node, ...props }) => <a className="text-cyan-400 hover:text-cyan-300 underline" {...props} />,
                    ul: ({ node, ...props }) => <ul className="list-disc list-inside text-gray-300 mb-4 space-y-2" {...props} />,
                    ol: ({ node, ...props }) => <ol className="list-decimal list-inside text-gray-300 mb-4 space-y-2" {...props} />,
                    blockquote: ({ node, ...props }) => (
                      <blockquote className="border-l-4 border-cyan-500 pl-4 italic text-gray-400 my-4" {...props} />
                    ),
                    table: ({ node, ...props }) => (
                      <div className="overflow-x-auto my-6">
                        <table className="min-w-full border border-gray-700" {...props} />
                      </div>
                    ),
                    thead: ({ node, ...props }) => <thead className="bg-gray-800" {...props} />,
                    tbody: ({ node, ...props }) => <tbody className="divide-y divide-gray-700" {...props} />,
                    tr: ({ node, ...props }) => <tr {...props} />,
                    th: ({ node, ...props }) => <th className="px-4 py-2 text-left text-cyan-400 font-semibold" {...props} />,
                    td: ({ node, ...props }) => <td className="px-4 py-2 text-gray-300" {...props} />,
                    code: ({ node, inline, ...props }) =>
                      inline ? (
                        <code className="bg-gray-800 text-cyan-400 px-2 py-1 rounded text-sm" {...props} />
                      ) : (
                        <code className="block bg-gray-800 text-cyan-400 p-4 rounded-lg overflow-x-auto my-4" {...props} />
                      ),
                    strong: ({ node, ...props }) => <strong className="text-white font-bold" {...props} />,
                    hr: ({ node, ...props }) => <hr className="border-gray-700 my-8" {...props} />,
                  }}
                >
                  {content}
                </ReactMarkdown>
              </div>
            </div>

            {/* Related Articles */}
            {relatedArticles.length > 0 && (
              <div className="mt-16">
                <h2 className="text-2xl font-bold mb-6 text-white">Related Articles</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {relatedArticles.map((related) => (
                    <Link
                      key={related.slug}
                      to={`/support/article/${related.slug}`}
                      className="block bg-gray-900 border border-gray-800 rounded-lg p-6 hover:border-cyan-500 hover:shadow-lg hover:shadow-cyan-500/20 transition-all"
                    >
                      <h3 className="font-bold text-lg mb-2 text-white">{related.title}</h3>
                      <p className="text-sm text-gray-400 mb-3">{related.description}</p>
                      <span className="text-cyan-400 text-sm font-semibold">Read more →</span>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Still Need Help? */}
            <div className="mt-16 text-center bg-gradient-to-br from-gray-900 to-black border border-cyan-500/20 rounded-lg p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">Still Need Help?</h2>
              <p className="text-gray-400 mb-6">
                Can't find what you're looking for? Our support team is here to assist you 24/7.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/contact"
                  className="inline-block bg-gradient-to-r from-cyan-500 to-teal-500 text-white font-bold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity"
                >
                  Contact Support
                </Link>
                <Link
                  to="/faq"
                  className="inline-block bg-gray-800 border border-gray-700 text-white font-bold py-3 px-6 rounded-lg hover:border-cyan-500 transition-colors"
                >
                  Browse FAQ
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Article;
