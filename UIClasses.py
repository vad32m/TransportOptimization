from PyQt4 import QtCore, QtGui, uic
import sys

class StartWindow(QtGui.QWidget):

    callback = None
    
    def __init__(self,callback,parent = None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/StartWin.ui",self)
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"),self.proceed)
        self.setFixedSize(self.size())
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2)
        self.callback = callback
        
    def proceed(self):
        if self.LoadGraph.isChecked():
            self.callback('file')
        elif self.NewDirRB.isChecked():
            self.callback('dir')
        elif self.NewUndirRB.isChecked():
            self.callback('undir')
        else:
            QtGui.QMessageBox.question(self, 'Message',"Chose propriate radio button", QtGui.QMessageBox.Ok)

class FinalWindow(QtGui.QWidget):

    callback = None
    currpixmap = None
    
    def __init__(self,names,callback,parent = None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/VisRepr.ui",self)
        self.connect(self.findPath, QtCore.SIGNAL("clicked()"),self.fPath)
        self.setFixedSize(self.size())
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2)
        self.callback = callback
        sc = QtGui.QGraphicsScene()
        sc.addPixmap(QtGui.QPixmap('file.png'))
        self.gview.setScene(sc)
        self.gview.show()
        self.gview.scale(0.5,0.5)
        for i in names.keys():
            self.first.insertItem(i,names[i])
            self.last.insertItem(i,names[i])
        

    def fPath(self):
        path,length = self.callback(self.first.currentIndex(),self.last.currentIndex())
        QtGui.QMessageBox.question(self, 'Answer','Path:' + str(path) + ('\n Len:') + str(length), QtGui.QMessageBox.Ok)
        sc = QtGui.QGraphicsScene()
        sc.addPixmap(QtGui.QPixmap('file.png'))
        self.gview.setScene(sc)
        self.gview.show()
        
        
        
        

class MakeGraphWin(QtGui.QWidget):
    __Nodes = None
    __Matrix = None
    __Callback = None
    
    def __init__(self, callback, directed = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("UIForms/NGWin.ui",self)
        self.setFixedSize(self.size())
        desktop = QtGui.QApplication.desktop()
        self.move((desktop.width()-self.width())/2,(desktop.height()-self.height())/2)
        self.connect(self.AddNode, QtCore.SIGNAL("clicked()"),self.newNode)
        self.connect(self.Proceed, QtCore.SIGNAL("clicked()"),self.makeSomeGraph)
        if directed:
            self.connect(self.AdTable, QtCore.SIGNAL("cellChanged(int,int)"),self.celCtrlDir)
        else:
            self.connect(self.AdTable, QtCore.SIGNAL("cellChanged(int,int)"),self.celCtrl)
        self.__Nodes = []
        self.__Matrix = []
        self.__Callback = callback

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
        self.__Callback()
        return

    def NodesAndMatrix(self):
        return tuple(self.__Nodes), self.__Matrix

if __name__ == "__main__":

    def CbFunc(first,last):
        return (1,2),3
    
    app = QtGui.QApplication(sys.argv)
    window = FinalWindow(names = {0:'a',1:'b',2:'c'},callback = CbFunc)
    window.show()
    sys.exit(app.exec_())
    
