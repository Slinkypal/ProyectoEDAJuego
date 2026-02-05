from structures.binary_tree import BinaryTree

class Player:
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.score=0
        self.tree=BinaryTree()
