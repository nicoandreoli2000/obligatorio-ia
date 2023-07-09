import numpy as np
from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, player, depth):
        self.depth = depth
        self.player = player
        self.opponent = 2 if player == 1 else 1

    def next_action(self, board):
        return self.minimax(board, self.depth, True)[1]
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_final():
            return self.heuristic_utility(board), None

        if maximizing_player:
            max_eval = -np.inf
            best_action = None
            for action in range(board.length):
                board_copy = board.clone()
                if board_copy.add_tile(action, self.player):
                    eval, _ = self.minimax(board_copy, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = action
            return max_eval, best_action
        else:
            min_eval = np.inf
            best_action = None
            for action in range(board.length):
                board_copy = board.clone()
                if board_copy.add_tile(action, self.opponent):
                    eval, _ = self.minimax(board_copy, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_action = action
            return min_eval, best_action

    
    def heuristic_utility(self, board):
       return (self.calculate_score(board, self.player) - self.calculate_score(board, self.opponent))
    
    def calculate_score(self, board, player):
        score = 0

        # Evaluar filas
        for row in range(board.heigth):
            for col in range(board.length - 3):
                window = board[row, col:col+4]
                score += self.evaluate_window(window, player)

        # Evaluar columnas
        for col in range(board.length):
            for row in range(board.heigth - 3):
                window = board[row:row+4, col]
                score += self.evaluate_window(window, player)

        # Evaluar diagonales descendentes
        for row in range(board.heigth - 3):
            for col in range(board.length - 3):
                window = [board[row+i, col+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Evaluar diagonales ascendentes
        for row in range(board.heigth - 3):
            for col in range(board.length - 3):
                window = [board[row+3-i, col+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

        
    def evaluate_window(self, window, player):
        score = 0

        window = list(window)

        if window.count(player) == 4:
            score += 10000
        if window.count(player) == 3 and window.count(0) == 1:
            score += 100
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 10

        return score

