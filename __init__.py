from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify,before_render_template , send_file
import sqlite3
import os
from Form import userSignup, userLogin, ProductForm, PromotionForm, PasswordChange, ProductFilter, CheckoutForm , ContactForm
from Product import ProductManager, Product  # Import the Product class
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from Promotion import PromotionManager
from User import DisplayUser,UserAccount
from Cart import CartManager
from Contact import ContactManager
from Order import OrderManager
import plotly.express as px
import pandas as pd
import io
import stripe
import requests
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/image'

#recaptcha api
RECAPTCHA_SITE_KEY = '6LeQyW4pAAAAAOWNyXcX1G-3UfTy63yjWp5mwiPK'
RECAPTCHA_SECRET_KEY = '6LeQyW4pAAAAACgnyB-xTbxBuIENP9CS_TfaQWA8'

#SMTP api
SENDINBLUE_API_KEY = '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'
SENDINBLUE_API_URL = 'https://api.sendinblue.com/v3/smtp/email'

stripe.api_key = "sk_test_51OdTteBzJLH01t0Myv424qrnRDEOHP461k6PUoqXAhYq7P7NsnBCApYGdAxXe0FJsVhjCbGBzXdVrUV6D4RFRyrr00Hn7m5zPx"
stripe_publishable_key = 'pk_test_51OdTteBzJLH01t0MKNrsG9H6v7YVEtRf5JZtalicClnYsR7y8CxjHPniuiuqpZYxYMCBw95cTG2YdWYlVBvCsZIp00DNnocI5x'

# ---------------Clear Session when load---------------#

session_cleared = False
@app.before_request
def before_request():
    global session_cleared
    if not session_cleared:
        session.clear()
        session_cleared = True

# ---------------Code For reCAPTCHA---------------#
# Function to verify reCAPTCHA response
def verify_recaptcha(recaptcha_response):
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = response.json()
    return result['success']


