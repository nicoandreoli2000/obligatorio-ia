import numpy as np
from connect_four_env import ConnectFourBaseEnv

class MinimaxAgent:
    def __init__(self, player):
        self.player = player

    def next_action(self, env):
        _, action = self.minimax(env, depth=4, maximizing_player=True)
        return action
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_final():
            return self.evaluate(board), None

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
                if board_copy.add_tile(action, -self.player):
                    eval, _ = self.minimax(board_copy, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_action = action
            return min_eval, best_action

    
    def evaluate(self, board):
        if board.winner == self.player:
            return 1000
        elif board.winner == -self.player:
            return -1000
        else:
            score = 0

            # Evaluar filas
            for row in range(board.heigth):
                for col in range(board.length - 3):
                    window = board[row, col:col+4]
                    score += self.evaluate_window(window)

            # Evaluar columnas
            for col in range(board.length):
                for row in range(board.heigth - 3):
                    window = board[row:row+4, col]
                    score += self.evaluate_window(window)

            # Evaluar diagonales descendentes
            for row in range(board.heigth - 3):
                for col in range(board.length - 3):
                    window = [board[row+i, col+i] for i in range(4)]
                    score += self.evaluate_window(window)

            # Evaluar diagonales ascendentes
            for row in range(3, board.heigth):
                for col in range(board.length - 3):
                    window = [board[row-i, col+i] for i in range(4)]
                    score += self.evaluate_window(window)

            score -= self.block_opponent_lines(board)
            return score
        
    def block_opponent_lines(self, board):
        opponent = -self.player
        score = 0

        # Evaluar filas del oponente
        for row in range(board.heigth):
            for col in range(board.length - 3):
                window = board[row, col:col+4]
                score += self.evaluate_opponent_window(window, opponent)

        # Evaluar columnas del oponente
        for col in range(board.length):
            for row in range(board.heigth - 3):
                window = board[row:row+4, col]
                score += self.evaluate_opponent_window(window, opponent)

        # Evaluar diagonales descendentes del oponente
        for row in range(board.heigth - 3):
            for col in range(board.length - 3):
                window = [board[row+i, col+i] for i in range(4)]
                score += self.evaluate_opponent_window(window, opponent)

        # Evaluar diagonales ascendentes del oponente
        for row in range(3, board.heigth):
            for col in range(board.length - 3):
                window = [board[row-i, col+i] for i in range(4)]
                score += self.evaluate_opponent_window(window, opponent)

        return score
        
    def evaluate_window(self, window):
        player_count = np.count_nonzero(window == self.player)
        opponent_count = np.count_nonzero(window == -self.player)
        empty_count = np.count_nonzero(window == 0)

        if player_count == 4:
            return 1000
        elif opponent_count == 4:
            return -1000
        else:
            return player_count - opponent_count + empty_count * 0.1
        
    def evaluate_opponent_window(self, window, opponent):
        player_count = np.count_nonzero(window == self.player)
        opponent_count = np.count_nonzero(window == opponent)
        empty_count = np.count_nonzero(window == 0)

        if player_count == 4:
            return 1000
        elif opponent_count == 4:
            return -1000
        else:
            return opponent_count - player_count + empty_count * 0.1

"""
    def minimax(self, env, depth, maximizing_player):
        if depth == 0 or env.is_final(): ##is_final
            return self.evaluate(env), None

        if maximizing_player:
            max_eval = -np.inf
            best_action = None
            for action in range(env._length):
                if env._grid.add_tile(action, self.player):
                    env_copy = self.copy_env(env)
                    env_copy.step(action)
                    eval, _ = self.minimax(env_copy, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = action
            return max_eval, best_action
        else:
            min_eval = np.inf
            best_action = None
            for action in range(env._length):
                if env._grid.add_tile(action, -self.player):
                    env_copy = self.copy_env(env)
                    env_copy.step(action)
                    eval, _ = self.minimax(env_copy, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_action = action
            return min_eval, best_action

    def evaluate(self, env):
        if env._grid.winner == self.player:
            return 100
        elif env._grid.winner == -self.player:
            return -100
        else:
            return 0

    def copy_env(self, env):
        env_copy = ConnectFourBaseEnv()
        env_copy._current_player = env._current_player
        env_copy._grid = env._grid.copy()
        return env_copy
"""