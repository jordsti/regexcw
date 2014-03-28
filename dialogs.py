'''
Created on Mar 28, 2014

@author: Jordan Guerin
'''
from PyQt4 import QtGui, QtCore

class solved_dialog(QtGui.QDialog):
    
    def __init__(self, parent):
        super(solved_dialog, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        self.lbl_grats = QtGui.QLabel("The crossword was solved !")
        
        self.btn_save = QtGui.QPushButton("Save your board")
        self.btn_save.clicked.connect(self.save_result)
        
        self.btn_close = QtGui.QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        
        grid.addWidget(self.lbl_grats, 0, 0)
        grid.addWidget(self.btn_save, 1, 0)
        grid.addWidget(self.btn_close, 1, 1)
        
        self.setLayout(grid)
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle("Grats !")
        self.show()
        
    def save_result(self):
        print "save"

class newgame_dialog(QtGui.QDialog):
    
    def __init__(self, parent):
        super(newgame_dialog, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        self.lbl_dim = QtGui.QLabel("Table dimension :")
        self.lbl_rows = QtGui.QLabel("Rows : ")
        self.lbl_cols = QtGui.QLabel("Cols : ")
        
        self.tb_rows = QtGui.QLineEdit()
        self.tb_rows.setText(str(self.parent.rows))
        
        
        self.tb_cols = QtGui.QLineEdit()
        self.tb_cols.setText(str(self.parent.cols))
        
        self.btn_ok = QtGui.QPushButton("Ok", self)
        self.btn_ok.clicked.connect(self.create_game)
        
        self.btn_cancel = QtGui.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.close)
        
        grid.addWidget(self.lbl_dim, 0, 0)
        
        grid.addWidget(self.lbl_rows, 1, 0)
        grid.addWidget(self.tb_rows, 1, 1)
        
        grid.addWidget(self.lbl_cols, 2, 0)
        grid.addWidget(self.tb_cols, 2, 1)
        
        grid.addWidget(self.btn_ok, 3, 0)
        grid.addWidget(self.btn_cancel, 3, 1)
        
        self.setLayout(grid)
        self.setGeometry(100, 100, 300, 140)
        self.setWindowTitle("New Game")
        self.show()
    
    def create_game(self):
        
        rows = int(str(self.tb_rows.text()))
        cols = int(str(self.tb_cols.text()))
        
        self.parent.rows = rows
        self.parent.cols = cols
        
        self.parent.new_game()
        
        self.close()