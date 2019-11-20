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
    
    
    def play(self):
        #Archaïque pour le moment mais les actions possibles ne seront pas toujours celles ci
        #Si une case est bloquée par exemple
        possible_actions = ["up", "down", "right", "left"]
        action = possible_actions[random.randint(0,3)]


        

        """
        possible_actions = [("up",(0,-1)),("down",(0,1)),("left",(-1,0)),("right",(1,0))]
            x,y = self._pos
            #Every logical action (remove out of bound and other player's case actions)
            actions = [a for a in possible_actions if game.get_case((x + a[1][0], y + a[1][1])) == "0" or game.get_case((x + a[1][0], y + a[1][1])) == str(self._id)]
            #favor case that has not been taken yet over case that the player has already taken
            privileged_actions = [a for a in actions if game.get_case((x + a[1][0], y + a[1][1])) == "0"]
            
            if len(privileged_actions) != 0:
                action = privileged_actions[random.randint(0, len(privileged_actions) - 1)][0]
            else:
                action = actions[random.randint(0,len(actions) - 1)][0]
        """




        """
        Je laisse tomber pour le moment, tant que je n'ai pas implémenté greedy_step
        if not self._trainable:
            action = possible_actions[random.randint(0,3)]
        """
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
