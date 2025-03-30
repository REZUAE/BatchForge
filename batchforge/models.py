from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class DAGRun(Base):
    __tablename__ = "dag_runs"

    id = Column(Integer, primary_key=True)
    dag_id = Column(String, nullable=False)
    status = Column(String, default="running")  # running, success, failed
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)

class TaskRun(Base):
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True)
    dag_run_id = Column(Integer, ForeignKey("dag_runs.id"), nullable=False)
    task_id = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, success, failed
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)
    retries = Column(Integer, default=0)
