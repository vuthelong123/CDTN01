"""Hệ thống Quản lý Yêu cầu Bảo hành - Mekong Mobile (Luồng L2).

Entrypoint chính của ứng dụng web Flask (Track SE).
Khởi tạo ứng dụng, đăng ký các Blueprints tách lớp và filters.
"""
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask

# Đảm bảo đường dẫn import tương đối từ thư mục src/
sys.path.insert(0, os.path.dirname(__file__))

from repositories import close_db
from routes import (ROLE_LABELS, admin_bp, auth_bp, reception_bp,
                    tech_bp)
from services import (CATEGORY_LABELS, PRIORITY_LABELS, STATUS_LABELS,
                      STATUS_ORDER, mask_phone)

# Nạp file .env từ thư mục gốc BT2
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET", "dev-only-change-me")
app.teardown_appcontext(close_db)

# Đăng ký các Blueprint phân tầng
app.register_blueprint(auth_bp)
app.register_blueprint(reception_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tech_bp)

# Đăng ký alias endpoint ngắn gọn để các templates url_for('admin'), url_for('reception')... hoạt động trơn tru
for rule in list(app.url_map.iter_rules()):
    if "." in rule.endpoint:
        short_endpoint = rule.endpoint.split(".", 1)[1]
        existing_endpoints = {r.endpoint for r in app.url_map.iter_rules()}
        if short_endpoint not in existing_endpoints:
            app.add_url_rule(
                rule.rule,
                endpoint=short_endpoint,
                view_func=app.view_functions[rule.endpoint],
                methods=rule.methods,
            )


# ----------------------------------------------------------------------------
# Template Filters & Context Processor
# ----------------------------------------------------------------------------
@app.template_filter("dt")
def fmt_datetime(value):
    """Định dạng ngày giờ kiểu Việt Nam."""
    return value.strftime("%d/%m/%Y %H:%M") if value else "—"


@app.template_filter("d")
def fmt_date(value):
    return value.strftime("%d/%m/%Y") if value else "—"


app.add_template_filter(mask_phone, "mask")


@app.context_processor
def inject_globals():
    return dict(
        ROLE_LABELS=ROLE_LABELS,
        STATUS_LABELS=STATUS_LABELS,
        STATUS_ORDER=STATUS_ORDER,
        PRIORITY_LABELS=PRIORITY_LABELS,
        CATEGORY_LABELS=CATEGORY_LABELS,
        now=datetime.now(),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
