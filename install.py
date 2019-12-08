#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:12:39 2019

@author: birromer
"""

# install necessary packages

import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lark-parser'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'argparse'])


def install_packages():
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lark-parser'])
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'argparse'])