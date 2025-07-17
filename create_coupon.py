from app import app
from models import db, Coupon
from datetime import datetime, timedelta

with app.app_context():
    new_coupon = Coupon(
        code='URBANAURA20',
        discount_percent=10,
        expiration_date=datetime.utcnow() + timedelta(days=30),
        usage_limit=5
    )
    db.session.add(new_coupon)
    db.session.commit()
    print("🎉 Sample coupon created!")
