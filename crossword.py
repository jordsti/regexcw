'''
Created on Mar 27, 2014

@author: Jordan Guerin
'''
import sys
import os
import random
import re

class wordbank:
    
    def __init__(self, filepath = 'words.txt'):
        self.filepath = filepath
        self.words = []
        self.load()
        
    def load(self):
        
        if os.path.exists(self.filepath):
            fp = open(self.filepath, 'r')
            
            lines = fp.readlines()
            fp.close()
            
            for l in lines:
                l = l.strip('\r')
                l = l.strip('\n')
                l = l.strip()
                if len(l) > 0:
                    self.words.append(l)
    
    def generate_word(self, length):
        
        words = self.words_by_length(length)
        
        if len(words) < 4:
            return self.generate_combine_word(length)
        else:
            i = random.randint(0, len(words)-1)
            return words[i]
    
    def generate_combine_word(self, length):
        
        lmin, lmax = self.get_min_max()
    
        w1_lg = random.randint(lmin, lmax)
        w2_lg = length - w1_lg
        
        w1 = self.words_by_length(w1_lg)
        w2 = self.words_by_length(w2_lg)
        random.seed()
        w1i = random.randint(0, len(w1) - 1)
        word1 = w1[w1i]

        if len(w2) == 0:
            word2 = self.generate_combine_word(w2_lg)
        else:
            w2i = random.randint(0, len(w2) - 1)
            word2 = w2[w2i]
        
        return word1 + word2
    
    def get_min_max(self):
        
        lmin = 4096
        lmax = 0
        
        for w in self.words:
            
            lg = len(w)
            
            if lg < lmin:
                lmin = lg
                
            if lg > lmax:
                lmax = lg
        
        return lmin, lmax
    
    def words_by_length(self, length):
        
        words = []
        
        for w in self.words:
            
            if len(w) == length:
                words.append(w)
                
        return words
        

class case:
    
    def __init__(self):
        self.value = None

    
    def get(self):
        if self.value == None:
            return ""
        else:
            return self.value

class crossword:
    def __init__(self, cols_nb = 8, rows_nb = 8):
        
        self.dimension = (cols_nb, rows_nb)
        
        self.rows = []
        
        self.v_patterns = []
        self.h_patterns = []
        
        for r in range(rows_nb):
            col = []
            self.rows.append(col)
            for c in range(cols_nb):
                col.append(case())
    
    def get_vertical_word(self, index):
        
        if index < self.dimension[0]:
            
            word = ""
            for r in self.rows:
                word = word + r[index].get()
            
            return word
            
        else:
            return None
    
    def get_horizontal_word(self, index):
        
        if index < self.dimension[1]:
            word = ""
            row = self.rows[index]
            
            for c in row:
                word = word + c.get()
            return word
            
        else:
            return None
    

    def fill_word_row(self, word, index):
        
        i = 0
        
        row = self.rows[index]
        
        for c in word:
            row[i].value = c
            
            i = i + 1
    
    def get_nb_rows(self):
        return self.dimension[1]
    def get_nb_cols(self):
        return self.dimension[0]


