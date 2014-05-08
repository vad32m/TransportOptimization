#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import pygraphviz as pgv
from pygraphviz import *
from PyQt4.QtGui import *  # компоненты интерфейса
class InvalidArgError:
    pass

class OrientedGraph:
    def __init__(self , inputmatr, names):
        if ( type(inputmatr) is tuple) and ( type(names) is tuple):
            pass
        else:
            raise InvalidArgError
        if (len(inputmatr)!=len(names)):
            raise InvalidArgError
        self.matrix = []
        for A in inputmatr:
            if ( type(A) is tuple) and ( len(A) == len(inputmatr)):
                self.matrix.append(A)
            else:
                raise InvalidArgError
        self.matrix = tuple(self.matrix)
        print self.matrix


    
t1 = 2,3,5
t2 = 1,3,7
t3 = 2,5,6
t = t1,t2,t3

names = 'a','b','c'
G = OrientedGraph(t,names)




            
