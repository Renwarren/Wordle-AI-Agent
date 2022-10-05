from random import choice
from utility import *
from collections import Counter


from constants import GREEN,YELLOW,GREY

class solver():

    def __init__(self,guess,guess_list):
        self.guess = guess
        self.guess_list = guess_list

    def fill_word(self):
        self.guess_list = slice_word(load_dict("words.txt"))

    def choose_word(self):
        self.guess = choice(self.guess_list)

    def get_frequency(self):
        return Counter(self.guess)
    
    def has_distinct(self,freq_vect):
        return len(freq_vect) == len(self.guess)

    def remove_words_distinct(self,feedback):
        temp_tuple = tuple(self.guess_list) #cannot iterate through a list and modify it at the same time. 
        for word in temp_tuple:
            for i in range(5):
                if feedback[i] == GREY and self.guess[i] in word:
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == GREEN and self.guess[i] != word[i] :
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == GREEN and self.guess[i] not in word :
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == YELLOW and self.guess[i] not in word:
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == YELLOW and self.guess[i] == word[i]:
                    self.guess_list.remove(word)
                    break
    
    def remove_words_repeat(self,feedback):
        temp_tuple = tuple(self.guess_list) #cannot iterate through a list and modify it at the same time. 
        for word in temp_tuple:
            for i in range(5):
                if feedback[i] == GREY and self.guess[i] == word[i]:
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == GREEN and self.guess[i] != word[i] :
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == GREEN and self.guess[i] not in word :
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == YELLOW and self.guess[i] not in word:
                    self.guess_list.remove(word)
                    break
                elif feedback[i] == YELLOW and self.guess[i] == word[i]:
                    self.guess_list.remove(word)
                    break

    def remove_words(self,feedback,freq_vect):
        if self.has_distinct(freq_vect):
            self.remove_words_distinct(feedback)
        else:
            self.remove_words_repeat(feedback)
            
            