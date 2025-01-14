# convert a list into linked list

class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, val):
        if self.tail is None:
            self.tail = Node(val)
            self.head = Node(val)

        else:
            self.tail = Node(val)
            self.tail.next = self.tail

        self.size += 1


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

a = [1, 2, 3, 4]
ll = LinkedList()

for i in a:
    ll.insert(i)

print(ll)