# Daily Drawdown Calculation Explained

**Last Updated:** November 4, 2025

---

The Maximum Daily Loss rule is one of the most important rules to understand. This article explains exactly how it is calculated.

## The Rule: 5% Maximum Daily Loss

Your account equity cannot fall by more than 5% of your initial account balance on any given day. The calculation is based on your balance at the start of the day (00:00 server time).

---

## How It's Calculated

At the beginning of each new trading day (00:00 server time), we record your account balance. Your daily loss limit is then set at 5% below this starting balance.

**Formula:**
`Daily Loss Limit = (Balance at 00:00) - (5% of Initial Account Balance)`

### Example 1: No Open Trades

- **Account Size:** $100,000
- **Max Daily Loss (5%):** $5,000
- **Balance at 00:00:** $100,000

Your daily loss limit for the day is **$95,000** (`$100,000 - $5,000`). Your equity cannot drop below this value.

### Example 2: Profitable Account

- **Account Size:** $100,000
- **Max Daily Loss (5%):** $5,000
- **Balance at 00:00:** $103,000

Your daily loss limit for the day is **$98,000** (`$103,000 - $5,000`).

---

## Important Considerations

### Includes Floating Positions
The calculation includes both closed trades and open (floating) positions. If you have an open trade with a floating loss, it will be counted towards your daily drawdown.

### Based on Equity, Not Balance
The rule applies to your **equity**, not just your balance. This means you need to monitor the real-time value of your account, including any open trades.

### Resets Every Day
The daily loss limit resets every day at 00:00 server time, based on your new starting balance.

---

## How to Monitor Your Daily Drawdown

Your MarketEdgePros dashboard provides a real-time view of your daily drawdown limit and how close you are to it. We highly recommend checking this regularly throughout your trading day.

> **Best Practice:** To stay safe, many traders aim to stop trading for the day if they are down 3-4%, well before they hit the 5% limit.

---

### Questions?

If you are unsure about the daily drawdown calculation, please contact our support team.

- **[Contact Support](/contact)**
- **[Total Drawdown Limits](/support/total-drawdown-limits)**
