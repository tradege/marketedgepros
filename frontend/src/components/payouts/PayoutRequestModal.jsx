import React, { useState, useEffect } from "react";
import {
  Modal,
  Button,
  Form,
  Alert,
  Spinner,
  Row,
  Col,
  InputGroup,
} from "react-bootstrap";
import { FaMoneyBillWave, FaInfoCircle } from "react-icons/fa";
import payoutService from "../../services/payoutService";

const PayoutRequestModal = ({ show, onHide, onSuccess, availableBalance }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [formData, setFormData] = useState({
    amount: "",
    payment_method: "bank_transfer",
    payment_details: "",
  });

  useEffect(() => {
    if (show) {
      checkEligibility();
    }
  }, [show]);

  const checkEligibility = async () => {
    try {
      setLoading(true);
      const response = await payoutService.checkEligibility();
      setEligibility(response);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to check eligibility");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const calculateProfitSplit = () => {
    const amount = parseFloat(formData.amount) || 0;
    const profitSplit = eligibility?.profit_split_percentage || 80;
    return (amount * profitSplit) / 100;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation
    const amount = parseFloat(formData.amount);
    if (!amount || amount <= 0) {
      setError("Please enter a valid amount");
      return;
    }

    if (amount > availableBalance) {
      setError("Amount exceeds available balance");
      return;
    }

    if (
      eligibility?.minimum_payout_amount &&
      amount < eligibility.minimum_payout_amount
    ) {
      setError(
        `Minimum payout amount is $${eligibility.minimum_payout_amount}`
      );
      return;
    }

    if (!formData.payment_details) {
      setError("Please provide payment details");
      return;
    }

    try {
      setLoading(true);
      await payoutService.requestPayout(formData);
      onSuccess();
      onHide();
      setFormData({
        amount: "",
        payment_method: "bank_transfer",
        payment_details: "",
      });
    } catch (err) {
      setError(err.message || "Failed to request payout");
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const getPaymentDetailsPlaceholder = () => {
    switch (formData.payment_method) {
      case "bank_transfer":
        return "IBAN or Account Number";
      case "paypal":
        return "PayPal Email";
      case "crypto":
        return "Wallet Address";
      default:
        return "Payment Details";
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>
          <FaMoneyBillWave className="me-2" />
          Request Payout
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {loading && !eligibility ? (
          <div className="text-center py-4">
            <Spinner animation="border" variant="primary" />
            <p className="mt-2">Checking eligibility...</p>
          </div>
        ) : !eligibility?.eligible ? (
          <Alert variant="warning">
            <FaInfoCircle className="me-2" />
            {eligibility?.message || "You are not eligible for payout yet"}
          </Alert>
        ) : (
          <Form onSubmit={handleSubmit}>
            {error && <Alert variant="danger">{error}</Alert>}

            {/* Eligibility Info */}
            <Alert variant="info">
              <Row>
                <Col md={6}>
                  <small className="text-muted">Available Balance</small>
                  <h5 className="mb-0">{formatCurrency(availableBalance)}</h5>
                </Col>
                <Col md={6}>
                  <small className="text-muted">Profit Split</small>
                  <h5 className="mb-0">{eligibility.profit_split_percentage}%</h5>
                </Col>
              </Row>
              {eligibility.minimum_payout_amount && (
                <div className="mt-2">
                  <small>
                    Minimum payout: {formatCurrency(eligibility.minimum_payout_amount)}
                  </small>
                </div>
              )}
            </Alert>

            {/* Amount */}
            <Form.Group className="mb-3">
              <Form.Label>Amount to Withdraw</Form.Label>
              <InputGroup>
                <InputGroup.Text>$</InputGroup.Text>
                <Form.Control
                  type="number"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  max={availableBalance}
                  required
                />
              </InputGroup>
              {formData.amount && (
                <Form.Text className="text-success">
                  You will receive: {formatCurrency(calculateProfitSplit())}
                </Form.Text>
              )}
            </Form.Group>

            {/* Payment Method */}
            <Form.Group className="mb-3">
              <Form.Label>Payment Method</Form.Label>
              <Form.Select
                name="payment_method"
                value={formData.payment_method}
                onChange={handleChange}
                required
              >
                <option value="bank_transfer">Bank Transfer</option>
                <option value="paypal">PayPal</option>
                <option value="crypto">Cryptocurrency</option>
              </Form.Select>
            </Form.Group>

            {/* Payment Details */}
            <Form.Group className="mb-3">
              <Form.Label>Payment Details</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="payment_details"
                value={formData.payment_details}
                onChange={handleChange}
                placeholder={getPaymentDetailsPlaceholder()}
                required
              />
              <Form.Text className="text-muted">
                Please provide accurate payment details to avoid delays
              </Form.Text>
            </Form.Group>

            {/* Submit Button */}
            <div className="d-grid gap-2">
              <Button
                variant="primary"
                type="submit"
                size="lg"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Spinner
                      as="span"
                      animation="border"
                      size="sm"
                      className="me-2"
                    />
                    Processing...
                  </>
                ) : (
                  <>Request Payout</>
                )}
              </Button>
            </div>
          </Form>
        )}
      </Modal.Body>
    </Modal>
  );
};

export default PayoutRequestModal;
