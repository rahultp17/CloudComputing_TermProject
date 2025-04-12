from flask import Blueprint
from sqlalchemy import text  # ✅ Add this
from app import db

dbtest_bp = Blueprint('dbtest', __name__)

@dbtest_bp.route('/db-test')
def db_test():
    try:
        db.session.execute(text("SELECT 1"))  # ✅ Wrap in text()
        return "✅ Database connected successfully!", 200
    except Exception as e:
        return f"❌ DB connection failed: {e}", 500
