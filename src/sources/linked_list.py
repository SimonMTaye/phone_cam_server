from typing import Any, Optional


class Node:
    def __init__(
        self, val: Any, prev_node: Optional["Node"], next_node: Optional["Node"]
    ):
        self.previous = prev_node
        self.next = next_node
        self.val = val

    def add_next(self, next_node: "Node"):
        self.next = next_node
        next_node.previous = self

    def add_previous(self, prev_node: "Node"):
        self.previous = prev_node
        prev_node.next = self


class LinkedList:

    last: Optional[Node] = None
    first: Optional[Node] = None
    _item_count: int = 0

    def append(self, val: Any):
        new_node = Node(val, None, None)
        if not self.first:
            self.first = new_node
            self.last = new_node
        else:
            self.last.add_next(new_node)
            self.last = new_node
        self._item_count += 1
    
    def head(self):
        return self.first.val

    #TODO Use __delitem__ instead
    def pop(self) -> Any:
        if self._item_count == 0:
            return
        else:
            end_node = self.last
            self.last = end_node.previous
            self._item_count -= 1
            return end_node.val

    def __len__(self):
        return self._item_count

    def __iter__(self):
        for i in range(self._item_count):
            node = self.first
            yield node.val
            node = node.next

    def __reversed__(self):
        for i in range(self._item_count):
            node = self.last
            yield node.val
            node = node.previous

    # TODO Make more efficent: Go backwards if key is larger than half way size of len
    def _get_node(self, key: int) -> Node:
        self._validate_key(key)
        node = self.first
        while key > 0:
            node = node.next
            key -= 1
        assert isinstance(node, Node)
        return node

    def __getitem__(self, key: int):
        return self._get_node(key).val

    def __setitem__(self, key: int, value: Any):
        self[key].val = value

    def __delitem__(self, key: int):
        if key == 0:
            if len(self) == 1:
                self.first = None
                self.last = None
            else:
                self.first = self.first.next
        else:
            unwanted_node = self._get_node(key)
            unwanted_node.previous.next = unwanted_node.next
            del unwanted_node
        self._item_count -= 1

    def _validate_key(self, key):
        if key >= len(self):
            raise IndexError("Index is out of range")
        if key < 0:
            raise IndexError("Index is less than 0")
        if not isinstance(key, int):
            raise TypeError("Index must be an integer")
