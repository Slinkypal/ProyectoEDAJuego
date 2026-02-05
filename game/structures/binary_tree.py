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
        if not self.root: self.root = TreeNode(q, a)
        else: self._add(self.root, q, a)
    def _add(self, node, q, a):
        if a:
            if node.right: self._add(node.right, q, a)
            else: node.right = TreeNode(q, a)
        else:
            if node.left: self._add(node.left, q, a)
            else: node.left = TreeNode(q, a)

class QuestionNode:
    def __init__(self, id, question_text, correct_answer):
        self.id = id
        self.question = question_text
        self.correct_answer = correct_answer
        self.left = None
        self.right = None

class QuestionBST:
    def __init__(self):
        self.root = None

    def insert(self, id, question_text, correct_answer):
        if not self.root:
            self.root = QuestionNode(id, question_text, correct_answer)
        else:
            self._insert(self.root, id, question_text, correct_answer)

    def _insert(self, node, id, question_text, correct_answer):
        if id < node.id:
            if node.left: self._insert(node.left, id, question_text, correct_answer)
            else: node.left = QuestionNode(id, question_text, correct_answer)
        elif id > node.id:
            if node.right: self._insert(node.right, id, question_text, correct_answer)
            else: node.right = QuestionNode(id, question_text, correct_answer)

    def search(self, id):
        return self._search(self.root, id)

    def _search(self, node, id):
        if node is None or node.id == id:
            return node
        if id < node.id:
            return self._search(node.left, id)
        return self._search(node.right, id)
