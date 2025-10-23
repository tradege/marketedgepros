import { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import InputAdornment from '@mui/material/InputAdornment';
import {
  Add,
  Edit,
  Delete,
  Visibility,
  TrendingUp,
  Speed,
  EmojiEvents,
} from '@mui/icons-material';

const programs = [
  {
    id: 1,
    name: 'Two Phase $100K',
    type: 'two_phase',
    accountSize: 100000,
    profitSplit: 80,
    phase1Target: 8,
    phase2Target: 5,
    maxDailyLoss: 5,
    maxTotalLoss: 10,
    price: 299,
    enrolledTraders: 234,
    status: 'active',
  },
  {
    id: 2,
    name: 'One Phase $50K',
    type: 'one_phase',
    accountSize: 50000,
    profitSplit: 75,
    phase1Target: 10,
    maxDailyLoss: 5,
    maxTotalLoss: 10,
    price: 199,
    enrolledTraders: 189,
    status: 'active',
  },
  {
    id: 3,
    name: 'Instant Funding $200K',
    type: 'instant',
    accountSize: 200000,
    profitSplit: 90,
    maxDailyLoss: 3,
    maxTotalLoss: 6,
    price: 499,
    enrolledTraders: 67,
    status: 'active',
  },
];

const programTypeConfig = {
  two_phase: {
    label: 'Two Phase',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    color: '#667eea',
    icon: TrendingUp,
  },
  one_phase: {
    label: 'One Phase',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    color: '#4facfe',
    icon: Speed,
  },
  instant: {
    label: 'Instant Funding',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    color: '#fa709a',
    icon: EmojiEvents,
  },
};

export default function ProgramsManagement() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    type: 'two_phase',
    accountSize: 100000,
    profitSplit: 80,
    price: 299,
  });

  const handleOpenDialog = (program = null) => {
    if (program) {
      setSelectedProgram(program);
      setFormData(program);
    } else {
      setSelectedProgram(null);
      setFormData({
        name: '',
        type: 'two_phase',
        accountSize: 100000,
        profitSplit: 80,
        price: 299,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedProgram(null);
  };

  const handleSave = () => {
    handleCloseDialog();
  };

  const handleDelete = (program) => {
    if (window.confirm(`Are you sure you want to delete ${program.name}?`)) {
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            Programs Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Create and manage trading programs
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          sx={{
            background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #38f9d7 0%, #43e97b 100%)',
            },
          }}
        >
          Add Program
        </Button>
      </Box>

      {/* Programs Grid */}
      <Grid container spacing={3}>
        {programs.map((program) => {
          const config = programTypeConfig[program.type];
          const Icon = config.icon;
          
          return (
            <Grid item xs={12} md={6} lg={4} key={program.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: 8,
                  },
                }}
              >
                {/* Card Header */}
                <Box
                  sx={{
                    background: config.gradient,
                    p: 3,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                  }}
                >
                  <Box
                    sx={{
                      width: 56,
                      height: 56,
                      borderRadius: 2,
                      backgroundColor: 'rgba(255,255,255,0.2)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Icon sx={{ fontSize: 32, color: 'white' }} />
                  </Box>
                  <Box flex={1}>
                    <Chip
                      label={config.label}
                      size="small"
                      sx={{
                        backgroundColor: 'rgba(255,255,255,0.3)',
                        color: 'white',
                        fontWeight: 600,
                        mb: 1,
                      }}
                    />
                    <Typography variant="h6" sx={{ color: 'white', fontWeight: 700 }}>
                      {program.name}
                    </Typography>
                  </Box>
                </Box>

                {/* Card Content */}
                <CardContent sx={{ flex: 1 }}>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Account Size
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        ${(program.accountSize / 1000).toFixed(0)}K
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Profit Split
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                        {program.profitSplit}%
                      </Typography>
                    </Grid>
                    {program.phase1Target && (
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Phase 1 Target
                        </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {program.phase1Target}%
                        </Typography>
                      </Grid>
                    )}
                    {program.phase2Target && (
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Phase 2 Target
                        </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {program.phase2Target}%
                        </Typography>
                      </Grid>
                    )}
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Max Daily Loss
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600, color: 'error.main' }}>
                        {program.maxDailyLoss}%
                        </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Max Total Loss
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600, color: 'error.main' }}>
                        {program.maxTotalLoss}%
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Box
                        sx={{
                          mt: 2,
                          p: 2,
                          borderRadius: 2,
                          backgroundColor: 'background.default',
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                        }}
                      >
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            Price
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: config.color }}>
                            ${program.price}
                          </Typography>
                        </Box>
                        <Box textAlign="right">
                          <Typography variant="body2" color="text.secondary">
                            Enrolled
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {program.enrolledTraders}
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>

                {/* Card Actions */}
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button
                    size="small"
                    startIcon={<Visibility />}
                  >
                    View
                  </Button>
                  <Button
                    size="small"
                    startIcon={<Edit />}
                    onClick={() => handleOpenDialog(program)}
                    color="primary"
                  >
                    Edit
                  </Button>
                  <Button
                    size="small"
                    startIcon={<Delete />}
                    onClick={() => handleDelete(program)}
                    color="error"
                  >
                    Delete
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Add/Edit Program Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedProgram ? 'Edit Program' : 'Add New Program'}
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <TextField
              label="Program Name"
              fullWidth
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              label="Type"
              select
              fullWidth
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            >
              <MenuItem value="two_phase">Two Phase</MenuItem>
              <MenuItem value="one_phase">One Phase</MenuItem>
              <MenuItem value="instant">Instant Funding</MenuItem>
            </TextField>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Account Size"
                  type="number"
                  fullWidth
                  value={formData.accountSize}
                  onChange={(e) => setFormData({ ...formData, accountSize: parseInt(e.target.value) })}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">$</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Profit Split"
                  type="number"
                  fullWidth
                  value={formData.profitSplit}
                  onChange={(e) => setFormData({ ...formData, profitSplit: parseInt(e.target.value) })}
                  InputProps={{
                    endAdornment: <InputAdornment position="end">%</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Price"
                  type="number"
                  fullWidth
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: parseInt(e.target.value) })}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">$</InputAdornment>,
                  }}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            sx={{
              background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            }}
          >
            {selectedProgram ? 'Save Changes' : 'Create Program'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

