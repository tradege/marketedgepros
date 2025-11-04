import React from "react";
import { Link } from "react-router-dom";
import { Home, Search, ArrowLeft, HelpCircle } from "lucide-react";
import { Helmet } from "react-helmet-async";

const NotFound = () => {
  return (
    <>
      <Helmet>
        <title>404 - Page Not Found | MarketEdgePros</title>
        <meta name="robots" content="noindex,nofollow" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center px-4">
        <div className="max-w-2xl w-full">
          {/* 404 Card */}
          <div className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-12 text-center">
            {/* 404 Number */}
            <div className="mb-8">
              <h1 className="text-9xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                404
              </h1>
            </div>

            {/* Message */}
            <h2 className="text-3xl font-bold text-white mb-4">
              Page Not Found
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Sorry, the page you are looking for does not exist or has been moved.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link
                to="/"
                className="inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all"
              >
                <Home className="w-5 h-5 mr-2" />
                Go to Home
              </Link>
              
              <Link
                to="/support"
                className="inline-flex items-center justify-center px-6 py-3 bg-white/10 text-white font-semibold rounded-lg hover:bg-white/20 transition-all border border-white/20"
              >
                <HelpCircle className="w-5 h-5 mr-2" />
                Get Help
              </Link>
            </div>

            {/* Suggestions */}
            <div className="border-t border-white/10 pt-8">
              <p className="text-gray-400 mb-4">You might want to try:</p>
              <div className="grid sm:grid-cols-2 gap-3 text-left">
                <Link
                  to="/programs"
                  className="flex items-center p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all group"
                >
                  <ArrowLeft className="w-4 h-4 mr-2 text-cyan-400 group-hover:translate-x-1 transition-transform" />
                  <span className="text-white">Browse Programs</span>
                </Link>
                
                <Link
                  to="/support/faq"
                  className="flex items-center p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all group"
                >
                  <Search className="w-4 h-4 mr-2 text-cyan-400" />
                  <span className="text-white">Search FAQ</span>
                </Link>
                
                <Link
                  to="/about"
                  className="flex items-center p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all group"
                >
                  <ArrowLeft className="w-4 h-4 mr-2 text-cyan-400 group-hover:translate-x-1 transition-transform" />
                  <span className="text-white">About Us</span>
                </Link>
                
                <Link
                  to="/support/create-ticket"
                  className="flex items-center p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all group"
                >
                  <HelpCircle className="w-4 h-4 mr-2 text-cyan-400" />
                  <span className="text-white">Contact Support</span>
                </Link>
              </div>
            </div>
          </div>

          {/* Additional Help */}
          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              If you believe this is an error, please{" "}
              <Link to="/support/create-ticket" className="text-cyan-400 hover:text-cyan-300 underline">
                contact our support team
              </Link>
              .
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default NotFound;
