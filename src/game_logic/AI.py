from .player import Player
import random

class IA(Player):
    
    def __init__(self, player_id, start_x, start_y, epsilon=0.99, learning_rate=0.00001, is_trainable=True):
        Player.__init__(self, player_id, start_x, start_y)
        self._trainable = is_trainable
        self._V = {}
        self._eps = epsilon
        self._lr = learning_rate
        self._history = []

    '''
    Properties and setters defined so we can add extra verification if we want to
    ''' 
    @property
    def V(self):
        return self._V

    #@V.setter
    #Setter ici ? Pour avoir plus facile à ajouter les nouveaux états

    @property
    def eps(self):
        return self._eps
    @eps.setter
    def eps(self, new_eps):
        self._eps = new_eps
    
    @property
    def lr(self):
        return self._lr
    @lr.setter
    def lr(self, new_lr):
        self._lr = new_lr

    @property
    def is_trainable(self):
        return self._trainable
    
    def add_transition(self, transition):
        self._history.append(transition)
    
    def greedy_step(self, game):
        possible_actions = [("up",(0,-1)),("down",(0,1)),("left",(-1,0)),("right",(1,0))]
        v_max = 0
        vi = None

        for i in range(len(possible_actions)):
            a = possible_actions[i][1]
            temp_board = game
            is_valid = temp_board.validate(a, temp_board._players[temp_board._turn])
            
            if is_valid:                
                if temp_board.game_board in self.V:
                    if v_max < self.V[temp_board.game_board]:
                        v_max = self.V[temp_board.game_board]
                        vi = i
            
        return possible_actions[vi if vi is not None else 0]


    def play(self, game):
        possible_actions = [("up",(0,-1)),("down",(0,1)),("left",(-1,0)),("right",(1,0))]
        #Every logical action (remove out of bound and other player's case actions)
        actions = [a for a in possible_actions if game.get_case((self._x + a[1][0], self._y + a[1][1])) == "0" or game.get_case((self._x + a[1][0], self._y + a[1][1])) == str(self._id)]
        #favor case that has not been taken yet over case that the player has already taken
        privileged_actions = [a for a in actions if game.get_case((self._x + a[1][0], self._y + a[1][1])) == "0"]
            
        if self._trainable:
            if random.uniform(0,1) < self.eps:
                #Exploration
                if len(privileged_actions) != 0:
                    action = privileged_actions[random.randint(0, len(privileged_actions) - 1)][0]
                else:
                    action = possible_actions[random.randint(0,len(possible_actions)-1)][0]
            else:
                #Exploitation
                action = self.greedy_step(game)
        else:
            #"Randomly" computed player sem-intelligente
            if len(privileged_actions) != 0:
                action = privileged_actions[random.randint(0, len(privileged_actions) - 1)][0]
            else:
                action = possible_actions[random.randint(0,len(actions) - 1)][0]

        return action


    def train(self):
        if self.is_trainable:
            for transition in reversed(self._history):
                s, sp, r = transition
                if(not s in self._V):
                    self._V[s] = 0
                if(not sp in self._V):
                    self._V[sp] = 0

                if(r == 0):
                    self._V[s] = self._V[s] + self._lr*(self._V[sp] - self._V[s])
                else:
                    self._V[s] = self._V[s] + self._lr*(r - self._V[s])

        self._history = []         
    #Inutile selon moi car la transition que l'on modifira sera toujours la dernière enregistrée 
    # self._history[-1]
    def update_transition(self, transition, id=-1):
        self._history[id] = transition

    #La aussi je doute de la légitimité de cette fonction    
    def get_transition(self, id=-1):
        return self._history[id]

    #Pareil
    def show_transition(self):
        print(self._history)
