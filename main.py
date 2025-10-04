from heap import heapsort
from prqueue import simulate_scheduler, Task
import random


def main():
    print("=== Priority Scheduling Simulation ===\n")

    # Define a small set of tasks with varying priorities and arrival times
    tasks = [
        Task(task_id="A", priority=3, arrival_time=0, deadline=5),
        Task(task_id="B", priority=5, arrival_time=1, deadline=3),
        Task(task_id="C", priority=1, arrival_time=2, deadline=6),
        Task(task_id="D", priority=4, arrival_time=0, deadline=4)
    ]

    print("Created tasks:")
    for t in tasks:
        print(f"  Task {t.task_id}: priority={t.priority}, arrival={t.arrival_time}, deadline={t.deadline}")
    print("\n--- Starting Scheduler Simulation ---")

    # Run the simulation (max-heap means higher priority value = higher priority)
    schedule = simulate_scheduler(tasks, use_max_heap=True)

    print("\n--- Scheduler Timeline ---")
    for t, task in schedule:
        print(f"At time {t}: executing task {task.task_id} (priority={task.priority})")

    print("\n=== Heapsort Demonstration ===")
    data = [random.randint(0, 100) for _ in range(20)]
    print("Original data:", data)

    sorted_data = heapsort(data)
    print("Sorted data:", sorted_data)

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()
