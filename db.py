import psycopg2

try:
    conn = psycopg2.connect(
        host="172.19.0.2",
        port="5432",
        dbname="DB1",
        user="admin",
        password="pri123!!"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Registration")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL:", e)

finally:
    # Close cursor and connection in finally block to ensure they are always closed
    if cursor:
        cursor.close()
    if conn:
        conn.close()
