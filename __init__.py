from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from Form import userSignup, userLogin, ProductForm , PromotionForm
from Product import ProductManager, Product  # Import the Product class
from werkzeug.utils import secure_filename
from Promotion import PromotionManager

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
        return render_template('product_detail.html', product=product)

@app.route('/adminDashboard')
def adminDashboard():
    if 'User_ID' in session:
        return render_template('adminDashboard.html', username=session['Username'], role=session['Role'])
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


# def ID_exists(ID):
#     conn = sqlite3.connect('Promotion.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM promotions WHERE ID=?', (ID,))
#     existing_ID = cursor.fetchone()
#     conn.close()
#     return existing_ID is not None

def get_promotion_connection():
    conn = sqlite3.connect('Promotion.db')
    return conn
def read_Promotion():
    conn = sqlite3.connect('Promotion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM promotions')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/adminPromotions', methods=['GET', 'POST'])
def adminPromotions():
    # checkID = PromotionForm(request.form)
    # ID = checkID.ID.data
    #
    # if ID_exists(ID):
    #     flash('Username already exists. Please choose a different username.', 'danger')
    # else:
    promotionForm = PromotionForm(request.form)
    if request.method == 'POST':
        ID = promotionForm.ID.data
        name = promotionForm.name.data
        discount = promotionForm.discount.data
        description = promotionForm.description.data

        promotion_manager = PromotionManager()
        promotion_manager.add_promotion(ID,name,discount,description)
        promotion_manager.close_connection()
    rows = read_Promotion()

    return render_template('adminPromotions.html', form=promotionForm, rows=rows)


@app.route('/adminEditAdmin')
def adminEditAdmin():
    return render_template('adminEditAdmin.html')


@app.route('/adminEditCustomer')
def adminEditCustomer():
    return render_template('adminEditCustomer.html')

def create_Promotion():
    conn = sqlite3.connect('Promotion.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promotions (
            ID INTEGER,
            name TEXT,
            discount REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


create_Promotion()




if __name__ == '__main__':
    app.run()
