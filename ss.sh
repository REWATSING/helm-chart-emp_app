#!/bin/bash

# Create backend folder and files
mkdir -p backend
cat > backend/app.py <<EOF
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
EOF

cat > backend/requirements.txt <<EOF
flask
pymysql
EOF

cat > backend/Dockerfile <<EOF
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
EOF

# Create frontend folder and files
mkdir -p frontend
cat > frontend/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
  <title>Employees</title>
</head>
<body>
  <h1>Employee List</h1>
  <ul id="emp-list"></ul>

  <script src="app.js"></script>
</body>
</html>
EOF

cat > frontend/app.js <<EOF
fetch('/api/employees')
  .then(res => res.json())
  .then(data => {
    const list = document.getElementById('emp-list');
    data.forEach(emp => {
      const li = document.createElement('li');
      li.innerText = \`\${emp.id}: \${emp.name}\`;
      list.appendChild(li);
    });
  });
EOF

cat > frontend/Dockerfile <<EOF
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
EOF

echo "✅ backend/ and frontend/ structure created with app code."

