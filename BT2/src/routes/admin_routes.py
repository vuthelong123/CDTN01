"""Routes dành cho Quản trị viên: UC03 tra cứu, UC04 gán KTV, UC07 đóng phiếu."""
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from repositories import MySQLTicketRepository
from services import (STATUS_LABELS, ValidationError, assign_technician,
                      close_ticket, warranty_state)

from .auth_routes import login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", endpoint="admin")
@login_required("QUAN_TRI")
def admin_view():
    repo = MySQLTicketRepository()
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")

    conds, args = [], []
    if q:
        conds.append("t.ticket_code LIKE %s")
        args.append(f"%{q}%")
    if status in STATUS_LABELS:
        conds.append("t.ticket_status = %s")
        args.append(status)

    tickets = repo.find_tickets(" AND ".join(conds), args)
    for t in tickets:
        t["warranty"] = warranty_state(t)

    counts = repo.get_status_counts()
    technicians = repo.get_active_technicians()

    return render_template(
        "admin.html",
        tickets=tickets,
        counts=counts,
        technicians=technicians,
        q=q,
        status=status,
    )


@admin_bp.route("/admin/assign/<int:ticket_id>", methods=["POST"], endpoint="assign_ticket")
@login_required("QUAN_TRI")
def assign_ticket_route(ticket_id):
    repo = MySQLTicketRepository()
    tech_id = request.form.get("technician_id", type=int)
    try:
        code = assign_technician(repo, ticket_id, tech_id, session["employee_id"])
        flash(f"Đã phân công phiếu {code}.", "success")
    except ValidationError as exc:
        repo.rollback()
        flash(exc.message, "error")
    except Exception as exc:
        repo.rollback()
        flash(f"Lỗi: {exc}", "error")
    return redirect(request.referrer or url_for("admin"))


@admin_bp.route("/admin/close/<int:ticket_id>", methods=["POST"], endpoint="close_ticket")
@login_required("QUAN_TRI")
def close_ticket_route(ticket_id):
    repo = MySQLTicketRepository()
    try:
        code = close_ticket(repo, ticket_id, session["employee_id"])
        flash(f"Đã đóng phiếu {code}.", "success")
    except ValidationError as exc:
        repo.rollback()
        flash(exc.message, "error")
    except Exception as exc:
        repo.rollback()
        flash(f"Lỗi: {exc}", "error")
    return redirect(request.referrer or url_for("admin"))
