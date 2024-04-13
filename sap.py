from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="DB1",
            user="admin",
            password="pri123!!"
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Registration")
        rows = cursor.fetchall()

        return render_template('index.html', rows=rows)

    except psycopg2.Error as e:
        return "An error occurred: {}".format(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Extract form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        conn = None
        cursor = None
        
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                dbname="DB1",
                user="admin",
                password="pri123!!"
            )

            cursor = conn.cursor()

            # Insert data into Registration table
            cursor.execute("INSERT INTO Registration (fname, lname, email, username, password) VALUES (%s, %s, %s, %s, %s)", (fname, lname, email, username, password))

            conn.commit()

            return redirect(url_for('index'))

        except psycopg2.Error as e:
            return "An error occurred: {}".format(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

if __name__ == '__main__':
    app.run(debug=True)
