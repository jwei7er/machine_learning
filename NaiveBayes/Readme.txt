#########################################
# Readme instructions for running nb.py #
#                                       #
#       Written by Jordan Weiler        #
#########################################

1) To run nb.py from the command line, type:

--------------------------------------------------
python nb.py training.csv test.csv beta model_file
--------------------------------------------------


2) Additional notes:

    A) It is assumed that training_file and test_file are .csv files with binary values.

    B) The value of beta should be a real number >= 0.

    C) The naive Bayes model will be written out to the specified model_file.

    D) Additional optional arguments can be provided after the 4 arguments listed above:

        a) "trainLimit=#" - without quotation marks and replacing # with an integer number. This limits the training to the specified amount of rows given or the entire size of the training file, whichever is less.

        b) "showTestProb" - without quotation marks. This turns on printing each of the test data probabilities.

        An example command line containing both of these additional optional arguments would be:

        -------------------------------------------------------------------------
        python nb.py training.csv test.csv 2 nb.model trainLimit=300 showTestProb
        -------------------------------------------------------------------------
