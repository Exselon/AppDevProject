from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from Form import userSignup, userLogin, ProductForm , PromotionForm
from Product import ProductManager, Product  # Import the Product class
from werkzeug.utils import secure_filename
from Promotion import PromotionManager
from User import DisplayUser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/image'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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




####################check for username############################
def username_exists(username):
    conn = sqlite3.connect('Userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE Username=?', (username,))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user is not None

####################Check file upload name############################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

####################CODE FOR LOGIN############################
@app.route('/login', methods=['GET', 'POST'])
def login():
    userLoginform = userLogin(request.form)
    if request.method == 'POST':
        username = userLoginform.username.data
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
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('Login.html', form=userLoginform)


####################CODE FOR Signup############################
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

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    selected_size = request.form.get('selected_size')
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if quantity is not provided
    print(f"Product ID: {product_id}, Selected Size: {selected_size}, Quantity: {quantity}")
    # Add your cart handling logic here
    return "Product added to cart successfully!"

@app.route('/userdashboard')
def userdashboard():
    if 'User_ID' in session:
        return render_template('userprofile.html', username=session['Username'], role=session['Role'], UserID=session['User_ID'])
    else:
        flash('You need to log in first.', 'warning')
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
        product_manager.add_product(filename_only, name, price, category, stock, description, size)
        product_manager.close_connection()



        return redirect(url_for('Productpage'))
    return render_template('adminProducts.html', form=productForm)


def get_promotion_connection():
    conn = sqlite3.connect('Promotion.db')
    return conn


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




if __name__ == '__main__':
    app.run()
