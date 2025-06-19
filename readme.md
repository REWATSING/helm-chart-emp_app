# Employee Management App (Kubernetes + Helm)

This project is a complete **Kubernetes-deployable Helm-based** setup for a CRUD Employee Management System. It includes:

* ✅ **Backend**: Python Flask REST API (employee add/list)
* ✅ **Frontend**: Nginx serving static HTML/JS
* ✅ **Database**: MySQL with pre-creation of `employees` table
* ✅ **Helm**: Modular Helm chart with separate templates for frontend, backend, and DB

---

## ⚙️ Stack Overview

| Component | Tech              | Purpose                      |
| --------- | ----------------- | ---------------------------- |
| Backend   | Python + Flask    | Exposes API: /employees      |
| Frontend  | Nginx + HTML/JS   | Static UI for interaction    |
| DB        | MySQL             | Stores employee names        |
| Deploy    | Kubernetes + Helm | Package and deploy all parts |

---

## 🧱 Folder Structure

```bash
helm-employee-app/
├── backend/
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── frontend/
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── mysql/
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── values.yaml          # Global config
├── Chart.yaml           # Main chart metadata
└── README.md            # This file
```

---

## 🐋 Docker Images Used

| Component | Image               | Tag      |
| --------- | ------------------- | -------- |
| Backend   | `vishnu420/emp-api` | `latest` |
| Frontend  | `vishnu420/emp-ui`  | `v2`     |

Ensure images are pushed **before deploying Helm**.

```bash
docker build -t vishnu420/emp-api:latest ./backend
docker build -t vishnu420/emp-ui:v2 ./frontend
docker push vishnu420/emp-api:latest
docker push vishnu420/emp-ui:v2
```

---

## 📦 values.yaml (Config)

```yaml
backend:
  image:
    repository: vishnu420/emp-api
    tag: latest
    pullPolicy: Always
  replicas: 1

frontend:
  image:
    repository: vishnu420/emp-ui
    tag: v2
    pullPolicy: Always
  replicas: 1

mysql:
  rootPassword: rootpass
  database: empdb
```

---

## 🚀 Helm Commands

### Install

```bash
helm install employee-app ./ --namespace default
```

### Upgrade (after code/image changes)

```bash
docker push vishnu420/emp-api:latest  # Push updated image
helm upgrade employee-app ./ --namespace default
```

### Rollback

```bash
helm rollback employee-app 1 --namespace default
```

### Uninstall

```bash
helm uninstall employee-app --namespace default
```

---

## 🌐 Service Info (Minikube)

```bash
minikube service frontend
```

Expected port is via NodePort: `http://localhost:<nodeport>` (e.g. 32326)

---

## 🛠 Backend Flask App

```python
@app.route('/employees', methods=['GET'])
def list_employees():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM employees")
    return jsonify(cursor.fetchall())

@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.json.get('name')
    cursor = get_conn().cursor()
    cursor.execute("INSERT INTO employees (name) VALUES (%s)", (name,))
    conn.commit()
    return jsonify({"message": "Employee added"}), 201
```

### DB init on startup (in `__main__`)

```python
setup()  # Tries 10x until MySQL is ready, then creates table if not exists
```

---

## 📄 Nginx Config (frontend Docker)

```nginx
server {
  listen 80;
  location / {
    root /usr/share/nginx/html;
    index index.html;
  }

  location /employees/ {
    proxy_pass http://backend:80/employees/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  location = /employees {
    proxy_pass http://backend:80/employees;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

---

## 🧪 Testing

### Get all pods and services:

```bash
kubectl get all
```

### Port forward frontend

```bash
kubectl port-forward service/frontend 8080:80
```

Then open `http://localhost:8080` in browser.

---

## 🧠 Interview/Notes

* Set `imagePullPolicy: Always` to ensure latest images are pulled.
* You learned how to:

  * Dockerize Flask and static frontend apps
  * Use Helm to deploy microservices
  * Use NodePort and service discovery in K8s
  * Connect frontend to backend via Nginx reverse proxy
  * Setup retry logic in Python for MySQL readiness
* Make sure interviewer sees `helm upgrade`, `imagePush`, and testing logs.

---

## 📸 Screenshot (Optional)

Add a screenshot here once the app is working fully in browser.

---

## 🙋‍♂️ Author

**Rewat Singh**
DevOps Engineer | Kubernetes | Docker | Python

---

Happy deploying 🚀
