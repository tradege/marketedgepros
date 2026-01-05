import api from "../services/api";

const payoutService = {
  /**
   * Check if user is eligible for payout
   */
  checkEligibility: async () => {
    try {
      const response = await api.get("/payouts/check-eligibility");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Request a new payout
   */
  requestPayout: async (payoutData) => {
    try {
      const response = await api.post("/payouts/request", payoutData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Get all payouts for current user
   */
  getMyPayouts: async (status = null) => {
    try {
      const params = status ? { status } : {};
      const response = await api.get("/payouts/my-payouts", { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Get payout statistics for current user
   */
  getMyStatistics: async () => {
    try {
      const response = await api.get("/payouts/my-statistics");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Get a specific payout by ID
   */
  getPayout: async (payoutId) => {
    try {
      const response = await api.get(`/payouts/${payoutId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Admin functions
  admin: {
    /**
     * Get all pending payout requests
     */
    getPendingPayouts: async () => {
      try {
        const response = await api.get("/payouts/admin/pending");
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    /**
     * Approve a payout request
     */
    approvePayout: async (payoutId, notes = null) => {
      try {
        const response = await api.post(`/payouts/admin/${payoutId}/approve`, {
          notes,
        });
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    /**
     * Reject a payout request
     */
    rejectPayout: async (payoutId, reason) => {
      try {
        const response = await api.post(`/payouts/admin/${payoutId}/reject`, {
          reason,
        });
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    /**
     * Mark a payout as paid
     */
    markAsPaid: async (payoutId, notes = null) => {
      try {
        const response = await api.post(
          `/payouts/admin/${payoutId}/mark-paid`,
          { notes }
        );
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    /**
     * Get overall payout statistics
     */
    getAllStatistics: async () => {
      try {
        const response = await api.get("/payouts/admin/statistics");
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },
  },
};

export default payoutService;
