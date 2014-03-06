# Author: Jordan Weiler
# Date:   January 24, 2013
#
# The Attribute class holds binary counts for attributes and calculates entropy and information gain.

import math

def log2(x):
    return math.log(x) / math.log(2)

class Attribute:
    def __init__(self, name):
        self.name = name
        self.zero_zero = 0
        self.zero_one = 0
        self.one_zero = 0
        self.one_one = 0
        self.total_entropy = 0.0
        self.zero_entropy = 0.0
        self.one_entropy = 0.0
        self.gain = 0.0
        
    def AddNewData(self, attrib_value, y_value):
        """
        Add new data to attribute's totals
        """
        if attrib_value   == "0":
            if   y_value  == "0": self.zero_zero += 1
            elif y_value  == "1": self.zero_one  += 1
        
        elif attrib_value == "1":
            if   y_value  == "0": self.one_zero  += 1
            elif y_value  == "1": self.one_one   += 1
        
    def ToString(self):
        """
        Convert attribute to string representation
        """
        return self.name + ", " + str(self.zero_zero) + ", " + str(self.zero_one) + ", " + \
               str(self.one_zero) + ", " + str(self.one_one) + ", " + str(self.total_entropy) + ", " + \
               str(self.zero_entropy) + ", " + str(self.one_entropy) + ", " + str(self.gain)

    def CalcInformationGain(self):
        """
        Calculate the information gain
        """
        self.CalcTotalEntropy()
        self.CalcZeroEntropy()
        self.CalcOneEntropy()
        self.CalcGain()
        
    def CalcTotalEntropy(self):
        """
        Calculate the total entropy
        """
        total = self.zero_zero + self.zero_one + self.one_zero + self.one_one + 0.0
        zeroes = self.zero_zero + self.one_zero + 0.0
        ones = self.zero_one + self.one_one + 0.0
        self.total_entropy = self.CalcEntropy(total, zeroes, ones)
        
    def CalcZeroEntropy(self):
        """
        Calculate the entropy if the attribute is 0
        """
        total = self.zero_zero + self.zero_one + 0.0
        zeroes = self.zero_zero + 0.0
        ones = self.zero_one + 0.0
        self.zero_entropy = self.CalcEntropy(total, zeroes, ones)
        
    def CalcOneEntropy(self):
        """
        Calculate the entropy if the attribute is 1
        """
        total = self.one_zero + self.one_one + 0.0
        zeroes = self.one_zero + 0.0
        ones = self.one_one + 0.0
        self.one_entropy = self.CalcEntropy(total, zeroes, ones)
        
    def CalcEntropy(self, total, zeroes, ones):
        """
        Calculate entropy
        """
        if total == 0 or zeroes == 0 or ones == 0:
            return 0
        else:
            return -1.0 * ((zeroes / total) * log2(zeroes / total) + (ones / total) * log2(ones / total))
        
    def CalcGain(self):
        """
        Calculate gain from splitting on the attribute
        """
        total = self.zero_zero + self.zero_one + self.one_zero + self.one_one + 0.0
        zeroes = self.zero_zero + self.zero_one + 0.0
        ones = self.one_zero + self.one_one + 0.0
        self.gain = round(self.total_entropy - (zeroes / total) * self.zero_entropy - (ones / total) * self.one_entropy,12)
        