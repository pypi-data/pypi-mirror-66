#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import randint
from time import sleep


# In[2]:


class Game:
    
    """ Representing a game of guessing a computer generated number within a set range. 
             
    """
    
    def __init__(self, players, max_number):
        self.max_number = max_number
        self.players = players        
                  
    def play_game(self):
        
        """ Starts a game of guessing a computer generated number within a set range. 
        
        Attributes:
        players (list) representing the Computer player and the Player 
            who interacts with the program
        max_number (int) representing the max limmit of the range of integerswithin 
            which the computer chooses a randomn integer  

        """
        
        attempts = 1
        picked_number = self.players[0].pick_number(self.max_number)   
        guess = self.players[1].guess_number(self.max_number, response=None)
        
#         print(guess)
        
        while guess != picked_number:
            print(guess)
            
            if guess > picked_number:
                response = 'lower' 
                print("Too high. The generated number is lower.")
#                 output = int(input("Try again. The number is between 0 and {}.".format(max_number)))
                
        
            if guess < picked_number:
                response = 'higher'
                print("Too low. The number is greater than {}.".format(guess))
#                 output = int(input("Try again. The number is between 0 and {}.".format(max_number)))    

            attempts += 1
            guess = self.players[1].guess_number(self.max_number, response=response)
        
        print(guess)
        print("Dobre! You made it on {} attempt(s).".format(attempts))



# In[3]:


class Player:
    
    def __init__(self, name):
        self.name = name

    def pick_number(self, max_number):
        """
        Returns an int
        """
        raise NotImplementedError
        
    def guess_number(self, max_number, response=None):
        """
        Returns an int
        """
        raise NotImplementedError
        


# In[4]:


class ComputerPlayer(Player):
    
    def __init__(self):
        super().__init__(name = 'computersko')
        self.previous_guess = None
        
    def pick_number(self, max_number):
        return randint(0, max_number)
    
    def guess_number(self,max_number, response = None):
        sleep(1)
        if response is None:
            self.previous_guess = randint(0, max_number)
        elif response == 'lower':
            self.previous_guess = randint(0, self.previous_guess)
        elif response == 'higher':
            self.previous_guess = randint(self.previous_guess, max_number)

        return self.previous_guess
        
    


# In[5]:


computersko = ComputerPlayer()


# In[6]:


class PersonPlayer(Player):
    
    def pick_number(self, max_number):
        return int(input("Pick a number within 0 and {} and let the Computer guess.".format(max_number)))
    
    def guess_number(self, max_number, response=None):
        return int(input("Guess a number within the range of 0 and {}".format(max_number)))
        


# In[7]:


person = PersonPlayer('katzko')


# In[8]:


gamesko = Game(players = [person, computersko], max_number=20) 


# In[9]:


gamesko.play_game()


# In[2]:





# In[3]:





# In[10]:


# testing

# def play_game(max_number, generated_number):
#     attempts = 1

#     players_guess = input("Computer chose a random integer between 0 and {}. Can you guess the number?".format(max_nunmber))
#     output = int(players_guess)
#     while output != generated_number:

#         if output > generated_number:
#             attempts += 1
#             print("Too high. The generated number is lower.")
#             output = int(input("Computer chose a random integer between 0 and {}. Can you guess the number?".format(max_number)))

#         if output < generated_number:
#             attempts += 1
#             print("Too low. The number is greater than {}.".format(players_guess))
#             output = int(input("Computer chose a random integer between 0 and {}. Can you guess the number?".format(max_number)))    
                
#     print("Dobre! You made it on {} attempt(s).".format(attempts))

        
# play_game(20,17)
        


# In[11]:


# testing

# def random_number(max_number):
#     print(randint(0, max_number))
        
# random_number(20)


# In[ ]:


# testing

# def random_number(max_number):
#     return input("Computer chose a random integer between 0 and {}. Can you guess the number?".format(max_number))
    
# #     print(randint(0, max_number))

# random_number(20)


# In[ ]:


#testing data types

# players_guess = input("Computer chose a random integer between 0 and {}. Can you guess the number?".format(17))
# players_guess
# type(players_guess)


# In[ ]:


# players_guess = int(players_guess)
# type(players_guess)

