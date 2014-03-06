Instructions for running id3.py
==============================


1. To run id3.py from the command line, type:

        python id3.py training.csv test.csv model_file


2. Additional notes:

    a. It is assumed that training_file and test_file are .csv files with binary values.

    b. The decision tree created in id3.py will be written out to the model file.

    c. Additional optional arguments can be provided after the 4 arguments listed above:

      * *chisquare=off* - This will turn off the Chi Square test to determine when to stop splitting attributes.
    
      * *debug* - This will turn on debug print lines.

      An example command line containing both of the additional optional arguments would be:

            python id3.py training.csv test.csv model_file chisquare=off debug

