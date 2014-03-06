# Author: Jordan Weiler
# Date:   January 24, 2013
#
# This uses the ID3 algorithm to create a decision tree based on input training data with binary attributes and 
# compares the decision tree against input test data to measure the accuracy.

from attribute import Attribute
from tree import Tree
import sys, math

global _attrib_dict, _attrib_cnt, _use_chi_square, _debug
global _training_file, _training_file_data
global _test_file, _test_file_data
global _model_file

_use_chi_square = True
_debug = False

def BuildTree(path_tuple):
    """
    Build a tree structure from a given path tuple
    """
    if _debug: print "##\nBuild Tree...\ntuple:", path_tuple
    
    node_to_split,y_value = FindBestGain(path_tuple)
    
    if node_to_split < 0:
        if _debug: print "found leaf for tuple: ", path_tuple
        training_tree = Tree("leaf")
        training_tree.y_value = y_value
        training_tree.is_leaf = True
    else:
        # Create node for attribute to split on
        training_tree = Tree(_attrib_dict[str(node_to_split)])
        
        # Build left side of tree for node
        left_tuple = path_tuple + [(node_to_split,0)]
        left_tree = BuildTree(left_tuple)
        training_tree.AddLeftChild(left_tree)
            
        # Build right side of tree for node
        right_tuple = path_tuple + [(node_to_split, 1)]
        right_tree = BuildTree(right_tuple)
        training_tree.AddRightChild(right_tree)

    return training_tree

def ChiSquaredTest(attribute):
    """
    Chi Squared test to determine whether we can stop splitting attributes and return a leaf node
    """
    if _use_chi_square == False:
        return True
    
    a = attribute.zero_zero
    b = attribute.zero_one
    c = attribute.one_zero
    d = attribute.one_one
    
    if (a + b) == 0 or (c + d) == 0 or (b + d) == 0 or (a + c) == 0:
        chi_squared = 0
    else:
        chi_squared = math.pow((a * d - b * c),2.0) * (a + b + c + d) / ((a + b) * (c + d) * (b + d) * (a + c))
        
    if _debug: print "chiSquared:", chi_squared
    
    # For 1 degree of freedom (a.k.a. binary decision tree), 6.635 ensures 99% accuracy
    if chi_squared > 6.635:
        return True
    else:
        return False
   
def CloseFiles():
    """
    Close the input and output files
    """
    _training_file.close()
    _test_file.close()
    _model_file.close()

def FindBestGain(path_tuple):
    """
    Finds the best information gain for all attributes
    Return: tuple of (attribute index, leaf value) depending on whether an attribute should be split or a leaf node should be returned
    """
    max_gain = 0
    temp_bucket = dict()
    
    # spin through each row in the training file and throw out rows that don't match the path tuple
    for row in _training_file_data:
        skip = False
        split_row = row.split(",")
        if len(path_tuple) > 0:
            for att_index,val in path_tuple:
                # If the row's value for an attribute doesn't match the attribute's value in the path, skip
                if int(split_row[att_index]) != val:
                    skip = True
                    continue
        if skip == True:
            continue
        for i in range(len(split_row)):
            str_i = str(i)
            if str_i not in temp_bucket:
                temp_bucket[str_i] = Attribute(_attrib_dict[str_i])
            temp_bucket[str_i].AddNewData(split_row[i], split_row[len(split_row)-1])
            
    # Calculate information gain for all attributes
    gains = []
    for i in range(_attrib_cnt-1):
        if str(i) in temp_bucket:
            temp_bucket[str(i)].CalcInformationGain()
            if _debug: print "fbg: ", temp_bucket[str(i)].ToString()
            gains.append(temp_bucket[str(i)].gain)
        else:
            gains.append(0.0)
    
    # Find max gain
    max_gain = max(gains)
    if max_gain == 0:
        # If max gain is zero, return class value
        y_class = temp_bucket[str(_attrib_cnt-1)]
        if _debug: print "######## 0 gain\ny value is ", y_class.ToString()
        if y_class.one_one > 0:
            if _debug: print "returning 1..."
            return (-1,1)
        else:
            if _debug: print "returning 0..."
            return (-1,0)
    else:
        # Max gain is not zero so check if splitting passes the chi squared test
        # If it does, split on max gain attribute. If not, return class.
        gain_index = gains.index(max_gain)
        
        if len(path_tuple) > 0:
            passed_test = ChiSquaredTest(temp_bucket[str(gain_index)])
        else:
            passed_test = True
        
        if passed_test == False:
            if _debug: print "######## failed chi squared test attr name: ", _attrib_dict[str(gain_index)]
            attrib = temp_bucket[str(gain_index)]
            if (attrib.zero_zero + attrib.one_zero) >= (attrib.zero_one + attrib.one_one):
                return (-1, 0)
            else:
                return (-1, 1)
        else:
            if _debug: print "######## Max gain is: ", max_gain, " at index: ", gain_index, " att name: ", _attrib_dict[str(gain_index)]
            return (gain_index,-1)

