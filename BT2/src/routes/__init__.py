from .admin_routes import admin_bp
from .auth_routes import ROLE_HOME, ROLE_LABELS, auth_bp, login_required
from .reception_routes import reception_bp
from .tech_routes import tech_bp

__all__ = [
    "auth_bp",
    "reception_bp",
    "admin_bp",
    "tech_bp",
    "login_required",
    "ROLE_LABELS",
    "ROLE_HOME",
]
