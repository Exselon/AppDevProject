from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify,before_render_template
import sqlite3
import os
from Form import userSignup, userLogin, ProductForm , PromotionForm, PasswordChange
from Product import ProductManager, Product  # Import the Product class
from werkzeug.utils import secure_filename
from Promotion import PromotionManager
from User import DisplayUser
from Cart import CartManager

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
    product_manager = ProductManager()
    products = product_manager.get_all_products()
    product_manager.close_connection()

    return render_template('Product.html', products=products)

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
@app.route('/passwordchange', methods=['POST'])
def passwordchange():
    passwordchangeform = PasswordChange(request.form)

    if 'User_ID' in session:

        UserID = session['User_ID']
        password_change = DisplayUser()
        current_password = password_change.get_password_by_id(UserID)
        password_change.close_connection()

        return render_template('passwordchange.html', current_password=current_password,UserId=session['User_ID'], form=passwordchangeform)

    else:
        flash('You need to log in first.', 'warning')
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

        return render_template('adminDashboard.html', username=session['Username'], role=session['Role'],UserID=session['User_ID'])
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
        product_manager.add_product(filename_only, name, price, categories_string, stock, description, size)
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

        for item in cart:
            product_id = item[2]  # Replace with the actual key or attribute name
            product = product_manager.get_product_by_id(product_id)

            if product:
                product_data_list.append(product)
            else:
                print(f"Product with ID {product_id} not found in the product database.")
        # Now, product_data_list contains information about products in the cart
        product_manager.close_connection()

        return render_template('cart.html',cart=cart, UserID=userid, product_data_list=product_data_list)

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




# <------------- Incomplete Cart code ------------------>
# @app.route('/update_cart', methods=['POST'])
# def update_cart():
#     cart_id = request.form.get('CartID')
#     quantity = int(request.form.get('quantity', 1))
#     cart_manager = CartManager()
#     cart_manager.update_cart(cart_id, quantity)
#     cart_manager.close_connection()


if __name__ == '__main__':
    app.run()
