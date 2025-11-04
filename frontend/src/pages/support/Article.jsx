import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { articles } from "../../data/articles";
import { Helmet } from "react-helmet-async";
import { 
  BookOpen, 
  Clock, 
  Tag, 
  ArrowLeft, 
  ChevronRight,
  MessageCircle
} from "lucide-react";

const Article = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [relatedArticles, setRelatedArticles] = useState([]);

  useEffect(() => {
    const foundArticle = articles.find(a => a.slug === slug);
    
    if (!foundArticle) {
      navigate("/404");
      return;
    }

    setArticle(foundArticle);

    const related = articles
      .filter(a => a.category === foundArticle.category && a.slug !== slug)
      .slice(0, 3);
    setRelatedArticles(related);
  }, [slug, navigate]);

  if (!article) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>{article.title} | MarketEdgePros Support</title>
        <meta name="description" content={article.excerpt} />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
        <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <Link 
              to="/support" 
              className="inline-flex items-center text-cyan-400 hover:text-cyan-300 transition-colors mb-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Support Hub
            </Link>
            
            <div className="flex items-center text-sm text-gray-400 space-x-2">
              <Link to="/" className="hover:text-white transition-colors">Home</Link>
              <ChevronRight className="w-4 h-4" />
              <Link to="/support" className="hover:text-white transition-colors">Support</Link>
              <ChevronRight className="w-4 h-4" />
              <span className="text-white">{article.category}</span>
              <ChevronRight className="w-4 h-4" />
              <span className="text-cyan-400">{article.title}</span>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 py-12">
          <article className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 overflow-hidden">
            <div className="p-8 border-b border-white/10">
              <div className="flex items-center space-x-4 mb-4">
                <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-sm font-medium">
                  {article.category}
                </span>
                <div className="flex items-center text-gray-400 text-sm">
                  <Clock className="w-4 h-4 mr-1" />
                  {article.readTime} min read
                </div>
              </div>
              
              <h1 className="text-4xl font-bold text-white mb-4">
                {article.title}
              </h1>
              
              <p className="text-xl text-gray-300">
                {article.excerpt}
              </p>

              {article.tags && article.tags.length > 0 && (
                <div className="flex items-center flex-wrap gap-2 mt-4">
                  <Tag className="w-4 h-4 text-gray-400" />
                  {article.tags.map((tag, index) => (
                    <span 
                      key={index}
                      className="px-2 py-1 bg-white/5 text-gray-400 rounded text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="p-8 prose prose-invert prose-cyan max-w-none">
              <div 
                className="text-gray-300 leading-relaxed space-y-6"
                dangerouslySetInnerHTML={{ __html: article.content }}
              />
            </div>
          </article>

          {relatedArticles.length > 0 && (
            <div className="mt-12">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <BookOpen className="w-6 h-6 mr-2 text-cyan-400" />
                Related Articles
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                {relatedArticles.map((related) => (
                  <Link
                    key={related.slug}
                    to={`/support/article/${related.slug}`}
                    className="bg-white/5 backdrop-blur-md rounded-xl border border-white/10 p-6 hover:bg-white/10 transition-all group"
                  >
                    <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-cyan-400 transition-colors">
                      {related.title}
                    </h3>
                    <p className="text-gray-400 text-sm line-clamp-2">
                      {related.excerpt}
                    </p>
                    <div className="flex items-center text-cyan-400 text-sm mt-4">
                      Read more
                      <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          <div className="mt-12 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 backdrop-blur-md rounded-2xl border border-cyan-500/20 p-8">
            <div className="flex items-start space-x-4">
              <MessageCircle className="w-8 h-8 text-cyan-400 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-white mb-2">
                  Still Need Help?
                </h3>
                <p className="text-gray-300 mb-4">
                  Cannot find what you are looking for? Our support team is here to assist you.
                </p>
                <Link
                  to="/support/create-ticket"
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all"
                >
                  Create Support Ticket
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Article;
