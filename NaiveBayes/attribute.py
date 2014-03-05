# Author: Jordan Weiler
# Date:   February 7, 2013
#
# The Attribute class holds binary counts for the attribute value in relation to the class value.
#

class Attribute:
    def __init__(self, name):
        self.name = name
        self.zero_zero = 0
        self.zero_one  = 0
        self.one_zero  = 0
        self.one_one   = 0
        self.prob_zero = 0.0
        self.prob_one  = 0.0
        self.prob_zero_given_zero = 0.0
        self.prob_zero_given_one  = 0.0
        self.prob_one_given_zero  = 0.0
        self.prob_one_given_one   = 0.0
    
    def AddNewData(self, attrib_value, y_value):
        """
        Add new data row to the attribute's totals
        """
        if attrib_value   == "0":
            if   y_value  == "0": self.zero_zero += 1
            elif y_value  == "1": self.zero_one  += 1

        elif attrib_value == "1":
            if   y_value  == "0": self.one_zero  += 1
            elif y_value  == "1": self.one_one   += 1
                
    def CalculateProbabilities(self, beta_0, beta_1):
        """
        Calculate the attribute's probabilities.
        Note that probabilities cannot be higher than 1.0 or lower than 0.0.
        """
        denom = self.zero_zero + self.zero_one + self.one_zero + self.one_one + beta_0 + beta_1 - 2
        if denom != 0:
            self.prob_zero = min( max( (self.zero_zero + self.zero_one + beta_0 - 1) / denom, 0.0 ), 1.0 )
            self.prob_one  = min( max( (self.one_zero + self.one_one + beta_1 - 1) / denom, 0.0 ), 1.0 )
        
        denom = self.zero_zero + self.one_zero + beta_0 + beta_1 - 2
        if denom != 0:
            self.prob_zero_given_zero = min( max( (self.zero_zero + beta_0 - 1) / denom, 0.0 ), 1.0 )
            self.prob_one_given_zero  = min( max( (self.one_zero + beta_1 - 1) / denom, 0.0 ), 1.0 )
        
        denom = self.zero_one + self.one_one + beta_0 + beta_1 - 2
        if denom != 0:
            self.prob_zero_given_one = min( max( (self.zero_one + beta_0 - 1) / denom, 0.0 ), 1.0 )
            self.prob_one_given_one  = min( max( (self.one_one + beta_1 - 1) / denom, 0.0 ), 1.0 )
        
    def PrintAttribute(self):
        """ Useful when debugging """
        return self.name + ", " + str(self.zero_zero) + ", " + str(self.zero_one) + ", " + \
               str(self.one_zero) + ", " + str(self.one_one) + ", " + str(self.prob_zero) + ", " + \
               str(self.prob_one) + ", " + str(self.prob_zero_given_zero) + ", " + \
               str(self.prob_zero_given_one) + ", " + str(self.prob_one_given_zero) + ", " + \
               str(self.prob_one_given_one)

