import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { programsAPI, paymentsAPI } from '../services/api';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import {
  Check, X, TrendingUp, Shield, Zap, DollarSign, 
  ArrowLeft, CreditCard, Lock, AlertCircle
} from 'lucide-react';
import Layout from '../components/layout/Layout';

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY);

function CheckoutForm({ program, selectedAddons, onSuccess }) {
  const stripe = useStripe();
  const elements = useElements();
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  const totalPrice = program.price + selectedAddons.reduce((sum, addon) => sum + addon.price, 0);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      // 1. Purchase program (creates challenge)
      const purchaseResponse = await programsAPI.purchase(program.id, {
        addon_ids: selectedAddons.map(a => a.id)
      });

      const challengeId = purchaseResponse.data.challenge.id;

      // 2. Create payment intent
      const paymentResponse = await paymentsAPI.createPaymentIntent(challengeId);
      const { client_secret } = paymentResponse.data.payment;

      // 3. Confirm payment with Stripe
      const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(
        client_secret,
        {
          payment_method: {
            card: elements.getElement(CardElement),
          },
        }
      );

      if (stripeError) {
        setError(stripeError.message);
        setIsProcessing(false);
        return;
      }

      // 4. Confirm payment on backend
      await paymentsAPI.confirmPayment(paymentIntent.id);

      // Success!
      onSuccess(challengeId);
    } catch (err) {
      setError(err.response?.data?.error || 'Payment failed. Please try again.');
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Card Details
        </label>
        <div className="p-4 border border-gray-300 rounded-lg">
          <CardElement
            options={{
              style: {
                base: {
                  fontSize: '16px',
                  color: '#424770',
                  '::placeholder': {
                    color: '#aab7c4',
                  },
                },
                invalid: {
                  color: '#9e2146',
                },
              },
            }}
          />
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="flex justify-between items-center text-lg font-bold">
          <span>Total:</span>
          <span>${totalPrice.toLocaleString()}</span>
        </div>
      </div>

      <button
        type="submit"
        disabled={!stripe || isProcessing}
        className="btn btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
      >
        <Lock className="w-5 h-5" />
        {isProcessing ? 'Processing...' : `Pay $${totalPrice.toLocaleString()}`}
      </button>

      <p className="text-xs text-gray-500 text-center">
        <Lock className="w-3 h-3 inline mr-1" />
        Secure payment powered by Stripe
      </p>
    </form>
  );
}

export default function ProgramDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [program, setProgram] = useState(null);
  const [selectedAddons, setSelectedAddons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCheckout, setShowCheckout] = useState(false);

  useEffect(() => {
    loadProgram();
  }, [id]);

  const loadProgram = async () => {
    try {
      const response = await programsAPI.getById(id);
      setProgram(response.data);
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  const toggleAddon = (addon) => {
    setSelectedAddons(prev => {
      const exists = prev.find(a => a.id === addon.id);
      if (exists) {
        return prev.filter(a => a.id !== addon.id);
      } else {
        return [...prev, addon];
      }
    });
  };

  const handlePaymentSuccess = (challengeId) => {
    navigate(`/challenges/${challengeId}?success=true`);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-600 mt-4">Loading program...</p>
        </div>
      </div>
    );
  }

  if (!program) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Program not found</h2>
          <button onClick={() => navigate('/programs')} className="btn btn-primary mt-4">
            Back to Programs
          </button>
        </div>
      </div>
    );
  }

  const totalPrice = program.price + selectedAddons.reduce((sum, addon) => sum + addon.price, 0);

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <button
            onClick={() => navigate('/programs')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Programs
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{program.name}</h1>
          <p className="text-gray-600 mt-2">{program.description || 'Professional trading challenge'}</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Program Details */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Program Details</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <DollarSign className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Account Size</p>
                    <p className="font-bold text-gray-900">${program.account_size.toLocaleString()}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Profit Target</p>
                    <p className="font-bold text-gray-900">{program.profit_target}%</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                    <Shield className="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Max Daily Loss</p>
                    <p className="font-bold text-gray-900">{program.max_daily_loss}%</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <Zap className="w-5 h-5 text-yellow-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Profit Split</p>
                    <p className="font-bold text-gray-900">{program.profit_split}%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Add-ons */}
            {program.addons && program.addons.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Available Add-ons</h2>
                <div className="space-y-3">
                  {program.addons.map((addon) => {
                    const isSelected = selectedAddons.find(a => a.id === addon.id);
                    return (
                      <div
                        key={addon.id}
                        onClick={() => toggleAddon(addon)}
                        className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                          isSelected
                            ? 'border-primary-500 bg-primary-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                              isSelected ? 'bg-primary-600 border-primary-600' : 'border-gray-300'
                            }`}>
                              {isSelected && <Check className="w-4 h-4 text-white" />}
                            </div>
                            <div>
                              <h3 className="font-medium text-gray-900">{addon.name}</h3>
                              <p className="text-sm text-gray-600">{addon.description}</p>
                            </div>
                          </div>
                          <span className="font-bold text-gray-900">
                            +${addon.price.toLocaleString()}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar - Checkout */}
          <div className="lg:col-span-1">
            <div className="card sticky top-4">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                {showCheckout ? 'Checkout' : 'Order Summary'}
              </h2>

              {!showCheckout ? (
                <>
                  <div className="space-y-3 mb-6">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Program</span>
                      <span className="font-medium">${program.price.toLocaleString()}</span>
                    </div>
                    {selectedAddons.map((addon) => (
                      <div key={addon.id} className="flex justify-between">
                        <span className="text-gray-600 text-sm">{addon.name}</span>
                        <span className="font-medium text-sm">+${addon.price.toLocaleString()}</span>
                      </div>
                    ))}
                    <div className="border-t pt-3 flex justify-between items-center">
                      <span className="text-lg font-bold">Total</span>
                      <span className="text-2xl font-bold text-primary-600">
                        ${totalPrice.toLocaleString()}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() => setShowCheckout(true)}
                    className="btn btn-primary w-full flex items-center justify-center gap-2"
                  >
                    <CreditCard className="w-5 h-5" />
                    Proceed to Checkout
                  </button>
                </>
              ) : (
                <Elements stripe={stripePromise}>
                  <CheckoutForm
                    program={program}
                    selectedAddons={selectedAddons}
                    onSuccess={handlePaymentSuccess}
                  />
                </Elements>
              )}

              {showCheckout && (
                <button
                  onClick={() => setShowCheckout(false)}
                  className="btn btn-secondary w-full mt-3"
                >
                  Back to Summary
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
    </Layout>
  );
}

