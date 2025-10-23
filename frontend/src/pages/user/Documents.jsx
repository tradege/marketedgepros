import { useEffect, useState } from 'react';
import { Upload, FileText, CheckCircle, Clock, XCircle, AlertCircle } from 'lucide-react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import LinearProgress from '@mui/material/LinearProgress';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import api from '../../services/api';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [overallStatus, setOverallStatus] = useState('not_submitted');
  const [isLoading, setIsLoading] = useState(true);
  const [uploadingType, setUploadingType] = useState(null);
  const [error, setError] = useState(null);

  const documentTypes = [
    {
      type: 'id_proof',
      label: 'ID Proof',
      description: 'Government-issued ID (Passport, Driver\'s License, National ID)',
      required: true,
    },
    {
      type: 'address_proof',
      label: 'Address Proof',
      description: 'Utility bill, bank statement (not older than 3 months)',
      required: true,
    },
    {
      type: 'selfie',
      label: 'Selfie with ID',
      description: 'Clear photo of yourself holding your ID',
      required: true,
    },
    {
      type: 'bank_statement',
      label: 'Bank Statement',
      description: 'Recent bank statement for withdrawal verification',
      required: false,
    },
  ];

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.get('/kyc/documents');
      setDocuments(response.data.documents || []);
      setStatistics(response.data.statistics || {});
      setOverallStatus(response.data.overall_status || 'not_submitted');
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to load documents');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (type, event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a valid file (JPG, PNG, or PDF)');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    try {
      setUploadingType(type);
      const formData = new FormData();
      formData.append('file', file);

      await api.post(`/kyc/documents/${type}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      await loadDocuments();
      setError(null);
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to upload document. Please try again.');
    } finally {
      setUploadingType(null);
    }
  };

  const getDocumentStatus = (type) => {
    const doc = documents.find(d => d.type === type);
    return doc ? doc.status : 'not_uploaded';
  };

  const getDocumentInfo = (type) => {
    return documents.find(d => d.type === type);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved':
        return 'success';
      case 'pending':
        return 'warning';
      case 'rejected':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case 'rejected':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
    }
  };

  const isFullyVerified = statistics?.approved === documentTypes.filter(dt => dt.required).length;

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          Documents & Verification
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload your documents for account verification
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Verification Status */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Verification Status
            </Typography>
            {isFullyVerified && (
              <Chip
                icon={<CheckCircle />}
                label="Fully Verified"
                color="success"
                sx={{ fontWeight: 600 }}
              />
            )}
          </Box>

          <Grid container spacing={2} mb={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center" p={2} bgcolor="grey.50" borderRadius={2}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Required Documents
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {statistics?.total || 0}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center" p={2} bgcolor="success.50" borderRadius={2}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Approved
                </Typography>
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 700 }}>
                  {statistics?.approved || 0}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center" p={2} bgcolor="warning.50" borderRadius={2}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Pending Review
                </Typography>
                <Typography variant="h4" color="warning.main" sx={{ fontWeight: 700 }}>
                  {statistics?.pending || 0}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center" p={2} bgcolor="error.50" borderRadius={2}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Rejected
                </Typography>
                <Typography variant="h4" color="error.main" sx={{ fontWeight: 700 }}>
                  {statistics?.rejected || 0}
                </Typography>
              </Box>
            </Grid>
          </Grid>

          {!isFullyVerified && (
            <Alert severity="info">
              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                Action Required
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5 }}>
                Please upload all required documents to complete your account verification. 
                This is necessary for withdrawals and funded account access.
              </Typography>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Document Upload Cards */}
      <Grid container spacing={3}>
        {documentTypes.map((docType) => {
          const status = getDocumentStatus(docType.type);
          const docInfo = getDocumentInfo(docType.type);

          return (
            <Grid item xs={12} md={6} key={docType.type}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="start" gap={2} mb={3}>
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        bgcolor: 'primary.50',
                        borderRadius: 2,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                      }}
                    >
                      <FileText className="w-6 h-6 text-primary-600" />
                    </Box>
                    <Box flex={1}>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {docType.label}
                        {docType.required && (
                          <span style={{ color: 'red', marginLeft: 4 }}>*</span>
                        )}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                        {docType.description}
                      </Typography>
                    </Box>
                  </Box>

                  {docInfo && docInfo.status !== 'not_uploaded' ? (
                    <Box>
                      <Box
                        display="flex"
                        justifyContent="space-between"
                        alignItems="center"
                        p={2}
                        bgcolor="grey.50"
                        borderRadius={2}
                        mb={2}
                      >
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 500 }}>
                            {docInfo.name}
                          </Typography>
                          {docInfo.uploaded_at && (
                            <Typography variant="caption" color="text.secondary">
                              Uploaded: {new Date(docInfo.uploaded_at).toLocaleDateString()}
                            </Typography>
                          )}
                        </Box>
                        <Chip
                          label={docInfo.status}
                          color={getStatusColor(docInfo.status)}
                          size="small"
                          sx={{ fontWeight: 600 }}
                        />
                      </Box>

                      {docInfo.notes && (
                        <Alert 
                          severity={docInfo.status === 'rejected' ? 'error' : 'info'}
                          sx={{ mb: 2 }}
                        >
                          <Typography variant="body2">
                            <strong>Note:</strong> {docInfo.notes}
                          </Typography>
                        </Alert>
                      )}

                      {docInfo.status === 'rejected' && (
                        <Button
                          variant="contained"
                          component="label"
                          fullWidth
                          startIcon={<Upload />}
                          disabled={uploadingType === docType.type}
                        >
                          {uploadingType === docType.type ? 'Uploading...' : 'Re-upload Document'}
                          <input
                            type="file"
                            accept="image/*,.pdf"
                            onChange={(e) => handleFileUpload(docType.type, e)}
                            hidden
                          />
                        </Button>
                      )}
                    </Box>
                  ) : (
                    <Button
                      variant="contained"
                      component="label"
                      fullWidth
                      startIcon={<Upload />}
                      disabled={uploadingType === docType.type}
                    >
                      {uploadingType === docType.type ? 'Uploading...' : 'Upload Document'}
                      <input
                        type="file"
                        accept="image/*,.pdf"
                        onChange={(e) => handleFileUpload(docType.type, e)}
                        hidden
                      />
                    </Button>
                  )}
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
}

