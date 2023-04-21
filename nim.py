import random
import tkinter as tk
from tkinter import Label


class NimGame:
    def __init__(self, num_objects):
        self.num_objects = num_objects
        self.current_player = 1
        self.winner = None

    def start_game(self, player_starts):
        self.current_player = player_starts
        self.winner = None

    def take_turn(self, num_removed):
        self.num_objects -= num_removed
        if self.num_objects <= 0:
            self.winner = self.current_player
        else:
            self.current_player = 1 if self.current_player == 2 else 2

    def get_possible_moves(self):
        return list(range(1, min(self.num_objects+1, 4)))

    def is_terminal(self):
        return self.winner is not None


class NimAI:
    def __init__(self, game):
        self.game = game

    def evaluate(self, node):
        if node.is_terminal():
            if node.winner == 1:
                return float('inf')
            else:
                return float('-inf')
        else:
            return node.num_objects

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.is_terminal():
            return self.evaluate(node)

        if maximizingPlayer:
            value = float('-inf')
            for move in node.get_possible_moves():
                child = NimGame(node.num_objects)
                child.current_player = 2
                child.num_objects = node.num_objects - move
                child.take_turn(move)
                value = max(value, self.minimax(child, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value

        else:
            value = float('inf')
            for move in node.get_possible_moves():
                child = NimGame(node.num_objects)
                child.current_player = 1
                child.num_objects = node.num_objects - move
                child.take_turn(move)
                value = min(value, self.minimax(child, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def get_best_move(self, node, depth):
        best_value = float('-inf')
        best_move = None
        for move in node.get_possible_moves():
            child = NimGame(node.num_objects)
            child.current_player = 2
            child.num_objects = node.num_objects - move
            child.take_turn(move)
            value = self.minimax(child, depth-1, float('-inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move


class NimGUI:
    def __init__(self):
        self.game = NimGame(20)
        self.ai = NimAI(self.game)
        self.window = tk.Tk()
        self.window.title("Nim Game")

        # Start menu
        start_menu = tk.Menu(self.window)
        self.window.config(menu=start_menu)

        # Game menu
        game_menu = tk.Menu(start_menu)
        start_menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Exit", command=self.window.destroy)

        # Player menu
        player_menu = tk.Menu(start_menu)
        start_menu.add_cascade(label="Player", menu=player_menu)
        player_menu.add_radiobutton(label="Human starts", variable=self.game.current_player, value=1, command=self.new_game)
        player_menu.add_radiobutton(label="Computer starts", variable=self.game.current_player, value=2, command=self.new_game)

        # Main frame
        main_frame = tk.Frame(self.window)
        main_frame.pack()

        # Object frame
        object_frame = tk.Frame(main_frame)
        object_frame.pack(side=tk.LEFT, padx=10)

        object_label = tk.Label(object_frame, text="Number of objects:")
        object_label.pack()

        self.object_count_label = tk.Label(object_frame, text=self.game.num_objects)
        self.object_count_label.pack()

        # Remove frame
        remove_frame = tk.Frame(main_frame)
        remove_frame.pack(side=tk.LEFT, padx=10)

        remove_label = tk.Label(remove_frame, text="Remove:")
        remove_label.pack()

        self.remove_entry = tk.Entry(remove_frame, width=5)
        self.remove_entry.pack()

        submit_button = tk.Button(remove_frame, text="Submit", command=self.take_turn)
        submit_button.pack(pady=10)

        self.update_display()

    def new_game(self):
        self.game = NimGame(self.game.num_objects)
        self.ai = NimAI(self.game)
        self.game.start_game(self.game.current_player)
        self.update_display()

    def take_turn(self):
        num_removed = int(self.remove_entry.get())
        self.game.take_turn(num_removed)
        self.update_display()
        if not self.game.is_terminal() and self.game.current_player == 2:
            ai_move = self.ai.get_best_move(self.game, 3)
            self.game.take_turn(ai_move)
            self.update_display()

    def update_display(self):
        self.object_count_label.config(text=self.game.num_objects)
        self.current_player_label.config(text=f"Current player: {self.game.current_player}")
        if self.game.is_terminal():
            winner = "Human" if self.game.winner == 1 else "Computer"
            winner_label = tk.Label(self.window, text=f"{winner} wins!")
            winner_label.pack()

if __name__ == "__main__":
    gui = NimGUI()
    gui.window.mainloop()
