class Queue:
    def __init__(self, max=None):
        self.max = max
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self, item):
        self.queue.remove(item)