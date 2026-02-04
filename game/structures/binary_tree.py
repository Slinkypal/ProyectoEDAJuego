class TreeNode:
    def __init__(self, q, a):
        self.q = q
        self.a = a
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def add(self, q, a):
        if not self.root:
            self.root = TreeNode(q, a)
        else:
            self._add(self.root, q, a)

    def _add(self, node, q, a):
        if a:
            if node.right:
                self._add(node.right, q, a)
            else:
                node.right = TreeNode(q, a)
        else:
            if node.left:
                self._add(node.left, q, a)
            else:
                node.left = TreeNode(q, a)
