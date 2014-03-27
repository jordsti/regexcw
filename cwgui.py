'''
Created on Mar 27, 2014

@author: Jordan Guerin
'''

from PyQt4 import QtGui, QtCore
import sys

class crossword_gui(QtGui.QMainWindow):
    
    def __init__(self):
        super(crossword_gui, self).__init__()
        
        self.init_ui()
        
    def init_menu(self):
        
        file_menu = self.menuBar().addMenu('&File')
        
        new_game = QtGui.QAction('New Game', self)
        new_game.triggered.connect(self.new_game)
        
        close = QtGui.QAction('Quit', self)
        close.triggered.connect(self.close)
        
        file_menu.addAction(new_game)
        file_menu.addAction(close)
        
    def new_game(self):
        print 'new game!'
        
    
    def init_cases(self, nb_cols, nb_rows):
        
        for r in range(nb_rows):
            
            row = []
            self.cases.append(row)
            
            for c in range(nb_cols):
                
                label = QtGui.QLineEdit()
                
                label.setText('0')
                label.setGeometry(0, 0, 20, 20)
                row.append(label)
                
                self.grid.addWidget(label, r, c)
                
        
        for c in range(nb_cols):
            label = QtGui.QLabel()
            label.setText(str(c+1)+'. None')
            
            self.grid.addWidget(label, 8+c+1, 3, 1, 4)
        
        for r in range(nb_rows):
            label = QtGui.QLabel()
            label.setText(str(r+1)+'. None')
            
            self.grid.addWidget(label, 8+r+1, 0, 1, 4)
        
        
    def init_ui(self):
        
        self.h_patterns = []
        self.v_patterns = []
        
        self.init_menu()
        
        self.main_widget = QtGui.QWidget()
        self.main_widget.setGeometry(0, 0, 400, 600)
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        
        self.cases = []
        
        self.init_cases(8,8)
        
        lbl_hpattern = QtGui.QLabel('Horizontal')
        self.grid.addWidget(lbl_hpattern, 8, 0, 1, 4)
        
        lbl_vpattern = QtGui.QLabel('Vertical')
        self.grid.addWidget(lbl_vpattern, 8, 3, 1, 4)
        
        self.main_widget.setLayout(self.grid)
        
        self.setCentralWidget(self.main_widget)
        self.setGeometry(100, 100, 400, 600)
        self.setWindowTitle("RegEx Crossword")
        self.show()
        

def main():
    
    app = QtGui.QApplication(sys.argv)
    gui = crossword_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()