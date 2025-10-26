import { useEffect, useState } from 'react';
import { Save, Bell, Mail, Loader, CheckCircle, AlertCircle } from 'lucide-react';
import useNotificationStore from '../../stores/notificationStore';

const notificationTypes = [
  { key: 'withdrawal', label: 'Withdrawals', description: 'Updates about your withdrawal requests' },
  { key: 'commission', label: 'Commissions', description: 'Notifications about earned commissions' },
  { key: 'kyc', label: 'KYC Verification', description: 'Updates about your KYC status' },
  { key: 'payment', label: 'Payments', description: 'Payment confirmations and updates' },
  { key: 'challenge', label: 'Challenges', description: 'Challenge progress and results' },
  { key: 'system', label: 'System', description: 'System announcements and updates' },
];

export default function NotificationSettings() {
  const { preferences, loading, fetchPreferences, updatePreferences } = useNotificationStore();
  const [localPreferences, setLocalPreferences] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState(null);
  
  useEffect(() => {
    fetchPreferences();
  }, [fetchPreferences]);
  
  useEffect(() => {
    if (preferences) {
      setLocalPreferences(preferences);
    }
  }, [preferences]);
  
  const handleInAppChange = (type) => (event) => {
    setLocalPreferences((prev) => ({
      ...prev,
      in_app: {
        ...prev.in_app,
        [type]: event.target.checked,
      },
    }));
  };
  
  const handleEmailChange = (type) => (event) => {
    setLocalPreferences((prev) => ({
      ...prev,
      email: {
        ...prev.email,
        [type]: event.target.checked,
      },
    }));
  };
  
  const handleEmailEnabledChange = (event) => {
    setLocalPreferences((prev) => ({
      ...prev,
      settings: {
        ...prev.settings,
        email_enabled: event.target.checked,
      },
    }));
  };
  
  const handleEmailFrequencyChange = (value) => {
    setLocalPreferences((prev) => ({
      ...prev,
      settings: {
        ...prev.settings,
        email_frequency: value,
      },
    }));
  };
  
  const handleSave = async () => {
    setSaving(true);
    setSaveSuccess(false);
    setSaveError(null);
    
    const success = await updatePreferences(localPreferences);
    
    if (success) {
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } else {
      setSaveError('Failed to save preferences');
    }
    
    setSaving(false);
  };
  
  if (loading || !localPreferences) {
    return (
      <div className="max-w-3xl mx-auto p-6">
        <div className="flex justify-center p-12">
          <Loader className="w-8 h-8 text-purple-500 animate-spin" />
        </div>
      </div>
    );
  }
  
  return (
    <div className="max-w-3xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white mb-2">Notification Settings</h1>
        <p className="text-gray-400">Manage how you receive notifications</p>
      </div>
      
      {/* Success/Error Messages */}
      {saveSuccess && (
        <div className="mb-6 p-4 bg-green-500/20 border border-green-500/50 rounded-lg flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-green-400" />
          <p className="text-green-400">Preferences saved successfully!</p>
        </div>
      )}
      {saveError && (
        <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-400" />
          <p className="text-red-400">{saveError}</p>
        </div>
      )}
      
      {/* In-App Notifications */}
      <div className="mb-6 bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg p-6">
        <div className="flex items-center gap-2 mb-3">
          <Bell className="w-5 h-5 text-purple-400" />
          <h2 className="text-xl font-semibold text-white">In-App Notifications</h2>
        </div>
        <p className="text-gray-400 mb-6">Receive notifications within the application</p>
        
        <div className="space-y-4">
          {notificationTypes.map((type) => (
            <label key={type.key} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
              <div className="flex-1">
                <p className="text-white font-medium">{type.label}</p>
                <p className="text-sm text-gray-400">{type.description}</p>
              </div>
              <div className="relative inline-block w-12 h-6 transition duration-200 ease-in-out">
                <input
                  type="checkbox"
                  checked={localPreferences.in_app[type.key] || false}
                  onChange={handleInAppChange(type.key)}
                  className="opacity-0 w-0 h-0 peer"
                />
                <span className="absolute cursor-pointer inset-0 bg-gray-600 rounded-full transition-colors peer-checked:bg-purple-600"></span>
                <span className="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform peer-checked:translate-x-6"></span>
              </div>
            </label>
          ))}
        </div>
      </div>
      
      {/* Email Notifications */}
      <div className="mb-6 bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg p-6">
        <div className="flex items-center gap-2 mb-3">
          <Mail className="w-5 h-5 text-purple-400" />
          <h2 className="text-xl font-semibold text-white">Email Notifications</h2>
        </div>
        <p className="text-gray-400 mb-6">Receive notifications via email</p>
        
        {/* Email Enabled Toggle */}
        <label className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 cursor-pointer transition-colors mb-6">
          <div className="flex-1">
            <p className="text-white font-medium">Enable Email Notifications</p>
            <p className="text-sm text-gray-400">Turn on/off all email notifications</p>
          </div>
          <div className="relative inline-block w-12 h-6 transition duration-200 ease-in-out">
            <input
              type="checkbox"
              checked={localPreferences.settings.email_enabled || false}
              onChange={handleEmailEnabledChange}
              className="opacity-0 w-0 h-0 peer"
            />
            <span className="absolute cursor-pointer inset-0 bg-gray-600 rounded-full transition-colors peer-checked:bg-purple-600"></span>
            <span className="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform peer-checked:translate-x-6"></span>
          </div>
        </label>
        
        <div className="border-t border-white/10 my-6"></div>
        
        {/* Email Frequency */}
        <div className="mb-6">
          <p className="text-white font-medium mb-4">Email Frequency</p>
          <div className="space-y-3">
            {[
              { value: 'instant', label: 'Instant', description: 'Receive emails immediately' },
              { value: 'daily', label: 'Daily Digest', description: 'Receive a daily summary' },
              { value: 'weekly', label: 'Weekly Digest', description: 'Receive a weekly summary' },
            ].map((option) => (
              <label
                key={option.value}
                className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                  localPreferences.settings.email_enabled 
                    ? 'hover:bg-white/5' 
                    : 'opacity-50 cursor-not-allowed'
                }`}
              >
                <input
                  type="radio"
                  name="email_frequency"
                  value={option.value}
                  checked={localPreferences.settings.email_frequency === option.value}
                  onChange={() => handleEmailFrequencyChange(option.value)}
                  disabled={!localPreferences.settings.email_enabled}
                  className="w-4 h-4 text-purple-600 border-gray-600 focus:ring-purple-500"
                />
                <div className="ml-3">
                  <p className="text-white">{option.label}</p>
                  <p className="text-sm text-gray-400">{option.description}</p>
                </div>
              </label>
            ))}
          </div>
        </div>
        
        <div className="border-t border-white/10 my-6"></div>
        
        {/* Email Notification Types */}
        <div className="space-y-4">
          {notificationTypes.map((type) => (
            <label
              key={type.key}
              className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
                localPreferences.settings.email_enabled 
                  ? 'hover:bg-white/5' 
                  : 'opacity-50 cursor-not-allowed'
              }`}
            >
              <div className="flex-1">
                <p className="text-white font-medium">{type.label}</p>
                <p className="text-sm text-gray-400">{type.description}</p>
              </div>
              <div className="relative inline-block w-12 h-6 transition duration-200 ease-in-out">
                <input
                  type="checkbox"
                  checked={localPreferences.email[type.key] || false}
                  onChange={handleEmailChange(type.key)}
                  disabled={!localPreferences.settings.email_enabled}
                  className="opacity-0 w-0 h-0 peer"
                />
                <span className={`absolute cursor-pointer inset-0 rounded-full transition-colors ${
                  localPreferences.settings.email_enabled 
                    ? 'bg-gray-600 peer-checked:bg-purple-600' 
                    : 'bg-gray-700'
                }`}></span>
                <span className="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform peer-checked:translate-x-6"></span>
              </div>
            </label>
          ))}
        </div>
      </div>
      
      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {saving ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              Saving...
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              Save Preferences
            </>
          )}
        </button>
      </div>
    </div>
  );
}

