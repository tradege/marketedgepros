import { useState, useEffect } from 'react';
import { Copy, CheckCircle, Clock, AlertCircle, Loader } from 'lucide-react';
import api from '../services/api';
import useAuthStore from '../store/authStore';

function CryptoCheckout({ program, selectedAddons, onSuccess }) {
  const { user } = useAuthStore();
  const [paymentData, setPaymentData] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [status, setStatus] = useState('pending');
  const [checkCount, setCheckCount] = useState(0);
  
  const totalPrice = program.price + selectedAddons.reduce((sum, addon) => sum + addon.price, 0);

  useEffect(() => {
    createPayment();
  }, []);

  useEffect(() => {
    if (paymentData && status === 'pending') {
      const MAX_CHECKS = 360; // 1 hour (360 * 10 seconds)
      const interval = setInterval(() => {
        setCheckCount(prev => {
          if (prev >= MAX_CHECKS) {
            clearInterval(interval);
            setStatus('expired');
            return prev;
          }
          checkPaymentStatus();
          return prev + 1;
        });
      }, 10000);

      return () => clearInterval(interval);
    }
  }, [paymentData, status]);

  const createPayment = async () => {
    setIsCreating(true);
    setError(null);

    try {
      const response = await api.post('/crypto/create-payment', {
        program_id: program.id,
        amount: totalPrice,
        email: user?.email || 'guest@marketedgepros.com'
      });

      if (response.data.success) {
        setPaymentData(response.data);
        setStatus('waiting');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create payment');
    } finally {
      setIsCreating(false);
    }
  };

  const checkPaymentStatus = async () => {
    if (!paymentData) return;

    try {
      const response = await api.get(`/crypto/payment-status/${paymentData.payment_id}`);
      
      if (response.data.success) {
        const newStatus = response.data.status;
        setStatus(newStatus);

        if (newStatus === 'finished') {
          onSuccess(paymentData.order_id);
        }
      }
    } catch (err) {
      console.error('Error checking payment status:', err);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isCreating) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <Loader className="w-12 h-12 text-cyan-400 animate-spin" />
        <p className="text-gray-300">Creating payment...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-500/10 border border-red-500/30 rounded-lg">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-300 mb-1">Payment Error</h3>
            <p className="text-sm text-red-300/80">{error}</p>
            <button
              onClick={createPayment}
              className="mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!paymentData) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-center gap-2 p-4 bg-white/5 border border-white/10 rounded-lg">
        {status === 'waiting' && (
          <>
            <Clock className="w-5 h-5 text-yellow-400 animate-pulse" />
            <span className="text-yellow-300 font-medium">Waiting for payment...</span>
          </>
        )}
        {status === 'finished' && (
          <>
            <CheckCircle className="w-5 h-5 text-green-400" />
            <span className="text-green-300 font-medium">Payment confirmed!</span>
          </>
        )}
        {status === 'failed' && (
          <>
            <AlertCircle className="w-5 h-5 text-red-400" />
            <span className="text-red-300 font-medium">Payment failed</span>
          </>
        )}
      </div>

      <div className="bg-gradient-to-br from-cyan-500/10 to-teal-500/10 border border-cyan-500/30 rounded-lg p-6 space-y-4">
        <h3 className="text-lg font-semibold text-white mb-4">Send USDT (TRC20)</h3>
        
        <div>
          <label className="block text-sm text-gray-400 mb-2">Amount to Send</label>
          <div className="flex items-center justify-between p-4 bg-black/30 rounded-lg">
            <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
              {paymentData.pay_amount} {paymentData.pay_currency?.toUpperCase()}
            </span>
            <button
              onClick={() => copyToClipboard(paymentData.pay_amount.toString())}
              className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            >
              {copied ? <CheckCircle className="w-5 h-5 text-green-400" /> : <Copy className="w-5 h-5 text-gray-400" />}
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-2">Send to Address</label>
          <div className="flex items-center gap-2 p-4 bg-black/30 rounded-lg">
            <code className="flex-1 text-sm text-cyan-300 break-all">{paymentData.pay_address}</code>
            <button
              onClick={() => copyToClipboard(paymentData.pay_address)}
              className="p-2 hover:bg-white/10 rounded-lg transition-colors flex-shrink-0"
            >
              {copied ? <CheckCircle className="w-5 h-5 text-green-400" /> : <Copy className="w-5 h-5 text-gray-400" />}
            </button>
          </div>
        </div>

        <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
          <h4 className="font-medium text-yellow-300 mb-2 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            Important Instructions
          </h4>
          <ul className="text-sm text-yellow-300/80 space-y-1 ml-6 list-disc">
            <li>Send only USDT on TRC20 network</li>
            <li>Send the exact amount shown above</li>
            <li>Payment will be confirmed automatically</li>
            <li>Do not close this page until payment is confirmed</li>
          </ul>
        </div>
      </div>

      <div className="text-center text-sm text-gray-500">
        Payment ID: {paymentData.payment_id}
      </div>
    </div>
  );
}

export default CryptoCheckout;
