import { Helmet } from 'react-helmet-async';

/**
 * StructuredData Component
 * Adds Schema.org JSON-LD structured data for SEO
 */
export default function StructuredData({ type = 'website', data = {} }) {
  const getSchema = () => {
    switch (type) {
      case 'website':
        return {
          '@context': 'https://schema.org',
          '@type': 'WebSite',
          name: 'MarketEdgePros',
          url: 'https://marketedgepros.com',
          description: 'Professional prop trading platform for ambitious traders. Get funded and trade with up to $400,000 capital.',
          potentialAction: {
            '@type': 'SearchAction',
            target: {
              '@type': 'EntryPoint',
              urlTemplate: 'https://marketedgepros.com/search?q={search_term_string}'
            },
            'query-input': 'required name=search_term_string'
          }
        };

      case 'organization':
        return {
          '@context': 'https://schema.org',
          '@type': 'FinancialService',
          name: 'MarketEdgePros',
          url: 'https://marketedgepros.com',
          logo: 'https://marketedgepros.com/logo.png',
          description: 'Professional prop trading platform offering funded trading accounts to skilled traders worldwide.',
          address: {
            '@type': 'PostalAddress',
            addressCountry: 'US'
          },
          contactPoint: {
            '@type': 'ContactPoint',
            contactType: 'Customer Service',
            email: 'info@marketedgepros.com',
            availableLanguage: ['English']
          },
          sameAs: [
            'https://facebook.com/marketedgepros',
            'https://twitter.com/marketedgepros',
            'https://instagram.com/marketedgepros',
            'https://linkedin.com/company/marketedgepros',
            'https://discord.gg/jKbmeSe7'
          ]
        };

      case 'product':
        return {
          '@context': 'https://schema.org',
          '@type': 'Product',
          name: data.name || 'Trading Program',
          description: data.description || 'Professional funded trading program',
          brand: {
            '@type': 'Brand',
            name: 'MarketEdgePros'
          },
          offers: {
            '@type': 'Offer',
            price: data.price || '0',
            priceCurrency: 'USD',
            availability: 'https://schema.org/InStock',
            url: data.url || 'https://marketedgepros.com/programs'
          }
        };

      case 'faq':
        return {
          '@context': 'https://schema.org',
          '@type': 'FAQPage',
          mainEntity: data.questions?.map(q => ({
            '@type': 'Question',
            name: q.question,
            acceptedAnswer: {
              '@type': 'Answer',
              text: q.answer
            }
          })) || []
        };

      case 'article':
        return {
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: data.title || '',
          description: data.description || '',
          author: {
            '@type': 'Organization',
            name: 'MarketEdgePros'
          },
          publisher: {
            '@type': 'Organization',
            name: 'MarketEdgePros',
            logo: {
              '@type': 'ImageObject',
              url: 'https://marketedgepros.com/logo.png'
            }
          },
          datePublished: data.datePublished || new Date().toISOString(),
          dateModified: data.dateModified || new Date().toISOString()
        };

      case 'breadcrumb':
        return {
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: data.items?.map((item, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            name: item.name,
            item: item.url
          })) || []
        };

      default:
        return null;
    }
  };

  const schema = getSchema();

  if (!schema) return null;

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
}

