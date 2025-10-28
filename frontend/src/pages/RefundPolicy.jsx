
import React from 'react';
import Layout from '../components/layout/Layout';

function RefundPolicy() {
  return (
    <Layout>
      <div className="bg-gray-900 text-white min-h-screen">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold mb-8 text-center">Refund Policy</h1>
          <div className="prose prose-invert lg:prose-xl mx-auto">
            <p>At MarketEdgePros, we offer a transparent and fair refund policy. Please read the following terms carefully.</p>

            <h2>Challenge Fees</h2>
            <p>All fees for our trading challenges are non-refundable once the challenge has started. This is because we incur costs for providing the trading platform and data feeds.</p>

            <h2>Eligibility for Refund</h2>
            <p>You may be eligible for a refund under the following circumstances:</p>
            <ul>
              <li>If you request a refund within 24 hours of purchase AND you have not placed any trades.</li>
              <li>If there was a technical issue on our end that prevented you from starting the challenge.</li>
            </ul>

            <h2>How to Request a Refund</h2>
            <p>To request a refund, please contact our support team at <a href="mailto:support@marketedgepros.com">support@marketedgepros.com</a> with your account details and reason for the request. All refund requests are subject to review.</p>

            <h2>Processing Time</h2>
            <p>Refunds, if approved, will be processed within 5-7 business days to the original method of payment.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default RefundPolicy;

