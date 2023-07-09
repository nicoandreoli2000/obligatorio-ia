import numpy as np
from agent import Agent
from board import Board

class MinimaxAgent(Agent):
    def __init__(self, player):
        self.player = player

    def next_action(self, obs):
        _, action = self.minimax(obs, depth=5, maximizing_player=True)
        return action
    
    def minimax(self, board : Board, depth, maximizing_player):
        if depth == 0 or board.is_final():
            return self.heuristic_utility(board), None

        best_action = None
        possible_moves = board.get_posible_actions()

        if (len(possible_moves) == 0):
            return self.minimax(board, 0, not maximizing_player)

        if maximizing_player:
            max_eval = -np.inf
            for action in possible_moves:
                board_copy = board.clone()
                if board_copy.add_tile(action, self.player):
                    result, = self.minimax(board_copy, depth - 1, False)
                    if result > max_eval:
                        max_eval = result
                        best_action = action
            return max_eval, best_action
        else:
            min_eval = np.inf
            for action in possible_moves:
                board_copy = board.clone()
                if board_copy.add_tile(action, -self.player):
                    result, = self.minimax(board_copy, depth - 1, True)
                    if result < min_eval:
                        min_eval = result
                        best_action = action
            return min_eval, best_action


    
    def heuristic_utility(self, board : Board):
        score = 0

        WIN_CONDITION = 100
        TILES = 1
        THREATS = 20
        EATABLE_TILES = -10

        score += board.winner * WIN_CONDITION        

        for i in range(board.length):
            for j in range(board.heigth):
                player = board[i][j]
                
                eatable_tiles = self.count_eatable_tiles(board, player, i, j) 
                threats = self.countThreats(board, player, i, j)

                score += player * (EATABLE_TILES * eatable_tiles + THREATS * threats + TILES)

        return score

    def countThreats(self, board : Board, player, i, j):
        threats = 0
        
        # Horizontal
        if j < board.length - 3:
            if board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == 0:
                threats += 1
        if j > 2:
            if board[i][j - 1] == player and board[i][j - 2] == player and board[i][j - 3] == 0:
                threats += 1

        # Vertical
        if i < board.heigth - 3:
            if board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == 0:
                threats += 1

        # Diagonal
        if i < board.heigth - 3 and j < board.length - 3:
            if board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and board[i + 3][j + 3] == 0:
                threats += 1
        if i > 2 and j > 2:
            if board[i - 1][j - 1] == player and board[i - 2][j - 2] == player and board[i - 3][j - 3] == 0:
                threats += 1
        if i < board.heigth - 3 and j > 2:
            if board[i + 1][j - 1] == player and board[i + 2][j - 2] == player and board[i + 3][j - 3] == 0:
                threats += 1
        if i > 2 and j < board.length - 3:
            if board[i - 1][j + 1] == player and board[i - 2][j + 2] == player and board[i - 3][j + 3] == 0:
                threats += 1
            
        return threats
    
    def count_eatable_tiles(self, board : Board, player, i, j):
        return 0
        
