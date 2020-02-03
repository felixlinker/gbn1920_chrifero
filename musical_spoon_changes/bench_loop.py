#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:43:51 2020

@author: praktikum
"""

from core import *
import os
"""
def parse_that():
	
	g = parse_chem('./structures_3.5.4/ectoine.json')
	reverse_parser(g)
		    
parse_that()
print("Finished.")
"""

def parse_all(dir):
	g_list = []
	for file in os.listdir(str(dir)):
		if file.endswith(".graph"):
			g = parse('./' + str(dir) + '/' + file)
			g_list.append(g)

	return g_list

        
        
        

