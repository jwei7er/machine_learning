# Author: Jordan Weiler
# Date:   February 7, 2013
#
# This script uses the naive Bayes algorithm to compute the probabilities 
# of a class given binary attribute values.
#
# 4 arguments are expected from the command line:
#   trainingfile: .csv binary file used to train the model
#   testfile:     .csv binary file used to test the model
#   betaprior:    beta prior real value >= 0.0, usually 2.0
#   modelfile:    output file for the model
#
# example run:
#   python nb.py train.csv test.csv 2 output.model
#
from attribute import Attribute
import sys, math

global training_file_name, training_file, training_file_data
global test_file_name, test_file, test_file_data
global model_file_name, model_file	
global attrib_dict, attrib_cnt
global beta, train_limit, show_test_prob

train_limit = 999999999
show_test_prob = False

def CloseFiles():
    """
    Closes the input and output files
    """
    training_file.close()
    test_file.close()
    model_file.close()

def LoadAttribDict():
    """
    Loads a dictionary of attribute indexes and attribute names
    """
    global attrib_dict, attrib_cnt

    attributes = training_file.readline().rstrip().split(",")
    attrib_cnt = len(attributes)
    attrib_dict = dict()
    for i in range(attrib_cnt):
        attrib_dict[str(i)] = attributes[i]

def OpenFiles(args):
    """
    Opens the input files and output file
    """
    global training_file_name, training_file
    global test_file_name, test_file
    global model_file_name, model_file
    global beta

    training_file_name = args[0]
    test_file_name = args[1]
    try:
        beta = float(args[2])
        if beta < 0:
            raise ValueError
    except ValueError:
        print ""
        print "WARNING: Beta value must be a real number >= 0.0 not '" + args[2] + "'"
        print "Defaulting beta value to 2.0"
        print ""
        beta = 2.0
    model_file_name = args[3]

    training_file = open(training_file_name, "r")
    test_file = open(test_file_name, "r")
    model_file = open(model_file_name, "w")

def ParseInputArguments():
    """
    Parses through all arguments
    """
    args = sys.argv[1:]
    if len(args) < 4:
        print ""
        print "ERROR! 4 arguments were not given"
        print "Syntax expects <train> <test> <beta> <model>"
        print "  <train> and <test> are .csv binary files"
        print "  <beta> is the beta prior value >= 0.0"
        print "  <model> is the output file for the model"
        print ""
        exit(1)
    OpenFiles(args)

    ParseOptionalArguments(args[4:])

def ParseOptionalArguments(args):
    """
    Parses through any optional arguments
    """
    global train_limit, show_test_prob
    
    if len(args) > 0:
        for i in range(len(args)):
            if args[i][0:11].lower() == "trainlimit=":
                train_limit = int(args[i][11:])
            if args[i].lower() == "showtestprob":
                show_test_prob = True

def StoreFileData():
    """
    Stores the training and test data into global variables
    """
    global training_file_data, test_file_data

    training_file_data = [line.rstrip() for line in training_file]
    
    # Read the first line and toss away. It contains the attributes which we already saved from the training file.
    test_file.readline()
    test_file_data = [line.rstrip() for line in test_file]

def TestData(model):
    """
    Validates the trained naive Bayes model against test data to determine accuracy of the model
    """
    correct, total = 0, 0.0

    # Spin through each test row, predict the row's class, and determine the overall accuracy of the predictions
    for row in test_file_data:
        split_row = row.split(",")
        
        row_sum = model[-1] # Equal to w_0
        for i in range(len(split_row)-1):
            # Only add weights to row summation if the attribute is equal to 1
            if split_row[i] == "1":
                row_sum += model[i]
        
        # Use 1 / (1 + e^-z) to get weight summation back into probability
        row_prob = 1 / (1 + math.exp(-row_sum))
        if show_test_prob == True:
            print str(row_prob)
                
        if row_prob >= 0.5:
            if int(split_row[-1]) == 1: correct += 1
        else:
            if int(split_row[-1]) == 0: correct += 1
        total += 1

    print "Accuracy: ", (correct / total)

def TrainData():
    """
    Trains the naive Bayes model against training data to create a model to use against test data
    Returns: list of w_0 and w_i weight values for each attribute to determine prediction against test data
    """
    nb_model = dict()

    # Spin through each training row and aggregate data
    num_trained = 0
    for row in training_file_data:
        split_row = row.split(",")
        for i in range(len(split_row)):
            key = str(i)
            if key not in nb_model:
                nb_model[key] = Attribute(attrib_dict[key])
            nb_model[key].AddNewData(split_row[i], split_row[-1])
        
        num_trained += 1
        if num_trained >= train_limit:
            # The training limit has been met so break out of for loop
            break

    # Calculate the probabilities for each attribute
    for i in range(len(nb_model)):
        nb_model[str(i)].CalculateProbabilities(beta, beta)
        
    # w_0 = log( P(C=1)/P(C=0) ) + SUM(from i=1 to n) log( P(X_i=0|C=1) / P(X_i=0|C=0) )
    if nb_model[str(attrib_cnt-1)].prob_one == 0 or nb_model[str(attrib_cnt-1)].prob_zero == 0:
        if nb_model[str(attrib_cnt-1)].prob_one == 0:
            w_0 = -99 #simulate negative infinity without overflow error
        else:
            w_0 = 99  #simulate positive infinity without overflow error
    else:
        w_0 = math.log(nb_model[str(attrib_cnt-1)].prob_one / nb_model[str(attrib_cnt-1)].prob_zero)
    
    for i in range(len(nb_model)-1):
        if nb_model[str(i)].prob_zero_given_one != 0 and nb_model[str(i)].prob_zero_given_zero != 0:
            w_0 += math.log(nb_model[str(i)].prob_zero_given_one / nb_model[str(i)].prob_zero_given_zero)
        
    # w_i = log( P(X_i=1|C=1)/P(X_i=1|C=0) ) - log( P(X_i=0|C=1)/P(X_i=0|C=0) )
    weights = []
    for i in range(len(nb_model)-1):
        attrib = nb_model[str(i)]
        if (attrib.prob_one_given_one == 0 or attrib.prob_one_given_zero == 0) and (attrib.prob_zero_given_one == 0 or attrib.prob_zero_given_zero == 0):
            weights.append(0.0)
        elif attrib.prob_one_given_one == 0 or attrib.prob_one_given_zero == 0:
            weights.append(0.0 - math.log(attrib.prob_zero_given_one / attrib.prob_zero_given_zero))
        elif attrib.prob_zero_given_one == 0 or attrib.prob_zero_given_zero == 0:
            weights.append(math.log(attrib.prob_one_given_one / attrib.prob_one_given_zero))
        else:
            weights.append(math.log(attrib.prob_one_given_one / attrib.prob_one_given_zero) - math.log(attrib.prob_zero_given_one / attrib.prob_zero_given_zero))

    # Prepend w_0 to model
    model = str(w_0) + "\n"
    # Append all attributes to model
    for i in range(len(weights)):
        model += nb_model[str(i)].name + "\t" + str(weights[i]) + "\n"

    # Write model to output file
    model_file.write(model)
    
    # Append w_0 to weights list. This contains all weights and is ordered by attribute index with w_0 being last.
    weights.append(w_0)
    
    return weights

if __name__ == "__main__":
    """
    The main function called when nb.py is run from the command line
    """
    ParseInputArguments()
    
    LoadAttribDict()
    
    StoreFileData()

    TestData(TrainData())

    CloseFiles()

    pass
