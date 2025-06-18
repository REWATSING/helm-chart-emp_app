from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_conn():
    return pymysql.connect(host='mysql', user='root', password='rootpass', database='empdb')


# Auto-create DB table
@app.before_first_request
def setup():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )
    """)
    conn.commit()
    
@app.route('/employees', methods=['GET'])
def list_employees():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM employees")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.json['name']
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name) VALUES (%s)", (name,))
    conn.commit()
    return jsonify({"message": "Added"}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
