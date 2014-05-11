import  UIClasses as uicl
from  GraphClasses import *
from PyQt4 import QtGui,QtCore
import sys

CurrentGraph = None

def CallBackA(arg):
    global window, CurrentGraph
    if arg == 'file':
        path = QtGui.QFileDialog.getOpenFileName(window, 'Open file', '/home')
        if path == '':
            return
        f = open(path,'r')
        line = f.readline()
        if '<oriented>' in line:
            f.close()
            CurrentGraph = OrientedGraph()
            try:
                CurrentGraph.ReadFromFile(path)
            except CorruptedFileError:
                QtGui.QMessageBox.question(window, 'Error',"Corrupted file", QtGui.QMessageBox.Ok)
                return
            window.hide()
            CurrentGraph.VisualiseToFile()
            window = uicl.FinalWindow(CurrentGraph.Nodes(),CallBackC)
            window.show()
        elif '<unoriented>' in line:
            f.close()
            CurrentGraph = UnorientedGraph((),())
            try:
                CurrentGraph.ReadFromFile(path)
            except CorruptedFileError:
                QtGui.QMessageBox.question(window, 'Error',"Corrupted file", QtGui.QMessageBox.Ok)
                return
            window.hide()
            CurrentGraph.VisualiseToFile()
            window = uicl.FinalWindow(CurrentGraph.Nodes(),CallBackC)
            window.show()
            
        else:
            QtGui.QMessageBox.question(window, 'Error',"Corrupted file", QtGui.QMessageBox.Ok)
    elif arg == 'dir':
        window.hide()
        window = uicl.MakeGraphWin(CallBackB,True)
        window.show()
    else:
        window.hide()
        window = uicl.MakeGraphWin(CallBackB,False)
        window.show()
    return
        
def CallBackB(isDir):
    global window, CurrentGraph
    nodes,matrix =  window.NodesAndMatrix()
    if isDir:
        CurrentGraph = OrientedGraph(matrix,nodes)
    else:
        CurrentGraph = UnorientedGraph(matrix,nodes)
    CurrentGraph.VisualiseToFile()
    window.hide()
    window = uicl.FinalWindow(CurrentGraph.Nodes(),CallBackC)
    window.show()
    return

def CallBackC(first,last,save):
    global window, CurrentGraph
    if save == '':
        return
    if save == None:
        a = CurrentGraph.GetShortestWay(first,last)
        CurrentGraph.VisualiseToFile(a)
        return a, CurrentGraph.DijkstraAlg(first)[0][last]
    if save[0] == '/':
        CurrentGraph.WriteToFile(save + '.gra')
        return

        
app = QtGui.QApplication(sys.argv)
window = uicl.StartWindow(CallBackA)
window.show()
sys.exit(app.exec_())
