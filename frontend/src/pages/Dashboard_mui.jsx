import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import LinearProgress from '@mui/material/LinearProgress';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import {
  TrendingUp,
  AttachMoney,
  EmojiEvents,
  CheckCircle,
  Schedule,
  Error,
  ArrowForward,
  Refresh,
} from '@mui/icons-material';
import UserLayout from '../components/mui/UserLayout';
import useAuthStore from '../store/authStore';
import { programsAPI } from '../services/api';

export default function Dashboard() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState({
    totalChallenges: 0,
    activeChallenges: 0,
    passedChallenges: 0,
    totalProfit: 0,
  });

  useEffect(() => {
    loadChallenges();
  }, []);

  const loadChallenges = async () => {
    try {
      const response = await programsAPI.getMyChallenges();
      const challengesData = response.data.challenges || [];
      setChallenges(challengesData);
      
      // Calculate stats
      setStats({
        totalChallenges: challengesData.length,
        activeChallenges: challengesData.filter(c => c.status === 'active').length,
        passedChallenges: challengesData.filter(c => c.status === 'passed').length,
        totalProfit: challengesData.reduce((sum, c) => sum + (c.profit || 0), 0),
      });
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'passed':
        return 'info';
      case 'failed':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
      case 'passed':
        return <CheckCircle />;
      case 'failed':
        return <Error />;
      case 'pending':
        return <Schedule />;
      default:
        return <Schedule />;
    }
  };

  const statsCards = [
    {
      title: 'Total Challenges',
      value: stats.totalChallenges,
      icon: <TrendingUp />,
      color: '#667eea',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      title: 'Active Challenges',
      value: stats.activeChallenges,
      icon: <EmojiEvents />,
      color: '#43e97b',
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    },
    {
      title: 'Passed Challenges',
      value: stats.passedChallenges,
      icon: <CheckCircle />,
      color: '#4facfe',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    },
    {
      title: 'Total Profit',
      value: `$${stats.totalProfit.toLocaleString()}`,
      icon: <AttachMoney />,
      color: '#fa709a',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
  ];

  return (
    <UserLayout>
      <Container maxWidth="xl">
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" sx={{ color: 'white', fontWeight: 700, mb: 1 }}>
            Welcome back, {user?.full_name || user?.email}!
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.6)' }}>
            Here's your trading overview
          </Typography>
        </Box>

        {/* Stats Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {statsCards.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  bgcolor: '#1a1f2e',
                  borderRadius: 3,
                  border: '1px solid rgba(255,255,255,0.1)',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: `0 12px 24px ${stat.color}40`,
                    borderColor: stat.color,
                  },
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        borderRadius: 2,
                        background: stat.gradient,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                      }}
                    >
                      {stat.icon}
                    </Box>
                  </Box>
                  <Typography variant="h4" sx={{ color: 'white', fontWeight: 700, mb: 0.5 }}>
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)' }}>
                    {stat.title}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Quick Actions */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6}>
            <Card
              sx={{
                bgcolor: '#1a1f2e',
                borderRadius: 3,
                border: '1px solid rgba(102, 126, 234, 0.3)',
                background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
              }}
            >
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h6" sx={{ color: 'white', fontWeight: 700, mb: 2 }}>
                  Start a New Challenge
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', mb: 3 }}>
                  Choose from our trading programs and start your journey to get funded
                </Typography>
                <Button
                  variant="contained"
                  endIcon={<ArrowForward />}
                  onClick={() => navigate('/programs')}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                >
                  Browse Programs
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card
              sx={{
                bgcolor: '#1a1f2e',
                borderRadius: 3,
                border: '1px solid rgba(67, 233, 123, 0.3)',
                background: 'linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%)',
              }}
            >
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h6" sx={{ color: 'white', fontWeight: 700, mb: 2 }}>
                  Complete Your Profile
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', mb: 3 }}>
                  Update your information and complete KYC verification
                </Typography>
                <Button
                  variant="contained"
                  endIcon={<ArrowForward />}
                  onClick={() => navigate('/profile')}
                  sx={{
                    background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                >
                  Go to Profile
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* My Challenges */}
        <Card
          sx={{
            bgcolor: '#1a1f2e',
            borderRadius: 3,
            border: '1px solid rgba(255,255,255,0.1)',
          }}
        >
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h6" sx={{ color: 'white', fontWeight: 700 }}>
                My Challenges
              </Typography>
              <IconButton onClick={loadChallenges} sx={{ color: 'rgba(255,255,255,0.6)' }}>
                <Refresh />
              </IconButton>
            </Box>

            {isLoading ? (
              <Box sx={{ py: 4 }}>
                <LinearProgress sx={{ bgcolor: 'rgba(255,255,255,0.1)' }} />
              </Box>
            ) : challenges.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 6 }}>
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.6)', mb: 2 }}>
                  You don't have any challenges yet
                </Typography>
                <Button
                  variant="contained"
                  onClick={() => navigate('/programs')}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                  }}
                >
                  Start Your First Challenge
                </Button>
              </Box>
            ) : (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.02)' }}>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }}>
                        Program
                      </TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }}>
                        Account Size
                      </TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }}>
                        Status
                      </TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }}>
                        Progress
                      </TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }}>
                        Profit
                      </TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 600 }} align="right">
                        Actions
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {challenges.map((challenge) => (
                      <TableRow
                        key={challenge.id}
                        sx={{
                          '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                        }}
                      >
                        <TableCell sx={{ color: 'white', fontWeight: 600 }}>
                          {challenge.program_name}
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.8)' }}>
                          ${challenge.account_size?.toLocaleString()}
                        </TableCell>
                        <TableCell>
                          <Chip
                            icon={getStatusIcon(challenge.status)}
                            label={challenge.status}
                            color={getStatusColor(challenge.status)}
                            size="small"
                            sx={{ textTransform: 'capitalize' }}
                          />
                        </TableCell>
                        <TableCell>
                          <Box sx={{ width: 100 }}>
                            <LinearProgress
                              variant="determinate"
                              value={challenge.progress || 0}
                              sx={{
                                height: 8,
                                borderRadius: 4,
                                bgcolor: 'rgba(255,255,255,0.1)',
                              }}
                            />
                          </Box>
                        </TableCell>
                        <TableCell
                          sx={{
                            color: challenge.profit >= 0 ? '#43e97b' : '#ff6b6b',
                            fontWeight: 600,
                          }}
                        >
                          ${challenge.profit?.toLocaleString() || 0}
                        </TableCell>
                        <TableCell align="right">
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => navigate(`/challenges/${challenge.id}`)}
                            sx={{
                              borderColor: '#667eea',
                              color: '#667eea',
                              '&:hover': {
                                borderColor: '#667eea',
                                bgcolor: 'rgba(102, 126, 234, 0.1)',
                              },
                            }}
                          >
                            View Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      </Container>
    </UserLayout>
  );
}

