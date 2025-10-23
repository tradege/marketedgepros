import { useState, useEffect, lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './store/authStore';
import Notification from './components/Notification';
import ChatWidget from './components/ChatWidget';
import { ADMIN_ROLES } from './constants/roles';

// Auth Pages (Lazy Loaded)
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const VerifyEmail = lazy(() => import('./pages/VerifyEmail'));
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'));
const ResetPassword = lazy(() => import('./pages/ResetPassword'));

// Public Pages (Lazy Loaded)
const HomePage = lazy(() => import('./pages/NewHomePage'));
const Programs = lazy(() => import('./pages/ProgramsNew'));
const ProgramDetails = lazy(() => import('./pages/ProgramDetails'));

const AboutUs = lazy(() => import('./pages/AboutUs'));
const HowItWorks = lazy(() => import('./pages/HowItWorks'));
const FAQ = lazy(() => import('./pages/FAQ'));
const Contact = lazy(() => import('./pages/Contact'));
const TermsOfService = lazy(() => import('./pages/TermsOfService'));
const PrivacyPolicy = lazy(() => import('./pages/PrivacyPolicy'));
const RiskDisclosure = lazy(() => import('./pages/RiskDisclosure'));

// Shared Pages (Lazy Loaded)
const Dashboard = lazy(() => import('./pages/Dashboard_mui'));
import RoleBasedDashboard from './components/RoleBasedDashboard';
const KYC = lazy(() => import('./pages/KYC'));
const Profile = lazy(() => import('./pages/user/Profile_mui'));
const MyChallenges = lazy(() => import('./pages/user/MyChallenges'));
const ChallengeDetails = lazy(() => import('./pages/ChallengeDetails'));

// Admin Pages (Lazy Loaded)
const AdminLayout = lazy(() => import('./components/mui/AdminLayout'));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboardConnected'));
const UserManagement = lazy(() => import('./pages/admin/UserManagementConnected'));
const ProgramsManagement = lazy(() => import('./pages/admin/ProgramsManagement_mui'));
const PaymentsManagement = lazy(() => import('./pages/admin/PaymentsManagementConnected'));
const KYCApproval = lazy(() => import('./pages/admin/KYCApprovalConnected'));
const PaymentApprovals = lazy(() => import('./pages/admin/PaymentApprovals'));
const Settings = lazy(() => import('./pages/admin/Settings_mui'));

// Agent Pages (Lazy Loaded)
const AgentDashboard = lazy(() => import('./pages/agent/AgentDashboard'));
const TradersManagement = lazy(() => import('./pages/agent/TradersManagement'));
const Commissions = lazy(() => import('./pages/agent/Commissions'));
const Reports = lazy(() => import('./pages/agent/Reports'));

// Trader Pages (Lazy Loaded)
const TraderDashboard = lazy(() => import('./pages/user/UserDashboard_mui'));
const TradingHistory = lazy(() => import('./pages/trader/TradingHistory'));
const Withdrawals = lazy(() => import('./pages/trader/Withdrawals'));
const Documents = lazy(() => import('./pages/user/Documents'));

// Guards
import RoleGuard from './components/guards/RoleGuard';

// Protected Route Component
function ProtectedRoute({ children, adminOnly = false, userOnly = false }) {
  const { isAuthenticated, isLoading, user } = useAuthStore();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-600 mt-4">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check if admin trying to access user-only pages
  const isAdmin = user && ADMIN_ROLES.includes(user.role);
  
  if (userOnly && isAdmin) {
    return <Navigate to="/admin" replace />;
  }

  return children;
}

// Public Route Component (redirect if already logged in)
function PublicRoute({ children }) {
  const { isAuthenticated, isLoading, user } = useAuthStore();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-600 mt-4">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated && user) {
    // Redirect based on user role
    if (ADMIN_ROLES.includes(user.role)) {
      return <Navigate to="/admin" replace />;
    }
    
    if (user.role === 'agent') {
      return <Navigate to="/agent" replace />;
    }
    
    // Regular users go to home
    return <Navigate to="/" replace />;
  }

  return children;
}

function App() {
  const { init } = useAuthStore();

  useEffect(() => {
    init();
  }, [init]);

  return (
    <BrowserRouter>
      <Notification />
      <ChatWidget />
      <Suspense fallback={
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <p className="text-gray-300 mt-4">Loading...</p>
          </div>
        </div>
      }>
        <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/programs" element={<Programs />} />

        <Route path="/programs/:id" element={<ProgramDetails />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/terms-of-service" element={<TermsOfService />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/risk-disclosure" element={<RiskDisclosure />} />

        {/* Auth Routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        {/* Shared Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <RoleBasedDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/kyc"
          element={
            <ProtectedRoute>
              <KYC />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute userOnly={true}>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/challenges"
          element={
            <ProtectedRoute userOnly={true}>
              <MyChallenges />
            </ProtectedRoute>
          }
        />
        <Route
          path="/challenges/:id"
          element={
            <ProtectedRoute userOnly={true}>
              <ChallengeDetails />
            </ProtectedRoute>
          }
        />
        <Route
          path="/documents"
          element={
            <ProtectedRoute userOnly={true}>
              <Documents />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute userOnly={true}>
              <Profile />
            </ProtectedRoute>
          }
        />

        {/* Admin Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <AdminDashboard />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <UserManagement />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/programs"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <ProgramsManagement />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/payments"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <PaymentsManagement />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/kyc"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <KYCApproval />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/payment-approvals"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster']}>
                <AdminLayout>
                  <PaymentApprovals />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/settings"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['supermaster', 'super_admin', 'admin', 'master']}>
                <AdminLayout>
                  <Settings />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />

        {/* Agent Routes */}
        <Route
          path="/agent"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <AgentDashboard />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/traders"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <TradersManagement />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/commissions"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <Commissions />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/reports"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <Reports />
              </RoleGuard>
            </ProtectedRoute>
          }
        />

        {/* Trader Routes */}
        <Route
          path="/trader"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <TraderDashboard />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/history"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <TradingHistory />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/withdrawals"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <Withdrawals />
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/documents"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <Documents />
              </RoleGuard>
            </ProtectedRoute>
          }
        />

        {/* 404 */}
        <Route
          path="*"
          element={
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
              <div className="text-center">
                <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
                <p className="text-xl text-gray-600 mb-8">Page not found</p>
                <a href="/" className="btn btn-primary">
                  Go to Home
                </a>
              </div>
            </div>
          }
        />
      </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default App;

