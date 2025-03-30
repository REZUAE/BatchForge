from batchforge.db import SessionLocal
from batchforge.models import DAGRun, TaskRun

db = SessionLocal()
runs = db.query(DAGRun).all()
for run in runs:
    print(run.id, run.dag_id, run.status, run.started_at, run.finished_at)
db.close()
