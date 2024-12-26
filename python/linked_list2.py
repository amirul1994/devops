from math import ceil
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.length = 0

    def insert(self, data):
        if self.size == 0:
            self.head = Node(data)
            self.tail = self.head

        else:
            temp = Node(data)
            self.tail.next = temp
            self.tail = temp

        self.size += 1

    def search(self, data):
        temp = self.head

        while temp:
            if temp.value == data:
                return temp

            temp = temp.next

    def traverse(self):
        temp = self.head
        result = []
        self.length = 0

        while temp is not None:
            result.append(temp.value)
            print(temp.value)
            self.length += 1
            temp = temp.next

        print('the length is: ', self.length)
        return result

    def middle(self):
        temp = self.head
        length = 0

        while temp is not None:
            length += 1
            temp = temp.next

        mid = length//2

        temp = self.head

        for _ in range(mid):
            temp = temp.next

        print(temp.value)


    def delete(self, data):
        if self.size == 0:
            return False

        if self.head is not None and self.head.value == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            #return True

        temp = self.head

        while temp is not None and temp.next is not None:
            if temp.next.value == data:
                temp.next = temp.next.next
                self.size -= 1
                #return True
            temp = temp.next
        #return False


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

sll = LinkedList()
sll.insert(1)
sll.insert(2)
sll.insert(3)
sll.insert(4)
sll.insert(5)

print(sll.search(4))

r = sll.traverse()
print(r)


#sll.delete(3)
sll.traverse()
sll.middle()