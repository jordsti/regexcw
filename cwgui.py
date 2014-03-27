'''
Created on Mar 27, 2014

@author: Jordan Guerin
'''

from PyQt4 import QtGui, QtCore
import sys
import crossword
import re

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
        generator = crossword.generator(8, 8)
        generator.build_patterns()
        self.cw = generator.get_crossword()
        
        for r in range(self.cw.dimension[1]):
            
            row = self.cases[r]
            
            for c in range(self.cw.dimension[0]):
                
                le = row[c]
                le.setText('')
        
        i = 0
        
        for r in self.cw.h_patterns:
            
            label = self.h_patterns[i]
            label.setText(str(i+1)+'. '+r)
            
            i = i + 1
        
        i = 0
        
        for c in self.cw.v_patterns:
            
            label = self.v_patterns[i]
            label.setText(str(i+1)+'. '+c)
            
            
            i = i + 1
        
    
    def init_cases(self, nb_cols, nb_rows):
        
        for r in range(nb_rows):
            
            row = []
            self.cases.append(row)
            
            for c in range(nb_cols):
                
                label = QtGui.QLineEdit()
                label.editingFinished.connect(self.validate)
                label.setText('0')
                label.setGeometry(0, 0, 20, 20)
                row.append(label)
                
                self.grid.addWidget(label, r, c)
                
        
        for c in range(nb_cols):
            label = QtGui.QLabel()
            label.setText(str(c+1)+'. None')
            self.v_patterns.append(label)
            self.grid.addWidget(label, 8+c+1, 3, 1, 4)
        
        for r in range(nb_rows):
            label = QtGui.QLabel()
            label.setText(str(r+1)+'. None')
            self.h_patterns.append(label)
            self.grid.addWidget(label, 8+r+1, 0, 1, 4)
        
        
    def init_ui(self):

        self.valid_format = QtGui.QTextFormat()
        self.valid_format.setForeground(QtCore.Qt.green)

        self.invalid_format = QtGui.QTextFormat()
        self.invalid_format.setForeground(QtCore.Qt.red)
                
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

    def get_h_word(self, index):
        word = ''

        row = self.cases[index]

        for case in row:
            val = str(case.text())
            word = word + val

        return word

    def get_v_word(self, index):
        word = ''

        for r in self.cases:
            val = str(r[index].text())
            word = word + val

        return word
            

    def validate(self):
        i = 0
        err = 0
        for h in self.cw.h_patterns:
            word = self.get_h_word(i)

            m = re.match(h, word)

            if m == None:
                print "Invalid H " + str(i+1)
                err = err + 1

            
            i = i + 1

        i = 0
        for c in self.cw.v_patterns:
            word = self.get_v_word(i)

            m = re.match(c, word)

            if m == None:
                print "Invalid V " + str(i+1)
                err = err + 1
            
            i = i + 1

        if err == 0:
            print "Solved!"

def main():
    
    app = QtGui.QApplication(sys.argv)
    gui = crossword_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
