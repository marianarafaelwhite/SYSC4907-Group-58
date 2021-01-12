"""
Node & List of Nodes logic

Some code references the following:
https://github.com/abulanov/sfc_app/blob/master/sfc_app.py
https://github.com/abulanov/sfc_app/blob/master/asymlist.py
"""


class Node:
    """
    Node class

    Attributes
    ----------
    id : int
    bidirectional : bool
        True if can go forward and backward from node
    previous : Node
        Pointer to previous Node
    next : Node
        Pointer to next Node
    """

    def __init__(self, node_id, bidirectional):
        """
        Initialize Node

        Based on abulanov/sfc_app's asymlist.py Node's __init__

        Parameters
        ----------
        node_id : int
        bidirectional : bool
        """
        self.id = node_id
        self.bidirectional = bidirectional
        self.previous = None
        self.next = None

    def __str__(self):
        """
        Based on abulanov/sfc_app's asymlist.py Node's __str__

        Returns
        -------
        str
            String representation of node ID (readable)
        """
        return '{}'.format(self._id)

    def __repr__(self):
        """
        Based on abulanov/sfc_app's asymlist.py Node's __repr__

        Returns
        -------
        str
            String representation of node ID (unambiguous)
        """
        return 'Node: {i}, Previous: {p}, Next: {n}'.format(
            i=self.id,
            p=self.previous,
            n=self.next)


class NodeList:
    """
    List of nodes loosely follows a doubly linked list approach
    """

    def __init__(self, node_id, bidirectional=True):
        """
        Initialize list of Nodes

        Based on abulanov/sfc_app's asymlist.py AsymLList's __init__

        Parameters
        ----------
        node_id : int
        bidirectional : bool
            Can go forward & backward (True by default)
        """
        # Create list of one node that points back to itself
        node = Node(node_id, bidirectional)
        self.start = node
        self.last = node
        self.current = None
        self.back = node if bidirectional else None

    def append(self, node_id, bidirectional=True):
        """
        Add a new node to end of list

        Based on abulanov/sfc_app's asymlist.py AsymLList's append

        Parameters
        ----------
        node_id : int
        bidirectional : bool
            Can go forward & backward (True by default)

        Returns
        -------
        self.last : Node
            Newly created node (end of list)
        """
        # Create new node to add to list
        node = Node(node_id, bidirectional)

        # New node's previous node is the node from before (back)
        node.previous = self.back

        # Update current last node's next attribute
        self.last.next = node

        # Back reference is now the new node if bidirectional
        self.back = node if bidirectional else self.back

        # Set new last node & return
        self.last = node
        return self.last

    def forward(self):
        """
        Move forward through list

        Based on abulanov/sfc_app's asymlist.py AsymLList's fwd

        Return
        ------
        self.current : Node
            Current node after moving forward
        """
        # If current never set, or next doesn't exist, start at beginning
        if not self.current or not self.current.next:
            self.current = self.start
        else:
            self.current = self.current.next
        return self.current

    def backward(self):
        """
        Move backward through list

        Based on abulanov/sfc_app's asymlist.py AsymLList's rwd

        Return
        ------
        self.current : Node
            Current node after moving backward
        """
        # If current never set, or previous doesn't exist, start at back
        if not self.current or not self.current.previous:
            if not self.back:
                raise Exception('Impossible to go backwards!')
            self.current = self.back
        else:
            self.current = self.current.previous
        return self.current

    def get_forward_list(self):
        """
        Get list to transverse forwards through the list

        Based on abulanov/sfc_app's asymlist.py AsymLList's forward

        Returns
        -------
        forward_list : list
            List of nodes going forward
        """
        forward_list = []
        ptr = self.start
        while ptr:
            forward_list.append(ptr)
            ptr = ptr.next
        return forward_list

    def get_backward_list(self):
        """
        Get list to transverse backwards through the list

        Based on abulanov/sfc_app's asymlist.py AsymLList's backward

        Returns
        -------
        reverse_list : list
            List of nodes going backwards
        """
        reverse_list = []
        ptr = self.back
        while ptr:
            reverse_list.append(ptr)
            ptr = ptr.previous
        return reverse_list
