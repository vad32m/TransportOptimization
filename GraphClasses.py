#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import pygraphviz as pgv
from pygraphviz import *


class InvalidArgError(Exception):
    pass


class BadGraphError(Exception):
    pass


class CorruptedFileError(Exception):
    pass


class EmptyGraphError(Exception):
    pass


class OrientedGraph:

    
    def __init__(self , inputmatr = (), names = ()): #graph, created without args - empty
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

    def GetNodeId(self,name): #returns node id by name
        if name not in self.__ndict.values():
            raise InvalidArgError
        for i in range(len(self.__ndict)):
            if self.__ndict[i] == name:
                return i

            
    def DijkstraAlg(self, point):
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
        if (type(point) is not int) or (point not in range( len(self.__ndict))):
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
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
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
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
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

    def WriteToFile(self,fileloc = 'graph.gro'):
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):# nothing to write if graph is empty
            raise EmptyGraphError
        _file = open(fileloc,'w') #open file
        _file.seek(0)
        _file.truncate() #clear file
        _file.write('<oriented>\n') #tag for oriented graph
        for a in range(len(self.__matrix)): #writing line of node names to file
            string = self.__ndict[a] + ';'
            _file.write(string)
        _file.write('\n')
        for i in range(len(self.__matrix)): #writing adjacency matrix to file
            for j in range(len(self.__matrix)):
                string = str(self.__matrix[i][j]) + ' '
                _file.write(string)
            _file.write('\n')
        _file.close() #operating with finished

    def ReadFromFile(self,fileloc = 'graph.gro'):
        RowList = []
        CollumnList = []
        currstring = ''
        try:
            _file = open(fileloc,'r') #open the file
        except IOError:
            raise CorruptedFileError
        if ('<oriented>' not in _file.readline()): #searching for <oriented> tag
            _file.close()
            raise CorruptedFileError #no tag - error
        else:
            i = 0
            for c in _file.readline(): #this cycle reads names of nodes from file
                if c != ';':
                    currstring = currstring + c 
                else:
                    self.__ndict[i] = currstring 
                    i = i + 1
                    currstring = ''
            for i in range(len(self.__ndict)): #this cycle reads adjacency matrix
                for c in _file.readline(): 
                    if c == ' ':
                        CollumnList.append( int(currstring))
                        currstring = ''
                    else:
                        currstring = currstring + c
                RowList.append( tuple( CollumnList))
                CollumnList = []
            if len(RowList) != len(self.__ndict): #different lengths of arrays - bad file
                raise CorruptedFileError
            for i in RowList:
                if len(i) != len(self.__ndict): #diffferent sizes inside matrixes  - bad file
                    raise CorruptedFileError
            self.__matrix = tuple( RowList)
            _file.close() #work finished

            
class UnorientedGraph:

    
    def __init__(self , inputmatr = (), names = ()): #graph, created without args - empty
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
        self._CorrectMatrix()
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

    def GetNodeId(self,name): #returns node id by name
        if name not in self.__ndict.values():
            raise InvalidArgError
        for i in range(len(self.__ndict)):
            if self.__ndict[i] == name:
                return i
            
    def _CorrectMatrix(self): #takes only rigt upper part of the matrix and makes all matrix symmetrical
        self.__matrix = list(self.__matrix)
        for i in range(len(self.__matrix)): #nothing comlicated here
            self.__matrix[i] = list(self.__matrix[i])
        for i in range(len(self.__matrix)):
            for j in range(i,len(self.__matrix)):
                self.__matrix[j][i] = self.__matrix[i][j]
        for i in range(len(self.__matrix)):
            self.__matrix[i] = tuple(self.__matrix[i])
        self.__matrix = tuple(self.__matrix)

        
    def DijkstraAlg(self, point):
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
        if (type(point) is not int) or (point not in range( len(self.__ndict))):
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
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
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
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):
            raise EmptyGraphError
        G = pgv.AGraph(strict=True,directed=False,forcelabels = True) #pyGraphVis makes magic simple
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

    def WriteToFile(self,fileloc = 'graph.gru'):
        if (len(self.__ndict) == 0) or (len(self.__matrix) == 0):# nothing to write if graph is empty
            raise EmptyGraphError
        _file = open(fileloc,'w') #open file
        _file.seek(0)
        _file.truncate() #clear file
        _file.write('<unoriented>\n') #tag for oriented graph
        for a in range(len(self.__matrix)): #writing line of node names to file
            string = self.__ndict[a] + ';'
            _file.write(string)
        _file.write('\n')
        for i in range(len(self.__matrix)): #writing adjacency matrix to file
            for j in range(len(self.__matrix)):
                string = str(self.__matrix[i][j]) + ' '
                _file.write(string)
            _file.write('\n')
        _file.close() #operating with finished

    def ReadFromFile(self,fileloc = 'graph.gru'):
        RowList = []
        CollumnList = []
        currstring = ''
        try:
            _file = open(fileloc,'r') #open the file
        except IOError:
            raise CorruptedFileError
        if ('<unoriented>' not in _file.readline()): #searching for <oriented> tag
            _file.close()
            raise CorruptedFileError #no tag - error
        else:
            i = 0
            for c in _file.readline(): #this cycle reads names of nodes from file
                if c != ';':
                    currstring = currstring + c 
                else:
                    self.__ndict[i] = currstring 
                    i = i + 1
                    currstring = ''
            for i in range(len(self.__ndict)): #this cycle reads adjacency matrix
                for c in _file.readline(): 
                    if c == ' ':
                        CollumnList.append( int(currstring))
                        currstring = ''
                    else:
                        currstring = currstring + c
                RowList.append( tuple( CollumnList))
                CollumnList = []
            if len(RowList) != len(self.__ndict): #different lengths of arrays - bad file
                raise CorruptedFileError
            for i in RowList:
                if len(i) != len(self.__ndict): #diffferent sizes inside matrixes  - bad file
                    raise CorruptedFileError
            self.__matrix = tuple( RowList)
            self._CorrectMatrix()
            _file.close() #work finished
                
            
        
    


    
t1 = 0,1,0,0,0,1
t2 = 1,0,0,1,0,1
t3 = 1,0,0,0,0,1
t4 = 1,0,0,0,0,0
t5 = 0,0,0,1,0,1
t6 = 0,0,1,0,1,0
t = t1,t2,t3,t4,t5,t6

names = 'New York','London','Bejing','Washington','Kyiv','Odessa'
G = OrientedGraph(t,names)
G.VisualiseToFile()
