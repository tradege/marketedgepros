import React, { useState, useEffect } from 'react';

/**
 * Payment Method Form Component
 * Allows users to set up their payment method for withdrawals
 */
const PaymentMethodForm = () => {
  const [methodType, setMethodType] = useState('bank');
  const [currentMethod, setCurrentMethod] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  
  const [formData, setFormData] = useState({
    // Bank fields
    bank_name: '',
    account_number: '',
    branch_number: '',
    account_holder_name: '',
    // PayPal fields
    paypal_email: '',
    // Crypto fields
    crypto_address: '',
    crypto_network: 'TRC20',
    // Wise fields
    wise_email: '',
  });

  useEffect(() => {
    fetchCurrentMethod();
  }, []);

  const fetchCurrentMethod = async () => {
    try {
      const response = await fetch('/api/payment-method', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentMethod(data);
        setMethodType(data.method_type);
        setFormData({
          bank_name: data.bank_name || '',
          account_number: data.account_number || '',
          branch_number: data.branch_number || '',
          account_holder_name: data.account_holder_name || '',
          paypal_email: data.paypal_email || '',
          crypto_address: data.crypto_address || '',
          crypto_network: data.crypto_network || 'TRC20',
          wise_email: data.wise_email || '',
        });
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching payment method:', err);
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        method_type: methodType,
        ...formData,
      };

      const response = await fetch('/api/payment-method', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: 'Payment method saved successfully!' });
        setCurrentMethod(data.payment_method);
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to save payment method' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'An error occurred. Please try again.' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Payment Method</h1>
        <p className="mt-2 text-gray-600">Set up how you want to receive your commissions</p>
      </div>

      {/* Current Method Info */}
      {currentMethod && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <span className="text-2xl mr-3">ℹ️</span>
            <div>
              <p className="font-medium text-blue-900">Current Payment Method</p>
              <p className="text-sm text-blue-700 mt-1">
                {currentMethod.method_type.charAt(0).toUpperCase() + currentMethod.method_type.slice(1)}
                {currentMethod.method_type === 'bank' && ` - ${currentMethod.bank_name}`}
                {currentMethod.method_type === 'paypal' && ` - ${currentMethod.paypal_email}`}
                {currentMethod.method_type === 'crypto' && ` - ${currentMethod.crypto_network}`}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Message */}
      {message && (
        <div
          className={`rounded-lg p-4 mb-6 ${
            message.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6">
        {/* Method Type Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select Payment Method
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { value: 'bank', label: 'Bank Transfer', icon: '🏦' },
              { value: 'paypal', label: 'PayPal', icon: '💳' },
              { value: 'crypto', label: 'Crypto (USDT)', icon: '₿' },
              { value: 'wise', label: 'Wise', icon: '🌍' },
            ].map((method) => (
              <button
                key={method.value}
                type="button"
                onClick={() => setMethodType(method.value)}
                className={`p-4 border-2 rounded-lg text-center transition-all ${
                  methodType === method.value
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-3xl mb-2">{method.icon}</div>
                <div className="text-sm font-medium">{method.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Bank Transfer Fields */}
        {methodType === 'bank' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bank Name *
              </label>
              <input
                type="text"
                name="bank_name"
                value={formData.bank_name}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Bank Leumi, Bank Hapoalim"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Account Number *
              </label>
              <input
                type="text"
                name="account_number"
                value={formData.account_number}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Account number"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Branch Number
              </label>
              <input
                type="text"
                name="branch_number"
                value={formData.branch_number}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Branch number (if applicable)"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Account Holder Name *
              </label>
              <input
                type="text"
                name="account_holder_name"
                value={formData.account_holder_name}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Full name as on bank account"
              />
            </div>
          </div>
        )}

        {/* PayPal Fields */}
        {methodType === 'paypal' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              PayPal Email *
            </label>
            <input
              type="email"
              name="paypal_email"
              value={formData.paypal_email}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="your@email.com"
            />
            <p className="mt-2 text-sm text-gray-500">
              Make sure this email is linked to your PayPal account
            </p>
          </div>
        )}

        {/* Crypto Fields */}
        {methodType === 'crypto' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Network *
              </label>
              <select
                name="crypto_network"
                value={formData.crypto_network}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="TRC20">TRC20 (Tron)</option>
                <option value="ERC20">ERC20 (Ethereum)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                USDT Wallet Address *
              </label>
              <input
                type="text"
                name="crypto_address"
                value={formData.crypto_address}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                placeholder="Your USDT wallet address"
              />
              <p className="mt-2 text-sm text-yellow-600">
                ⚠️ Double-check your address! Incorrect addresses cannot be recovered.
              </p>
            </div>
          </div>
        )}

        {/* Wise Fields */}
        {methodType === 'wise' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Wise Email *
            </label>
            <input
              type="email"
              name="wise_email"
              value={formData.wise_email}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="your@email.com"
            />
            <p className="mt-2 text-sm text-gray-500">
              Email associated with your Wise account
            </p>
          </div>
        )}

        {/* Submit Button */}
        <div className="mt-6">
          <button
            type="submit"
            disabled={saving}
            className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {saving ? 'Saving...' : 'Save Payment Method'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PaymentMethodForm;

