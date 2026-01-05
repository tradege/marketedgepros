from flask import Blueprint, request, jsonify
from src.middleware.auth import get_current_user
from decimal import Decimal
from src.services.payout_service import PayoutService
from src.models.user import User
from src.models.payout_request import PayoutRequest
from src.models.trading_program import TradingProgram
from src.extensions import db
from src.middleware.auth import jwt_required, admin_required

payouts_bp = Blueprint("payouts", __name__, url_prefix="/api/payouts")

@payouts_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required
def list_payouts():
    """List payouts for current user (alias for /my-payouts)"""
    return get_my_payouts()


@payouts_bp.route("/check-eligibility", methods=["GET"])
@jwt_required
def check_payout_eligibility():
    """Check if user can request a payout"""
    try:
        user = get_current_user()
        # user already retrieved
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get user's active program
        # TODO: Implement logic to get user's current program
        program = db.session.query(TradingProgram).first()  # Placeholder
        
        if not program:
            return jsonify({"error": "No active program found"}), 404
        
        eligibility = PayoutService.can_request_payout(user, program)
        
        return jsonify(eligibility), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/request", methods=["POST"])
@jwt_required
def request_payout():
    """Request a new payout"""
    try:
        user = get_current_user()
        # user already retrieved
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Validate input
        if not data.get("amount"):
            return jsonify({"error": "Amount is required"}), 400
        
        if not data.get("payment_method"):
            return jsonify({"error": "Payment method is required"}), 400
        
        amount = Decimal(str(data["amount"]))
        payment_method = data["payment_method"]
        payment_details = data.get("payment_details", {})
        
        # Get user's active program
        # TODO: Implement logic to get user's current program
        program = db.session.query(TradingProgram).first()  # Placeholder
        
        if not program:
            return jsonify({"error": "No active program found"}), 404
        
        # Create payout request
        payout = PayoutService.request_payout(
            user=user,
            program=program,
            amount=amount,
            payment_method=payment_method,
            payment_details=payment_details
        )
        
        return jsonify({
            "message": "Payout request submitted successfully",
            "payout": payout.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/my-payouts", methods=["GET"])
@jwt_required
def get_my_payouts():
    """Get all payouts for current user"""
    try:
        user = get_current_user()
        status = request.args.get("status")
        
        payouts = PayoutService.get_user_payouts(user.id, status)
        
        return jsonify({
            "payouts": [p.to_dict() for p in payouts],
            "count": len(payouts)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/my-statistics", methods=["GET"])
@jwt_required
def get_my_payout_statistics():
    """Get payout statistics for current user"""
    try:
        user = get_current_user()
        stats = PayoutService.get_payout_statistics(user.id)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/<int:payout_id>", methods=["GET"])
@jwt_required
def get_payout(payout_id):
    """Get a specific payout"""
    try:
        user = get_current_user()
        # user already retrieved
        
        payout = db.session.query(PayoutRequest).get(payout_id)
        
        if not payout:
            return jsonify({"error": "Payout not found"}), 404
        
        # Check if user owns this payout or is admin
        if payout.user_id != user.id and user.role not in ["supermaster", "master"]:
            return jsonify({"error": "Unauthorized"}), 403
        
        return jsonify(payout.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin routes
@payouts_bp.route("/admin/pending", methods=["GET"])
@jwt_required
@admin_required
def get_pending_payouts():
    """Get all pending payout requests (Admin only)"""
    try:
        payouts = PayoutService.get_pending_payouts()
        
        return jsonify({
            "payouts": [p.to_dict() for p in payouts],
            "count": len(payouts)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/admin/<int:payout_id>/approve", methods=["POST"])
@jwt_required
@admin_required
def approve_payout(payout_id):
    """Approve a payout request (Admin only)"""
    try:
        approver = get_current_user()
        data = request.get_json() or {}
        notes = data.get("notes")
        
        payout = PayoutService.approve_payout(payout_id, approver.id, notes)
        
        return jsonify({
            "message": "Payout approved successfully",
            "payout": payout.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/admin/<int:payout_id>/reject", methods=["POST"])
@jwt_required
@admin_required
def reject_payout(payout_id):
    """Reject a payout request (Admin only)"""
    try:
        approver = get_current_user()
        data = request.get_json()
        
        if not data or not data.get("reason"):
            return jsonify({"error": "Rejection reason is required"}), 400
        
        reason = data["reason"]
        
        payout = PayoutService.reject_payout(payout_id, approver.id, reason)
        
        return jsonify({
            "message": "Payout rejected successfully",
            "payout": payout.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/admin/<int:payout_id>/mark-paid", methods=["POST"])
@jwt_required
@admin_required
def mark_payout_paid(payout_id):
    """Mark a payout as paid (Admin only)"""
    try:
        data = request.get_json() or {}
        notes = data.get("notes")
        
        payout = PayoutService.mark_as_paid(payout_id, notes)
        
        return jsonify({
            "message": "Payout marked as paid successfully",
            "payout": payout.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payouts_bp.route("/admin/statistics", methods=["GET"])
@jwt_required
@admin_required
def get_all_payout_statistics():
    """Get overall payout statistics (Admin only)"""
    try:
        stats = PayoutService.get_payout_statistics()
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
