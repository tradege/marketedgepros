import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { programsAPI, paymentsAPI } from '../services/api';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import {
  Check, X, TrendingUp, Shield, Zap, DollarSign, 
  ArrowLeft, CreditCard, Lock, AlertCircle, Bitcoin
} from 'lucide-react';
import Layout from '../components/layout/Layout';
import CryptoCheckout from '../components/CryptoCheckout';

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
      const purchaseResponse = await programsAPI.purchase(program.id, {
        addon_ids: selectedAddons.map(a => a.id)
      });

      const challengeId = purchaseResponse.data.challenge.id;
      const paymentResponse = await paymentsAPI.createPaymentIntent(challengeId);
      const { client_secret } = paymentResponse.data.payment;

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

      await paymentsAPI.confirmPayment(paymentIntent.id);
      onSuccess(challengeId);
    } catch (err) {
      setError(err.response?.data?.error || 'Payment failed. Please try again.');
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Card Details
        </label>
        <div className="p-4 bg-white/5 border border-white/10 rounded-lg">
          <CardElement
            options={{
              style: {
                base: {
                  fontSize: '16px',
                  color: '#ffffff',
                  '::placeholder': {
                    color: '#9ca3af',
                  },
                },
                invalid: {
                  color: '#ef4444',
                },
              },
            }}
          />
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
        <div className="flex justify-between items-center text-lg font-bold text-white">
          <span>Total:</span>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">${totalPrice.toLocaleString()}</span>
        </div>
      </div>

      <button
        type="submit"
        disabled={!stripe || isProcessing}
        className="w-full py-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Lock className="w-5 h-5" />
        {isProcessing ? 'Processing...' : `Pay $${totalPrice.toLocaleString()}`}
      </button>

      <p className="text-xs text-gray-400 text-center flex items-center justify-center gap-1">
        <Lock className="w-3 h-3" />
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
  const [paymentMethod, setPaymentMethod] = useState('crypto'); // 'stripe' or 'crypto'

  useEffect(() => {
    loadProgram();
  }, [id]);

  const loadProgram = async () => {
    try {
      const response = await programsAPI.getById(id);
      setProgram(response.data);
    } catch (error) {
    } finally {
      // Fallback to static programs if API fails
      const staticPrograms = [
        // One Phase
        { id: 1, name: "$10K One Phase", type: "one_phase", account_size: 10000, profit_target: 8, max_daily_loss: 5, max_total_loss: 10, profit_split: 80, price: 99, addons: [], description: "Perfect for beginners. One evaluation phase with 8% profit target." },
        { id: 2, name: "$25K One Phase", type: "one_phase", account_size: 25000, profit_target: 8, max_daily_loss: 5, max_total_loss: 10, profit_split: 80, price: 199, addons: [], description: "Intermediate traders. One evaluation phase with 8% profit target." },
        { id: 3, name: "$50K One Phase", type: "one_phase", account_size: 50000, profit_target: 8, max_daily_loss: 5, max_total_loss: 10, profit_split: 85, price: 299, addons: [], description: "Advanced traders. One evaluation phase with 8% profit target and 85% profit split." },
        { id: 4, name: "$100K One Phase", type: "one_phase", account_size: 100000, profit_target: 8, max_daily_loss: 5, max_total_loss: 10, profit_split: 90, price: 499, addons: [], description: "Professional traders. One evaluation phase with 8% profit target and 90% profit split." },
        // Two Phase
        { id: 5, name: "$10K Two Phase", type: "two_phase", account_size: 10000, profit_target: 10, max_daily_loss: 5, max_total_loss: 10, profit_split: 80, price: 79, addons: [], description: "Affordable entry. Two evaluation phases with 10% total profit target." },
        { id: 6, name: "$25K Two Phase", type: "two_phase", account_size: 25000, profit_target: 10, max_daily_loss: 5, max_total_loss: 10, profit_split: 80, price: 149, addons: [], description: "Popular choice. Two evaluation phases with 10% total profit target." },
        { id: 7, name: "$50K Two Phase", type: "two_phase", account_size: 50000, profit_target: 10, max_daily_loss: 5, max_total_loss: 10, profit_split: 85, price: 249, addons: [], description: "Serious traders. Two evaluation phases with 10% total profit target and 85% profit split." },
        { id: 8, name: "$100K Two Phase", type: "two_phase", account_size: 100000, profit_target: 10, max_daily_loss: 5, max_total_loss: 10, profit_split: 90, price: 399, addons: [], description: "Elite traders. Two evaluation phases with 10% total profit target and 90% profit split." },
        // Three Phase
        { id: 9, name: "$10K Three Phase", type: "three_phase", account_size: 10000, profit_target: 12, max_daily_loss: 4, max_total_loss: 8, profit_split: 75, price: 59, addons: [], description: "Budget-friendly. Three evaluation phases with 12% total profit target." },
        { id: 10, name: "$25K Three Phase", type: "three_phase", account_size: 25000, profit_target: 12, max_daily_loss: 4, max_total_loss: 8, profit_split: 75, price: 119, addons: [], description: "Extended evaluation. Three phases with 12% total profit target." },
        { id: 11, name: "$50K Three Phase", type: "three_phase", account_size: 50000, profit_target: 12, max_daily_loss: 4, max_total_loss: 8, profit_split: 80, price: 199, addons: [], description: "Comprehensive evaluation. Three phases with 12% total profit target and 80% profit split." },
        { id: 12, name: "$100K Three Phase", type: "three_phase", account_size: 100000, profit_target: 12, max_daily_loss: 4, max_total_loss: 8, profit_split: 85, price: 349, addons: [], description: "Premium evaluation. Three phases with 12% total profit target and 85% profit split." },
        // Instant Funding
        { id: 13, name: "$5K Instant Funding", type: "instant_funding", account_size: 5000, profit_target: 0, max_daily_loss: 3, max_total_loss: 6, profit_split: 50, price: 199, addons: [], description: "Start trading immediately with no evaluation required." },
        { id: 14, name: "$10K Instant Funding", type: "instant_funding", account_size: 10000, profit_target: 0, max_daily_loss: 3, max_total_loss: 6, profit_split: 50, price: 299, addons: [], description: "Instant access to funded account. No evaluation needed." },
        { id: 15, name: "$25K Instant Funding", type: "instant_funding", account_size: 25000, profit_target: 0, max_daily_loss: 3, max_total_loss: 6, profit_split: 60, price: 499, addons: [], description: "Immediate funding with 60% profit split. No evaluation required." },
        { id: 16, name: "$50K Instant Funding", type: "instant_funding", account_size: 50000, profit_target: 0, max_daily_loss: 3, max_total_loss: 6, profit_split: 70, price: 799, addons: [], description: "Premium instant funding with 70% profit split. Trade immediately." },
      ];
      
      const foundProgram = staticPrograms.find(p => p.id === parseInt(id));
      if (foundProgram) {
        setProgram(foundProgram);
      }
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
      <Layout>
        <div className="min-h-screen bg-black flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500"></div>
            <p className="text-gray-300 mt-4">Loading program...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!program) {
    return (
      <Layout>
        <div className="min-h-screen bg-black flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-white mb-2">Program not found</h2>
            <button 
              onClick={() => navigate('/programs')} 
              className="mt-4 px-6 py-3 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300"
            >
              Back to Programs
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  const totalPrice = program.price + selectedAddons.reduce((sum, addon) => sum + addon.price, 0);

  return (
    <Layout>
      <div className="min-h-screen bg-black">
        {/* Header */}
        <div className="border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <button
              onClick={() => navigate('/programs')}
              className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Programs
            </button>
            <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400 mb-4">
              {program.name}
            </h1>
            <p className="text-gray-300 text-lg">{program.description || 'Professional trading challenge'}</p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-6">
              {/* Program Details */}
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
                <h2 className="text-2xl font-bold text-white mb-6">Program Details</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
                      <DollarSign className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Account Size</p>
                      <p className="font-bold text-white text-lg">${program.account_size.toLocaleString()}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Profit Target</p>
                      <p className="font-bold text-cyan-400 text-lg">{program.profit_target}%</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
                      <Shield className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Max Daily Loss</p>
                      <p className="font-bold text-red-400 text-lg">{program.max_daily_loss}%</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
                      <Zap className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Profit Split</p>
                      <p className="font-bold text-cyan-400 text-lg">{program.profit_split}%</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Add-ons */}
              {program.addons && program.addons.length > 0 && (
                <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
                  <h2 className="text-2xl font-bold text-white mb-6">Available Add-ons</h2>
                  <div className="space-y-4">
                    {program.addons.map((addon) => {
                      const isSelected = selectedAddons.find(a => a.id === addon.id);
                      return (
                        <div
                          key={addon.id}
                          onClick={() => toggleAddon(addon)}
                          className={`p-5 border-2 rounded-xl cursor-pointer transition-all ${
                            isSelected
                              ? 'border-cyan-500 bg-cyan-500/10'
                              : 'border-white/10 hover:border-white/30 bg-white/5'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                              <div className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center ${
                                isSelected ? 'bg-cyan-500 border-cyan-500' : 'border-white/30'
                              }`}>
                                {isSelected && <Check className="w-4 h-4 text-white" />}
                              </div>
                              <div>
                                <h3 className="font-semibold text-white">{addon.name}</h3>
                                <p className="text-sm text-gray-400">{addon.description}</p>
                              </div>
                            </div>
                            <span className="font-bold text-cyan-400 text-lg">
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
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 sticky top-4">
                <h2 className="text-2xl font-bold text-white mb-6">
                  {showCheckout ? 'Checkout' : 'Order Summary'}
                </h2>

                {!showCheckout ? (
                  <>
                    <div className="space-y-4 mb-6">
                      <div className="flex justify-between text-gray-300">
                        <span>Program</span>
                        <span className="font-medium text-white">${program.price.toLocaleString()}</span>
                      </div>
                      {selectedAddons.map((addon) => (
                        <div key={addon.id} className="flex justify-between text-gray-400 text-sm">
                          <span>{addon.name}</span>
                          <span className="font-medium text-gray-300">+${addon.price.toLocaleString()}</span>
                        </div>
                      ))}
                      <div className="border-t border-white/10 pt-4 flex justify-between items-center">
                        <span className="text-lg font-bold text-white">Total</span>
                        <span className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-400">
                          ${totalPrice.toLocaleString()}
                        </span>
                      </div>
                    </div>

                    <button
                      onClick={() => setShowCheckout(true)}
                      className="w-full py-4 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 flex items-center justify-center gap-2"
                    >
                      <CreditCard className="w-5 h-5" />
                      Proceed to Checkout
                    </button>
                  </>
                ) : (
                  <div className="space-y-6">
                    {/* Payment Method Selector */}
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-3">
                        Select Payment Method
                      </label>
                      <div className="grid grid-cols-2 gap-3">
                        <button
                          onClick={() => setPaymentMethod('crypto')}
                          className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                            paymentMethod === 'crypto'
                              ? 'border-cyan-500 bg-cyan-500/10'
                              : 'border-white/10 bg-white/5 hover:border-white/30'
                          }`}
                        >
                          <Bitcoin className="w-6 h-6 mx-auto mb-2 text-cyan-400" />
                          <div className="text-sm font-medium text-white">USDT</div>
                          <div className="text-xs text-gray-400 mt-1">Crypto</div>
                        </button>
                        <button
                          onClick={() => setPaymentMethod('stripe')}
                          className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                            paymentMethod === 'stripe'
                              ? 'border-cyan-500 bg-cyan-500/10'
                              : 'border-white/10 bg-white/5 hover:border-white/30'
                          }`}
                        >
                          <CreditCard className="w-6 h-6 mx-auto mb-2 text-cyan-400" />
                          <div className="text-sm font-medium text-white">Card</div>
                          <div className="text-xs text-gray-400 mt-1">Stripe</div>
                        </button>
                      </div>
                    </div>

                    {/* Payment Form */}
                    {paymentMethod === 'crypto' ? (
                      <CryptoCheckout
                        program={program}
                        selectedAddons={selectedAddons}
                        onSuccess={handlePaymentSuccess}
                      />
                    ) : (
                      <Elements stripe={stripePromise}>
                        <CheckoutForm
                          program={program}
                          selectedAddons={selectedAddons}
                          onSuccess={handlePaymentSuccess}
                        />
                      </Elements>
                    )}
                  </div>
                )}

                {showCheckout && (
                  <button
                    onClick={() => setShowCheckout(false)}
                    className="w-full py-3 bg-white/5 border border-white/10 rounded-xl text-white font-medium hover:bg-white/10 transition-all duration-300 mt-4"
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

