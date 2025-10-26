import { useEffect, useState } from 'react';
import { Upload, FileText, CheckCircle, Clock, XCircle, AlertCircle, Loader } from 'lucide-react';
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
      description: 'Government-issued ID (Passport, Driver License, National ID)',
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

    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a valid file (JPG, PNG, or PDF)');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    try {
      setUploadingType(type);
      const formData = new FormData();
      formData.append('file', file);

      await api.post(\`/kyc/documents/\${type}/upload\`, formData, {
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
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'rejected':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  const isFullyVerified = statistics?.approved === documentTypes.filter(dt => dt.required).length;

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loader className="w-8 h-8 text-purple-500 animate-spin" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Documents & Verification
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload your documents for account verification
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/20 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-400 rounded-lg">
          {error}
        </div>
      )}

      <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            Verification Status
          </h2>
          {isFullyVerified && (
            <span className="inline-flex items-center gap-2 px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm font-semibold">
              <CheckCircle className="w-4 h-4" />
              Fully Verified
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Required Documents</p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{statistics?.total || 0}</p>
          </div>
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Approved</p>
            <p className="text-3xl font-bold text-green-600 dark:text-green-400">{statistics?.approved || 0}</p>
          </div>
          <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Pending Review</p>
            <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{statistics?.pending || 0}</p>
          </div>
          <div className="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Rejected</p>
            <p className="text-3xl font-bold text-red-600 dark:text-red-400">{statistics?.rejected || 0}</p>
          </div>
        </div>

        {!isFullyVerified && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-sm font-semibold text-blue-900 dark:text-blue-200 mb-1">Action Required</p>
            <p className="text-sm text-blue-800 dark:text-blue-300">
              Please upload all required documents to complete your account verification.
            </p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {documentTypes.map((docType) => {
          const status = getDocumentStatus(docType.type);
          const docInfo = getDocumentInfo(docType.type);

          return (
            <div key={docType.type} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <FileText className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {docType.label}
                    {docType.required && <span className="text-red-500 ml-1">*</span>}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{docType.description}</p>
                </div>
              </div>

              {docInfo && docInfo.status !== 'not_uploaded' ? (
                <div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg mb-3">
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">{docInfo.name}</p>
                      {docInfo.uploaded_at && (
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          Uploaded: {new Date(docInfo.uploaded_at).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                    <span className={\`px-2 py-1 text-xs font-semibold rounded \${getStatusColor(docInfo.status)}\`}>
                      {docInfo.status}
                    </span>
                  </div>

                  {docInfo.notes && (
                    <div className={\`p-3 rounded-lg mb-3 \${
                      docInfo.status === 'rejected'
                        ? 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
                        : 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
                    }\`}>
                      <p className={\`text-sm \${
                        docInfo.status === 'rejected'
                          ? 'text-red-800 dark:text-red-300'
                          : 'text-blue-800 dark:text-blue-300'
                      }\`}>
                        <strong>Note:</strong> {docInfo.notes}
                      </p>
                    </div>
                  )}

                  {docInfo.status === 'rejected' && (
                    <label className={\`flex items-center justify-center gap-2 w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors cursor-pointer \${
                      uploadingType === docType.type ? 'opacity-50 cursor-not-allowed' : ''
                    }\`}>
                      {uploadingType === docType.type ? (
                        <>
                          <Loader className="w-5 h-5 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Upload className="w-5 h-5" />
                          Re-upload Document
                        </>
                      )}
                      <input
                        type="file"
                        accept="image/*,.pdf"
                        onChange={(e) => handleFileUpload(docType.type, e)}
                        disabled={uploadingType === docType.type}
                        className="hidden"
                      />
                    </label>
                  )}
                </div>
              ) : (
                <label className={\`flex items-center justify-center gap-2 w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors cursor-pointer \${
                  uploadingType === docType.type ? 'opacity-50 cursor-not-allowed' : ''
                }\`}>
                  {uploadingType === docType.type ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Upload className="w-5 h-5" />
                      Upload Document
                    </>
                  )}
                  <input
                    type="file"
                    accept="image/*,.pdf"
                    onChange={(e) => handleFileUpload(docType.type, e)}
                    disabled={uploadingType === docType.type}
                    className="hidden"
                  />
                </label>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
