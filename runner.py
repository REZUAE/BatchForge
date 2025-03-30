import subprocess
from batchforge.dag_parser import load_dag
from batchforge.task_executor import topological_sort

def run_dag(dag_path):
    dag = load_dag(dag_path)
    tasks = topological_sort(dag["tasks"])
    print(dag['tasks'])

    for task in tasks:
        print(f"\n🔹 Running {task['id']}...")
        result = subprocess.run(task["command"], shell=True)
        if result.returncode != 0:
            print(f"❌ Task {task['id']} failed.\n")
            break
        else:
            print(f"✅ Task {task['id']} succeeded.\n")

if __name__ == "__main__":
    run_dag("./dags/example_dag.yaml")