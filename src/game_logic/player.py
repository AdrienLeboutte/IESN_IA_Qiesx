class Player:

    def __init__(self, id, start_x, start_y):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.case_claimed = 0

    '''
    Properties and setters defined so we can add extra verification if we want to
    '''
    @property
    def xy(self):
        return (self.x, self.y)
    @xy.setter
    def xy(self, new_xy):
        self.x, self.y = new_xy

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
        self.case_claimed += 1

    '''
        I don't really know what to do here, we're asking the player what he wants to do but how?
        Feels like an extra layer might be necessary so I'll just use my old method and return the new_x, new_y
    '''
    def move(self, direction):
        if direction == "up":
            new_x = self.x
            new_y = self.y - 1
        elif direction == "down":
            new_x = self.x
            new_y = self.y + 1
        elif direction == "left":
            new_x = self.x - 1
            new_y = self.y
        elif direction == "right":
            new_x = self.x + 1
            new_y = self.y
        else:
            new_x = self.x
            new_y = self.y
        return (new_x, new_y)