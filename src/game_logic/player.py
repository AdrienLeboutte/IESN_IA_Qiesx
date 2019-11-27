import random

class Player:

    def __init__(self, player_id, start_x, start_y):
        self._id = player_id
        self._x = start_x
        self._y = start_y
        self._case_claimed = 0

    '''
    Properties and setters defined so we can add extra verification if we want to
    '''
    @property
    def id(self):
        return self._id

    @property
    def xy(self):
        return (self._x, self._y)
    @xy.setter
    def xy(self, new_xy):
        self._x, self._y = new_xy

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, new_x):
        self._x = new_x
    
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def case_claimed(self):
        return self._case_claimed
    @case_claimed.setter
    def case_claimed(self, new_nb):
        self._case_claimed = new_nb

    '''This method is used to increment the number of case claimed by one'''
    def add_one_case(self):
        self._case_claimed += 1

    '''
        I don't really know what to do here, we're asking the player what he wants to do but how?
        Feels like an extra layer might be necessary so I'll just use my old method and return the new_x, new_y
    '''
    def move(self, action = None):
        actions = ["up", "right", "down", "left"]

        if action == "up":
            new_x = self._x
            new_y = self._y - 1
        elif action == "down":
            new_x = self._x
            new_y = self._y + 1
        elif action == "left":
            new_x = self._x - 1
            new_y = self._y
        elif action == "right":
            new_x = self._x + 1
            new_y = self._y
        else:
            new_x = self._x
            new_y = self._y
        return (new_x, new_y)
        
    def play(self):
        """
        ask the player for the move he want to do
        return: up/down/right/left
        """
        correct_answers = ["up", "down", "right", "left"]
        action = ""
        while(str.lower(action) not in correct_answers):
            action = input("Player {} >>> ".format(self._id))

        return action