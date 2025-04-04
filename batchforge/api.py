from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from runner import run_dag
from batchforge.db import SessionLocal
from batchforge.models import DAGRun, TaskRun

app = FastAPI()

class DAGTriggerRequest(BaseModel):
    dag_path: str

@app.post("/dag/run")
def trigger_dag(request: DAGTriggerRequest):
    try:
        run_dag(request.dag_path)
        return {"message": f"DAG started from {request.dag_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dag/{dag_id}/runs")
def get_dag_runs(dag_id: str):
    db = SessionLocal()
    runs = db.query(DAGRun).filter(DAGRun.dag_id == dag_id).order_by(DAGRun.id.desc()).all()
    db.close()

    return [
        {
            "dag_run_id": run.id,
            "status": run.status,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
        }
        for run in runs
    ]

@app.get("/dag/{dag_id}/status")
def get_latest_status(dag_id: str):
    db = SessionLocal()
    run = (
        db.query(DAGRun)
        .filter(DAGRun.dag_id == dag_id)
        .order_by(DAGRun.id.desc())
        .first()
    )
    db.close()

    if run:
        return {
            "dag_run_id": run.id,
            "status": run.status,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
        }
    else:
        raise HTTPException(status_code=404, detail="DAG run not found")
