from PyQt4 import QtCore, QtGui, uic
import sys

class StartWindow(QtGui.QWidget): #realization of start window

    callback = None #function to call, when all work via window is done
    
    def __init__(self,callback,parent = None): 
      
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/StartWin.ui",self)
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"),self.proceed) #handling with button
        self.setFixedSize(self.size()) #make window size to be fixed
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2) #place window in centre of screen
        self.callback = callback
        
    def proceed(self):
        if self.LoadGraph.isChecked():
            self.callback('file') #load from file option checked
        elif self.NewDirRB.isChecked():
            self.callback('dir') #make new directed graph option checked
        elif self.NewUndirRB.isChecked():
            self.callback('undir') #make new undirected graph option checked
        else:
            QtGui.QMessageBox.question(self, 'Message',"Chose propriate radio button", QtGui.QMessageBox.Ok)

class FinalWindow(QtGui.QWidget): #window for visualizing graph and route search

    _callback = None
    _names = None
    
    def __init__(self,names,callback,parent = None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/VisRepr.ui",self)
        self.connect(self.findPath, QtCore.SIGNAL("clicked()"),self.fPath)
        self.connect(self.save, QtCore.SIGNAL("clicked()"),self._save)
        self.setFixedSize(self.size())
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2)
        self._callback = callback
        sc = QtGui.QGraphicsScene()
        sc.addPixmap(QtGui.QPixmap('CGraph.png'))
        self.gview.setScene(sc)
        self.gview.show()
        self.gview.scale(0.5,0.5)
        for i in names.keys():
            self.first.insertItem(i,names[i])
            self.last.insertItem(i,names[i])
        self._names = names
    
    def fPath(self):
        path,length = self._callback(self.first.currentIndex(),self.last.currentIndex(),None)
        pth = '' + self._names[path[0][0]]
        for i in path:
            pth = pth + '->'+ self._names[i[1]]
        QtGui.QMessageBox.question(self, 'Answer','Path:' + pth + ('\n Len:') + str(length), QtGui.QMessageBox.Ok)
        sc = QtGui.QGraphicsScene()
        sc.addPixmap(QtGui.QPixmap('CGraph.png'))
        self.gview.setScene(sc)
        self.gview.show()

    def _save(self):
        a = QtGui.QFileDialog()
        a.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        self._callback(self.first.currentIndex(),self.last.currentIndex(),a.getOpenFileName(self, 'Save file', '/home'))
        
    def wheelEvent(self,event):
        if event.delta() > 0:
            self.gview.scale(0.7,0.7)
        else:
            self.gview.scale(1.3,1.3)

class MakeGraphWin(QtGui.QWidget):
    __Nodes = None
    __Matrix = None
    __Callback = None
    __directed = None
    
    def __init__(self, callback, directed = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/NGWin.ui",self)
        self.setFixedSize(self.size())
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2)
        self.connect(self.AddNode, QtCore.SIGNAL("clicked()"),self.newNode)
        self.connect(self.Proceed, QtCore.SIGNAL("clicked()"),self.makeSomeGraph)
        if not directed:
            self.connect(self.AdTable, QtCore.SIGNAL("cellChanged(int,int)"),self.celCtrlDir)
        else:
            self.connect(self.AdTable, QtCore.SIGNAL("cellChanged(int,int)"),self.celCtrl)
        self.__Nodes = []
        self.__Matrix = []
        self.__Callback = callback
        self.__directed = directed

    def newNode(self):
        currtxt = self.NewNode.text()
        if (currtxt != '') and (currtxt not in self.__Nodes):
            self.AdTable.insertColumn(len(self.__Nodes))
            self.AdTable.insertRow(len(self.__Nodes))
            self.__Nodes.append( str(currtxt))
            slist = QtCore.QStringList(self.__Nodes)
            self.AdTable.setVerticalHeaderLabels(slist)
            self.AdTable.setHorizontalHeaderLabels(slist)
            self.NewNode.setText('')
        else:
            pass

    def celCtrlDir(self,row,column):
        if row == column:
            self.AdTable.item(row,column).setText('0')
        else:
            try:
                self.AdTable.setItem(column,row,QtGui.QTableWidgetItem(self.AdTable.item(row,column).text()))
            except RuntimeError:
                pass
            
    def celCtrl(self,row,column):
        if row == column:
            self.AdTable.item(row,column).setText('0')

    def makeSomeGraph(self):
        CollumnList = []
        RowList = []
        if len(self.__Nodes) < 2:
            QtGui.QMessageBox.question(self, 'Message',"Not enough nodes", QtGui.QMessageBox.Ok)
            return
        for i in range(len(self.__Nodes)): #this cycle reads adjacency matrix
            for j in range(len(self.__Nodes)):
                try: 
                    currstring = self.AdTable.item(i,j).text()
                except AttributeError:
                    QtGui.QMessageBox.question(self, 'Message',"Check matrix, please", QtGui.QMessageBox.Ok)
                    return
                for c in currstring:
                    if c not in('1','2','3','4','5','6','7','8','9','0'):
                        QtGui.QMessageBox.question(self, 'Message',"Check matrix, please", QtGui.QMessageBox.Ok)
                        return
                CollumnList.append(int(currstring))
            RowList.append( tuple( CollumnList))
            CollumnList = []
        self.__Matrix = tuple(RowList)
        self.__Callback(self.__directed)
        return

    def NodesAndMatrix(self):
        return tuple(self.__Nodes), self.__Matrix