class generator:
    def __init__(self, rows = 8, cols = 8):
        
        self.cw = crossword(cols, rows)
        self.word_length = cols
        
        self.wb = wordbank()
        
        for i in range(self.word_length):
            word = self.wb.generate_word(self.word_length)
            #print word
            self.cw.fill_word_row(word, i)
        
    
    def get_crossword(self):
        
        n_cw = crossword(self.cw.dimension[0], self.cw.dimension[1])
        
        n_cw.h_patterns = self.cw.h_patterns
        n_cw.v_patterns = self.cw.v_patterns
        
        return n_cw
    
    def build_patterns(self):
        
        for i in range(self.cw.dimension[1]):
            random.seed()
            word = self.cw.get_horizontal_word(i)
            regex = self.generate_regex(word)
            
            self.cw.h_patterns.append(regex)
        
        for i in range(self.cw.dimension[0]):
            random.seed()
            word = self.cw.get_vertical_word(i)
            regex = self.generate_regex(word)
            
            self.cw.v_patterns.append(regex)
            
        
    def generate_regex(self, word):
        regex = ""
        r_type = random.randint(0, 2)
        #0 -> any char .
        #1 -> specific char
        #2 -> range []
        #3 -> ( ) capture repeat, no implemented
        
        current = 0
        rc_length = random.randint(1, len(word)/2)
        
        while current < len(word):
            random.seed()
            if r_type == 0:
                if rc_length == 1:
                    regex = regex + '.'
                    #0 -> no change
                    #1 -> ?
                    #2 -> +
                    suffix = random.randint(0, 2)
                    
                    if suffix == 1:
                        regex = regex + '?'
                    elif suffix == 2:
                        regex = regex + '+'
                else:
                    # operator type
                    #0 -> * 0 or more
                    #1 -> + 1 or more
                    #2 -> { }
                    oper = random.randint(0, 2)
                    
                    if oper == 0:
                        regex = regex + '.*'
                    elif oper == 1:
                        regex = regex + '.+'
                    elif oper == 2:
                        regex = regex + '.{1,'+str(rc_length)+'}'
            
            elif r_type == 1:
                sub = word[current:current+rc_length]

                lg = len(sub)
                
                #0 -> no change
                #1 -> () capture + other word
                #2 -> () +
                #3 -> () *
                #4 -> () ?
            
                oper = random.randint(0, 4)

                if oper == 0:
                    regex = regex + sub
                elif oper == 1:
                    words = self.wb.words_by_length(lg)
                    words.append(sub)
                    cwords = []
                    cmax = len(words) - 1
                    cmin = 0
                    
                    nb = random.randint(cmin, cmax)
                    
                    if nb > 5:
                        nb = 5
                    
                    while not len(cwords) == nb:
                        w = random.choice(words)
                        
                        if w not in cwords:
                            cwords.append(w)
                    
                    if not sub in cwords:
                        pos = random.randint(0, len(cwords))
                        
                        if pos == len(cwords):
                            pos = pos - 1
                        
                        cwords.insert(pos, sub)
                    
                    sub_regex = '('
                    
                    if len(cwords) > 0:
                        for w in cwords:
                            sub_regex = sub_regex + w + '|'
                        
                        
                        sub_regex = sub_regex.rstrip('|') + ')'
                    else:
                        sub_regex = '('+sub+')'
                    
                    regex = regex + sub_regex
                

                
                elif oper == 2:
                    regex = regex + '(' + sub + ')+'
                elif oper == 3:
                    regex = regex + '(' + sub + ')*'
                elif oper == 4:
                    regex = regex + '(' + sub + ')?'
            
            elif r_type == 2:
                sub = word[current:current+rc_length]
                cmin = 4000
                cmax = 0

                for c in sub:
                    i = ord(c)
                    
                    if i < cmin:
                        cmin = i
                    if i > cmax:
                        cmax = i
                
                
                #0 []{length}
                #1 []+
                #2 []*
                
                oper = random.randint(0, 2)
                sub_regex = ''
                if cmin == cmax:
                    sub_regex = '[' + chr(cmin) + ']'
                else:
                    sub_regex = '[' + chr(cmin) + '-' + chr(cmax) + ']'

                if oper == 0:
                    sub_regex = sub_regex +  '{'+str(len(sub))+'}'
                elif oper == 1:
                    sub_regex = sub_regex + '+'
                elif oper == 2:
                    sub_regex = sub_regex + '*'

                regex = regex + sub_regex
            
            current = current + rc_length
            wrange = len(word) - rc_length - 1
            rc_length = random.randint(1, wrange)
            
            if current + rc_length > len(word):
                rc_length = len(word) - rc_length
                
                
        return regex
                

if __name__ == '__main__':
    print "Crossword module test"
    
    print "crossword class"
    
    gen = generator()
    
    gen.build_patterns()

    print "Horizontal Pattern"
    for h in gen.cw.h_patterns:
        print "\t" + h

    print "Vertical Pattern"
    for v in gen.cw.v_patterns:
        print "\t" + v

    for i in range(ord('A'), ord('Z') + 1):
    
        print chr(i)
    
    
    
