"""Routes dành cho Kỹ thuật viên: UC05 xem phiếu, UC06 cập nhật trạng thái."""
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from repositories import MySQLTicketRepository
from services import (STATUS_LABELS, TECH_TRANSITIONS, ValidationError,
                      update_tech_status, warranty_state)

from .auth_routes import login_required

tech_bp = Blueprint("technician", __name__)


@tech_bp.route("/technician", endpoint="technician")
@login_required("KY_THUAT")
def technician_view():
    repo = MySQLTicketRepository()
    tickets = repo.find_tickets("t.technician_id = %s", (session["technician_id"],))
    for t in tickets:
        t["warranty"] = warranty_state(t)
        t["next_statuses"] = TECH_TRANSITIONS.get(t["ticket_status"], [])
    return render_template("technician.html", tickets=tickets)


@tech_bp.route("/technician/update/<int:ticket_id>", methods=["POST"], endpoint="update_status")
@login_required("KY_THUAT")
def update_status_route(ticket_id):
    repo = MySQLTicketRepository()
    new_status = request.form.get("new_status")
    try:
        code, old_st, new_st = update_tech_status(
            repo,
            ticket_id,
            session["technician_id"],
            new_status,
            session["employee_id"],
        )
        flash(f"Phiếu {code}: {STATUS_LABELS[old_st]} → {STATUS_LABELS[new_st]}.", "success")
    except ValidationError as exc:
        repo.rollback()
        flash(exc.message, "error")
    except Exception as exc:
        repo.rollback()
        flash(f"Lỗi: {exc}", "error")
    return redirect(url_for("technician"))
