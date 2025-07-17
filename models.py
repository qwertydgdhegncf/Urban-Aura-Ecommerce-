from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount_percent = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=False)
    used_count = db.Column(db.Integer, default=0)

    def is_valid(self):
        return (
            self.used_count < self.usage_limit
            and self.expiration_date >= datetime.utcnow()
        )
