from flask import Flask, jsonify, request
import pymysql
import os

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "rootpass"),
        database=os.getenv("DB_NAME", "empdb"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/employees', methods=['GET'])
def list_employees():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees")
            result = cur.fetchall()
    return jsonify(result)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO employees (name) VALUES (%s)", (name,))
            conn.commit()
    return jsonify({'message': 'Employee added'}), 201

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            conn.commit()
    return jsonify({'message': f'Employee {emp_id} deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)