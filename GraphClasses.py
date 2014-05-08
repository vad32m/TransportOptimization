#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import pygraphviz as pgv
from pygraphviz import *
from PyQt4.QtGui import *  
class InvalidArgError:
    pass

class BadGraphError:
    pass

class OrientedGraph:
    def __init__(self , inputmatr, names): #class constructo
        if ( type(inputmatr) is tuple) and ( type(names) is tuple):
            pass
        else:
            raise InvalidArgError #if input values are not tuples - error
        if (len(inputmatr)!=len(names)):
            raise InvalidArgError #if names and adjacency arrays have different sizes - error
        self.__matrix = []
        for A in inputmatr:
            if ( type(A) is tuple) and ( len(A) == len(inputmatr)):
                self.__matrix.append(A) #copy adjacency to local private variable
            else:
                raise InvalidArgError
        self.__matrix = tuple(self.__matrix) #convert matrix from list to tuple form
        for i in range(len(self.__matrix)):
            if self.__matrix[i][i] != 0:
                raise InvalidArgError #diagonal elements - zeros, else - error
        self.__distoparr = {} #dictionary, key - node number, value - distance
        self.__parrent = {} #dictionary, key - node number, value - parrent node
        self.__ndict = {} #dictionary, key - node name, value - node number
        self.i = 0
        for name in names:
            self.__ndict[name] = self.i
            self.i = self.i + 1
        del self.i

        
    def DijkstraAlg(self, point):
        if type(point) is not int:
            raise InvalidArgError
        for i in range(len(self.__matrix)):
            if i == point:
                self.__distoparr[i] = 0.0
            else:
                self.__distoparr[i] = float('inf') 
        ptq = [point] #query of nodes to examine
        ptf = [] #list of examined nodes
        for i in range ( len(self.__matrix)):
            shtpt = ptq[0] #variable which stores number of the closest node
            for a in ptq:
                if self.__distoparr[a] < shtpt:
                    self.__shtpt = a #select closest node
            ptq.remove(shtpt) #delete current point from the list
            ptf.append(shtpt) #add current point to list of examine
            for j in range (len(self.__matrix)): #iterating over nodes
                if self.__matrix[shtpt][j] == 0: #zero means nodes doesnt connected
                    continue #proceed to the next node
                elif (self.__distoparr[j] > self.__distoparr[shtpt] + self.__matrix[shtpt][j]): #if way from this node is the shortest - update data
                    self.__distoparr[j] = self.__distoparr[shtpt] + self.__matrix[shtpt][j]
                    self.__parrent[j] = shtpt
                if (j not in ptf) and (j not in ptq): #add fresh nodes to the query if required
                    ptq.append(j)
            if len(ptq) == 0:
                break
        return self.__distoparr, self.__parrent

    def GetShortestWay(self,firstnode,lastnode):
        if firstnode == lastnode:
            t = firstnode,lastnode
            return t
        distlist,parlist = self.DijkstraAlg(firstnode)
        if distlist[lastnode] == float('inf'):
            raise BadGraphError
        else:
            currel = lastnode
            route = [currel]
            while True:
                currel = parlist[currel]
                route.insert(0,currel)
                if currel == firstnode:
                    break
            return tuple(route)
            
        
        


    
t1 = 0,1,1,1,0,1
t2 = 1,0,0,0,0,1
t3 = 1,0,0,1,0,1
t4 = 1,0,1,0,1,0
t5 = 0,0,0,1,0,1
t6 = 1,1,1,0,1,0
t = t1,t2,t3,t4,t5,t6

names = 'a','b','c','d','e','f'
G = OrientedGraph(t,names)

            