def LoadAttributeDict():
    """
    Load a dictionary of attribute indexes and attribute names
    """
    global _attrib_dict, _attrib_cnt
    
    attributes = _training_file.readline().rstrip().split(",")
    _attrib_cnt = len(attributes)
    _attrib_dict = dict()
    for i in range(_attrib_cnt):
        _attrib_dict[attributes[i]] = i
        _attrib_dict[str(i)] = attributes[i]

def OpenFiles(args):
    """
    Open the input and output files
    """
    global _training_file, _test_file, _model_file
    
    _training_file = open(args[0], "r")
    _test_file = open(args[1], "r")
    _model_file = open(args[2], "w")

def ParseInputArguments():
    """
    Parse through all arguments
    """
    args = sys.argv[1:]
    if len(args) < 3:
        print ""
        print "ERROR! 3 arguments were not given"
        print "Syntax expects <train> <test> <beta> <model>"
        print "  <train> and <test> are .csv binary files"
        print "  <beta> is the beta prior value >= 0.0"
        print "  <model> is the output file for the model"
        print ""
        exit(1)
    OpenFiles(args)
    ParseOptionalArguments(args[3:])

def ParseOptionalArguments(opt_args):
    """
    Parse through any optional arguments
    """
    global _use_chi_square, _debug
    
    if len(opt_args) > 0:
        for i in range(len(opt_args)):
            if opt_args[i].lower() == "chisquare=off":
                _use_chi_square = False
            elif opt_args[i].lower() == "debug":
                _debug = True
            else:
                print "### Warning: Did not understand \"" + opt_args[i] + "\" command line argument. ###"
  
def PrintTree(node, tree_string, depth):
    """
    Build the print version of the decision tree
    """
    for i in range(depth):
        tree_string += "| "
        
    # Print the left side of the tree
    if node.left.is_leaf == True:
        tree_string += node.name + " = 0 : " + str(node.left.y_value) + "\n"
    else:
        tree_string += node.name + " = 0 : \n"
        tree_string = PrintTree(node.left, tree_string, (depth+1))
        
    for i in range(depth):
        tree_string += "| "
    
    # Print the right side of the tree
    if node.right.is_leaf == True:
        tree_string += node.name + " = 1 : " + str(node.right.y_value) + "\n"
    else:
        tree_string += node.name + " = 1 : \n"
        tree_string = PrintTree(node.right, tree_string, (depth+1))
        
    return tree_string

def StoreFileData():
    """
    Store the training and test data into global variables
    """
    global _training_file_data, _test_file_data
    
    _training_file_data = [line.rstrip() for line in _training_file]
    
    # Read the first line and toss away. It contains the attributes which we already saved from the training file.
    _test_file.readline()
    _test_file_data = [line.rstrip() for line in _test_file]
        
def TestData(decision_tree):
    """
    Compare the decision tree against the test data
    Return: a tuple of (correctly predicted rows, total rows)
    """
    correct, total = 0, 0
    
    for line in _test_file_data:
        if TestRowAgainstTree(line.split(","), decision_tree):
            correct += 1
        total += 1
    
    print "Decision tree was", correct, "/", total, "= " + str(correct * 100.0 / total) + "% accurate"

def TestRowAgainstTree(row, decision_tree):
    """
    Recursive validation of decision tree against the test data.
    Return: boolean value of whether the decision tree's prediction was correct
    """
    if decision_tree.is_leaf:
        if decision_tree.y_value == int(row[-1]):
            return True
        else:
            return False
    else:
        if int( row[ _attrib_dict[decision_tree.name] ] ) == 1:
            return TestRowAgainstTree(row, decision_tree.right)
        else:
            return TestRowAgainstTree(row, decision_tree.left)

def TrainData():
    """
    Create a decision tree based on the training data.
    Return: a trained decision tree
    """
    model_tree = BuildTree([])
    
    # Write decision tree out to output file
    _model_file.write(PrintTree(model_tree, "", 0))
    
    if _debug: print PrintTree(model_tree, "", 0)
    
    return model_tree

if __name__ == "__main__":
    """
    The main function called when id3.py is called from the command line with 3 files and additional optional arguments
    """
    ParseInputArguments()

    # Load first line attributes into global dictionary """
    LoadAttributeDict()
    
    # Store the file data to use later """
    StoreFileData()
    
    # Train and test the accuracy of the decision tree """
    TestData(TrainData())
    
    CloseFiles()
    