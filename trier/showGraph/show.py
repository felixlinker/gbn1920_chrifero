#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:46:02 2020

@author: praktikum
"""

from show_graph import *
from parser2 import *
import sys
import os

def show_graph_file(filename):
    g = parse(filename)
    show_graph(g)
    return None

def show_json_file(filename):
    g = parse_chem(filename)
    show_graph(g)

def show_all(directory):
    direc = os.fsencode(directory)
    for file in os.listdir(direc):
        filename = os.fsencode(file).decode('utf-8')
        if filename.endswith('.json'):
            g = parse_chem(directory +'/'+ filename)
            show_graph(g)
        if filename.endswith('.graph'):
            dir_s = directory.split('/')
            g = parse(directory +'/'+ filename)
            show_graph(g)
    print('End of directory reached.')

'''
######Example for function syntax:

show_graph_file('small_2.graph')
show_json_file('2_CID_190.json')
show_all('/u/home/praktikum/Workspace/gbn1920_chrifero-master/showGraph/json')
'''
