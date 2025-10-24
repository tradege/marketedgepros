import { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Switch,
  FormControlLabel,
  FormGroup,
  Divider,
  Button,
  Alert,
  CircularProgress,
  RadioGroup,
  Radio,
  FormControl,
  FormLabel,
} from '@mui/material';
import {
  Save as SaveIcon,
  Notifications as NotificationsIcon,
  Email as EmailIcon,
} from '@mui/icons-material';
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
  
  const handleEmailFrequencyChange = (event) => {
    setLocalPreferences((prev) => ({
      ...prev,
      settings: {
        ...prev.settings,
        email_frequency: event.target.value,
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
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Notification Settings
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Manage how you receive notifications
        </Typography>
      </Box>
      
      {/* Success/Error Messages */}
      {saveSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Preferences saved successfully!
        </Alert>
      )}
      {saveError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {saveError}
        </Alert>
      )}
      
      {/* In-App Notifications */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <NotificationsIcon color="primary" />
          <Typography variant="h6">In-App Notifications</Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Receive notifications within the application
        </Typography>
        
        <FormGroup>
          {notificationTypes.map((type) => (
            <Box key={type.key} sx={{ mb: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={localPreferences.in_app[type.key] || false}
                    onChange={handleInAppChange(type.key)}
                  />
                }
                label={
                  <Box>
                    <Typography variant="body1">{type.label}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {type.description}
                    </Typography>
                  </Box>
                }
              />
            </Box>
          ))}
        </FormGroup>
      </Paper>
      
      {/* Email Notifications */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <EmailIcon color="primary" />
          <Typography variant="h6">Email Notifications</Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Receive notifications via email
        </Typography>
        
        {/* Email Enabled Toggle */}
        <FormControlLabel
          control={
            <Switch
              checked={localPreferences.settings.email_enabled || false}
              onChange={handleEmailEnabledChange}
            />
          }
          label={
            <Box>
              <Typography variant="body1">Enable Email Notifications</Typography>
              <Typography variant="caption" color="text.secondary">
                Turn on/off all email notifications
              </Typography>
            </Box>
          }
          sx={{ mb: 3 }}
        />
        
        <Divider sx={{ my: 3 }} />
        
        {/* Email Frequency */}
        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">Email Frequency</FormLabel>
          <RadioGroup
            value={localPreferences.settings.email_frequency || 'instant'}
            onChange={handleEmailFrequencyChange}
          >
            <FormControlLabel
              value="instant"
              control={<Radio />}
              label={
                <Box>
                  <Typography variant="body2">Instant</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Receive emails immediately
                  </Typography>
                </Box>
              }
              disabled={!localPreferences.settings.email_enabled}
            />
            <FormControlLabel
              value="daily"
              control={<Radio />}
              label={
                <Box>
                  <Typography variant="body2">Daily Digest</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Receive a daily summary
                  </Typography>
                </Box>
              }
              disabled={!localPreferences.settings.email_enabled}
            />
            <FormControlLabel
              value="weekly"
              control={<Radio />}
              label={
                <Box>
                  <Typography variant="body2">Weekly Digest</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Receive a weekly summary
                  </Typography>
                </Box>
              }
              disabled={!localPreferences.settings.email_enabled}
            />
          </RadioGroup>
        </FormControl>
        
        <Divider sx={{ my: 3 }} />
        
        {/* Email Notification Types */}
        <FormGroup>
          {notificationTypes.map((type) => (
            <Box key={type.key} sx={{ mb: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={localPreferences.email[type.key] || false}
                    onChange={handleEmailChange(type.key)}
                    disabled={!localPreferences.settings.email_enabled}
                  />
                }
                label={
                  <Box>
                    <Typography variant="body1">{type.label}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {type.description}
                    </Typography>
                  </Box>
                }
              />
            </Box>
          ))}
        </FormGroup>
      </Paper>
      
      {/* Save Button */}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
          onClick={handleSave}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </Button>
      </Box>
    </Container>
  );
}

