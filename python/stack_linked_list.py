class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
        curNode = self.head

        while curNode:
            yield curNode
            curNode = curNode.next

class Stack:
    def __init__(self):
        self.LinkedList = LinkedList()

    def __str__(self):
        values = [str(x.value) for x in self.LinkedList]
        return '\n'.join(values) if values else 'Stack is empty'

    def isEmpty(self):
        if self.LinkedList.head == None:
            return True
        else:
            return False

    def push(self, value):
        node = Node(value)
        node.next = self.LinkedList.head
        self.LinkedList.head = node

    def pop(self):
        nodeValue = self.LinkedList.head.value
        self.LinkedList.head = self.LinkedList.head.next
        return nodeValue

    def peek(self):
        nodeValue = self.LinkedList.head.value
        return nodeValue

    def delete(self):
        self.LinkedList.head = None


customStack = Stack()
customStack.push(1)
customStack.push(2)
customStack.push(3)
print(customStack.isEmpty())
print(customStack)
print('------')
print(customStack.pop())
print('-------')
print(customStack)
print('----------')
print(customStack.peek())
customStack.delete()
print(customStack)