from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify,before_render_template
import sqlite3
import os
from Form import userSignup, userLogin, ProductForm, PromotionForm, PasswordChange, ProductFilter, CheckoutForm
from Product import ProductManager, Product  # Import the Product class
from werkzeug.utils import secure_filename
from Promotion import PromotionManager
from User import DisplayUser
from Cart import CartManager
# from info import InfoManager
import plotly.express as px
#import stripe
# stripe.api_key = "sk_test_51OdTteBzJLH01t0Myv424qrnRDEOHP461k6PUoqXAhYq7P7NsnBCApYGdAxXe0FJsVhjCbGBzXdVrUV6D4RFRyrr00Hn7m5zPx"
# import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/image'

# ---------------Clear Session when load---------------#

session_cleared = False
@app.before_request
def before_request():
    global session_cleared
    if not session_cleared:
        session.clear()
        session_cleared = True
# ---------------CODE FOR DB---------------#

def create_Userdata():
    conn = sqlite3.connect('Userdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            PhoneNumber TEXT,
            Email TEXT NOT NULL,
            DateOfBirth DATE NOT NULL,
            Role TEXT DEFAULT 'customer'
        )
    ''')
    conn.commit()
    conn.close()

create_Userdata()

def create_Product():
    conn = sqlite3.connect('Product.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            name TEXT,
            price REAL,
            category TEXT,
            stock INTEGER,
            description TEXT,
            size TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_Product()

def create_Promotion():
    conn = sqlite3.connect('Promotion.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promotions (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            discount REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_Promotion()

def create_Cart():
    conn = sqlite3.connect('Cart.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            CartID INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            size TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_Cart()


# def create_Order():
#     conn = sqlite3.connect('Order.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS orders (
#             OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             product_id INTEGER,
#             quantity INTEGER,
#             size TEXT,
#             total_price REAL,  -- Assuming you want to store the total price for the order
#             order_date TEXT,   -- You can use DATETIME or TEXT for the order date
#             payment_status TEXT,
#             FOREIGN KEY (user_id) REFERENCES users(user_id),  -- Make sure to replace 'users' with your actual users table name
#             FOREIGN KEY (product_id) REFERENCES products(product_id)  -- Replace 'products' with your actual products table name
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# create_Order()
#
#
# def create_Info():
#     conn = sqlite3.connect('Info.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS info (
#         user_id INTEGER,
#         fname TEXT,
#         lname TEXT,
#         address BLOB,
#         email TEXT,
#         postalcode INTEGER,
#         nameoncard TEXT,
#         cardno INTEGER,
#         expirydate BLOB,
#         cvv INTEGER,
#         unitno BLOB
#         )
#     ''')
#
#     conn.commit()
#     conn.close()
#
#
# create_Info()


# ---------------Code for Home---------------#
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

# ---------------check for username---------------#
def username_exists(username):
    conn = sqlite3.connect('Userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE Username=?', (username,))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user is not None

