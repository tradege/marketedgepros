
import React from 'react';
import Layout from '../components/layout/Layout';

function CookiePolicy() {
  return (
    <Layout>
      <div className="bg-gray-900 text-white min-h-screen">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold mb-8 text-center">Cookie Policy</h1>
          <div className="prose prose-invert lg:prose-xl mx-auto">
            <p>This Cookie Policy explains how MarketEdgePros uses cookies and similar technologies to recognize you when you visit our website.</p>

            <h2>What are cookies?</h2>
            <p>Cookies are small data files that are placed on your computer or mobile device when you visit a website. Cookies are widely used by website owners in order to make their websites work, or to work more efficiently, as well as to provide reporting information.</p>

            <h2>How we use cookies</h2>
            <p>We use cookies for several reasons. Some cookies are required for technical reasons in order for our website to operate, and we refer to these as "essential" or "strictly necessary" cookies. Other cookies also enable us to track and target the interests of our users to enhance the experience on our website.</p>

            <h2>Types of cookies we use</h2>
            <ul>
              <li><strong>Essential cookies:</strong> These are necessary to provide you with services available through our website and to use some of its features, such as access to secure areas.</li>
              <li><strong>Performance and functionality cookies:</strong> These are used to enhance the performance and functionality of our website but are non-essential to their use.</li>
              <li><strong>Analytics and customization cookies:</strong> These cookies collect information that is used either in aggregate form to help us understand how our website is being used or how effective our marketing campaigns are.</li>
            </ul>

            <h2>Your choices</h2>
            <p>You have the right to decide whether to accept or reject cookies. You can exercise your cookie preferences by setting or amending your web browser controls to accept or refuse cookies.</p>

            <p>If you have any questions about our use of cookies, please contact us at <a href="mailto:support@marketedgepros.com">support@marketedgepros.com</a>.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default CookiePolicy;

