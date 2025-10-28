
import React from 'react';
import Layout from '../components/layout/Layout';

function Careers() {
  return (
    <Layout>
      <div className="bg-gray-900 text-white min-h-screen">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold mb-8 text-center">Careers</h1>
          <div className="prose prose-invert lg:prose-xl mx-auto">
            <p>Join our team of innovators and help us build the future of prop trading. We are always looking for talented individuals to join our mission.</p>

            <h2>Open Positions</h2>
            <p>We do not have any open positions at the moment, but we are always interested in hearing from talented people. If you believe you have what it takes to be a part of our team, please send your resume and a cover letter to <a href="mailto:careers@marketedgepros.com">careers@marketedgepros.com</a>.</p>

            <h2>Why Join Us?</h2>
            <ul>
              <li>Work with a passionate and talented team.</li>
              <li>Shape the future of the prop trading industry.</li>
              <li>Competitive salary and benefits.</li>
              <li>Flexible work environment.</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Careers;

