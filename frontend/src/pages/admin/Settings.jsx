import { useState } from 'react';
import AdminLayout from '../../components/admin/AdminLayout';
import { Save } from 'lucide-react';

export default function Settings() {
  const [generalSettings, setGeneralSettings] = useState({
    platformName: 'MarketEdgePros',
    supportEmail: 'support@marketedgepros.com',
    contactPhone: '+1 (555) 123-4567',
    enableRegistration: true,
    enableEmailNotifications: true,
  });

  const [paymentSettings, setPaymentSettings] = useState({
    stripeApiKey: 'sk_test_...',
    paypalClientId: '...',
    minimumPayout: '100',
    enableStripe: true,
    enablePaypal: false,
  });

  const handleGeneralSave = () => {
    // TODO: Implement save functionality
    alert('General settings saved successfully!');
  };

  const handlePaymentSave = () => {
    // TODO: Implement save functionality
    alert('Payment settings saved successfully!');
  };

  return (
    <AdminLayout>
      <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="mt-2 text-gray-300">Configure platform settings and preferences</p>
      </div>

      {/* Settings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* General Settings Card */}
        <div className="bg-slate-800/50 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-white mb-4">General Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Platform Name
              </label>
              <input
                type="text"
                value={generalSettings.platformName}
                onChange={(e) => setGeneralSettings({ ...generalSettings, platformName: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Support Email
              </label>
              <input
                type="email"
                value={generalSettings.supportEmail}
                onChange={(e) => setGeneralSettings({ ...generalSettings, supportEmail: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Contact Phone
              </label>
              <input
                type="tel"
                value={generalSettings.contactPhone}
                onChange={(e) => setGeneralSettings({ ...generalSettings, contactPhone: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="enableRegistration"
                checked={generalSettings.enableRegistration}
                onChange={(e) => setGeneralSettings({ ...generalSettings, enableRegistration: e.target.checked })}
                className="w-4 h-4 text-blue-600 border-white/20 rounded focus:ring-blue-500"
              />
              <label htmlFor="enableRegistration" className="ml-2 text-sm text-gray-200">
                Enable User Registration
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="enableEmailNotifications"
                checked={generalSettings.enableEmailNotifications}
                onChange={(e) => setGeneralSettings({ ...generalSettings, enableEmailNotifications: e.target.checked })}
                className="w-4 h-4 text-blue-600 border-white/20 rounded focus:ring-blue-500"
              />
              <label htmlFor="enableEmailNotifications" className="ml-2 text-sm text-gray-200">
                Enable Email Notifications
              </label>
            </div>

            <button
              onClick={handleGeneralSave}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center gap-2"
            >
              <Save className="w-5 h-5" />
              Save Changes
            </button>
          </div>
        </div>

        {/* Payment Settings Card */}
        <div className="bg-slate-800/50 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Payment Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Stripe API Key
              </label>
              <input
                type="password"
                value={paymentSettings.stripeApiKey}
                onChange={(e) => setPaymentSettings({ ...paymentSettings, stripeApiKey: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                PayPal Client ID
              </label>
              <input
                type="password"
                value={paymentSettings.paypalClientId}
                onChange={(e) => setPaymentSettings({ ...paymentSettings, paypalClientId: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Minimum Payout ($)
              </label>
              <input
                type="number"
                value={paymentSettings.minimumPayout}
                onChange={(e) => setPaymentSettings({ ...paymentSettings, minimumPayout: e.target.value })}
                className="w-full px-4 py-2 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="enableStripe"
                checked={paymentSettings.enableStripe}
                onChange={(e) => setPaymentSettings({ ...paymentSettings, enableStripe: e.target.checked })}
                className="w-4 h-4 text-blue-600 border-white/20 rounded focus:ring-blue-500"
              />
              <label htmlFor="enableStripe" className="ml-2 text-sm text-gray-200">
                Enable Stripe
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="enablePaypal"
                checked={paymentSettings.enablePaypal}
                onChange={(e) => setPaymentSettings({ ...paymentSettings, enablePaypal: e.target.checked })}
                className="w-4 h-4 text-blue-600 border-white/20 rounded focus:ring-blue-500"
              />
              <label htmlFor="enablePaypal" className="ml-2 text-sm text-gray-200">
                Enable PayPal
              </label>
            </div>

            <button
              onClick={handlePaymentSave}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center gap-2"
            >
              <Save className="w-5 h-5" />
              Save Changes
            </button>
          </div>
        </div>
      </div>
      </div>
    </AdminLayout>
  );
}