# ---------------Code For SMTP---------------#
def send_email(sender, recipient, subject, html_body):
    headers = {
        'Content-Type': 'application/json',
        'api-key': SENDINBLUE_API_KEY,
    }

    data = {
        'sender': {'email': sender},
        'to': [{'email': recipient}],
        'subject': subject,
        'htmlContent': html_body,
    }

    try:
        response = requests.post(SENDINBLUE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        print("Email sent successfully. Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error sending email:", e)
        print("API Response:", e.response.text)

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

def create_Contact():
    conn = sqlite3.connect('Contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Contact (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            Subject TEXT,
            Enquiry TEXT,
            Status TEXT,
            ResolveID INTEGER,
            Resolveby TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_Contact()

def create_Order():
    conn = sqlite3.connect('Order.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER,
            ProductID INTEGER,
            Quantity INTEGER,
            Size TEXT,
            OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES users(UserID),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID)
        )
    ''')
    conn.commit()
    conn.close()

create_Order()
# ---------------Code for Home---------------#
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    contactform = ContactForm(request.form)

    if request.method == 'POST':

        recaptcha_response = request.form['g-recaptcha-response']
        if not verify_recaptcha(recaptcha_response):
            return render_template('contactUs.html', form=contactform, site_key=RECAPTCHA_SITE_KEY)

        name = contactform.name.data
        email = contactform.email.data
        subject = contactform.subject.data
        msg = contactform.enquiry.data
        status = "open"
        resolveid = ""
        resolveby = ""

        newEnquiry = ContactManager()
        newEnquiry.Create_Enquiry(name,email,subject,msg,status,resolveid,resolveby)
        newEnquiry.close_connection()

        email_subject = f"Thank You for Your Inquiry: {subject}"
        email_html_body = f"""<p>Dear {name},</p>

        <p>Thank you for reaching out to us. We have received your inquiry regarding {subject}.</p>
        <p>Our team will review your message and get back to you as soon as possible.</p>

        <p><strong>Subject:</strong> {subject}</p>
        <p><strong>Message:</strong> {msg}</p>

        <p>If you have any further questions or need immediate assistance, please feel free to contact us.</p>

        <p>Best regards,<br>
        Eco-Wear Management</p>
        """

        # Send the formal email
        send_email('contact@ecowear.com', email, email_subject, email_html_body)
        return redirect(url_for('contact_us', success=True))

    return render_template('contactUs.html', form=contactform, site_key=RECAPTCHA_SITE_KEY)


# ---------------Check file upload name---------------#
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# ---------------Check for login---------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    userLoginform = userLogin(request.form)
    login_failure_message = None

    if request.method == 'POST':
        number = userLoginform.username.data # using contact number as username
        password = userLoginform.password.data

        user_login = UserAccount()
        userdata = user_login.logincheck(number)
        user_login.close_connection()

        if userdata and check_password_hash(userdata[2], password):
            session['User_ID'] = userdata[0]
            session['Username'] = userdata[1]
            session['hashedPW'] = userdata[2]
            session['Role'] = userdata[6]

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
    user_account = UserAccount()

    if request.method == 'POST':

        recaptcha_response = request.form['g-recaptcha-response']
        if not verify_recaptcha(recaptcha_response):
            return render_template('Signup.html', form=userSignupform, site_key=RECAPTCHA_SITE_KEY)

        username = userSignupform.name.data.lower()
        password = userSignupform.password.data
        number = userSignupform.number.data
        email = userSignupform.email.data
        dob = userSignupform.dob.data

        if user_account.number_exists(number):
            failure_message = "*Contact Number already exist*"
            return render_template('Signup.html', form=userSignupform, failure_message=failure_message)

        else:
            #hash code
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            user_account = UserAccount()
            user_account.register_user(username, hashed_password, number, email, dob)
            user_account.close_connection()

            return redirect(url_for('login'))

    return render_template('Signup.html', form=userSignupform, site_key=RECAPTCHA_SITE_KEY)


# ---------------Code for product---------------#
@app.route('/Product', methods=['GET', 'POST'])
def Productpage():

    ProductFilterForm = ProductFilter(request.form)

    product_manager = ProductManager()
    products = product_manager.get_all_products()

    if request.method == 'POST':

        if request.form.get('reset_button'):
            # Reset Btn
            return render_template('Product.html', products=products, form=ProductFilterForm)

        selected_price = request.form.get('pricerange')

        # Capture selected categories as a list
        selected_categories = [key.split('_')[1] for key, value in request.form.items() if key.startswith('category_')]

        print(f"Selected Price: {selected_price}")
        print(f"Selected Categories: {selected_categories}")

        if selected_categories:
            # Debugging: Print the SQL query
            keyword = selected_categories[0]
            query = f"SELECT * FROM products WHERE category LIKE '%{keyword}%'"
            print(f"SQL Query: {query}")

            # Filter products based on selected category and price
            filtered_products = product_manager.get_products_by_category(keyword, selected_price)
        else:
            # If no category is selected, still apply the price filter
            query = "SELECT * FROM products WHERE price BETWEEN ? AND ?"
            print(f"SQL Query: {query}")

            # Filter products based on price only
            filtered_products = product_manager.get_products_by_category(None, selected_price)

        # Use 'selected_price' and 'filtered_products' for rendering or any other logic
        return render_template('Product.html', products=filtered_products, form=ProductFilterForm)

    product_manager.close_connection()
    return render_template('Product.html', products=products, form=ProductFilterForm)


@app.route('/category/men')
def men_category():
    product_manager = ProductManager()
    men_products = product_manager.get_products_by_category('men')
    product_manager.close_connection()
    ProductFilterForm = ProductFilter(request.form)
    ProductFilterForm.category_men.data = True
    return render_template('Product.html', products=men_products, category='Men',form=ProductFilterForm)


@app.route('/category/women')
def women_category():
    product_manager = ProductManager()
    women_products = product_manager.get_products_by_category('women')
    product_manager.close_connection()
    ProductFilterForm = ProductFilter(request.form)
    ProductFilterForm.category_women.data = True
    return render_template('Product.html', products=women_products, category='Women',form=ProductFilterForm)


@app.route('/category/kids')
def kids_category():
    product_manager = ProductManager()
    kids_products = product_manager.get_products_by_category('kids')
    product_manager.close_connection()
    ProductFilterForm = ProductFilter(request.form)
    ProductFilterForm.category_kids.data = True
    return render_template('Product.html', products=kids_products, category='Kids',form=ProductFilterForm)


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
@app.route('/passwordchange', methods=['GET', 'POST'])
def passwordchange():

    passwordchangeform = PasswordChange(request.form)
    UserID = session.get('User_ID')
    # UserID = session['User_ID']
    password_change = DisplayUser()
    current_password = password_change.get_password_by_id(UserID)
    password_change.close_connection()

    if request.method == 'POST':
        CurrentPassword = passwordchangeform.CurrentPassword.data
        NewPassword = passwordchangeform.NewPassword.data
        ConfirmPassword = passwordchangeform.ConfirmPassword.data

        # use this code cos i hashed the pw
        # this is to check the current password match the hashed pw
        if check_password_hash(session['hashedPW'], CurrentPassword):
        # code to check password same as cfm pw
            #if true then this will load
            if NewPassword == ConfirmPassword:

                hashed_password = generate_password_hash(ConfirmPassword, method='pbkdf2:sha256')
                update_password = DisplayUser()
                update_password.update_password(hashed_password, UserID)
                update_password.close_connection()
                flash('Your password has been changed successfully', 'success')
                print('changed')
                return redirect(url_for('passwordchange'))
            else:
                #pw dont match
                return render_template('passwordchange.html', form=passwordchangeform)
        else:
        # hashed pw not same
            return render_template('passwordchange.html', form=passwordchangeform)

    return render_template('passwordchange.html', form=passwordchangeform)


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


@app.route('/adminViewProducts', methods=['GET', 'POST'])
def admin_View_Products():

    product_manager = ProductManager()
    products = product_manager.get_all_products()
    product_manager.close_connection()

    if request.method == 'POST':
        product_id = request.form.get('id')

        product_manager = ProductManager()
        product_manager.del_product(product_id)
        product_manager.close_connection()

        return redirect(url_for('admin_View_Products'))

    return render_template('adminViewProduct.html', products=products)

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

    sign_up = userSignup(request.form)
    if request.method == 'POST':
        username = sign_up.name.data
        password = sign_up.password.data
        number = sign_up.number.data
        email = sign_up.email.data
        dob = sign_up.dob.data
        role = 'admin'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        createadmin = UserAccount()
        createadmin.create_admin(username,hashed_password,number,email,dob,role)
        createadmin.close_connection()
        return redirect(url_for('adminEditUsers'))


    return render_template('adminEditUsers.html' , displayuser = displayuser , form=sign_up)


@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('UserID')

    User_manager = DisplayUser()
    User_manager.del_user(user_id)
    User_manager.close_connection()
    return redirect(url_for('adminEditUsers'))


@app.route('/adminContact')
def admin_contact():

    Viewcontact = ContactManager()
    allContact = Viewcontact.get_all_enquiry()
    Viewcontact.close_connection()
    return render_template("adminContact.html", contact=allContact)


@app.route('/adminContact/<int:contact_id>', methods=['GET','POST'])
def admin_view_contact_detail(contact_id):

    if 'User_ID' in session:

        getcontact = ContactManager()
        contactEnquiry = getcontact.get_enquiry_by_id(contact_id)
        getcontact.close_connection()

        return render_template("adminContact_detail.html", contact=contactEnquiry)

    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/updated_enquiry_status/<int:contact_id>', methods=['POST'])
def updated_enquiry_status(contact_id):

    if 'User_ID' in session:

        if request.method == 'POST':
            adminid = session['User_ID']
            adminname = session['Username']

            updatecontact = ContactManager()
            updatecontact.updated_status(adminid, adminname, contact_id)
            updatecontact.close_connection()
            return redirect(url_for('admin_contact'))

    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))


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


# <---------------------admin thing------------------------->
@app.route('/adminDownloads')
def adminDownloads():

    return render_template('adminDownloads.html')


@app.route('/downloadProductData')
def download_Productdata():
    conn = sqlite3.connect('Product.db ')

    query = "SELECT * FROM products"
    data = pd.read_sql(query, conn)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, index=False)
    writer.close()

    output.seek(0)

    return send_file(output, as_attachment=True, download_name='ProductList.xlsx' )

@app.route('/downloadUserData')
def download_Userdata():
    conn = sqlite3.connect('Userdata.db')

    query = "SELECT * FROM users"
    data = pd.read_sql(query, conn)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, index=False)
    writer.close()

    output.seek(0)

    return send_file(output, as_attachment=True, download_name='User_DataList.xlsx' )


#<--------------------- Check Out code --------------------->

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        selected_item_ids = request.form.getlist('selected_items[]')
        session['selected_item_ids'] = selected_item_ids
        return redirect(url_for('checkout'))

    selected_item_ids = session.get('selected_item_ids', [])
    selected_items = []
    total_price = 0

    for cart_id in selected_item_ids:
        cartmanager = CartManager()
        cart_item = cartmanager.get_cart_item_by_id(cart_id)
        cartmanager.close_connection()

        if cart_item:
            product_manager = ProductManager()
            product = product_manager.get_product_by_id(cart_item[2])
            product_manager.close_connection()

            if product:
                selected_items.append({
                    'CartID': cart_item[0],
                    'Product': product,
                    'Quantity': cart_item[3],
                    'Subtotal': cart_item[3] * product.price
                })
                total_price += cart_item[3] * product.price
            else:
                print(f"Product with ID {cart_item[2]} not found in the product database.")
        else:
            print(f"Cart item with ID {cart_id} not found in the cart database.")

    return render_template('checkout.html', selected_items=selected_items, total_price=total_price)


@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    selected_item_ids = session.get('selected_item_ids', [])
    total_price = request.args.get('total_price')

    if not selected_item_ids:
        flash('No items selected for payment.', 'error')
        return redirect(url_for('checkout'))

    selected_items = []
    for cart_id in selected_item_ids:
        cartmanager = CartManager()
        cart_item = cartmanager.get_cart_item_by_id(cart_id)
        cartmanager.close_connection()

        if cart_item:
            product_manager = ProductManager()
            product = product_manager.get_product_by_id(cart_item[2])
            product_manager.close_connection()

            if product:
                selected_items.append({
                    'CartID': cart_item[0],
                    'Product': product,
                    'Quantity': cart_item[3],
                    'Subtotal': cart_item[3] * product.price
                })
            else:
                print(f"Product with ID {cart_item[2]} not found in the product database.")
        else:
            print(f"Cart item with ID {cart_id} not found in the cart database.")

    # Create a Stripe Checkout Session
    line_items = []
    for item in selected_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['Product'].name,
                    # You can add more product details here if needed
                },
                'unit_amount': int(item['Product'].price * 100),  # Amount in cents
            },
            'quantity': item['Quantity'],
        })

    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('payment_success', _external=True),
        cancel_url=url_for('payment_cancel', _external=True),
    )

    return redirect(stripe_session.url, code=303)  # Redirect to Stripe Checkout page

@app.route('/payment_success')
def payment_success():
    selected_item_ids = session.get('selected_item_ids', [])

    if not selected_item_ids:
        flash('No items selected for payment.', 'error')
        return redirect(url_for('checkout'))

    # Insert selected items into the order database
    ordermanager = OrderManager()
    for cart_id in selected_item_ids:
        cartmanager = CartManager()
        cart_item = cartmanager.get_cart_item_by_id(cart_id)
        cartmanager.close_connection()

        if cart_item:
            # Assuming your order database schema is similar to cart items
            ordermanager.insert_order_item(cart_item)
            # Remove selected items from the cart database
            cartmanager = CartManager()
            cartmanager.remove_cart_item_by_id(cart_id)
            cartmanager.close_connection()

    # Clear the session after successful payment
    session.pop('selected_item_ids', None)

    return render_template('payment_success.html')

@app.route('/payment_cancel')  # Define the payment cancel endpoint
def payment_cancel():
    return render_template('payment_cancel.html')

if __name__ == '__main__':
    app.run()

