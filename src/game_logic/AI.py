from .player import Player

class IA(Player):
    
    def __init__(self, player_id, start_x, start_y, epsilon=0.99, learning_rate=0.00001, is_trainable=True):
        Player.__init__(self, player_id, start_x, start_y)
        self._trainable = is_trainable
        self._V = {}
        self._eps = 0.99
        self._lr = learning_rate
        self._history = []

        '''
        Properties and setters defined so we can add extra verification if we want to
        ''' 
    @property
    def V(self):
        return self._V

    @property
    def is_trainable(self):
        return self._trainable
    #@V.setter
    #Setter ici ? Pour avoir plus facile à ajouter les nouveaux états


    def add_transition(self, transition):
        self._history.append(transition)
    
    def update_transition(self, transition, id):
        self._history[id] = transition

    def get_transition(self, id):
        return self._history[id]

    def show_transition(self):
        print(self._history)