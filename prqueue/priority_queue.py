# priority_queue.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

# Represents a task with a priority value and optional scheduling metadata.
# Used by the PriorityQueue for scheduling and ordering operations.
@dataclass(order=True)
class Task:
    priority: int
    task_id: str = field(compare=False)
    arrival_time: Optional[int] = field(default=None, compare=False)
    deadline: Optional[int] = field(default=None, compare=False)
    payload: Optional[dict] = field(default=None, compare=False)

# Implements a priority queue using a binary heap.
# Provides O(log n) insertion and extraction for tasks based on priority.
class PriorityQueue:
    def __init__(self, use_max_heap: bool = True):
        # Initializes an empty heap and a map for quick index lookup.
        self.use_max_heap = use_max_heap
        self.heap: List[Task] = []
        self.position: Dict[str, int] = {}

    # Returns the effective priority key for a task based on heap type.
    def _key(self, task: Task) -> int:
        return task.priority if self.use_max_heap else -task.priority

    # Swaps two elements in the heap and updates their stored positions.
    def _swap(self, i: int, j: int):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i].task_id] = i
        self.position[self.heap[j].task_id] = j

    # Moves a node up the heap until the heap property is restored.
    def _sift_up(self, idx: int):
        while idx > 0:
            parent = (idx - 1) // 2
            if self._key(self.heap[parent]) < self._key(self.heap[idx]):
                self._swap(parent, idx)
                idx = parent
            else:
                break

    # Moves a node down the heap to maintain the heap property.
    def _sift_down(self, idx: int):
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            if left < n and self._key(self.heap[left]) > self._key(self.heap[largest]):
                largest = left
            if right < n and self._key(self.heap[right]) > self._key(self.heap[largest]):
                largest = right
            if largest != idx:
                self._swap(idx, largest)
                idx = largest
            else:
                break

    # Inserts a new task into the priority queue.
    def insert(self, task: Task):
        self.heap.append(task)
        idx = len(self.heap) - 1
        self.position[task.task_id] = idx
        self._sift_up(idx)

    # Checks whether the priority queue is empty.
    def is_empty(self) -> bool:
        return len(self.heap) == 0

    # Removes and returns the task with the highest priority.
    def extract_top(self) -> Task:
        if not self.heap:
            raise IndexError("extract_top from empty PriorityQueue")
        top = self.heap[0]
        last = self.heap.pop()
        del self.position[top.task_id]
        if self.heap:
            self.heap[0] = last
            self.position[last.task_id] = 0
            self._sift_down(0)
        return top

    # Increases or decreases the priority of an existing task.
    def increase_key(self, task_id: str, new_priority: int):
        idx = self.position.get(task_id)
        if idx is None:
            raise KeyError(f"Task {task_id} not found")
        task = self.heap[idx]
        old_priority = task.priority
        task.priority = new_priority
        if self.use_max_heap:
            if new_priority >= old_priority:
                self._sift_up(idx)
            else:
                self._sift_down(idx)
        else:
            if new_priority >= old_priority:
                self._sift_down(idx)
            else:
                self._sift_up(idx)

    # Decreases a task's priority; internally calls increase_key.
    def decrease_key(self, task_id: str, new_priority: int):
        self.increase_key(task_id, new_priority)

def simulate_scheduler(tasks: List[Task], use_max_heap: bool = True) -> List[Tuple[int, Task]]:
    """
    Simulates a simple priority-based task scheduler.

    The scheduler uses a priority queue (max-heap or min-heap) to determine which task 
    should be executed at each unit of simulated time. Tasks are inserted into the queue 
    according to their arrival times and extracted in order of priority.

    Args:
        tasks (List[Task]): A list of Task objects to be scheduled. Each task may have 
            an arrival_time (int) and a priority (int).
        use_max_heap (bool, optional): Determines whether to use a max-heap 
            (True: higher priority value = higher priority) or a min-heap 
            (False: lower priority value = higher priority). Defaults to True.

    Returns:
        List[Tuple[int, Task]]: A timeline represented as a list of tuples, 
        where each tuple contains:
            - The current simulation time (int)
            - The Task object being executed at that time
    """
    time_now = 0
    pq = PriorityQueue(use_max_heap=use_max_heap)
    timeline = []
    # Sort tasks by arrival time so they are added to the queue in order of arrival
    pending = sorted(tasks, key=lambda t: t.arrival_time if t.arrival_time is not None else 0)
    i = 0
    while i < len(pending) or not pq.is_empty():
        while i < len(pending) and (pending[i].arrival_time or 0) <= time_now:
            pq.insert(pending[i])
            i += 1
        if pq.is_empty():
            time_now = (pending[i].arrival_time or time_now) if i < len(pending) else time_now
            continue
        current = pq.extract_top()
        timeline.append((time_now, current))
        time_now += 1
    return timeline
