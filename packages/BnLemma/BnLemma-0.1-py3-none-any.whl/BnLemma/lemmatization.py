# -*- coding: utf-8 -*-
"""
Created on Mon May 20 03:06:51 2019

@author: karigor
"""


import word_lemma as lm
import edit_distance as ed

with open('mapvg.txt', 'r', encoding = 'utf-8') as datav:
    datav = [word for line in datav for word in line.split()]
    
map_vg = {}
for i in range(len(datav)):
  if datav[i] == "=":
    map_vg [datav[i-1]] = datav[i+1]

def lemma(sn):
    
    qs = sn.split()
    
    for i in range(len(qs)):
        if qs[i] in map_vg.keys():
            qs[i] =  map_vg[qs[i]]

        
    
    qs_list = ""
    for tar_word in qs:
        
        b = lm.DBSRA(tar_word)
        c = lm.trie_lemma(tar_word)
      
    
        un = 0
        if b == c:
            val =  b
        
        else:
        
           
            d2 = ed.min_dis(b,tar_word)
            d3 = ed.min_dis(c, tar_word)
        
            mi = min( d2, d3)
           
            if d2 == mi:
                val = b
            else:
                val =  c
        
            ln = len(tar_word)
            ln2 = len(val)
            
        
            ck = (mi/ln)*100
           
        
            if ck > 50:
                val = tar_word
                un = 1
     
        reval =val
    
        if un ==1:
            c_corpus = ['র','রে','রা','কে','দের','কে','তে']
            for i in range(len(val)):
                
                if val in c_corpus:
                    break
    
                val = val[1:]
            le_val= len(val)     
    
            val = reval[:len(reval)-le_val]  
        qs_list += " " + val
        
    return qs_list.strip(' ')



     

 