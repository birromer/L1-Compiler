#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:12:39 2019

@author: birromer
"""

from install import install_packages
from types import *
from compiler import compileSSM1
from SSM1 import SSM1

from lark import Lark
from lark import exceptions
from lark import Transformer
import argparse



if __name__ == "__main__":
  install_packages()
 
  def シ(syntax_tree):
    ssm1 = SSM1()
  
    type_inference = type_infer( syntax_tree, {} )
    if type_inference == False:
      raise Exception('The program is ill-typed :(')
  
    code = compileSSM1( syntax_tree )
    execution_result = ssm1.run( code , verbose=True)
  
    print(f"\nThe final value is {execution_result[1]}")
    return execution_result[1]  
  
  
  シ(('let', 'x', 'int', ('+', 3, ('+', 3, 4)), ('if', True, 'x', 2)))
