from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import threading
import webbrowser
from models import db, Coupon
from flask import request, redirect, flash, render_template
from models import Coupon



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # or PostgreSQL, MySQL, etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




app = Flask(__name__)

# -------------------- Flask-Mail Configuration --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'       # 🔁 Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'your_app_password_here'      # 🔁 Use App Password for Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# -------------------- Product List --------------------
products = [
    {'id': 0, 'name': 'T-shirt', 'price': 20},
    {'id': 1, 'name': 'Jeans', 'price': 40},
    {'id': 2, 'name': 'Sneakers', 'price': 60},
    {'id': 3, 'name': 'Jacket', 'price': 80},
    {'id': 4, 'name': 'Cap', 'price': 15},
    {'id': 5, 'name': 'Sunglasses', 'price': 25},
    {'id': 6, 'name': 'Watch', 'price': 120},
    {'id': 7, 'name': 'Socks', 'price': 10},
    {'id': 8, 'name': 'Backpack', 'price': 50},
    {'id': 9, 'name': 'Belt', 'price': 18},
    {'id': 10, 'name': 'Gloves', 'price': 22},
    {'id': 11, 'name': 'Hoodie', 'price': 45},
    {'id': 12, 'name': 'Beanie', 'price': 12},
    {'id': 13, 'name': 'Scarf', 'price': 16},
    {'id': 14, 'name': 'Boots', 'price': 75},
    {'id': 15, 'name': 'Dress', 'price': 90},
    {'id': 16, 'name': 'Skirt', 'price': 35},
    {'id': 17, 'name': 'Blazer', 'price': 95},
    {'id': 18, 'name': 'Heels', 'price': 65},
    {'id': 19, 'name': 'Sandals', 'price': 30},
    {'id': 20, 'name': 'Shorts', 'price': 28},
    {'id': 21, 'name': 'Tank Top', 'price': 18},
    {'id': 22, 'name': 'Cardigan', 'price': 55},
    {'id': 23, 'name': 'Polo Shirt', 'price': 32},
    {'id': 24, 'name': 'Leggings', 'price': 25},
    {'id': 25, 'name': 'Raincoat', 'price': 85},
    {'id': 26, 'name': 'Suitcase', 'price': 150},
    {'id': 27, 'name': 'Duffel Bag', 'price': 70},
    {'id': 28, 'name': 'Sports Bra', 'price': 26},
    {'id': 29, 'name': 'Slippers', 'price': 20},
    {'id': 30, 'name': 'Earrings', 'price': 40},
    {'id': 31, 'name': 'Necklace', 'price': 55},
    {'id': 32, 'name': 'Graphic Tee', 'price': 22},
    {'id': 33, 'name': 'Yoga Pants', 'price': 38},
    {'id': 34, 'name': 'Messenger Bag', 'price': 65},
    {'id': 35, 'name': 'Wool Coat', 'price': 110},
    {'id': 36, 'name': 'Evening Gown', 'price': 130},
    {'id': 37, 'name': 'Crossbody Purse', 'price': 48},
    {'id': 38, 'name': 'Sweatpants', 'price': 42},
    {'id': 39, 'name': 'Crop Top', 'price': 27},
    {'id': 40, 'name': 'Bucket Hat', 'price': 19},
    {'id': 41, 'name': 'Running Shoes', 'price': 75},
    {'id': 42, 'name': 'Ballet Flats', 'price': 60},
    {'id': 43, 'name': 'Tech Gloves', 'price': 28},
    {'id': 44, 'name': 'Leather Jacket', 'price': 150},
    {'id': 45, 'name': 'Denim Skirt', 'price': 40},
    {'id': 46, 'name': 'Charm Bracelet', 'price': 35},
    {'id': 47, 'name': 'Wool Sweater', 'price': 55},
    {'id': 48, 'name': 'Leg Warmers', 'price': 18},
    {'id': 49, 'name': 'Travel Wallet', 'price': 22},
    {'id': 50, 'name': 'Puffer Vest', 'price': 70},
    {'id': 51, 'name': 'Maxi Dress', 'price': 85},
]

cart = []

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    for product in products:
        if product['id'] == product_id:
            cart.append(product)
            break
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    if not cart:
        return redirect(url_for('index'))
    total = sum(item['price'] for item in cart)
    return render_template('checkout.html', total=total, cart=cart)

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    email = request.form.get('email')

    # Send order confirmation email
    try:
        msg = Message('UrbanAura - Order Confirmed!',
                      recipients=[email])
        msg.body = '🎉 Your order has been confirmed!\nThank you for shopping with us at UrbanAura.'
        mail.send(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

    # Redirect to confirmation page
    return render_template('confirm.html')

@app.route('/clear_cart')
def clear_cart():
    cart.clear()
    return redirect(url_for('view_cart'))

#print(request.form)
# print(email)  # Removed because 'email' is not defined at the module level


# Disable admin panel routes
@app.route('/admin')
def admin_panel():
    return redirect(url_for('index'))

@app.route('/add_product', methods=['POST'])
def add_product():
    return redirect(url_for('index'))

@app.route('/edit_product/<int:product_id>')
def edit_product(product_id):
    return redirect(url_for('index'))

@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    return redirect(url_for('index'))

@app.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    code = request.form['coupon_code'].strip().upper()
    coupon = Coupon.query.filter_by(code=code).first()

    if not coupon:
        flash('Invalid coupon code.')
        return redirect('/checkout')

    if not coupon.is_valid():
        flash('Coupon is expired or limit reached.')
        return redirect('/checkout')

    discount = coupon.discount_percent
    # Save this in session or cart
    flash(f'{discount}% discount applied!')
    coupon.used_count += 1
    db.session.commit()
    return redirect('/checkout')
# The calculation of discounted_total should be done inside the apply_coupon route where discount is defined.
# Remove or comment out the global usage of discount here to avoid NameError.
# Example (inside the route):
# discounted_total = total - (total * discount / 100)


# -------------------- Auto Open Browser --------------------
def open_browser():
    webbrowser.open("http://localhost:8080")

# -------------------- Run App --------------------
if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(host='0.0.0.0', port=8080, debug=True)


# -------------------- Coupon Model --------------------
# Inside app.py at the bottom or run in Python shell
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    from models import db
    with app.app_context():
        db.create_all()
        print("✅ Coupon table created")

