import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

/**
 * Component to display and copy referral code
 */
const ReferralCodeDisplay = ({ code, size = 'sm' }) => {
  const [copied, setCopied] = useState(false);

  if (!code) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
    }
  };

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2'
  };

  return (
    <div className="inline-flex items-center gap-1">
      <code className={`${sizeClasses[size]} bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded font-mono`}>
        {code}
      </code>
      <button
        onClick={handleCopy}
        className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
        title="Copy referral code"
      >
        {copied ? (
          <Check className="w-4 h-4 text-green-600" />
        ) : (
          <Copy className="w-4 h-4 text-gray-500" />
        )}
      </button>
    </div>
  );
};

export default ReferralCodeDisplay;

