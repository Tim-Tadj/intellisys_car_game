import queue
Prio_q = queue.PriorityQueue()
Prio_q.put((2, "test"))
Prio_q.put((1, "test2"))
print(Prio_q.get()[1])
print(Prio_q.get()[1])
