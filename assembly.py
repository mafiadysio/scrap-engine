# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 00:02:37 2018

@author: Ting Yew
"""

from TableOfValues import *

def SecondPass(filename, outputfile):
    '''
    filename    : A file handler. The file is HML symbolic code with all comments, newlines and indentations
                  removed. This function assumes that filename exists.
                  It is assumed that filename has underwent FirstPass and removepredefined functions.
                  As such, all symbolic references in A-instructions can be treated as varaible symbols.
    outputfile  : The name of the output file. More info on this file is given below.
    Second Pass does several things:
            - It replaces all variable symbols with their numerical representation.
                  e.g. @sum is converted to @16. 
            - Numerical representation refers to the memory addresses that are allocated to the variables.
            - Memory addresses assigned to each variable are unique.
            - Memory addresses allocated to variables start from 16 onwards. Because virtual registers
              run from R0 to R15.
            - Second Pass only starts filling in from the lowest memory addresses. Starting from 16.
    output      : A file. The file's name would be the value in outputfile.
    '''

    varDict = {} # dictionary. Key-value pair is variable name + address number. 
    n = 16 # address number for first variable. Will increment as new variables are encountered. 
    num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    file = open(filename, "r")
    outfile = open(outputfile, "w")
    for line in file:
        if line[0] == '@':
            # Case of A-instruction
            list = line.split('@')
            list = list[1].split('\n')
            symbol = list[0] # 2 cases: Either a mere number, or the variable name.
            if symbol[0] in num_list:
                # A-instruction is symbol-less. 
                outfile.write(line)
                continue
            elif symbol in varDict:
                # Variable Symbol present in dictionary
                outfile.write('@' + str(varDict[symbol]) + '\n')
            else:
                # Variable Symbol absent in A-instruction - symbol is encountered for the first time.
                # Variable Symbol will be added to dictionary.
                varDict[symbol] = n
                outfile.write('@' + str(n) + '\n')
                n += 1       
        else:
            # Not an A-instruction
            outfile.write(line)
    file.close()
    outfile.close()
    return outputfile

def FirstPass(labeldict, filename, outputfile):
    '''
    labeldict   : A dictionary. The dictionary containing all the labels.
    filename    : A file handler. The file is HML symbolic code with all comments, newlines and indentations
                  removed. This function assumes that filename exists.
    outputfile  : The name of the output file. More info on this file is given below.
    First Pass does two things. 
            1. It removes all labels (the parenthesises) from the file.
            2. It replaces all label symbols to their numerical representation. The numerical representation being
            their instruction address number.
    output      : A file. The file's name would be the value in outputfile.
    '''
    file = open(filename, "r")
    outfile = open(outputfile, "w")
    for line in file:
        if line[0] == '(':
            # left parenthesis indicates the prescence of a label.
            continue # Skip. So we don't write the label into outfile.
        elif line[0] == '@':
            # A-instruction
            list = line.split('@')
            list = list[1].split('\n')
            if list[0] in labeldict:
                # A-instruction with label symbol.
                outfile.write('@' + str(labeldict[list[0]]) + '\n') # replace label symbol with instruction address. 
            else:
                # A-instruction with no label symbol.
                outfile.write(line)
        else:
            # C-instruction
            outfile.write(line)
    file.close()
    outfile.close()
    return outputfile

def assignLabelAddress(filename):
    '''
    filename: A file handler. The file is HML symbolic code with all comments, newlines and indentations
              removed.
    output  : A dictionary. Key-value pair is label + address number.
              Labels are symbols enclosed in parenthesis. They are insertion points for Jump commands
              in HML.            
              Address number is obtained from the location of the label.
    '''
    i = -1 # increment counter
    labeldictionary = {} # label dictionary. Will be populated as function encounters labels.
    file = open(filename, "r")
    for line in file:
        i += 1
        if line[0] == '(':
            # left parenthesis indicates the prescence of a label.
            list = line.split('(')
            list = list[1].split(')')
            line = list[0] # line now contains label symbol
            labeldictionary[line] = i
            i -= 1      # labels are psuedo-commands - they have no binary representation in binary code.
                        # Hence cannot be allocated a instruction memory address.
        else:
            # line is not a label.
            continue
    file.close()
    return labeldictionary
            


def removepredefined(filename, outputfile):
    '''
    filename    : A file handler. The file is HML symbolic code with all comments, newlines and
                  indentations removed.
    outputfile  : The name of the output file. More info on this file is given below.
    output      : The output is a file. The file name would be as defined in parameter outputfile.
                  outputfile is a processed version of filename. In outputfile, every A-instruction 
                  has its pre-defined symbols replaced with its numerical representation.
                  Labels and C-instructions remain unaltered.
    Returns     : outputfile string.
    '''
    
    file = open(filename, "r")
    outfile = open(outputfile, "w")
    for line in file:
        if line[0] == '@':
            # Case of A-instruction
            list = line.split('@')
            list = list[1].split('\n')
            if list[0] in SymbolTable:
                # Pre-defined Symbol present in A-instruction
                outfile.write('@' + str(SymbolTable[list[0]]) + '\n')
            else:
                # Pre-defined symbol absent in A-instruction
                outfile.write(line)
        else:
            # Not an A-instruction
            outfile.write(line)
    file.close()
    outfile.close()
    return outputfile

def flattenfile(filename, outputfile):
    '''
    filename: A string. Filehandler. A text file. Containing Hack Assembly Code Symbolic.
    Outputs another text file "machine.hack", which is the same as the original 
    text file, but with all comments removed and all indentations removed.
    
    Assumes that input file contains valid HML symbolic code.
    
    This function returns outputfile.
    '''

    asmHandler = open(filename, "r")
    outHandler = open(outputfile, "w")
    for line in asmHandler:
        if line[0] == '\n':
            # remove all newlines
            continue
        else:
            list = line.split()
            line = ''.join(list)
            if line[0] == '/':
                # remove all comment lines, but not inline comments.
                continue
            list = line.split('/')
            if len(list) > 1:
                # there is at least one inline comment
                outHandler.write(list[0] + '\n')
                continue
            outHandler.write(line + '\n')
    asmHandler.close()        
    outHandler.close()
    
    return outputfile
