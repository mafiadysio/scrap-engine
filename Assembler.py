# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 20:06:42 2018

@author: Ting Yew
"""

from ACInstr import *
from TableOfValues import *
from assembly import *

def main():
    '''
    This is an assembler, for Hack Machine Language (HML). It converts HML Symbolic Code
    into HML Binary/Machine Code (i.e. it assembles).
    
    When this assembler is run, it will request for 1 input, which is the filename of the 
    file that is in HML Symbolic Code. This file name can be in .asm or .txt format.
    
    The assembler will output the assembled version in the same folder as the source code,
    with its filename in Xxx.hack extension.
    
    The assembler will also produce "working files", which arises from the intermediate
    processing stages. 
    
    The assembler processes the source code in 5 stages (represented as 5 functions). At the
    end of the 5th stage, the fully assembled code is produced.
        1. Flatten File. The source code has all comments, newlines and indentations removed.
        2. Remove Pre-defined. All pre-defined symbols in the code are replaced by their
           numerical counterpart.
        3. First Pass. All label symbols in the code are replaced with numerals, i.e. their
           memory addresses. All label symbols are recorded in a dictionary for numerical 
           replacement.
        4. Second Pass. All variable symbols in the code are replaced with numerals. At the
           end of this stage, the code would be symbol-less.
        5. Last Pass. The symbol-less code is converted to their binary representation.
    '''

    filename = input("Input Hack Machine Language Assembly Code's file \
                     name with extension (e.g.: Max.asm) : ")
    name = (filename.split('.'))[0]
    
    file = flattenfile(filename, name + '1flat.hack')

    file = removepredefined(file, name + '2NoPredefined.hack')
    
    ldictionary = assignLabelAddress(file)
    file = FirstPass(ldictionary, file, name + "3AftFirstpass.hack")
    
    file = SecondPass(file, name + "4AftSecondpass.hack")

    file = LastPass(file, name + '.hack')
    
    print("Assembled Code in {}".format(file))

if __name__ == "__main__":
    main()