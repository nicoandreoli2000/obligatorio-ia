import numpy as np
from agent import Agent
from board import Board

class MinimaxAgent(Agent):
    def __init__(self, player):
        self.player = player

    def next_action(self, obs):
        return self.minimax(obs, depth=5, maximizing_player=True)[1]
    
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
                    result, _ = self.minimax(board_copy, depth - 1, False)
                    if result > max_eval:
                        max_eval = result
                        best_action = action
            return max_eval, best_action
        else:
            min_eval = np.inf
            for action in possible_moves:
                board_copy = board.clone()
                if board_copy.add_tile(action, -self.player):
                    result, _ = self.minimax(board_copy, depth - 1, True)
                    if result < min_eval:
                        min_eval = result
                        best_action = action
            return min_eval, best_action


    
    def heuristic_utility(self, board : Board):
        score = 0

        WIN_CONDITION = 1000
        TILES = 1
        THREATS = 30 # Three together

        score += board.winner * WIN_CONDITION  


        for i in range(board.length - 1):
            for j in range(board.heigth - 1):
                player = board[i][j]

                if player == 0:
                    break

                multiplier = 1 if player == self.player else -1
                                
                player_threats = self.count_threats(board, player, i, j)
                opponent_threats = self.count_threats(board, -player, i, j)


                score += multiplier * TILES + (player_threats - opponent_threats) * THREATS

        return score

    def count_threats(self, board : Board, player, i, j):
        threats = 0
        
        # Horizontal
        if j < board.length - 3:
            if (
                board[i][j + 1] == player and
                board[i][j + 2] == player and
                board[i][j + 3] == 0
            ):
                threats += 1
        if j > 2:
            if (
                board[i][j - 1] == player and
                board[i][j - 2] == player and
                board[i][j - 3] == 0
            ):
                threats += 1

        # Vertical
        if i < board.heigth - 3:
            if (
                board[i + 1][j] == player and
                board[i + 2][j] == player and
                board[i + 3][j] == 0
            ):
                threats += 1

        # Diagonal
        if i < board.heigth - 3 and j < board.length - 3:
            if (
                board[i + 1][j + 1] == player and
                board[i + 2][j + 2] == player and
                board[i + 3][j + 3] == 0
            ):
                threats += 1
        if i > 2 and j > 2:
            if (
                board[i - 1][j - 1] == player and
                board[i - 2][j - 2] == player and
                board[i - 3][j - 3] == 0
            ):
                threats += 1
        if i < board.heigth - 3 and j > 2:
            if (
                board[i + 1][j - 1] == player and
                board[i + 2][j - 2] == player and
                board[i + 3][j - 3] == 0
            ):
                threats += 1
        if i > 2 and j < board.length - 3:
            if (
                board[i - 1][j + 1] == player and
                board[i - 2][j + 2] == player and
                board[i - 3][j + 3] == 0
            ):
                threats += 1
        
        return threats
