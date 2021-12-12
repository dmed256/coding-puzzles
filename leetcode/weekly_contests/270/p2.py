from repo_utils import *

#---[ Solution ]----------------------------------

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

#=================================================

def run(inputs):
    head = ListNode(inputs[0])
    node = head
    for val in inputs[1:]:
        node.next = ListNode(val)
        node = node.next

    head2 = Solution().deleteMiddle(head)
    if not head2:
        return []

    ans = [head2.val]
    while head2.next:
        head2 = head2.next
        ans.append(head2.val)
    return ans


run([1,3,4,7,1,2,6]) | eq([1,3,4,1,2,6])
run([1,2,3,4]) | eq([1,2,4])
run([2,1]) | eq([2])
run([2]) | eq([])
