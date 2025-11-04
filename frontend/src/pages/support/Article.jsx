import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { ArrowLeft, Clock, Tag, Home, FileText, HelpCircle } from "lucide-react";
import { Helmet } from "react-helmet-async";
import { articles } from "../../data/articles";
import Layout from "../../components/layout/Layout";

const Article = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [relatedArticles, setRelatedArticles] = useState([]);

  useEffect(() => {
    const foundArticle = articles.find((a) => a.slug === slug);
    
    if (!foundArticle) {
      navigate("/404");
      return;
    }

    setArticle(foundArticle);

    const related = articles
      .filter((a) => a.category === foundArticle.category && a.slug !== slug)
      .slice(0, 3);
    
    setRelatedArticles(related);
    window.scrollTo(0, 0);
  }, [slug, navigate]);

  if (!article) {
    return null;
  }

  return (
    <Layout>
      <Helmet>
        <title>{article.title} | MarketEdgePros Support</title>
        <meta name="description" content={article.excerpt} />
        <meta name="keywords" content={article.tags.join(", ")} />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 pt-8">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <Link
            to="/support"
            className="inline-flex items-center text-cyan-400 hover:text-cyan-300 mb-6 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Support Hub
          </Link>

          <nav className="flex items-center space-x-2 text-sm text-gray-400 mb-6">
            <Link to="/" className="hover:text-cyan-400 transition-colors">
              <Home className="w-4 h-4" />
            </Link>
            <span>/</span>
            <Link to="/support" className="hover:text-cyan-400 transition-colors">
              Support
            </Link>
            <span>/</span>
            <span className="text-gray-300">{article.category}</span>
            <span>/</span>
            <span className="text-white">{article.title}</span>
          </nav>

          <article className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 overflow-hidden">
            <div className="p-8 border-b border-white/10">
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 text-cyan-400 text-sm font-medium mb-4">
                <FileText className="w-4 h-4 mr-1.5" />
                {article.category}
              </div>

              <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
                {article.title}
              </h1>

              <p className="text-xl text-gray-300 mb-6">{article.excerpt}</p>

              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1.5" />
                  {article.readTime} min read
                </div>
                <div className="flex items-center gap-2">
                  <Tag className="w-4 h-4" />
                  {article.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 rounded bg-white/5 hover:bg-white/10 transition-colors cursor-pointer"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div
              className="p-8 prose prose-invert prose-lg max-w-none
                prose-headings:text-white prose-headings:font-bold
                prose-h2:text-3xl prose-h2:mt-8 prose-h2:mb-4 prose-h2:bg-gradient-to-r prose-h2:from-cyan-400 prose-h2:to-blue-400 prose-h2:bg-clip-text prose-h2:text-transparent
                prose-h3:text-2xl prose-h3:mt-6 prose-h3:mb-3 prose-h3:text-cyan-300
                prose-p:text-gray-300 prose-p:leading-relaxed prose-p:mb-4
                prose-ul:text-gray-300 prose-ul:my-4
                prose-ol:text-gray-300 prose-ol:my-4
                prose-li:my-2
                prose-strong:text-white prose-strong:font-semibold
                prose-a:text-cyan-400 prose-a:no-underline hover:prose-a:text-cyan-300 hover:prose-a:underline
                prose-code:text-cyan-400 prose-code:bg-white/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded"
              dangerouslySetInnerHTML={{ __html: article.content }}
            />
          </article>

          {relatedArticles.length > 0 && (
            <div className="mt-12">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <FileText className="w-6 h-6 mr-2 text-cyan-400" />
                Related Articles
              </h2>
              <div className="grid md:grid-cols-3 gap-4">
                {relatedArticles.map((related) => (
                  <Link
                    key={related.slug}
                    to={`/support/article/${related.slug}`}
                    className="group bg-white/5 backdrop-blur-md rounded-xl border border-white/10 p-6 hover:bg-white/10 hover:border-cyan-500/50 transition-all"
                  >
                    <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-cyan-400 transition-colors">
                      {related.title}
                    </h3>
                    <p className="text-sm text-gray-400 mb-3">{related.excerpt}</p>
                    <div className="flex items-center text-xs text-gray-500">
                      <Clock className="w-3 h-3 mr-1" />
                      {related.readTime} min read
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          <div className="mt-12 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-2xl p-8 text-center">
            <HelpCircle className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">Still Need Help?</h2>
            <p className="text-gray-300 mb-6">
              Cannot find what you are looking for? Our support team is here to assist you.
            </p>
            <Link
              to="/support/create-ticket"
              className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all"
            >
              <HelpCircle className="w-5 h-5 mr-2" />
              Create Support Ticket
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Article;
