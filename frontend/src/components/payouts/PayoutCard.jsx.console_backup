import React from "react";
import { Card, Badge, Row, Col } from "react-bootstrap";
import { FaMoneyBillWave, FaCalendar, FaCreditCard } from "react-icons/fa";

const PayoutCard = ({ payout }) => {
  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { variant: "warning", text: "Pending" },
      approved: { variant: "info", text: "Approved" },
      paid: { variant: "success", text: "Paid" },
      rejected: { variant: "danger", text: "Rejected" },
      processing: { variant: "primary", text: "Processing" },
    };

    const config = statusConfig[status] || { variant: "secondary", text: status };
    return <Badge bg={config.variant}>{config.text}</Badge>;
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  return (
    <Card className="mb-3 shadow-sm hover-shadow">
      <Card.Body>
        <Row className="align-items-center">
          <Col md={3}>
            <div className="d-flex align-items-center">
              <FaMoneyBillWave className="text-success me-2" size={24} />
              <div>
                <small className="text-muted">Amount</small>
                <h5 className="mb-0">{formatCurrency(payout.amount)}</h5>
              </div>
            </div>
          </Col>

          <Col md={3}>
            <div className="d-flex align-items-center">
              <FaMoneyBillWave className="text-primary me-2" size={20} />
              <div>
                <small className="text-muted">You Receive</small>
                <h6 className="mb-0 text-primary">
                  {formatCurrency(payout.profit_split_amount)}
                </h6>
              </div>
            </div>
          </Col>

          <Col md={2}>
            <div className="d-flex align-items-center">
              <FaCreditCard className="text-info me-2" size={20} />
              <div>
                <small className="text-muted">Method</small>
                <div className="text-capitalize">{payout.payment_method}</div>
              </div>
            </div>
          </Col>

          <Col md={2}>
            <div className="d-flex align-items-center">
              <FaCalendar className="text-secondary me-2" size={18} />
              <div>
                <small className="text-muted">Requested</small>
                <div>{formatDate(payout.request_date)}</div>
              </div>
            </div>
          </Col>

          <Col md={2} className="text-end">
            {getStatusBadge(payout.status)}
            {payout.status === "paid" && payout.paid_date && (
              <div className="mt-1">
                <small className="text-muted">
                  Paid: {formatDate(payout.paid_date)}
                </small>
              </div>
            )}
            {payout.status === "rejected" && payout.rejection_reason && (
              <div className="mt-1">
                <small className="text-danger">{payout.rejection_reason}</small>
              </div>
            )}
          </Col>
        </Row>

        {payout.notes && (
          <Row className="mt-2">
            <Col>
              <small className="text-muted">
                <strong>Notes:</strong> {payout.notes}
              </small>
            </Col>
          </Row>
        )}
      </Card.Body>
    </Card>
  );
};

export default PayoutCard;
