
from typing import List

# Performs heap sort to arrange a list of integers in ascending order.
# Builds a max heap and repeatedly extracts the largest element to sort the list.
# Time Complexity: O(n log n) in all cases
# Space Complexity: O(1) since it sorts in place
def heapsort(arr: List[int]) -> List[int]:
    a = arr[:]
    def sift_down(a, start, end):
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and a[child] < a[child + 1]:
                child += 1
            if a[root] < a[child]:
                a[root], a[child] = a[child], a[root]
                root = child
            else:
                break
    n = len(a)
    for start in range((n - 2) // 2, -1, -1):
        sift_down(a, start, n - 1)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end - 1)
    return a