# ---------------Check file upload name---------------#
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# ---------------Check for login---------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    userLoginform = userLogin(request.form)
    login_failure_message = None

    if request.method == 'POST':
        username = userLoginform.username.data # using contact number as username
        password = userLoginform.password.data

        # Check if the username and password match
        conn = sqlite3.connect('Userdata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE PhoneNumber=? AND password=?', (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session['User_ID'] = user[0]
            session['Username'] = user[1]
            session['Role'] = user[6]
            flash('Login successful!', 'success')

            if session['Role'] == "customer":
                print("customer")
                return redirect(url_for('userdashboard'))
            else:
                print("admin")
                return redirect(url_for('adminDashboard'))
        else:
            login_failure_message = "*Contact Number or password does not match.*"

    return render_template('Login.html', form=userLoginform, login_failure_message=login_failure_message)

# ---------------Code for logout---------------#
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------------Code For signup---------------#
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    userSignupform = userSignup(request.form)
    if request.method == 'POST':

        username = userSignupform.name.data.lower()
        password = userSignupform.password.data
        number = userSignupform.number.data
        email = userSignupform.email.data
        dob = userSignupform.dob.data

        if username_exists(username):
            flash('Username already exists. Please choose a different username.', 'danger')
        else:

            conn = sqlite3.connect('Userdata.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (Username, Password, PhoneNumber, Email, DateOfBirth) VALUES (?, ?, ?, ?, ?)',
                (username, password, number, email, dob))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')

        return redirect(url_for('login'))
    return render_template('Signup.html', form=userSignupform)

# ---------------Code for product---------------#
@app.route('/Product')
def Productpage():
    ProductFilterForm = ProductFilter(request.form)
    product_manager = ProductManager()
    products = product_manager.get_all_products()
    product_manager.close_connection()

    return render_template('Product.html', products=products, form=ProductFilterForm)

@app.route('/product/<int:product_id>')
def display_product(product_id):
    product_manager = ProductManager()
    product = product_manager.get_product_by_id(product_id)
    product_manager.close_connection()

    if product:
        sizes = product.size.split(',')
        return render_template('product_detail.html', product=product, sizes=sizes)

@app.route('/userdashboard')
def userdashboard():

    if 'User_ID' in session:

        UserID = session['User_ID']
        user_manager = DisplayUser()
        userdata = user_manager.get_user_by_id(UserID)
        user_manager.close_connection()
        if userdata is not None:
            return render_template('userprofile.html', userdata=userdata, UserID=session['User_ID'])
        else:
            flash('User not found.', 'warning')
            return redirect(url_for('login'))
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))
#################INCOMPLETE#########################
@app.route('/passwordchange', methods=['POST','GET'])
def passwordchange():
    passwordchangeform = PasswordChange(request.form)

    if 'User_ID' in session:
        return render_template('passwordchange.html', form=passwordchangeform)

    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/passwordchange', methods=['POST'])
def passwordchangebutton():
    UserID = session.get('User_ID')
    # UserID = session['User_ID']
    password_change = DisplayUser()
    current_password = password_change.get_password_by_id(UserID)
    password_change.close_connection()

    if request.method == 'POST':
        CurrentPassword = passwordchange.CurrentPasswordField.data
        NewPassword = passwordchange.NewPasswordField.data
        ConfirmPassword = passwordchange.ConfirmPasswordField.data

        if CurrentPassword == current_password:
            if NewPassword == ConfirmPassword:
                update_password = DisplayUser()
                updatepassword = update_password.update_password(ConfirmPassword, UserID)
                update_password.close_connection()
            else:
                flash('You need to log in first.', 'warning')
                print("check cfm else")
                return redirect(url_for('login'))
        else:
            flash('You need to log in first.', 'warning')
            print("current password else")
            return redirect(url_for('login'))

        return render_template('passwordchange.html', form=passwordchange)
    else:
        flash('You need to log in first.', 'warning')
        print("current qwewqqewqwe else")
        return redirect(url_for('login'))


#################code for del button on user profile#########################
@app.route('/del_user', methods=['POST'])
def del_user():
    UserID1 = request.form.get('delAccount')
    print(UserID1,"test")
    User_manager = DisplayUser()
    User_manager.del_user(UserID1)
    session.clear()
    User_manager.close_connection()
    return redirect(url_for('login'))

@app.route('/adminDashboard')
def adminDashboard():
    if 'User_ID' in session:
        data = {'Months': ['January', 'February', 'March', 'May','April','June','July','August','September', 'October','November','December'], 'Total Sold/ Month': [12, 5, 8, 9, 11, 15,7, 19, 11, 13 ,7 ,8]}

        fig = px.line(data, x='Months', y='Total Sold/ Month', title='Product Sales')

        plot_html = fig.to_html(full_html=False)
        return render_template('adminDashboard.html', username=session['Username'], role=session['Role'],UserID=session['User_ID'], plot_html=plot_html)
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))


