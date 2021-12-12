import math

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteMiddle(self, head):
        if not head.next:
            return None

        node1 = head
        node2 = head.next.next

        while node2 and node2.next:
            node1 = node1.next
            node2 = node2.next.next

        node1.next = node1.next.next
        return head
