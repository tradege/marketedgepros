import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';
import LineChartComponent from '../../components/charts/LineChartComponent';
import BarChartComponent from '../../components/charts/BarChartComponent';
import PieChartComponent from '../../components/charts/PieChartComponent';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const AnalyticsDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState(30);
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        `${API_BASE_URL}/analytics/comprehensive?days=${timeRange}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setAnalyticsData(response.data.data);
    } catch (err) {
      setError('Failed to load analytics data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTimeRangeChange = (event) => {
    setTimeRange(event.target.value);
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!analyticsData) {
    return null;
  }

  // Prepare data for charts
  const revenueData = analyticsData.revenue_over_time || [];
  const userGrowthData = analyticsData.user_growth || [];
  const challengeStats = analyticsData.challenge_statistics || {};
  const kycStats = analyticsData.kyc_statistics || {};
  const referralStats = analyticsData.referral_statistics || {};
  const paymentStats = analyticsData.payment_statistics || {};

  // Transform challenge status distribution for pie chart
  const challengeStatusData = (challengeStats.status_distribution || []).map(item => ({
    name: item.status.charAt(0).toUpperCase() + item.status.slice(1),
    value: item.count
  }));

  // Transform KYC distribution for pie chart
  const kycDistributionData = (kycStats.distribution || []).map(item => ({
    name: item.status.charAt(0).toUpperCase() + item.status.slice(1).replace('_', ' '),
    value: item.count
  }));

  // Transform payment method distribution for bar chart
  const paymentMethodData = (paymentStats.method_distribution || []).map(item => ({
    name: item.method.charAt(0).toUpperCase() + item.method.slice(1),
    count: item.count,
    amount: item.total_amount
  }));

  return (
    
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Analytics Dashboard
        </Typography>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Time Range</InputLabel>
          <Select
            value={timeRange}
            label="Time Range"
            onChange={handleTimeRangeChange}
          >
            <MenuItem value={7}>Last 7 days</MenuItem>
            <MenuItem value={30}>Last 30 days</MenuItem>
            <MenuItem value={90}>Last 90 days</MenuItem>
            <MenuItem value={180}>Last 6 months</MenuItem>
            <MenuItem value={365}>Last year</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {/* Revenue Over Time */}
        <Grid item xs={12} lg={6}>
          <LineChartComponent
            data={revenueData}
            title="Revenue Over Time"
            dataKeys={[
              { key: 'revenue', name: 'Revenue ($)' },
              { key: 'transactions', name: 'Transactions' }
            ]}
            colors={['#00C49F', '#8884D8']}
            height={350}
            yAxisLabel="Amount ($)"
          />
        </Grid>

        {/* User Growth */}
        <Grid item xs={12} lg={6}>
          <LineChartComponent
            data={userGrowthData}
            title="User Growth"
            dataKeys={[
              { key: 'registrations', name: 'New Users' },
              { key: 'cumulative', name: 'Total Users' }
            ]}
            colors={['#0088FE', '#FFBB28']}
            height={350}
            yAxisLabel="Users"
          />
        </Grid>

        {/* Challenge Status Distribution */}
        <Grid item xs={12} md={6} lg={4}>
          <PieChartComponent
            data={challengeStatusData}
            title="Challenge Status Distribution"
            dataKey="value"
            nameKey="name"
            height={300}
          />
        </Grid>

        {/* KYC Status Distribution */}
        <Grid item xs={12} md={6} lg={4}>
          <PieChartComponent
            data={kycDistributionData}
            title="KYC Status Distribution"
            dataKey="value"
            nameKey="name"
            height={300}
          />
        </Grid>

        {/* Payment Methods */}
        <Grid item xs={12} md={12} lg={4}>
          <BarChartComponent
            data={paymentMethodData}
            title="Payment Methods"
            dataKeys={[
              { key: 'count', name: 'Transactions' }
            ]}
            colors={['#8884D8']}
            height={300}
            xAxisKey="name"
            layout="vertical"
          />
        </Grid>

        {/* Challenge Daily Statistics */}
        {challengeStats.daily_data && challengeStats.daily_data.length > 0 && (
          <Grid item xs={12}>
            <LineChartComponent
              data={challengeStats.daily_data}
              title="Challenge Activity"
              dataKeys={[
                { key: 'created', name: 'Created' },
                { key: 'completed', name: 'Completed' },
                { key: 'funded', name: 'Funded' }
              ]}
              colors={['#8884D8', '#00C49F', '#FFBB28']}
              height={350}
              yAxisLabel="Challenges"
            />
          </Grid>
        )}

        {/* Top Performing Agents */}
        {referralStats.top_agents && referralStats.top_agents.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Top Performing Agents
              </Typography>
              <Box sx={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid #ddd' }}>
                      <th style={{ padding: '12px', textAlign: 'left' }}>Name</th>
                      <th style={{ padding: '12px', textAlign: 'left' }}>Email</th>
                      <th style={{ padding: '12px', textAlign: 'right' }}>Referrals</th>
                      <th style={{ padding: '12px', textAlign: 'right' }}>Total Commission</th>
                    </tr>
                  </thead>
                  <tbody>
                    {referralStats.top_agents.map((agent, index) => (
                      <tr key={agent.agent_id} style={{ borderBottom: '1px solid #eee' }}>
                        <td style={{ padding: '12px' }}>{agent.name}</td>
                        <td style={{ padding: '12px' }}>{agent.email}</td>
                        <td style={{ padding: '12px', textAlign: 'right' }}>{agent.referrals}</td>
                        <td style={{ padding: '12px', textAlign: 'right' }}>
                          ${agent.total_commission.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Box>
            </Paper>
          </Grid>
        )}

        {/* Referral Statistics Summary */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Referral Statistics
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                Total Referrals
              </Typography>
              <Typography variant="h4">
                {referralStats.total_referrals || 0}
              </Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                Active Referrals
              </Typography>
              <Typography variant="h4">
                {referralStats.active_referrals || 0}
              </Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                Conversion Rate
              </Typography>
              <Typography variant="h4">
                {referralStats.conversion_rate || 0}%
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Payment Statistics Summary */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Payment Status Distribution
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mt: 2 }}>
              {(paymentStats.status_distribution || []).map((item) => (
                <Box key={item.status} sx={{ minWidth: 150 }}>
                  <Typography variant="body2" color="textSecondary">
                    {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                  </Typography>
                  <Typography variant="h4">
                    {item.count}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
      </Container>
    
  );
};

export default AnalyticsDashboard;

