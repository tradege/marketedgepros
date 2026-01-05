import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Alert,
  Spinner,
  Badge,
  Tab,
  Tabs,
} from "react-bootstrap";
import {
  FaMoneyBillWave,
  FaChartLine,
  FaHistory,
  FaPlus,
} from "react-icons/fa";
import PayoutCard from "../../components/payouts/PayoutCard";
import PayoutRequestModal from "../../components/payouts/PayoutRequestModal";
import payoutService from "../../services/payoutService";

const Payouts = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [payouts, setPayouts] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [activeTab, setActiveTab] = useState("all");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [payoutsData, statsData] = await Promise.all([
        payoutService.getMyPayouts(),
        payoutService.getMyStatistics(),
      ]);

      setPayouts(payoutsData.payouts || []);
      setStatistics(statsData);
    } catch (err) {
      setError(err.message || "Failed to load payouts");
    } finally {
      setLoading(false);
    }
  };

  const handleRequestSuccess = () => {
    loadData();
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount || 0);
  };

  const filterPayouts = (status) => {
    if (status === "all") return payouts;
    return payouts.filter((p) => p.status === status);
  };

  const getFilteredPayouts = () => {
    return filterPayouts(activeTab);
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-3">Loading payouts...</p>
      </Container>
    );
  }

  return (
    <Container className="py-4">
      {/* Header */}
      <Row className="mb-4">
        <Col>
          <h2>
            <FaMoneyBillWave className="me-2" />
            Payouts
          </h2>
          <p className="text-muted">
            Request and manage your trading profit withdrawals
          </p>
        </Col>
        <Col xs="auto">
          <Button
            variant="primary"
            size="lg"
            onClick={() => setShowRequestModal(true)}
          >
            <FaPlus className="me-2" />
            Request Payout
          </Button>
        </Col>
      </Row>

      {error && <Alert variant="danger">{error}</Alert>}

      {/* Statistics Cards */}
      {statistics && (
        <Row className="mb-4">
          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <small className="text-muted">Available Balance</small>
                    <h4 className="mb-0 text-success">
                      {formatCurrency(statistics.available_balance)}
                    </h4>
                  </div>
                  <FaMoneyBillWave size={32} className="text-success" />
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <small className="text-muted">Total Withdrawn</small>
                    <h4 className="mb-0 text-primary">
                      {formatCurrency(statistics.total_withdrawn)}
                    </h4>
                  </div>
                  <FaChartLine size={32} className="text-primary" />
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <small className="text-muted">Total Payouts</small>
                    <h4 className="mb-0">{statistics.payout_count || 0}</h4>
                  </div>
                  <FaHistory size={32} className="text-info" />
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <small className="text-muted">Pending</small>
                    <h4 className="mb-0 text-warning">
                      {statistics.pending_count || 0}
                    </h4>
                  </div>
                  <Badge bg="warning" className="fs-4">
                    {statistics.pending_count || 0}
                  </Badge>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Payouts List */}
      <Card className="shadow-sm">
        <Card.Header>
          <Tabs
            activeKey={activeTab}
            onSelect={(k) => setActiveTab(k)}
            className="mb-0"
          >
            <Tab eventKey="all" title={`All (${payouts.length})`} />
            <Tab
              eventKey="pending"
              title={`Pending (${filterPayouts("pending").length})`}
            />
            <Tab
              eventKey="approved"
              title={`Approved (${filterPayouts("approved").length})`}
            />
            <Tab
              eventKey="paid"
              title={`Paid (${filterPayouts("paid").length})`}
            />
            <Tab
              eventKey="rejected"
              title={`Rejected (${filterPayouts("rejected").length})`}
            />
          </Tabs>
        </Card.Header>

        <Card.Body>
          {getFilteredPayouts().length === 0 ? (
            <div className="text-center py-5">
              <FaHistory size={48} className="text-muted mb-3" />
              <h5 className="text-muted">No payouts found</h5>
              <p className="text-muted">
                {activeTab === "all"
                  ? "You haven't requested any payouts yet"
                  : `No ${activeTab} payouts`}
              </p>
              {activeTab === "all" && (
                <Button
                  variant="primary"
                  onClick={() => setShowRequestModal(true)}
                  className="mt-3"
                >
                  <FaPlus className="me-2" />
                  Request Your First Payout
                </Button>
              )}
            </div>
          ) : (
            <div>
              {getFilteredPayouts().map((payout) => (
                <PayoutCard key={payout.id} payout={payout} />
              ))}
            </div>
          )}
        </Card.Body>
      </Card>

      {/* Request Payout Modal */}
      <PayoutRequestModal
        show={showRequestModal}
        onHide={() => setShowRequestModal(false)}
        onSuccess={handleRequestSuccess}
        availableBalance={statistics?.available_balance || 0}
      />
    </Container>
  );
};

export default Payouts;
