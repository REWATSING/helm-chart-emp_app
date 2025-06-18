from flask import Flask, request, jsonify
import pymysql
import time

app = Flask(__name__)

# Reusable DB connection function
def get_conn():
    try:
        return pymysql.connect(
            host='mysql',  # MySQL service name in Kubernetes
            user='root',
            password='rootpass',
            database='empdb',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print("❌ DB Connection Failed:", e)
        raise

# Setup DB table with retry logic
def setup():
    for attempt in range(10):
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100)
                )
            """)
            conn.commit()
            print("✅ Database table ready.")
            return
        except Exception as e:
            print(f"⏳ Attempt {attempt+1}/10: DB not ready - {e}")
            time.sleep(5)
    print("❌ Could not connect to DB after 10 attempts. Exiting.")
    raise SystemExit(1)

# Route: Get all employees
@app.route('/employees', methods=['GET'])
def list_employees():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employees")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name) VALUES (%s)", (name,))
        conn.commit()
        return jsonify({"message": "Employee added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    setup()  # Ensure DB is ready before starting server
    app.run(host='0.0.0.0', port=5000)
