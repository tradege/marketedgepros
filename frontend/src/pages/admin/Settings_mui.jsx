import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Save } from '@mui/icons-material';

export default function Settings() {
  return (
    <Box>
      <Box mb={4}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>Settings</Typography>
        <Typography variant="body1" color="text.secondary">Configure platform settings and preferences</Typography>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>General Settings</Typography>
              <Box display="flex" flexDirection="column" gap={2} mt={2}>
                <TextField label="Platform Name" defaultValue="MarketEdgePros" fullWidth />
                <TextField label="Support Email" defaultValue="support@marketedgepros.com" fullWidth />
                <TextField label="Contact Phone" defaultValue="+1 (555) 123-4567" fullWidth />
                <FormControlLabel control={<Switch defaultChecked />} label="Enable User Registration" />
                <FormControlLabel control={<Switch defaultChecked />} label="Enable Email Notifications" />
                <Button variant="contained" startIcon={<Save />} sx={{ mt: 2 }}>Save Changes</Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>Payment Settings</Typography>
              <Box display="flex" flexDirection="column" gap={2} mt={2}>
                <TextField label="Stripe API Key" type="password" defaultValue="sk_test_..." fullWidth />
                <TextField label="PayPal Client ID" type="password" defaultValue="..." fullWidth />
                <TextField label="Minimum Payout" defaultValue="100" type="number" fullWidth />
                <FormControlLabel control={<Switch defaultChecked />} label="Enable Stripe" />
                <FormControlLabel control={<Switch />} label="Enable PayPal" />
                <Button variant="contained" startIcon={<Save />} sx={{ mt: 2 }}>Save Changes</Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
