from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psycopg2

app = Flask(__name__)
app.secret_key = 'pri'

# Function to authenticate user
def authenticate_user(username, password):
    try:
        # Connect to your PostgreSQL database using localhost
        conn = psycopg2.connect(
            dbname="pawlatte",
            user="postgres",
            password="pri",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Prepare the query to fetch user credentials
        query = "SELECT * FROM registration WHERE username = %s AND password = %s"
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

# Function to create orders table
def create_orders_table():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="pawlatte",
            user="postgres",
            password="pri",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Create orders table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                item VARCHAR(100) NOT NULL,
                username VARCHAR(100) NOT NULL
            )
        """)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("Error creating orders table:", e)

# Call the function to create the orders table
create_orders_table()

# Route for login page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate the user
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

## Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle POST request for registration
        fname = request.form['fname']
        lname = request.form['lname']
        new_email = request.form['new-email']
        new_username = request.form['new-username']
        new_password = request.form['new-password']
        
        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname="pawlatte",
                user="postgres",
                password="pri",
                host="localhost",
                port="5432"
            )

            # Create a cursor object
            cur = conn.cursor()

            # Check if the username or email already exists in the database
            cur.execute("SELECT * FROM registration WHERE username = %s OR email = %s", (new_username, new_email))
            existing_user = cur.fetchone()

            if existing_user:
                return "Username or email already exists. Please choose a different one."

            # If username or email doesn't exist, insert the new user into the database
            cur.execute("INSERT INTO registration (fname, lname, email, username, password) VALUES (%s, %s, %s, %s, %s)", (fname, lname, new_email, new_username, new_password))
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Redirect to login page after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            return str(e)  # Return the error message for debugging
    else:
        # Handle GET request for registration
        return render_template('Signup.html')

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
    return render_template('petsCorner.html')

# Route for the user profile page
@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'user' in session and session['logged_in']:
        # Render the profile template and pass user data to it
        return render_template('profile.html', user=session['user'])
    else:
        # Redirect to the login page if user is not logged in
        return redirect(url_for('login'))

# Route for logout
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to the login page after logout
    return redirect(url_for('login'))

# Route to handle placing orders
@app.route('/place_order', methods=['POST'])
def place_order():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user' in session and session['logged_in']:
            # Retrieve the selected items from the request
            selected_items = request.json['selectedItems']
            username = session['user']['username']

            try:
                # Connect to PostgreSQL database
                conn = psycopg2.connect(
                    dbname="pawlatte",
                    user="postgres",
                    password="pri",
                    host="localhost",
                    port="5432"
                )

                # Create a cursor object
                cur = conn.cursor()

                # Insert each selected item into the orders table
                for item in selected_items:
                    cur.execute("INSERT INTO orders (item, username) VALUES (%s, %s)", (item, username))
                
                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cur.close()
                conn.close()

                # Return a success message
                return jsonify({"message": "Order placed successfully!"})

            except psycopg2.Error as e:
                print("Error placing order:", e)
                return jsonify({"error": "Failed to place order. Please try again later."})

        else:
            return jsonify({"error": "User not logged in. Please log in to place an order."})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
