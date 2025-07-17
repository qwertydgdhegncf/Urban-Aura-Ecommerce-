from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import threading
import webbrowser
from models import db, Coupon

app = Flask(__name__)
app.secret_key = 'urbanaura-secret-2025'


# -------------------- Flask Config --------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'         # 🔁 Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password_here'       # 🔁 Replace with your App Password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'   # 🔁 Replace with your email
mail = Mail(app)

# -------------------- Product List --------------------
products = [

    {'id': 0, 'name': 'T-shirt', 'price': 20},
    {'id': 1, 'name': 'Jeans', 'price': 40},
    {'id': 2, 'name': 'Sneakers', 'price': 60},
    {'id': 3, 'name': 'Jacket', 'price': 80},
    {'id': 4, 'name': 'Cap', 'price': 15},
    {'id': 5, 'name': 'Sunglasses', 'price': 30},
    {'id': 6, 'name': 'Watch', 'price': 100},
    {'id': 7, 'name': 'Backpack', 'price': 50},
    {'id': 8, 'name': 'Belt', 'price': 25},
    {'id': 9, 'name': 'Wallet', 'price': 35},
    {'id': 10, 'name': 'Scarf', 'price': 20},
    {'id': 11, 'name': 'Gloves', 'price': 15},
    {'id': 12, 'name': 'Hat', 'price': 18},
    {'id': 13, 'name': 'Socks', 'price': 10 },
    {'id': 14, 'name': 'Sweatshirt', 'price': 45},
    {'id': 15, 'name': 'Shorts', 'price': 30},
    {'id': 16, 'name': 'Flip Flops', 'price': 12},
    {'id': 17, 'name': 'Umbrella', 'price': 22},
    {'id': 18, 'name': 'Laptop Sleeve', 'price': 28},
    {'id': 19, 'name': 'Phone Case', 'price': 15},
    {'id': 20, 'name': 'Water Bottle', 'price': 10},
    {'id': 21, 'name': 'Yoga Mat', 'price': 35},
    {'id': 22, 'name': 'Fitness Tracker', 'price': 90},
    {'id': 23, 'name': 'Bluetooth Speaker', 'price': 70},
    {'id': 24, 'name': 'Portable Charger', 'price': 25},
    {'id': 25, 'name': 'Camera Bag', 'price': 55},
    {'id': 26, 'name': 'Travel Pillow', 'price': 20},
    {'id': 27, 'name': 'Luggage Tag', 'price': 8},
    {'id': 28, 'name': 'Keychain', 'price': 5},
    {'id': 29, 'name': 'Notebook', 'price': 12},
    {'id': 30, 'name': 'Pen Set', 'price': 10},
    {'id': 31, 'name': 'Desk Organizer', 'price': 30},
    {'id': 32, 'name': 'Wall Art', 'price': 45},
    {'id': 33, 'name': 'Photo Frame', 'price': 20},
    {'id': 34, 'name': 'Candle', 'price': 15},
    {'id': 35, 'name': 'Incense Holder', 'price': 12},
    {'id': 36, 'name': 'Essential Oil', 'price': 18},
    {'id': 37, 'name': 'Bathrobe', 'price': 50},
    {'id': 38, 'name': 'Slippers', 'price': 25},
    {'id': 39, 'name': 'Towel Set', 'price': 30},
    {'id': 40, 'name': 'Shower Curtain', 'price': 22},
    {'id': 41, 'name': 'Bath Mat', 'price': 15},
    {'id': 42, 'name': 'Toothbrush Holder', 'price': 8},
    {'id': 43, 'name': 'Soap Dispenser', 'price': 10},
    {'id': 44, 'name': 'Hair Dryer', 'price': 40},
    {'id': 45, 'name': 'Straightener', 'price': 50},
    {'id': 46, 'name': 'Curling Iron', 'price': 45},
    {'id': 47, 'name': 'Makeup Bag', 'price': 20},
    {'id': 48, 'name': 'Skincare Set', 'price': 60},
    {'id': 49, 'name': 'Perfume', 'price': 70},
    {'id': 50, 'name': 'Hairbrush', 'price': 15},
    {'id': 51, 'name': 'Nail Polish Set', 'price': 25},
    {'id': 52, 'name': 'Face Mask', 'price': 12},
    {'id': 53, 'name': 'Lip Balm', 'price': 5},
    {'id': 54, 'name': 'Sunscreen', 'price': 20},
    {'id': 55, 'name': 'Shampoo', 'price': 18},
    {'id': 56, 'name': 'Conditioner', 'price': 18},
    {'id': 57, 'name': 'Body Wash', 'price': 15},
    {'id': 58, 'name': 'Hand Cream', 'price': 10},
    {'id': 59, 'name': 'Foot Cream', 'price': 12}            
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

    # Send confirmation email
    try:
        msg = Message('UrbanAura - Order Confirmed!', recipients=[email])
        msg.body = '🎉 Your order has been confirmed!\nThank you for shopping with UrbanAura.'
        mail.send(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

    return render_template('confirm.html')

@app.route('/clear_cart')
def clear_cart():
    cart.clear()
    return redirect(url_for('view_cart'))

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

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    code = request.form.get('coupon_code').strip().upper()
    coupon = Coupon.query.filter_by(code=code).first()

    if not coupon:
        flash('Invalid coupon code.')
        return redirect('/checkout')

    if not coupon.is_valid():
        flash('Coupon is expired or limit reached.')
        return redirect('/checkout')

    discount = coupon.discount_percent
    flash(f'{discount}% discount applied!')
    coupon.used_count += 1
    db.session.commit()
    return redirect('/checkout')

# -------------------- Open Browser --------------------
def open_browser():
    webbrowser.open("http://localhost:8080")

# -------------------- Run App --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database and Coupon table ready.")
    threading.Timer(1.5, open_browser).start()
    app.run(host='0.0.0.0', port=8080, debug=True)
