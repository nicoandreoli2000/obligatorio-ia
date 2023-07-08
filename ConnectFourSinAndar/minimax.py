from math import sqrt
from agent import Agent
from board import Board
import numpy as np

class Minimax_agent:
    def __init__(self, height, length):
        self.height = (height % 2) + 1
        self.length = length

    def next_action(self, board):
        best_action, best_score = self.get_best_action(board, self.height, self.length)
        return best_action

    def minimax(env, depth, maximizing_player):
        if depth == 0 or env.is_board_full() or env.check_win(0, 0) or env.check_win(0, 6):
            return None, env.get_reward(True)

        if maximizing_player:
            max_value = float('-inf')
            best_action = None
            for action in range(env.action_space.n):
                if env.is_valid_action(action):
                    env_copy = env.copy()
                    _, reward, _, _ = env_copy.step(action)
                    _, value = minimax(env_copy, (depth - 1), False)
                    value += reward
                    if value > max_value:
                        max_value = value
                        best_action = action
            return best_action, max_value
        else:
            min_value = float('inf')
            for action in range(env.action_space.n):
                if env.is_valid_action(action):
                    env_copy = env.copy()
                    _, reward, _, _ = env_copy.step(action)
                    _, value = minimax(env_copy, depth - 1, True)
                    value -= reward
                    min_value = min(min_value, value)
            return None, min_value

    def step(self, action):
        if self.is_valid_action(action):
            row = self.get_next_row(action)
            self.board[row, action] = self.current_player
            done = self.is_game_over(row, action)
            reward = self.get_reward(done)
            self.current_player *= -1  # Cambiar al siguiente jugador
            return self.board, reward, done, {}

        # Acción inválida, penalización
        return self.board, -10, False, {}

    def is_valid_action(self, action):
        return self.board[0, action] == 0  # Verificar si la columna no está llena

    def get_next_row(self, action):
        for row in range(5, -1, -1):
            if self.board[row, action] == 0:
                return row

    def is_game_over(self, row, col):
        return self.check_win(row, col) or self.is_board_full()

    def check_win(self, row, col):
        player = self.board[row, col]
        # Verificar si hay 4 fichas consecutivas en la fila
        if self.check_line(row, 0, 0, 1, player):
            return True
        # Verificar si hay 4 fichas consecutivas en la columna
        if self.check_line(0, col, 1, 0, player):
            return True
        # Verificar si hay 4 fichas consecutivas en la diagonal ascendente
        if self.check_line(row, col, -1, 1, player):
            return True
        # Verificar si hay 4 fichas consecutivas en la diagonal descendente
        if self.check_line(row, col, 1, 1, player):
            return True
        return False

    def check_line(self, start_row, start_col, row_step, col_step, player):
        for step in range(4):
            row = start_row + step * row_step
            col = start_col + step * col_step
            if not (0 <= row < 6 and 0 <= col < 7 and self.board[row, col] == player):
                return False
        return True

    def is_board_full(self):
        return np.all(self.board != 0)

    def get_reward(self, done):
        if done:
            return 10  # Jugador actual ganó
        return 0

"""     
    def calculate_score(self, board):
        scores = self.get_scores(board)
        return 1000 * scores[4] + 3 * scores[3] + 2 * scores[2]

    def get_best_action(self, board, height: int, length: int = 2):
        if board.is_final() or length == 0:
            return None, self.calculate_score(board)

        if height != self.height:
            possible_actions = board.get_possible_actions()
            best_score = np.inf
            best_action = None

            for action in possible_actions:
                clone_board = board.clone()
                was_added = clone_board.add_tile(action, height)

                if was_added:
                    _, score = self.get_best_action(clone_board, self.change_height(height), length - 1)

                    if score < best_score:
                        best_score = score

            return None, best_score

        if height == self.height:
            best_action = None
            best_score = -np.inf
            possible_actions = board.get_possible_actions()

            for action in possible_actions:
                clone_board = board.clone()
                was_added = clone_board.add_tile(action, height)

                if was_added:
                    _, score = self.get_best_action(clone_board, self.change_height(height), length - 1)

                    if score >= best_score:
                        best_score = score
                        best_action = action

            return best_action, best_score

    def change_height(self, height):
        return ((height) % 2) + 1

    def get_scores(self, board):
        scores = {2: 0, 3: 0, 4: 0}
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        visited_tiles = set()

        for row in range(board.height):
            for column in range(board.length):
                tile = board[row][column]

                if tile != var2 and ((row, column) not in visited_tiles):
                    for (direction_row, direction_column) in directions:
                        valid_tiles = {1: True, -1: True}
                        current_score = 1

                        for counter in range(1, 4):
                            if not (valid_tiles[1] or valid_tiles[-1]):
                                break

                            for direction in [1, -1]:
                                valid_row = row + (direction_row * counter * direction)
                                valid_column = column + (direction_column * counter * direction)

                                if self.is_valid_cell(board, valid_row, valid_column) and (
                                        board[valid_row][valid_column] == board[row][column]
                                        or board[valid_row][valid_column] == var2):
                                    if board[valid_row][valid_column] != var2:
                                        visited_tiles.add((valid_row, valid_column))
                                        current_score += 1
                                else:
                                    valid_tiles[direction] = False

                        if (valid_tiles[1] or valid_tiles[-1]) and current_score > 1:
                            multiplier = -1 if tile != self.height else 1
                            scores[min(current_score, 4)] += multiplier

        return scores

    def is_valid_cell(self, board, row, column):
        valid_row = row >= 0 
----------------


    def next_action(self):
        next_move = self.get_action(self.board)  # Reuse the existing Board instance
        return next_move

    def get_action(self, board):
        best_score = -np.inf
        best_action = None

    def next_action(self, env):
        game = Board(env)  # Crea una instancia del juego Connect Four con el tablero actual
        agent = Minimax_agent(max_depth=4)  # Crea una instancia del agente Minimax con una profundidad de búsqueda de 4
        next_move = agent.get_action(game)  # Obtiene la siguiente jugada del agente
        return next_move
    
    ##probar funcion
    def next_action2(self, lllIlIlIIIIlIllllIIl):
        lIIllIIllIIIlIIl, llIlIlllIIllIIlllII = self.IIIIIIlllIIlIIII(lllIlIlIIIIlIllllIIl, self.IlllIIllIII, self.lIlIIIlllII)
        return lIIllIIllIIIlIIl
    
    def get_action(self, env):
        best_score = -np.inf
        best_action = None

        for action in range(env.action_space.n):
            if env.is_valid_action(action):
                new_state = env.get_next_state(action)
                score = self.minimax(new_state, depth=3, maximizing_player=False)
                if score > best_score:
                    best_score = score
                    best_action = action
        return best_action

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.is_game_over():
            return self.evaluate(state)

        if maximizing_player:
            max_score = -np.inf
            for action in range(state.action_space.n):
                if state.is_valid_action(action):
                    new_state = state.get_next_state(action)
                    score = self.minimax(new_state, depth - 1, False)
                    max_score = max(max_score, score)
            return max_score
        else:
            min_score = np.inf
            for action in range(state.action_space.n):
                if state.is_valid_action(action):
                    new_state = state.get_next_state(action)
                    score = self.minimax(new_state, depth - 1, True)
                    min_score = min(min_score, score)
            return min_score

    def evaluate(self, state):
        if state.is_winner(self.player):
            return 1
        elif state.is_winner(1 - self.player):
            return -1
        else:
            return 0
        
"""