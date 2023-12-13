from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from Form import userSignup, userLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


####################CODE FOR DB############################

def create_table():
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


create_table()


####################check for username############################
def username_exists(username):
    conn = sqlite3.connect('Userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE Username=?', (username,))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user is not None


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
            cursor.execute('INSERT INTO users (Username, Password, PhoneNumber, Email, DateOfBirth) VALUES (?, ?, ?, ?, ?)', (username, password, number, email, dob))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')

        return redirect(url_for('login'))
    return render_template('Signup.html', form=userSignupform)


@app.route('/adminDashboard')
def adminDashboard():
    if 'User_ID' in session:
        return render_template('adminDashboard.html',username=session['Username'], role=session['Role'])
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()


