import psycopg2

def connect_to_database():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname="registration",
        user="postgres",
        password="pri",
        host="localhost",
        port="5432"
    )
    return conn

def authenticate_user(username, password):
    """Authenticates a user based on username and password."""
    conn = connect_to_database()
    cur = conn.cursor()
    query = "SELECT * FROM registration WHERE username = %s AND password = %s"
    cur.execute(query, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def register_user(firstname, lastname, email, username, password):
    """Registers a new user."""
    conn = connect_to_database()
    cur = conn.cursor()
    query = "INSERT INTO registration (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (firstname, lastname, email, username, password))
    conn.commit()
    cur.close()
    conn.close()
