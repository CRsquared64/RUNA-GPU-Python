class Queue:
    def __init__(self, max=None):
        self.max = max
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self, item):
        self.queue.remove(item)
    def in_queue(self, item):
        if item in self.queue:
            return True
        else:
            return False
    def return_full(self):
        arr = []
        for i in range(len(self.queue)):
            arr.append([i + 1, self.queue[i][1], self.queue[i][2]])
        return arr