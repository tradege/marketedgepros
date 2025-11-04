export const articles = [
  {
    slug: "create-account",
    title: "How to Create an Account",
    category: "Getting Started",
    excerpt: "Learn how to sign up and create your MarketEdgePros account in just a few simple steps.",
    readTime: 3,
    tags: ["account", "signup", "getting started"],
    content: `
      <h2>Creating Your Account</h2>
      <p>Getting started with MarketEdgePros is quick and easy. Follow these simple steps to create your account:</p>
      
      <h3>Step 1: Visit the Registration Page</h3>
      <p>Click on the "Get Funded" button in the top right corner of our website, or navigate directly to the registration page.</p>
      
      <h3>Step 2: Fill in Your Details</h3>
      <p>Provide the following information:</p>
      <ul>
        <li>Full Name</li>
        <li>Email Address</li>
        <li>Password (minimum 8 characters)</li>
        <li>Country of Residence</li>
      </ul>
      
      <h3>Step 3: Verify Your Email</h3>
      <p>Check your inbox for a verification email and click the confirmation link.</p>
      
      <h3>Step 4: Complete Your Profile</h3>
      <p>Once verified, log in and complete your profile with additional information.</p>
      
      <h2>Next Steps</h2>
      <p>After creating your account, you can:</p>
      <ul>
        <li>Browse available trading challenges</li>
        <li>Complete KYC verification</li>
        <li>Make your first purchase</li>
      </ul>
    `
  },
  {
    slug: "choosing-challenge",
    title: "Choosing the Right Challenge",
    category: "Getting Started",
    excerpt: "Understand the different challenge types and find the perfect program for your trading style.",
    readTime: 5,
    tags: ["challenges", "programs", "selection"],
    content: `
      <h2>Understanding Our Challenge Programs</h2>
      <p>MarketEdgePros offers multiple challenge programs designed to suit different trading styles and experience levels.</p>
      
      <h3>One-Phase Challenge</h3>
      <p>Our fastest path to funding:</p>
      <ul>
        <li>Single evaluation phase</li>
        <li>8% profit target</li>
        <li>Quick path to funded account</li>
        <li>Ideal for experienced traders</li>
      </ul>
      
      <h3>Two-Phase Challenge</h3>
      <p>Balanced approach with two evaluation stages:</p>
      <ul>
        <li>Phase 1: 8% profit target</li>
        <li>Phase 2: 5% profit target</li>
        <li>More time to prove consistency</li>
        <li>Popular choice for most traders</li>
      </ul>
      
      <h3>Three-Phase Challenge</h3>
      <p>Extended evaluation period:</p>
      <ul>
        <li>Three progressive phases</li>
        <li>Lower profit targets per phase</li>
        <li>Maximum time to demonstrate skills</li>
        <li>Best for developing traders</li>
      </ul>
      
      <h2>Choosing the Right Program</h2>
      <p>Consider these factors:</p>
      <ul>
        <li>Your trading experience level</li>
        <li>Risk tolerance</li>
        <li>Time commitment</li>
        <li>Trading strategy</li>
      </ul>
    `
  },
  {
    slug: "first-payment",
    title: "Making Your First Payment",
    category: "Getting Started",
    excerpt: "Complete guide to purchasing your first challenge and getting started with trading.",
    readTime: 4,
    tags: ["payment", "purchase", "billing"],
    content: `
      <h2>Purchase Process</h2>
      <p>Follow these steps to purchase your first challenge:</p>
      
      <h3>Step 1: Select Your Challenge</h3>
      <p>Browse our programs and choose the challenge that fits your needs.</p>
      
      <h3>Step 2: Choose Account Size</h3>
      <p>Select from available account sizes:</p>
      <ul>
        <li>$5,000</li>
        <li>$10,000</li>
        <li>$25,000</li>
        <li>$50,000</li>
        <li>$100,000</li>
        <li>$200,000</li>
      </ul>
      
      <h3>Step 3: Payment Method</h3>
      <p>We accept:</p>
      <ul>
        <li>Credit/Debit Cards</li>
        <li>Cryptocurrency</li>
        <li>Bank Transfer</li>
      </ul>
      
      <h3>Step 4: Confirmation</h3>
      <p>After payment, you will receive:</p>
      <ul>
        <li>Payment confirmation email</li>
        <li>Trading account credentials</li>
        <li>MT5 login details</li>
      </ul>
    `
  },
  {
    slug: "setting-up-mt5",
    title: "Setting Up MT5",
    category: "Getting Started",
    excerpt: "Download, install, and configure MetaTrader 5 for trading with MarketEdgePros.",
    readTime: 6,
    tags: ["MT5", "platform", "setup"],
    content: `
      <h2>MetaTrader 5 Setup Guide</h2>
      <p>MetaTrader 5 (MT5) is the trading platform used for all MarketEdgePros challenges.</p>
      
      <h3>Download MT5</h3>
      <p>Visit the official MetaTrader website or download from:</p>
      <ul>
        <li>Windows Desktop</li>
        <li>Mac Desktop</li>
        <li>iOS App Store</li>
        <li>Google Play Store</li>
      </ul>
      
      <h3>Installation</h3>
      <ol>
        <li>Run the installer</li>
        <li>Follow the setup wizard</li>
        <li>Complete installation</li>
        <li>Launch MT5</li>
      </ol>
      
      <h3>Login to Your Account</h3>
      <p>Use the credentials provided in your welcome email:</p>
      <ul>
        <li>Server: [Provided in email]</li>
        <li>Login: [Your account number]</li>
        <li>Password: [Your trading password]</li>
      </ul>
      
      <h3>Platform Configuration</h3>
      <p>Customize your workspace:</p>
      <ul>
        <li>Add chart windows</li>
        <li>Set up indicators</li>
        <li>Configure trading tools</li>
        <li>Save your layout</li>
      </ul>
    `
  },
  {
    slug: "trading-rules",
    title: "Understanding Trading Rules",
    category: "Getting Started",
    excerpt: "Essential trading rules and guidelines you must follow during your challenge.",
    readTime: 7,
    tags: ["rules", "guidelines", "compliance"],
    content: `
      <h2>Trading Rules Overview</h2>
      <p>All traders must adhere to these rules to maintain their account and qualify for funding.</p>
      
      <h3>Daily Drawdown Limit</h3>
      <p>Maximum loss allowed in a single day:</p>
      <ul>
        <li>Calculated from daily starting balance</li>
        <li>Typically 5% of account size</li>
        <li>Includes floating and realized P&L</li>
        <li>Resets at midnight server time</li>
      </ul>
      
      <h3>Maximum Drawdown Limit</h3>
      <p>Overall account drawdown limit:</p>
      <ul>
        <li>Usually 10% of initial balance</li>
        <li>Calculated from highest balance achieved</li>
        <li>Never resets during challenge</li>
        <li>Breach results in account failure</li>
      </ul>
      
      <h3>Minimum Trading Days</h3>
      <p>Required number of active trading days:</p>
      <ul>
        <li>Varies by challenge type</li>
        <li>Typically 3-5 days minimum</li>
        <li>Must have at least one trade per day</li>
        <li>Weekends not counted</li>
      </ul>
      
      <h3>Prohibited Trading Practices</h3>
      <ul>
        <li>No hedging across accounts</li>
        <li>No tick scalping</li>
        <li>No high-frequency trading (HFT)</li>
        <li>No copy trading from external sources</li>
        <li>No exploitation of platform errors</li>
      </ul>
      
      <h3>Allowed Trading Strategies</h3>
      <ul>
        <li>Day trading</li>
        <li>Swing trading</li>
        <li>Position trading</li>
        <li>Expert Advisors (EAs) - with approval</li>
        <li>News trading - with restrictions</li>
      </ul>
    `
  }
];