@app.route('/adminOrder')
def adminOrder():
    return render_template('adminOrder.html')

@app.route('/adminProducts', methods=['GET', 'POST'])
def adminProducts():
    productForm = ProductForm(request.form)
    if request.method == 'POST':

        # Collect form Data
        name = productForm.name.data
        price = productForm.price.data
        category = productForm.category.data
        stock = productForm.stock.data
        description = productForm.description.data
        size = productForm.size.data

        #change add , for categroy
        categories_string = ', '.join(category)
        size_string = ', '.join(size)
        # Handle image upload
        image_upload = request.files['image']

        if image_upload and allowed_file(image_upload.filename):
            filename = secure_filename(image_upload.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_upload.save(image_path)

        # Extract just the filename without the path
        filename_only = os.path.basename(image_path)

        # Save the product to the database
        product_manager = ProductManager()
        product_manager.add_product(filename_only, name, price, categories_string, stock, description, size_string)
        product_manager.close_connection()



        return redirect(url_for('Productpage'))
    return render_template('adminProducts.html', form=productForm)

# Code for Promotions
@app.route('/adminPromotions', methods=['GET', 'POST'])
def adminPromotions():
    promotionForm = PromotionForm(request.form)


    getpromotion = PromotionManager()
    displaypromotion = getpromotion.get_all_promotion()
    getpromotion.close_connection()

    if request.method == 'POST':
        name = promotionForm.name.data
        discount = promotionForm.discount.data
        description = promotionForm.description.data

        promotion_manager = PromotionManager()
        promotion_manager.add_promotion(name,discount,description)
        promotion_manager.close_connection()
        return redirect(url_for('adminPromotions'))

    return render_template('adminPromotions.html', form=promotionForm, displaypromotion=displaypromotion)

@app.route('/delete_promotion', methods=['POST'])
def delete_promotion():
    promotion_id = request.form.get('id')

    promotion_manager = PromotionManager()
    promotion_manager.del_promotion(promotion_id)
    promotion_manager.close_connection()
    return redirect(url_for('adminPromotions'))

@app.route('/adminEditUsers' , methods=['GET', 'POST'])
def adminEditUsers():
    getUser = DisplayUser()
    displayuser = getUser.get_all_user()
    getUser.close_connection()
    return render_template('adminEditUsers.html', displayuser = displayuser)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('UserID')

    User_manager = DisplayUser()
    User_manager.del_user(user_id)
    User_manager.close_connection()
    return redirect(url_for('adminEditUsers'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    selected_size = request.form.get('selected_size')
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if quantity is not provided
    user_id = session.get('User_ID') #retrive user_id from session

    # print(user_id)
    # print(f"Product ID: {product_id}, Selected Size: {selected_size}, Quantity: {quantity}")

    cartmanager = CartManager()
    cartmanager.add_to_cart(user_id, product_id, quantity, selected_size)
    cartmanager.close_connection()
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():

    if 'User_ID' in session:

        userid = session['User_ID']
        cartmanager = CartManager()
        cart = cartmanager.get_cart_by_id(userid)
        cartmanager.close_connection()

        product_manager = ProductManager()  # Replace with the actual class for managing product data
        product_data_list = []

        total_price = 0

        # total_price = 0   #initialize total proce

        for item in cart:
            product_id = item[2]  # Replace with the actual key or attribute name
            product = product_manager.get_product_by_id(product_id)

            # product_id = item[1]
            # product = product_manager.get_product_by_id(product_id)

            if product:
                # product_data_list.append(product)
                # total_price += product.price * item[2]
                product_data_list.append(product)
                total_price += product.price * item[3]  # Assuming index 2 corresponds to quantity
            else:
                print(f"Product with ID {product_id} not found in the product database.")
        # Now, product_data_list contains information about products in the cart
        product_manager.close_connection()

        for item, product in zip(cart, product_data_list):
            print(f"Quantity: {item[3]}, Price: {product.price}, Subtotal: {item[3] * product.price}")


        return render_template('cart.html', cart=cart, UserID=userid, product_data_list=product_data_list, total_price=total_price)


    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))



@app.route('/del_cart', methods=['POST'])
def del_cart():
    cart_id = request.form.get('CartID')

    cart_manager = CartManager()
    cart_manager.del_cart(cart_id)
    cart_manager.close_connection()
    return redirect(url_for('view_cart'))

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    cart_manager = CartManager()
    if request.method == 'POST':
        cart_id = request.form.get('CartID')
        print(cart_id)
        action = request.form.get('action')

        if cart_id and action:
            cart_id = int(cart_id)
            current_quantity = get_current_quantity(cart_id)

            if action == 'increment':
                new_quantity = current_quantity + 1
            elif action == 'decrement' and current_quantity > 1:
                new_quantity = current_quantity - 1
            else:
                # No valid action, do nothing
                return redirect(url_for('cart'))

            cart_manager.update_cart_quantity(cart_id, new_quantity)

    return redirect(url_for('view_cart'))

def get_current_quantity(cart_id):
    conn = sqlite3.connect('Cart.db')
    cursor = conn.cursor()

    # Retrieve the current quantity from the database
    cursor.execute('SELECT quantity FROM cart WHERE CartID = ?', (cart_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        # Return 0 if the cart item is not found
        return 0


#<--------------------- Check Out code --------------------->
# @app.route('/checkout')
# def checkout():
#     checkoutForm = CheckoutForm(request.form)
#     if request.method == 'POST':
#         fname = checkoutForm.fname.data
#         lname = checkoutForm.lname.data
#         address = checkoutForm.address.data
#         email = checkoutForm.email.data
#         postalcode = checkoutForm.postalcode.data
#         nameoncard = checkoutForm.nameoncard.postalcode.data
#         cardno = checkoutForm.cardno.data
#         expirydate = checkoutForm.expirydate.data
#         cvv = checkoutForm.cvv.data
#         unitno = checkoutForm.unitno.data
#
#         info_manager = InfoManager()
#         info_manager.add_info(fname, lname, address, email, postalcode, nameoncard, cardno, expirydate, cvv, unitno)
#         info_manager.close_connection()
#     return render_template('checkout.html')

# @app.route('/checkout', methods=['GET'])
# def checkout():
#     cartmanager = CartManager()
#     cart_item = cartmanager.get_all_cart()
#
#     total_amount = total_amount
#     return render_template('checkout.html', cart_item=cart_item, total_price=total_amount)
#
#
# @app.route('/process-payment', methods=['POST'])
# def process_payment():
#     # Get customer information from the form
#     customer_name = request.form['name']
#     customer_email = request.form['email']
#
#     # Create a Checkout Session on the server
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#
#         line_items=[
#             # Include the cart items here
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': item['product_name'],
#                     },
#                     'unit_amount': item['price'],
#                 },
#                 'quantity': item['quantity'],
#             }
#
#             for item in cart_items
#         ],
#         mode='payment',
#         success_url=request.url_root + 'success',
#         cancel_url=request.url_root + 'cancel',
#     )
#
#     # Update your database with the order details (cart_items, customer_name, customer_email, etc.)
#     # ...
#
#     flash('Payment successful. Order placed!', 'success')
#     return redirect(url_for('success'))
#
#
# @app.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     # Create a Checkout Session on the server
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Your Product',
#                     },
#                     'unit_amount': 1000,  # The price in cents
#                 },
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url=request.url_root + 'success',
#         cancel_url=request.url_root + 'cancel',
#     )
#
#     return jsonify({'id': session.id})
#
#
# @app.route('/success', methods=['GET'])
# def success():
#     # Update your database with the successful order details
#     return "Payment successful. Order placed!"
#
# @app.route('/cancel', methods=['GET'])
# def cancel():
#     return "Payment canceled."


if __name__ == '__main__':
    app.run()
