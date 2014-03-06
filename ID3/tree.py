# Author: Jordan Weiler
# Date:   January 24, 2013
#
# The Tree class is used to build a decision tree.

class Tree:
    """
    Tree class builds binary tree
    """
    def __init__(self, name):
        self.name = name
        self.left = None
        self.left_value = 0
        self.right = None
        self.right_value = 0
        self.parent = None
        self.y_value = 0
        self.is_leaf = False
        
    def AddLeftChild(self, tree):
        """
        Add left child to the tree
        """
        self.left = tree
        tree.parent = self
        
    def AddRightChild(self, tree):
        """
        Add right child to the tree
        """
        self.right = tree
        tree.parent = self

    def ToString(self):
        """
        Convert tree to string representation
        """
        return self.name, ",", self.left, ",", self.left_value, ",", self.right, ",", self.right_value, ",", self.y_value, ",", self.is_leaf
    