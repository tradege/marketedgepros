import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import useAuthStore from '../../store/authStore';

export default function LandingNavbar() {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, user } = useAuthStore();

  const navLinks = [
    { name: 'How It Works', href: '/#how-it-works' },
    { name: 'Programs', to: '/programs' },
    { name: 'Features', href: '/#features' },
    { name: 'About', to: '/about' },
    { name: 'Blog', to: '/blog' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-lg"></div>
            <span className="text-xl font-bold text-white">MarketEdgePros</span>
          </Link>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              link.to ? (
                <Link 
                  key={link.name}
                  to={link.to} 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  {link.name}
                </Link>
              ) : (
                <a 
                  key={link.name}
                  href={link.href} 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  {link.name}
                </a>
              )
            ))}
          </div>
          
          {/* CTA Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link 
                  to="/dashboard" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Dashboard
                </Link>
                <span className="text-gray-400">
                  {user?.first_name || 'User'}
                </span>
              </>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full text-sm font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition-all text-white"
                >
                  Get Funded
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-gray-300 hover:text-white"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-4">
            {navLinks.map((link) => (
              link.to ? (
                <Link
                  key={link.name}
                  to={link.to}
                  className="block text-gray-300 hover:text-white transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {link.name}
                </Link>
              ) : (
                <a
                  key={link.name}
                  href={link.href}
                  className="block text-gray-300 hover:text-white transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {link.name}
                </a>
              )
            ))}
            <div className="pt-4 border-t border-white/10 space-y-2">
              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="block px-4 py-2 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-lg text-center text-white font-semibold"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="block text-center text-gray-300 hover:text-white transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="block px-4 py-2 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-lg text-center text-white font-semibold"
                    onClick={() => setIsOpen(false)}
                  >
                    Get Funded
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
