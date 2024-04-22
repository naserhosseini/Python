from collections import deque
import time, threading

class Queue:
    def __init__(self):
        self.buffer = deque()

    def enqueue(self, val):
        self.buffer.appendleft(val)

    def dequeue(self):
        return self.buffer.pop()

    def is_empty(self):
        return len(self.buffer) == 0

    def size(self):
        return len(self.buffer)

def place_order(orders):
    for order in orders:
        print('the order of {} of has been placed'.format(order))
        serve_food.enqueue(order)
        time.sleep(0.5)

def serve_order():
    time.sleep(1)
    while serve_food.size()>0:
        order = serve_food.dequeue()
        print('Order {} has been served'.format(order))
        time.sleep(2)


serve_food=Queue()
orders=['pizza','samosa','pasta','biryani','burger']

t1 = threading.Thread(target=place_order, args=(orders,))
t2 = threading.Thread(target=serve_order)
t1.start()
t2.start()
