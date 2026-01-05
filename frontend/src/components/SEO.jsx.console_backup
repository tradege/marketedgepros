import { Helmet } from 'react-helmet-async';

export default function SEO({
  title = 'MarketEdgePros',
  description = 'Professional prop trading firm offering instant funding, one-phase, and two-phase challenges. Get funded and trade with up to $200K capital.',
  keywords = 'prop trading, funded trading, trading challenge, forex funding, day trading, instant funding',
  ogImage = '/og-image.jpg',
  ogType = 'website',
  twitterCard = 'summary_large_image',
  canonical,
  noindex = false,
  nofollow = false,
  structuredData
}) {
  const siteUrl = 'https://marketedgepros.com';
  const fullTitle = title === 'MarketEdgePros' ? title : `${title} | MarketEdgePros`;
  const canonicalUrl = canonical || `${siteUrl}${window.location.pathname}`;
  const ogImageUrl = ogImage.startsWith('http') ? ogImage : `${siteUrl}${ogImage}`;

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      
      {/* Canonical URL */}
      <link rel="canonical" href={canonicalUrl} />
      
      {/* Robots */}
      {(noindex || nofollow) && (
        <meta name="robots" content={`${noindex ? 'noindex' : 'index'},${nofollow ? 'nofollow' : 'follow'}`} />
      )}
      
      {/* Open Graph */}
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:image" content={ogImageUrl} />
      <meta property="og:site_name" content="MarketEdgePros" />
      
      {/* Twitter Card */}
      <meta name="twitter:card" content={twitterCard} />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImageUrl} />
      <meta name="twitter:site" content="@marketedgepros" />
      <meta name="twitter:creator" content="@marketedgepros" />
      
      {/* Additional Meta Tags */}
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta httpEquiv="Content-Type" content="text/html; charset=utf-8" />
      <meta name="language" content="English" />
      <meta name="revisit-after" content="7 days" />
      <meta name="author" content="MarketEdgePros" />
      
      {/* Favicon */}
      <link rel="icon" type="image/x-icon" href="/favicon.ico" />
      <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
      <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
      <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
      
      {/* Structured Data */}
      {structuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}
    </Helmet>
  );
}

// Predefined SEO configurations for common pages
export const SEOConfigs = {
  home: {
    title: 'Professional Prop Trading Firm',
    description: 'Get funded with MarketEdgePros. Trade with up to $200K capital. Instant funding, one-phase, and two-phase challenges available. 80% profit split.',
    keywords: 'prop trading, funded trading account, trading challenge, instant funding, forex funding',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      name: 'MarketEdgePros',
      url: 'https://marketedgepros.com',
      logo: 'https://marketedgepros.com/logo.png',
      description: 'Professional prop trading firm offering funded trading accounts',
      sameAs: [
        'https://twitter.com/marketedgepros',
        'https://facebook.com/marketedgepros',
        'https://linkedin.com/company/marketedgepros'
      ]
    }
  },
  
  programs: {
    title: 'Trading Programs & Challenges',
    description: 'Choose from instant funding, one-phase, or two-phase trading challenges. Account sizes from $5K to $200K. 80% profit split. Start trading today.',
    keywords: 'trading programs, trading challenge, prop firm programs, funded account sizes',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      name: 'Trading Programs',
      description: 'Available trading programs and challenges',
      itemListElement: []
    }
  },
  
  onePhase: {
    title: 'One Phase Challenge',
    description: 'Single evaluation phase trading challenge. Prove your skills in one step and get funded. Account sizes from $5K to $200K.',
    keywords: 'one phase challenge, single step evaluation, quick funding, prop trading'
  },
  
  twoPhase: {
    title: 'Two Phase Challenge',
    description: 'Two-step evaluation trading challenge. Phase 1: 8% target, Phase 2: 5% target. Get funded with proven consistency.',
    keywords: 'two phase challenge, two step evaluation, consistent trading, prop firm evaluation'
  },
  
  instantFunding: {
    title: 'Instant Funding',
    description: 'Get funded immediately with no evaluation required. Start trading with real capital today. Account sizes from $5K to $50K.',
    keywords: 'instant funding, no evaluation, immediate funding, funded account'
  },
  
  about: {
    title: 'About Us',
    description: 'Learn about MarketEdgePros, our mission, values, and commitment to empowering traders worldwide.',
    keywords: 'about marketedgepros, prop firm mission, trading company'
  },
  
  howItWorks: {
    title: 'How It Works',
    description: 'Step-by-step guide to getting funded with MarketEdgePros. From registration to payout, we make it simple.',
    keywords: 'how prop trading works, getting funded, trading evaluation process'
  },
  
  faq: {
    title: 'Frequently Asked Questions',
    description: 'Find answers to common questions about our trading programs, rules, payouts, and more.',
    keywords: 'prop trading faq, trading questions, funded account questions',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: []
    }
  },
  
  contact: {
    title: 'Contact Us',
    description: 'Get in touch with MarketEdgePros. We\'re here to help with any questions about our trading programs.',
    keywords: 'contact prop firm, trading support, customer service'
  },
  
  login: {
    title: 'Login',
    description: 'Login to your MarketEdgePros account. Access your dashboard, challenges, and trading statistics.',
    keywords: 'trader login, account access, dashboard login',
    noindex: true
  },
  
  register: {
    title: 'Register',
    description: 'Create your MarketEdgePros account and start your journey to becoming a funded trader.',
    keywords: 'register trader account, sign up, create account'
  },
  
  dashboard: {
    title: 'Dashboard',
    description: 'Your MarketEdgePros trading dashboard. View your challenges, performance, and account statistics.',
    keywords: 'trading dashboard, account overview, trader portal',
    noindex: true
  }
};

