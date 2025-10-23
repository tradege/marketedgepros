import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import LinearProgress from '@mui/material/LinearProgress';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import { TrendingUp, AttachMoney, EmojiEvents, Schedule } from '@mui/icons-material';
import StatsCard from '../../components/mui/StatsCard';
import api from '../../services/api';

export default function UserDashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/users/dashboard');
      setDashboardData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      </Box>
    );
  }

  if (!dashboardData) {
    return null;
  }

  const { user, statistics, recent_challenges } = dashboardData;

  const userStats = [
    { 
      title: 'Active Challenges', 
      value: statistics.active_challenges.toString(), 
      subtitle: 'In progress', 
      icon: Schedule, 
      color: 'primary' 
    },
    { 
      title: 'Total Profit', 
      value: `$${statistics.total_profit.toLocaleString()}`, 
      subtitle: `${statistics.funded_challenges} funded account${statistics.funded_challenges !== 1 ? 's' : ''}`, 
      icon: AttachMoney, 
      color: 'success',
      trend: statistics.total_profit > 0 ? `+${statistics.total_profit}` : '0'
    },
    { 
      title: 'Success Rate', 
      value: `${statistics.success_rate}%`, 
      subtitle: `${statistics.passed_challenges} passed / ${statistics.failed_challenges} failed`, 
      icon: TrendingUp, 
      color: 'info' 
    },
    { 
      title: 'Funded Accounts', 
      value: statistics.funded_challenges.toString(), 
      subtitle: statistics.funded_challenges > 0 ? 'Congratulations!' : 'Keep trading!', 
      icon: EmojiEvents, 
      color: 'warning' 
    },
  ];

  const calculateProgress = (challenge) => {
    if (!challenge.initial_balance || !challenge.current_balance) return 0;
    const profit = challenge.profit;
    // Assuming 8% profit target for calculation (can be adjusted based on program rules)
    const target = challenge.initial_balance * 0.08;
    const progress = (profit / target) * 100;
    return Math.min(Math.max(progress, 0), 100);
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'primary',
      passed: 'success',
      failed: 'error',
      funded: 'warning',
      pending: 'info',
    };
    return colors[status] || 'default';
  };

  return (
    <Box>
      <Box mb={4}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          Welcome back, {user.first_name}! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's your trading overview
        </Typography>
      </Box>

      <Grid container spacing={3} mb={4}>
        {userStats.map((stat, i) => (
          <Grid item xs={12} sm={6} lg={3} key={i}>
            <StatsCard {...stat} />
          </Grid>
        ))}
      </Grid>

      <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, mb: 3 }}>
        Recent Challenges
      </Typography>

      {recent_challenges.length === 0 ? (
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center" py={4}>
              No challenges yet. Purchase a program to start your trading journey!
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {recent_challenges.map((challenge) => (
            <Grid item xs={12} md={6} key={challenge.id}>
              <Card>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      {challenge.program_name}
                    </Typography>
                    <Chip
                      label={challenge.status.toUpperCase()}
                      size="small"
                      color={getStatusColor(challenge.status)}
                      sx={{
                        fontWeight: 600,
                      }}
                    />
                  </Box>

                  <Box mb={3}>
                    <Box display="flex" justifyContent="space-between" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Progress
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {Math.round(calculateProgress(challenge))}%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={calculateProgress(challenge)}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        backgroundColor: 'rgba(103, 126, 234, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        },
                      }}
                    />
                  </Box>

                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Current Balance
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600, color: 'info.main' }}>
                        ${challenge.current_balance.toLocaleString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Profit/Loss
                      </Typography>
                      <Typography 
                        variant="h6" 
                        sx={{ 
                          fontWeight: 600, 
                          color: challenge.profit >= 0 ? 'success.main' : 'error.main' 
                        }}
                      >
                        ${challenge.profit.toLocaleString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Phase
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {challenge.phase || 'N/A'}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Started
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {challenge.created_at ? new Date(challenge.created_at).toLocaleDateString() : 'N/A'}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

