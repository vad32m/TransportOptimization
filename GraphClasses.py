#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import pygraphviz as pgv
from pygraphviz import *
from PyQt4 import QtGui
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
        self.__ndict = {} #dictionary, key - node number, value - node name
        i = 0
        for name in names:
            self.__ndict[i] = name
            i = i + 1

        
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
            return t #the best way to get to node b from node b is to go nowhere
        distlist,parlist = self.DijkstraAlg(firstnode) #apply DijkstraAlgorythm
        if distlist[lastnode] == float('inf'): #cant gat to lastnode - error
            raise BadGraphError
        else:
            currel = lastnode
            route = []
            while True:
                t = parlist[currel],currel #making pairs of edges
                currel = parlist[currel]
                route.insert(0,t)
                if currel == firstnode: 
                    break
            return tuple(route) #return the route

    def VisualiseToFile(self,subgraph = (),fileloc = 'file.png',plasement = 'circo'):
        G = pgv.AGraph(strict=True,directed=True,forcelabels = True) #pyGraphVis makes magic simple
        nodes = [] #this list will store numbers of nodes in subgraph
        for i in subgraph:
            nodes.append(i[0]);
            nodes.append(i[1]);
        for i in range(len(self.__matrix)): #add nodes from graph
            if i in nodes:
                G.add_node(self.__ndict[i], style = "filled", fillcolor = "grey", color = "red", shape = "doublecircle") #fetched out if in subgraph
            else:
                G.add_node(self.__ndict[i], style = "filled", fillcolor = "grey", shape = "doublecircle") #not fetched out
        for i in range(len(self.__matrix)): #add some edges
            for j in range(len(self.__matrix)):
                t = i,j
                if (self.__matrix[i][j] != 0) and (t in subgraph):
                    G.add_edge(self.__ndict[i],self.__ndict[j],label = str(self.__matrix[i][j]),color = "red" ,style = "bold") #fetched out if in subgraph
                elif (self.__matrix[i][j] != 0):
                    G.add_edge(self.__ndict[i],self.__ndict[j],label = str(self.__matrix[i][j])) #not fetched out
        G.draw(fileloc,prog=plasement) #generate image
        


    
t1 = 0,1,0,0,0,1
t2 = 1,0,0,0,0,1
t3 = 1,0,0,0,0,1
t4 = 1,0,0,0,0,0
t5 = 0,0,0,1,0,1
t6 = 0,0,1,0,1,0
t = t1,t2,t3,t4,t5,t6

names = 'New York','London','Bejing','Washington','Kyiv','Odessa'
G = OrientedGraph(t,names)
print G.GetShortestWay(1,3)
G.VisualiseToFile(G.GetShortestWay(1,3))
#filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', '/home')
print fileName
