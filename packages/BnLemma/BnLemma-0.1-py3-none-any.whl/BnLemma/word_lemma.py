# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 17:47:35 2018

@author: karigor
"""

with open("RootWords.yaml",'r',encoding = 'utf-8') as corpus:
    c_words = [word for line in corpus for word in line.split()]
    c_words_len = len(c_words)
    
mp_word = {}
for w in c_words:
    mp_word[w]=1
    

with open("iden.yaml",'r',encoding = 'utf-8') as ide:
    id_id = [word for line in ide for word in line.split()]
import trie
for words in c_words:
    trie.dictionary.add(words)




#levenshtein distance
def levenshtein(tar_word):
    import edit_distance as ed      
    c_len = 50
    c_word = c_words[0]
    for j in range(c_words_len):
        dis=ed.min_dis(tar_word, c_words[j])
        if c_len > dis:
            c_word = c_words[j]
            c_len= dis
    return c_word


#Trie distanace
def trie_lemma(word):
    import trie        
    return trie.dictionary.search(word)





#using SRA
def DBSRA(word):
    import SRA   
    return SRA.RA(word, mp_word)
  


