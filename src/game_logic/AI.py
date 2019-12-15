from .player import Player
import random

class IA(Player):
    
    def __init__(self, player_id, start_x, start_y, epsilon=0.99, learning_rate=0.0000000001, is_trainable=True):
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
    @V.setter
    def V(self, new_v):
        self._V = new_v

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
        actions = [a for a in possible_actions if game.get_case((self._x + a[1][0], self._y + a[1][1])) == "0" or game.get_case((self._x + a[1][0], self._y + a[1][1])) == str(self._id)]
        v_min = None
        vi = None

        for i in range(len(actions)):
            a = actions[i][1]
            next_player_pos = (self._x + a[0], self._y + a[1])
        
            splitted_board = game.game_board.split(";")
            state = splitted_board[0]
            i_next_player_pos = next_player_pos[0] + next_player_pos[1] * game.size_y
            splitted_board[0] = state[:i_next_player_pos] + str(self._id) + state[i_next_player_pos + 1:]
            splitted_board[game.turn + 1] = str(i_next_player_pos)
            next_state = ';'.join(splitted_board)

            if next_state in self.V:
                if v_min is None or v_min > self.V[next_state] :
                    v_min = self.V[next_state]
                    vi = i
            
        return actions[vi if vi is not None else 0]


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
                action = self.greedy_step(game)[0]
        else:
            #"Randomly" computed player sem-intelligente
            if len(privileged_actions) != 0:
                action = privileged_actions[random.randint(0, len(privileged_actions) - 1)][0]
            else:
                action = possible_actions[random.randint(0,len(actions) - 1)][0]

        return action


    def train(self):
        if self.is_trainable:
            for i, transition in enumerate(reversed(self._history)):
                s, sp, r = transition
                if(not s in self._V):
                    self._V[s] = 0
                if(sp is not None and not sp in self._V):
                    self._V[sp] = 0

                if(i != 0):
                    self._V[s] = self._V[s] + self._lr*(self._V[sp] - self._V[s])
                else:
                    self._V[s] = self._V[s] + self._lr*(r - self._V[s])

        self._history = []         
 

    def update_transition(self, transition, id=-1):
        self._history[id] = transition

    def get_transition(self, id=-1):
        return self._history[id]

    def show_transition(self):
        print(self._history)
