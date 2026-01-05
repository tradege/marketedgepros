import { Helmet } from 'react-helmet-async';

const SchemaMarkup = () => {
  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "MarketEdgePros",
    "url": "https://marketedgepros.com",
    "logo": "https://marketedgepros.com/logo.png",
    "description": "Professional prop trading platform providing funding to talented traders worldwide. Trade with up to $400,000 in capital and keep up to 90% of profits.",
    "foundingDate": "2020",
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "US"
    },
    "sameAs": [
      "https://www.facebook.com/marketedgepros",
      "https://twitter.com/marketedgepros",
      "https://www.instagram.com/marketedgepros",
      "https://www.linkedin.com/company/marketedgepros"
    ]
  };

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How fast can I get funded?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "With instant funding, you can start trading immediately. For evaluation programs, most traders complete them in 2-4 weeks."
        }
      },
      {
        "@type": "Question",
        "name": "Are there any time limits?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No! Unlike other firms, we don't impose time limits on evaluations. Trade at your own pace and comfort level."
        }
      },
      {
        "@type": "Question",
        "name": "How do payouts work?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Request payouts anytime after your first profitable trade. We process all payout requests within 24 hours on business days."
        }
      },
      {
        "@type": "Question",
        "name": "Can I scale my account?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Absolutely! Consistent traders can scale up to $400K and increase their profit split to 90% based on performance."
        }
      }
    ]
  };

  const reviewSchema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "MarketEdgePros Prop Trading Program",
    "description": "Professional prop trading funding program with up to $400,000 capital and 90% profit split",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "1247"
    },
    "review": [
      {
        "@type": "Review",
        "author": {
          "@type": "Person",
          "name": "Alex Thompson"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "MarketEdgePros changed my trading career. Fast payouts, fair rules, and excellent support. I scaled from $25K to $100K in 4 months!"
      },
      {
        "@type": "Review",
        "author": {
          "@type": "Person",
          "name": "Maria Garcia"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "Best prop firm I've worked with. No time pressure, realistic targets, and they actually care about trader success. Highly recommended!"
      },
      {
        "@type": "Review",
        "author": {
          "@type": "Person",
          "name": "James Wilson"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "The instant funding option was perfect for me. Started trading with real capital immediately and now making consistent profits with 90% split."
      }
    ]
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(organizationSchema)}
      </script>
      <script type="application/ld+json">
        {JSON.stringify(faqSchema)}
      </script>
      <script type="application/ld+json">
        {JSON.stringify(reviewSchema)}
      </script>
    </Helmet>
  );
};

export default SchemaMarkup;

