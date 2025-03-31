# 🛠️ BatchForge

**BatchForge** is a lightweight, Python-based DAG (Directed Acyclic Graph) job scheduler.  
It allows you to define task workflows in YAML, execute them with dependency resolution and retries, track execution metadata in PostgreSQL, and expose everything via a REST API with FastAPI.

---

## 🚀 Features

- ✅ YAML-based DAG definitions
- ✅ Dependency resolution (topological sort)
- ✅ Shell command execution with retry support
- ✅ PostgreSQL metadata tracking (DAG runs, task runs)
- ✅ REST API to trigger and monitor DAGs
- ✅ Dockerized environment for easy setup
- ✅ CI-ready with `requirements.txt`

---

## 📂 Project Structure

batchforge/ ├── batchforge/ │ ├── api.py # FastAPI app │ ├── dag_parser.py # YAML loader │ ├── db.py # SQLAlchemy session & setup │ ├── models.py # DAGRun & TaskRun tables │ ├── task_executor.py # Topological sort ├── dags/ │ └── example_dag.yaml # Example DAG ├── runner.py # CLI DAG executor ├── docker-compose.yml ├── requirements.txt └── README.md

yaml
Copy
Edit

---

## 🧪 Example DAG (YAML)

dag_id: example_dag
tasks:
  - id: task1
    command: echo "Hello from Task 1"
  - id: task2
    command: echo "Hello from Task 2"
    depends_on: [task1]
  - id: task3
    command: echo "Hello from Task 3"
    depends_on: [task1]
📦 Setup Instructions
1. Clone & Navigate
bash
Copy
Edit
git clone https://github.com/yourusername/batchforge.git
cd batchforge
2. Start PostgreSQL with Docker
bash
Copy
Edit
docker compose up -d
3. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
4. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
5. Initialize Database Tables
python
Copy
Edit
# Run this once to create tables
from batchforge.db import init_db
init_db()
▶️ Running the DAG (CLI)
bash
Copy
Edit
python runner.py
🌐 API Endpoints (FastAPI)
Start the API:

bash
Copy
Edit
uvicorn batchforge.api:app --reload
Open docs at: http://localhost:8000/docs

Method	Endpoint	Description
POST	/dag/run	Trigger a DAG run
GET	/dag/{dag_id}/runs	View all DAG runs
GET	/dag/{dag_id}/status	Get latest run status
📚 Tech Stack
Python

FastAPI

PostgreSQL

Docker

SQLAlchemy

Uvicorn

PyYAML

🧑‍💻 Author
Made with ☕ and Python by Your Name

📃 License
MIT License
