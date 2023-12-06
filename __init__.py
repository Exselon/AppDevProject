from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()

create_table()

##
def username_exists(username):
    conn = sqlite3.connect('Userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user is not None

####################CODE FOR LOGIN############################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        conn = sqlite3.connect('Userdata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')

            if session['role'] == "user":
                print("user")
            else:
                print("admin")
            return redirect(url_for('adminHome'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('Login.html')

####################CODE FOR Signup############################
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = "user"

        # Insert user into the users table
        if username_exists(username):
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            # Insert user into the users table
            conn = sqlite3.connect('Userdata.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')

        return redirect(url_for('login'))
    return render_template('Signup.html')

@app.route('/adminHome')
def dashboard():
    if 'user_id' in session:
        return render_template('adminHome.html', username=session['username'], role=session['role'])
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()