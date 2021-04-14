class eg1():
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2


import queue
Prio_q = queue.PriorityQueue()
Prio_q.put((2, eg1("1", "2")))
Prio_q.put((1, eg1("1", "3")))
Prio_q.put((1, eg1("1", "4")))
print(Prio_q.get()[1])
while Prio_q:
    print(Prio_q.get()[1])
