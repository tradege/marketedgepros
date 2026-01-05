import React, { useState, useEffect } from "react";
import Swal from 'sweetalert2';
import {
  Container,
  Row,
  Col,
  Card,
  Table,
  Button,
  Badge,
  Alert,
  Spinner,
  Form,
  InputGroup,
  Modal,
} from "react-bootstrap";
import {
  FaMoneyBillWave,
  FaCheck,
  FaTimes,
  FaEye,
  FaSearch,
  FaFilter,
} from "react-icons/fa";
import payoutService from "../../services/payoutService";

const PayoutManagement = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [payouts, setPayouts] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [selectedPayout, setSelectedPayout] = useState(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectReason, setRejectReason] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("pending");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [payoutsData, statsData] = await Promise.all([
        payoutService.admin.getPendingPayouts(),
        payoutService.admin.getAllStatistics(),
      ]);

      setPayouts(payoutsData.payouts || []);
      setStatistics(statsData);
    } catch (err) {
      setError(err.message || "Failed to load payouts");
    } finally {
      setLoading(false);
    }
  };

  const handleApprovePayout = async (payoutId) => {
    const result = await Swal.fire({
      title: "Approve Payout?",
      text: "Are you sure you want to approve this payout?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#10b981",
      cancelButtonColor: "#6b7280",
      confirmButtonText: "Yes, approve!",
      cancelButtonText: "Cancel"
    });
    
    if (!result.isConfirmed) return;

    try {
      setActionLoading(true);
      await payoutService.admin.approvePayout(payoutId);
      setSuccess("Payout approved successfully");
      loadData();
      setShowDetailsModal(false);
    } catch (err) {
      setError(err.message || "Failed to approve payout");
    } finally {
      setActionLoading(false);
    }
  };

  const handleRejectPayout = async () => {
    if (!rejectReason.trim()) {
      setError("Please provide a rejection reason");
      return;
    }

    try {
      setActionLoading(true);
      await payoutService.admin.rejectPayout(
        selectedPayout.id,
        rejectReason
      );
      setSuccess("Payout rejected");
      setRejectReason("");
      setShowRejectModal(false);
      setShowDetailsModal(false);
      loadData();
    } catch (err) {
      setError(err.message || "Failed to reject payout");
    } finally {
      setActionLoading(false);
    }
  };

  const handleMarkAsPaid = async (payoutId) => {
    const result = await Swal.fire({
      title: "Mark as Paid?",
      text: "Confirm that this payout has been completed.",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#10b981",
      cancelButtonColor: "#6b7280",
      confirmButtonText: "Yes, mark as paid!",
      cancelButtonText: "Cancel"
    });
    
    if (!result.isConfirmed) return;

    try {
      setActionLoading(true);
      await payoutService.admin.markAsPaid(payoutId);
      setSuccess("Payout marked as paid");
      loadData();
      setShowDetailsModal(false);
    } catch (err) {
      setError(err.message || "Failed to mark as paid");
    } finally {
      setActionLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount || 0);
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getStatusBadge = (status) => {
    const config = {
      pending: { variant: "warning", text: "Pending" },
      approved: { variant: "info", text: "Approved" },
      paid: { variant: "success", text: "Paid" },
      rejected: { variant: "danger", text: "Rejected" },
    };
    const c = config[status] || { variant: "secondary", text: status };
    return <Badge bg={c.variant}>{c.text}</Badge>;
  };

  const filteredPayouts = payouts.filter((p) => {
    const matchesSearch =
      searchTerm === "" ||
      p.user_id.toString().includes(searchTerm) ||
      p.id.toString().includes(searchTerm);
    const matchesStatus =
      statusFilter === "all" || p.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-3">Loading payouts...</p>
      </Container>
    );
  }

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h2>
            <FaMoneyBillWave className="me-2" />
            Payout Management
          </h2>
        </Col>
      </Row>

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert variant="success" dismissible onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Statistics */}
      {statistics && (
        <Row className="mb-4">
          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <small className="text-muted">Total Payouts</small>
                <h4>{statistics.total_payouts || 0}</h4>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <small className="text-muted">Pending</small>
                <h4 className="text-warning">{statistics.pending_payouts || 0}</h4>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <small className="text-muted">Total Amount</small>
                <h4 className="text-primary">
                  {formatCurrency(statistics.total_amount)}
                </h4>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <small className="text-muted">Paid Out</small>
                <h4 className="text-success">
                  {formatCurrency(statistics.total_paid)}
                </h4>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Filters */}
      <Card className="mb-3">
        <Card.Body>
          <Row>
            <Col md={6}>
              <InputGroup>
                <InputGroup.Text>
                  <FaSearch />
                </InputGroup.Text>
                <Form.Control
                  placeholder="Search by ID or User ID..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </InputGroup>
            </Col>
            <Col md={3}>
              <InputGroup>
                <InputGroup.Text>
                  <FaFilter />
                </InputGroup.Text>
                <Form.Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="paid">Paid</option>
                  <option value="rejected">Rejected</option>
                </Form.Select>
              </InputGroup>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Payouts Table */}
      <Card>
        <Card.Body>
          <Table responsive hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>Amount</th>
                <th>Profit Split</th>
                <th>Method</th>
                <th>Status</th>
                <th>Requested</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayouts.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-4">
                    No payouts found
                  </td>
                </tr>
              ) : (
                filteredPayouts.map((payout) => (
                  <tr key={payout.id}>
                    <td>#{payout.id}</td>
                    <td>{payout.user_id}</td>
                    <td>{formatCurrency(payout.amount)}</td>
                    <td className="text-primary">
                      {formatCurrency(payout.profit_split_amount)}
                    </td>
                    <td className="text-capitalize">{payout.payment_method}</td>
                    <td>{getStatusBadge(payout.status)}</td>
                    <td>{formatDate(payout.request_date)}</td>
                    <td>
                      <Button
                        size="sm"
                        variant="outline-primary"
                        className="me-1"
                        onClick={() => {
                          setSelectedPayout(payout);
                          setShowDetailsModal(true);
                        }}
                      >
                        <FaEye />
                      </Button>
                      {payout.status === "pending" && (
                        <>
                          <Button
                            size="sm"
                            variant="outline-success"
                            className="me-1"
                            onClick={() => handleApprovePayout(payout.id)}
                            disabled={actionLoading}
                          >
                            <FaCheck />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline-danger"
                            onClick={() => {
                              setSelectedPayout(payout);
                              setShowRejectModal(true);
                            }}
                            disabled={actionLoading}
                          >
                            <FaTimes />
                          </Button>
                        </>
                      )}
                      {payout.status === "approved" && (
                        <Button
                          size="sm"
                          variant="success"
                          onClick={() => handleMarkAsPaid(payout.id)}
                          disabled={actionLoading}
                        >
                          Mark Paid
                        </Button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Details Modal */}
      <Modal
        show={showDetailsModal}
        onHide={() => setShowDetailsModal(false)}
        size="lg"
      >
        <Modal.Header closeButton>
          <Modal.Title>Payout Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedPayout && (
            <div>
              <Row className="mb-3">
                <Col md={6}>
                  <strong>Payout ID:</strong> #{selectedPayout.id}
                </Col>
                <Col md={6}>
                  <strong>Status:</strong> {getStatusBadge(selectedPayout.status)}
                </Col>
              </Row>
              <Row className="mb-3">
                <Col md={6}>
                  <strong>User ID:</strong> {selectedPayout.user_id}
                </Col>
                <Col md={6}>
                  <strong>Program ID:</strong> {selectedPayout.program_id}
                </Col>
              </Row>
              <Row className="mb-3">
                <Col md={6}>
                  <strong>Amount:</strong> {formatCurrency(selectedPayout.amount)}
                </Col>
                <Col md={6}>
                  <strong>Profit Split:</strong>{" "}
                  {formatCurrency(selectedPayout.profit_split_amount)}
                </Col>
              </Row>
              <Row className="mb-3">
                <Col md={6}>
                  <strong>Payment Method:</strong>{" "}
                  <span className="text-capitalize">
                    {selectedPayout.payment_method}
                  </span>
                </Col>
                <Col md={6}>
                  <strong>Requested:</strong> {formatDate(selectedPayout.request_date)}
                </Col>
              </Row>
              <Row className="mb-3">
                <Col>
                  <strong>Payment Details:</strong>
                  <pre className="bg-light p-2 mt-1">
                    {selectedPayout.payment_details}
                  </pre>
                </Col>
              </Row>
              {selectedPayout.notes && (
                <Row className="mb-3">
                  <Col>
                    <strong>Notes:</strong>
                    <p>{selectedPayout.notes}</p>
                  </Col>
                </Row>
              )}
              {selectedPayout.rejection_reason && (
                <Row className="mb-3">
                  <Col>
                    <Alert variant="danger">
                      <strong>Rejection Reason:</strong>
                      <p className="mb-0">{selectedPayout.rejection_reason}</p>
                    </Alert>
                  </Col>
                </Row>
              )}
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDetailsModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Reject Modal */}
      <Modal show={showRejectModal} onHide={() => setShowRejectModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Reject Payout</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group>
            <Form.Label>Rejection Reason</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              placeholder="Enter reason for rejection..."
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowRejectModal(false)}>
            Cancel
          </Button>
          <Button
            variant="danger"
            onClick={handleRejectPayout}
            disabled={actionLoading || !rejectReason.trim()}
          >
            {actionLoading ? "Rejecting..." : "Reject Payout"}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default PayoutManagement;
