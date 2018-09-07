from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        if hit == miss:
            raise InvalidGuessAttempt
            
        if hit == True:
            self.hit = True
        elif miss == True:
            self.hit = False
        elif hit == False:
            self.hit = False
        elif miss == False:
            self.hit = True
    
    def is_hit(self):
        if self.hit:
            return self.hit
        else:
            return False
    def is_miss(self):
        if self.hit:
            return False
        else:
            return True

class GuessWord(object): #two attributes. answer and masked. method: perform_attempt, is_hit, is_miss
    def __init__(self, word):
        if not word or type(word) != str:
            raise InvalidWordException()
        
        self.answer = word.lower()                  #case insensitivity
        self.masked='*' * len(word)
    
    def perform_attempt(self, guessed_letter):
        if not guessed_letter or len(guessed_letter) != 1:
            raise InvalidGuessedLetterException
        guessed_letter = guessed_letter.lower()     #case insensitivity
        
        if guessed_letter in self.answer:
            
            count = 0
            indices = []
            for i in self.answer: #identify the indices
                if guessed_letter==i:
                    indices.append(count)
                count +=1
            
            #swap out the stars for the letters
            temp_masked= list(self.masked)
            for j in indices:
                temp_masked[j] = guessed_letter
            self.masked="".join(temp_masked)
            
            return GuessAttempt(guess = guessed_letter, hit = True)
        else:
            
            return GuessAttempt(guess = guessed_letter, hit = False)
    """     
    def is_hit(self):
        if self.hit:
            return self.hit
        else:
            return False
    def is_miss(self):
        if self.hit:
            return False
        else:
            return True
    """


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):        #word is a string in a list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(HangmanGame.select_random_word(word_list))
        
        
    def select_random_word(word_list):
        if type(word_list) != list or not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
        
        
    def guess(self, guessed_letter): #guess has to become a GuessAttempt object
        
        guessed_letter = guessed_letter.lower()
        
        if (self.is_finished() 
            or self.is_lost()
            or self.is_won()):
            
            raise GameFinishedException()
        
        guess_attempt = self.word.perform_attempt(guessed_letter)
        
        if guessed_letter not in self.previous_guesses:
            self.previous_guesses.append(guessed_letter)
        if guess_attempt.is_hit():
            if self.word.masked == self.word.answer:
                raise GameWonException()
            
        else:
            self.remaining_misses -= 1
            #self.word.masked also updated
            if self.remaining_misses == 0:
                raise GameLostException()
        return guess_attempt  #return game.word probably
        
        
    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses <= 0:
            return True
        else:
            return False
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else: 
            return False
    def is_lost(self):
        if self.remaining_misses <= 0:
            return True
        else:
            return False
    
    