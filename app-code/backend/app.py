from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host='mysql', user='root', password='rootpass', database='empdb',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/employees', methods=['GET'])
def get_employees():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees")
            result = cur.fetchall()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
