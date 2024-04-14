from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = '24beb10cd4b173e5fece3fec387128bc'

def register_user(fname, lname, email, username, password):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="DB1",
            user="admin",
            password="pri123!!",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Prepare the query to insert user registration data into the Registration table
        query = "INSERT INTO Registration (fname, lname, email, username, password) VALUES (%s, %s, %s, %s, %s)"
        data = (fname, lname, email, username, password)

        # Execute the query with user registration data as parameters
        cur.execute(query, data)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        print("User registered successfully.")
        return True

    except psycopg2.Error as e:
        print("Error registering user:", e)
        return False

def authenticate_user(username, password):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="DB1",
            user="admin",
            password="pri123!!",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Prepare the query to fetch user credentials
        query = "SELECT * FROM Registration WHERE username = %s AND password = %s"
        data = (username, password)

        # Execute the query with username and password as parameters
        cur.execute(query, data)

        # Fetch the first row (if any)
        user = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        # Return user data if authentication is successful, None otherwise
        return user

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Register the user
        if register_user(fname, lname, email, username, password):
            return "Registration successful. Please login <a href='/login'>here</a>."
        else:
            return "Registration failed. Please try again."
    else:
        return render_template('Signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate the user
        authenticated_user = authenticate_user(username, password)
        
        if authenticated_user:
            # Store user information in session
            session['username'] = username
            session['logged_in'] = True
            # Redirect to home page upon successful login
            return redirect(url_for('home_page'))
        else:
            return "Authentication failed. Invalid username or password."
    else:
        return render_template('MyAccount.html')

@app.route('/home')
def home_page():
    if 'username' in session and session['logged_in']:
        return render_template('Home.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
