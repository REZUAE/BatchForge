import subprocess
from datetime import datetime, timezone

from batchforge.dag_parser import load_dag
from batchforge.task_executor import topological_sort
from batchforge.db import SessionLocal
from batchforge.models import DAGRun, TaskRun


def run_dag(dag_path):
    dag = load_dag(dag_path)
    dag_id = dag["dag_id"]
    tasks = topological_sort(dag["tasks"])

    db = SessionLocal()
    dag_run = DAGRun(dag_id=dag_id)
    db.add(dag_run)
    db.commit()
    db.refresh(dag_run)

    all_tasks_success = True

    for task in tasks:
        print(f"\n🔹 Running {task['id']}...")
        task_run = TaskRun(
            dag_run_id=dag_run.id,
            task_id=task["id"],
            status="running",
            started_at=datetime.now()
        )
        db.add(task_run)
        db.commit()
        db.refresh(task_run)

        max_retries = task.get("max_retries", 0)
        attempts = 0
        success = False

        while attempts <= max_retries:
            print(f"  ▶️ Attempt {attempts + 1} of {max_retries + 1}")
            result = subprocess.run(task["command"], shell=True)
            task_run.retries = attempts
            attempts += 1

            if result.returncode == 0:
                success = True
                break
            else:
                print(f"  🔁 Task {task['id']} failed (attempt {attempts})")
                if attempts <= max_retries:
                    print("  ⏳ Retrying...")

        task_run.finished_at = datetime.utcnow()

        if success:
            task_run.status = "success"
            print(f"✅ Task {task['id']} succeeded.")
        else:
            task_run.status = "failed"
            all_tasks_success = False
            print(f"❌ Task {task['id']} failed after {attempts} attempt(s).")
            db.commit()
            break


        db.commit()

    dag_run.finished_at = datetime.now()
    dag_run.status = "success" if all_tasks_success else "failed"
    db.commit()

    print(f"\n🏁 DAG '{dag_id}' run completed with status: {dag_run.status}")
    db.close()


if __name__ == "__main__":
    run_dag("dags/example_dag.yaml")
    #test
    # run_dag("dags/hello_world.yaml")
    # run_dag("dags/hello_world_with_retries.yaml")
    # run_dag("dags/hello_world_with_max_active_runs.yaml")
    # run_dag("dags/hello_world_with_max_active_tasks.yaml")