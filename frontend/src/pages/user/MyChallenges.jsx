import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { programsAPI } from '../../services/api';
import UserLayout from '../../components/mui/UserLayout';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import {
  TrendingUp,
  AccessTime,
  CheckCircle,
  Cancel,
  ArrowForward,
} from '@mui/icons-material';

export default function MyChallenges() {
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await programsAPI.getMyChallenges();
      setChallenges(response.data.challenges || []);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return '#43e97b';
      case 'passed':
        return '#4facfe';
      case 'failed':
        return '#fa709a';
      case 'pending':
        return '#f093fb';
      default:
        return '#667eea';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <AccessTime />;
      case 'passed':
        return <CheckCircle />;
      case 'failed':
        return <Cancel />;
      default:
        return <TrendingUp />;
    }
  };

  if (loading) {
    return (
      <UserLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <CircularProgress />
        </Box>
      </UserLayout>
    );
  }

  return (
    <UserLayout>
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" sx={{ color: 'white', fontWeight: 700 }}>
            My Challenges
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/programs')}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              '&:hover': {
                background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
              },
            }}
          >
            Browse Programs
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {challenges.length === 0 ? (
          <Card sx={{ bgcolor: '#1a1f2e', borderRadius: 3, textAlign: 'center', py: 8 }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.7)', mb: 2 }}>
                You don't have any challenges yet
              </Typography>
              <Button
                variant="contained"
                onClick={() => navigate('/programs')}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  mt: 2,
                }}
              >
                Start Your First Challenge
              </Button>
            </CardContent>
          </Card>
        ) : (
          <Grid container spacing={3}>
            {challenges.map((challenge) => (
              <Grid item xs={12} md={6} lg={4} key={challenge.id}>
                <Card
                  sx={{
                    bgcolor: '#1a1f2e',
                    borderRadius: 3,
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    },
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
                        {challenge.program_name || 'Challenge'}
                      </Typography>
                      <Chip
                        icon={getStatusIcon(challenge.status)}
                        label={challenge.status}
                        sx={{
                          bgcolor: getStatusColor(challenge.status),
                          color: 'white',
                          fontWeight: 600,
                          textTransform: 'capitalize',
                        }}
                      />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', mb: 1 }}>
                        Account Size: <strong style={{ color: 'white' }}>${challenge.account_size?.toLocaleString()}</strong>
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', mb: 1 }}>
                        Profit Target: <strong style={{ color: '#43e97b' }}>{challenge.profit_target}%</strong>
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)' }}>
                        Max Drawdown: <strong style={{ color: '#fa709a' }}>{challenge.max_drawdown}%</strong>
                      </Typography>
                    </Box>

                    <Button
                      fullWidth
                      variant="outlined"
                      endIcon={<ArrowForward />}
                      onClick={() => navigate(`/challenges/${challenge.id}`)}
                      sx={{
                        borderColor: '#667eea',
                        color: '#667eea',
                        '&:hover': {
                          borderColor: '#764ba2',
                          bgcolor: 'rgba(102, 126, 234, 0.1)',
                        },
                      }}
                    >
                      View Details
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </UserLayout>
  );
}

