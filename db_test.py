import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="postgres",
        password="123456",
        port="5432"
    )

    print("✅ Connected!")

    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error:", e)