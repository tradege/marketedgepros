
import React from 'react';
import Layout from '../components/layout/Layout';

function TradingRules() {
  return (
    <Layout>
      <div className="bg-gray-900 text-white min-h-screen">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold mb-8 text-center">Trading Rules</h1>
          <div className="prose prose-invert lg:prose-xl mx-auto">
            <p>At MarketEdgePros, we are committed to providing a fair and transparent trading environment. All traders must adhere to the following rules to ensure a level playing field and responsible risk management.</p>

            <h2>General Rules</h2>
            <ul>
              <li>One account per person. Multiple accounts are not allowed.</li>
              <li>No use of any prohibited trading strategies, including but not limited to martingale, grid trading, or high-frequency trading bots.</li>
              <li>All trading must be performed manually by the account holder. No account sharing or third-party trading.</li>
              <li>Respect our risk management parameters at all times.</li>
            </ul>

            <h2>Risk Management</h2>
            <p>Our risk management rules are designed to protect both the trader and the firm from excessive losses.</p>
            <ul>
              <li><strong>Daily Loss Limit:</strong> You may not lose more than 5% of your initial account balance in a single day.</li>
              <li><strong>Maximum Drawdown:</strong> Your account balance may not fall below 10% of your initial account balance at any time.</li>
              <li><strong>Stop-Loss Required:</strong> All trades must have a valid stop-loss order.</li>
            </ul>

            <h2>Prohibited Strategies</h2>
            <p>The following strategies are strictly prohibited:</p>
            <ul>
              <li><strong>Martingale/Grid Trading:</strong> Averaging down or increasing position size after a losing trade.</li>
              <li><strong>High-Frequency Trading (HFT):</strong> Using automated systems to execute a large number of orders in fractions of a second.</li>
              <li><strong>Latency Arbitrage:</strong> Exploiting delays in price feeds.</li>
              <li><strong>Copy Trading:</strong> Copying trades from other traders or signals.</li>
            </ul>

            <h2>Violation of Rules</h2>
            <p>Any violation of these rules will result in an immediate termination of your trading account, and any profits will be forfeited. We reserve the right to update these rules at any time.</p>

            <p>If you have any questions about these rules, please contact our support team at <a href="mailto:support@marketedgepros.com">support@marketedgepros.com</a>.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default TradingRules;

