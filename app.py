from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'pri'

# Function to authenticate user
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

# Route for login page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate the user (replace this with your authentication logic)
        authenticated_user = authenticate_user(username, password)
        
        if authenticated_user:
            # Assuming authenticate_user returns a tuple with user details
            user_details = {
                'fname': authenticated_user[0],
                'lname': authenticated_user[1],
                'email': authenticated_user[2],
                'username': username,
                'password': authenticated_user[4]
            }
            # Store user information in session
            session['user'] = user_details
            session['logged_in'] = True
            # Redirect to home page upon successful login
            return redirect(url_for('home'))
        else:
            return "Authentication failed. Invalid username or password."
    else:
        return render_template('MyAccount.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_email = request.form['new-email']
        new_username = request.form['new-username']
        new_password = request.form['new-password']
        
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

            # Check if the username or email already exists in the database
            cur.execute("SELECT * FROM Registration WHERE username = %s OR email = %s", (new_username, new_email))
            existing_user = cur.fetchone()

            if existing_user:
                return "Username or email already exists. Please choose a different one."

            # If username or email doesn't exist, insert the new user into the database
            cur.execute("INSERT INTO Registration (fname, lname, email, username, password) VALUES (%s, %s, %s, %s, %s)", (new_username, new_email, new_password))
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Redirect to login page after successful registration
            return redirect(url_for('login'))

        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            return "An error occurred during registration. Please try again later."

    else:
        return render_template('MyAccount.html')

# Home page route
@app.route('/home')
def home():
    return render_template('Home.html')

# Courses page route
@app.route('/menu')
def menu():
    return render_template('Menu.html')

# Route for the course page
@app.route('/petscorner')
def petscorner():
    return render_template('petscorner.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
