def topological_sort(tasks):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    in_degree = defaultdict(int)
    task_map = {task['id']: task for task in tasks}

    # Build dependency graph
    for task in tasks:
        for dep in task.get("depends_on", []):
            graph[dep].append(task["id"])
            in_degree[task["id"]] += 1

    # Tasks with no dependencies
    queue = deque([task_id for task_id in task_map if in_degree[task_id] == 0])
    sorted_tasks = []

    while queue:
        current = queue.popleft()
        sorted_tasks.append(task_map[current])

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_tasks) != len(tasks):
        raise ValueError("Cycle detected in DAG")

    return sorted_tasks