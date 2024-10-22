class Queue:
    def __init__(self, max=None):
        self.max = max
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self, item):
        i = 0
        for items in self.queue:
            if (items[0] == item).all(): # all for numpy arrays
                self.queue.pop(i)
                break # incase there is multiple of same simulation, it would delete after
            i += 1
    def in_queue(self, item):
        for items in self.queue:
            if (items[0] == item).all():
                return True
        return False
    def return_full(self):
        arr = []
        for i in range(len(self.queue)):
            arr.append([i + 1, self.queue[i][1], self.queue[i][2]])
        return arr

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        return False