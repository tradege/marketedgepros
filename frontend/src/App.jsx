import { useState, useEffect, lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './store/authStore';
import Notification from './components/Notification';
import ChatWidget from './components/ChatWidget';
import { ADMIN_ROLES } from './constants/roles';
import { ToastProvider } from './contexts/ToastContext';

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
const FreeCourse = lazy(() => import('./pages/FreeCourse'));
const LightningChallenge = lazy(() => import('./pages/LightningChallenge'));
const SupportHub = lazy(() => import('./pages/SupportHub'));
const Blog = lazy(() => import('./pages/Blog'));
const TermsOfService = lazy(() => import('./pages/TermsOfService'));
const PrivacyPolicy = lazy(() => import('./pages/PrivacyPolicy'));
const RiskDisclosure = lazy(() => import('./pages/RiskDisclosure'));

// Shared Pages (Lazy Loaded)
const Dashboard = lazy(() => import('./pages/Dashboard'));
import RoleBasedDashboard from './components/RoleBasedDashboard';
const KYC = lazy(() => import('./pages/KYC'));
const Profile = lazy(() => import('./pages/user/Profile'));
const MyChallenges = lazy(() => import('./pages/user/MyChallenges'));
const ChallengeDetails = lazy(() => import('./pages/ChallengeDetails'));

// Admin Pages (Lazy Loaded)
const AdminLayout = lazy(() => import('./components/admin/AdminLayout'));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboardConnected'));
const AnalyticsDashboard = lazy(() => import('./pages/admin/AnalyticsDashboard'));
const UserManagement = lazy(() => import('./pages/admin/UserManagementConnected'));
const ProgramsManagement = lazy(() => import('./pages/admin/ProgramsManagement'));
const PaymentsManagement = lazy(() => import('./pages/admin/PaymentsManagementConnected'));
const KYCApproval = lazy(() => import('./pages/admin/KYCApprovalConnected'));
const PaymentApprovals = lazy(() => import('./pages/admin/PaymentApprovals'));
const Settings = lazy(() => import('./pages/admin/Settings'));
const WithdrawalManagement = lazy(() => import('./pages/admin/WithdrawalManagement'));

// Notification Pages (Lazy Loaded)
const Notifications = lazy(() => import('./pages/Notifications'));
const NotificationSettings = lazy(() => import('./pages/settings/NotificationSettings'));

// Agent Pages (Lazy Loaded)
const AgentLayout = lazy(() => import('./components/agent/AgentLayout'));
const AgentDashboard = lazy(() => import('./pages/agent/AgentDashboard'));
const TradersManagement = lazy(() => import('./pages/agent/TradersManagement'));
const Commissions = lazy(() => import('./pages/agent/Commissions'));
const Reports = lazy(() => import('./pages/agent/Reports'));

// Trader Pages (Lazy Loaded)
const TraderLayout = lazy(() => import('./components/trader/TraderLayout'));
const TraderDashboard = lazy(() => import('./pages/user/UserDashboard'));
const TradingHistory = lazy(() => import('./pages/trader/TradingHistory'));
const Withdrawals = lazy(() => import('./pages/trader/Withdrawals'));
const Documents = lazy(() => import('./pages/user/Documents'));
const Wallet = lazy(() => import('./pages/user/Wallet'));
const UserLayout = lazy(() => import('./components/layout/UserLayout'));

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
    
    if (user.role === 'trader') {
      return <Navigate to="/trader" replace />;
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
    <ToastProvider>
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
        <Route path="/free-course" element={<FreeCourse />} />
        <Route path="/lightning-challenge" element={<LightningChallenge />} />
        <Route path="/support" element={<SupportHub />} />
        <Route path="/blog" element={<Blog />} />
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
              <UserLayout>
                <RoleBasedDashboard />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/kyc"
          element={
            <ProtectedRoute>
              <UserLayout>
                <KYC />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <Profile />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/challenges"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <MyChallenges />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/challenges/:id"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <ChallengeDetails />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/documents"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <Documents />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/wallet"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <Wallet />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute userOnly={true}>
              <UserLayout>
                <Profile />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/notifications"
          element={
            <ProtectedRoute>
              <UserLayout>
                <Notifications />
              </UserLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings/notifications"
          element={
            <ProtectedRoute>
              <UserLayout>
                <NotificationSettings />
              </UserLayout>
            </ProtectedRoute>
          }
        />

        {/* Admin Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
                <AdminLayout>
                  <AdminDashboard />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/analytics"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
                <AdminLayout>
                  <AnalyticsDashboard />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
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
              <RoleGuard allowedRoles={ADMIN_ROLES}>
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
              <RoleGuard allowedRoles={ADMIN_ROLES}>
                <AdminLayout>
                  <PaymentsManagement />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/kyc-approval"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
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
              <RoleGuard allowedRoles={ADMIN_ROLES}>
                <AdminLayout>
                  <PaymentApprovals />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/withdrawals"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
                <AdminLayout>
                  <WithdrawalManagement />
                </AdminLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/settings"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={ADMIN_ROLES}>
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
                <AgentLayout>
                  <AgentDashboard />
                </AgentLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/traders"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <AgentLayout>
                  <TradersManagement />
                </AgentLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/commissions"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <AgentLayout>
                  <Commissions />
                </AgentLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/agent/reports"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['agent']}>
                <AgentLayout>
                  <Reports />
                </AgentLayout>
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
                <TraderLayout>
                  <TraderDashboard />
                </TraderLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/history"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <TraderLayout>
                  <TradingHistory />
                </TraderLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/withdrawals"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <TraderLayout>
                  <Withdrawals />
                </TraderLayout>
              </RoleGuard>
            </ProtectedRoute>
          }
        />
        <Route
          path="/trader/documents"
          element={
            <ProtectedRoute>
              <RoleGuard allowedRoles={['trader']}>
                <TraderLayout>
                  <Documents />
                </TraderLayout>
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
    </ToastProvider>
  );
}

export default App;

