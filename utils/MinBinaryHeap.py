class MinBinaryHeap:
    def __init__(self, compare_func=None, insert_func=None):
        self.heap = []
        self.value_index_map = {}
        if compare_func is None:
            self.compare = lambda x, y: x - y
        else:
            self.compare = compare_func
        if not insert_func is None:
            self.insert = insert_func

    def insert(self, value):
        self.heap.append(value)
        self._percolate_up(len(self.heap)-1)

    def delete(self, value):
        if value in self.heap:
            index = self.heap.index(value)
            self._swap(index, len(self.heap) - 1)
            self.heap.pop()
            self._percolate_down(index)
        else:
            raise ValueError('Element not found in heap')

    def update(self, updateIndex):
            parentIndex = (updateIndex - 1) // 2
            if updateIndex > 0 and self.compare(self.heap[updateIndex], self.heap[parentIndex]) < 0:
                self._percolate_up(updateIndex)
            else:
                self._percolate_down(updateIndex)


    def get_min(self):
        if len(self.heap) > 0:
            return self.heap[0]
        else:
            raise IndexError('Heap is empty')

    def pop_min(self):
        if len(self.heap) > 0:
            min_value = self.heap[0]  # 最小值为堆顶元素
            self._swap(0, len(self.heap) - 1)
            self.heap.pop()
            self._percolate_down(0)
            return min_value
        else:
            raise IndexError('Heap is empty')

    def _percolate_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.compare(self.heap[index], self.heap[parent]) < 0:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _percolate_down(self, index):
        while index < len(self.heap):
            left_child = (2 * index) + 1
            right_child = (2 * index) + 2
            smallest = index

            if left_child < len(self.heap) and self.compare(self.heap[left_child], self.heap[smallest]) < 0:
                smallest = left_child

            if right_child < len(self.heap) and self.compare(self.heap[right_child], self.heap[smallest]) < 0:
                smallest = right_child

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

# test
# heap = MinBinaryHeap()
# heap.insert(5)
# heap.insert(10)
# heap.insert(3)
# heap.insert(8)
# print(heap.heap)  # 输出: [3, 8, 5, 10]
#
# # 更新元素
# heap.heap[1] = 2
# heap.update(1)
# print(heap.heap)  # 输出: [2, 3, 5, 10]
#
# heap.heap[2] = 1
# heap.update(2)
# print(heap.heap)  # 输出: [1, 2, 3, 10]