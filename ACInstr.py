# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 18:47:39 2018

@author: Ting Yew
"""

from TableOfValues import *

def LastPass(filename, outputfile):
    '''
    '''
    file = open(filename, "r")
    fileout = open(outputfile, "w")
    for line in file:
        line = (line.split('\n'))[0]
        fileout.write(ACInstr(line) + '\n')
    file.close()
    fileout.close()
    return outputfile


def ACInstr(s):
    '''
    s = Valid symbolic A or C-instruction.
    Returns a string. The 16-bit binary representation of that instruction.
    '''
    if s[0] == '@':
        # A-instruction
        return AInstr(s)
    else:
        # C-instruction
        return CInstr(s)

def AInstr(t):
    '''
    t = Valid symbolic A-instruction.
    Returns a string. The 16-bit binary representation of that A-instruction.
    '''
    t = t[1:]
    t = int(bin(int(t))[2:])
    t = (str(t).zfill(16))
    return t
  
def CInstr(s):
    '''
    Takes in a symbolic C-instruction, and outputs a string - its binary representation.
    '''
    symbols = CParser(s)
    out = Cbinary(symbols)
    
    return out

def Cbinary(symbols):
    '''
    symbols: a tuple. Containing 3 str elements in the order "dest, comp, jump".
    output: a string. The binary representation of the entire C-instruction.
    '''
    dest = symbols[0]
    comp = symbols[1]
    jump = symbols[2]
    
    dest = DestTable[dest]
    comp = CompTable[comp]
    jump = JumpTable[jump]
    
    dest = (str(dest))[1:]
    comp = (str(comp))[1:]
    jump = (str(jump))[1:]
    
    s = '111' + comp + dest + jump
    
    return s

def CParser(s):
    ''' 
    s: Symbolic C-instruction. Assumed to be valid. 
    output: A Tuple of 3 str elements:
                dest - destination symbol
                comp - computation symbol
                jump - jump symbol
    '''
    list = s.split('=')
    if len(list) == 1:
        # no dest field; only comp and jump
        list = s.split(';')
        comp = list[0]
        jump = list[1]
        dest = 'null'
    else:
        # there is dest field
        list2 = list[1].split(';')
        if len(list2) == 1:
            # no jump field; only dest and comp
            dest = list[0]
            comp = list[1]
            jump = 'null'
        else:
            # dest, comp and jump fields all present
            dest = list[0]
            comp = list2[0]
            jump = list2[1]
    
    return (dest, comp, jump)

if __name__ == "__main__":
	main()
