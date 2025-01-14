# singly linked list - delete - one node

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class SLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # __iter__ method is used in python class
    # to define an iterator for the object
    def __iter__(self):
        node = self.head

        while node:
            yield node
            node = node.next

    def insertSLL(self, value, location):
        newNode = Node(value)

        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            if location == 0:
                newNode.next = self.head
                self.head = newNode
            elif location == 1:
                self.tail.next = newNode
                self.tail = newNode
            else:
                tempNode = self.head
                index = 0
                while index < location-1:
                    tempNode = tempNode.next
                    index += 1

                nextNode = tempNode.next
                tempNode.next = newNode
                newNode.next = nextNode

                if tempNode == self.tail:
                    self.tail = newNode

    # iterating means to repeat a set of instructions
    # until a set of condition is met

    # traversing means going through each element
    # one by one of a data structure

    def traverseSLL(self):
        if self.head is None:
            print('the singly linked list does not exist')
        else:
            node = self.head
            while node is not None:
                print(node.value)
                node = node.next

    def deleteNode(self, location):
        if self.head is None:
            print('the sll does not exist')
        else:
            if location == 0:
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                else:
                    self.head = self.head.next

            elif location == 1:
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                else:
                    node = self.head
                    while node is not None:
                        if node.next == self.tail:
                            break
                        node = node.next
                    node.next = None
                    self.tail = node
            else:
                tempNode = self.head
                index = 0
                while index < location - 1:
                    tempNode = tempNode.next
                    index += 1

                nextNode = tempNode.next
                tempNode.next = nextNode.next


singlyLinkedList = SLinkedList()
singlyLinkedList.insertSLL(1, 1)
singlyLinkedList.insertSLL(2, 1)
singlyLinkedList.insertSLL(3, 1)
singlyLinkedList.insertSLL(4, 1)

singlyLinkedList.insertSLL(0, 0)
singlyLinkedList.insertSLL(0, 3)

print([node.value for node in singlyLinkedList])

singlyLinkedList.traverseSLL()

singlyLinkedList.deleteNode(0)
print([node.value for node in singlyLinkedList])

# the time complexity to perform the deletion operation is O(n)
# the space complexity to perform the deletion operation is O(1)