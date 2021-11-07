"""
Tic Tac Toe Player
"""

import math
from operator import getitem
from copy import deepcopy

def flat(lst):
    """
    Flattens 2D list into 1D.
    """
    return [elem for row in lst for elem in row]

class Board():
    def __init__(self, player_is_you, board = None):
        if board == None:
            self.board = [[4, 4, 4, 4, 4, 4, 0], # your bank
                         [4, 4, 4, 4, 4, 4, 0]]  # opp bank
            '''
            YOU   0 1 2 3 4 5 6
            OPP 6 5 4 3 2 1 0
            '''
        else:
            self.board = board
        self.size = len(self.board[0])   # returns the length of a size (including the store)
        self.player = player_is_you      # 0 if player 1, 1 if player 2
        self.sum = sum(flat(self.board)) # number of pebbles on board
    
    def print(self):
        bcopy = deepcopy(self.board)
        print(f"Player {self.player}")
        store0 = bcopy[0].pop()
        store1 = bcopy[1].pop()
        print(' ', bcopy[0], store0)
        print(store1, [*reversed(bcopy[1])])

    def path(self, slot):
        """
        Returns path the pebbles go through when distributing
        """
        path = [(self.player, i) for i in range(self.size)]          # the path through your bank
        path += [(1 - self.player, i) for i in range(self.size - 1)] # the path through opp bank
        slot += 1
        return path[slot:] + path[:slot] # start path right after the action

    @staticmethod
    def pop(board, player, action):
        """
        Clears slot as well as returns value
        """
        [v, board[player][action]] = [board[player][action], 0]
        return v

    def actions(self, curr = []):
        """
        Returns set of all possible indexes available on the board.
        """
        acts = [index for index, elem in enumerate(self.board[self.player][:-1]) if elem != 0] # each non-empty slot
        ras = [[slot] for slot in acts if (slot + self.board[self.player][slot]) % (self.size * 2 - 1) == self.size - 1] # actions that land in store
        acts = [[elem] for elem in acts]
        if len(ras) == 0: return acts
        acts = [elem for elem in acts if elem not in ras]

        for ra in ras:
            nacts  = self.result(ra).actions(curr + ra)
            if len(nacts) == 0: # we have an empty side
                acts.append(ra)
            else:
                acts.extend(ra + nact for nact in nacts)
        return acts

    def result(self, actions):
        """
        Returns the board that results from making move on the board.
        """
        if len(actions) == 0: return self
        bcopy = deepcopy(self.board)
        for action in actions:
            value = Board.pop(bcopy, self.player, action)
            path = self.path(action) # start path right after action

            for i in range(0, value):
                [bank, slot] = path[i % len(path)]
                bcopy[bank][slot] += 1
            
        if bank == self.player and bcopy[bank][slot] == 1: # if final slot is empty
            store  = Board.pop(bcopy, bank, slot)
            store += Board.pop(bcopy, 1 - bank, (self.size - 2) - slot)
            bcopy[bank][-1] += store
        if bank == self.player and slot == 6: return Board(self.player, bcopy)

        return Board(1 - self.player, bcopy)
            
    def terminal(self):
        """
        Returns True if game is over, False otherwise.
        """
        for side in range(2):
            if all([slot == 0 for slot in self.board[side][:-1]]): # if a side is empty, then game over
                return True
            if self.board[side][-1] > self.sum / 2: # if one player has more than half of the pebbles stored, then game over
                return True
        return False

    def winner(self):
        """
        Returns the winner of the game, if there is one.
        """
        if self.terminal():
            for side in range(2):
                if self.board[side][-1] > self.board[1 - side][-1]:
                    return side
            return None
        raise Exception('Game has not ended')

    def utility(self):
        """
        Returns the value of a board.
        2 pts per stored pebble
        1 pt for pebble in play
        score: your pts - opp pts
        """
        if self.terminal():
            sums = [sum(side) for side in self.board]
            return 2 * (sums[0] - sums[1]) # since game ended, all pebbles in play are considered stored
        
        bcopy = deepcopy(self.board)
        for side in bcopy: side[-1] *= 2
        sums = [sum(side) for side in bcopy]
        return sums[0] - sums[1]

    def minimax(self, depth):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.player == 0:
            print('Worst score for Player 0')
            return self.worst_score(depth)
        if self.player == 1:
            print('Best score for Player 1')
            return self.minp_score(depth)

    # HELPER FUNCTIONS #

    def maxp_score(self, depth = 0, alpha = -math.inf, beta = math.inf):
        """
        Given board, returns (value of action, action) of best action on board if player Max
        """
        if self.terminal() or depth == 0:
            return (self.utility(),)

        bact, maxev = [], -math.inf
        for act in self.actions():
            act_value = self.result(act).minp_score(depth - 1, alpha, beta)[0]
            if maxev < act_value:
                maxev = act_value
                bact = act
            
            alpha = max(alpha, maxev)  #alpha = min score player Max can get
            if alpha >= beta: break # if min Max can get (ɑ) > min Min can get (β), then the rest can be ignored cause Max will choose ɑ
        return (maxev, bact)

    def minp_score(self, depth = 0, alpha = -math.inf, beta = math.inf):
        """
        Given board, returns (value of action, action) of best action on board if player Min
        """
        if self.terminal() or depth == 0: 
            return (self.utility(),)
        
        bact, minev = [], math.inf
        for act in self.actions():
            act_value = self.result(act).maxp_score(depth - 1, alpha, beta)[0]
            if minev > act_value: 
                minev = act_value
                bact = act

            beta = min(beta, minev) # beta = min score player Min can get
            if alpha >= beta: break
        return (minev, bact)

    def worst_score(self, depth = 0, alpha = -math.inf, beta = math.inf):
        """
        Given board, returns (value of action, action) of best action on board if player Max
        """
        if self.terminal() or depth == 0:
            return (self.utility(),)

        bact, bev = [], math.inf
        for act in self.actions():
            act_value = self.result(act).worst_score(depth - 1, alpha, beta)[0]
            if bev > act_value:
                bev = act_value
                bact = act
            
            #if beta <= bev: break # if min Max can get (ɑ) > min Min can get (β), then the rest can be ignored cause Max will choose ɑ
            #beta = min(beta, bev)
        return (bev, bact)

#print(Board(0, [[1,3,3,11,0,1,10], [1,0,3,0,1,1,13]]).minimax(5))
                # pl 0           # pl 1
board = Board(0)
print(1, board.minimax(1))
print(2, board.minimax(2))
print(5, board.minimax(5))