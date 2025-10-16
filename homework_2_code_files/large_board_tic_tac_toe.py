"""
Tic Tac Toe GUI with persistent board drawing and corrected cross/circle rendering.
"""

import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random


screen_width = 600
screen_height = 600
HEADER_SIZE = 200

pygame.init()

class Button:
    def __init__(self, rect, text, color, hover_color, text_color, action=None, font_size=28):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action  # function to call when clicked
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

class RandomBoardTicTacToe:
    def __init__(self, size=(screen_width, screen_height + HEADER_SIZE)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 3
        self.OFFSET = 5
        self.HEADER_SIZE = 200
        self.MARGIN = 5
        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        self.player_symbol = "X"  # Current symbol for human player
        self.mode = "player_vs_ai"

        # Define button colors
        gray = (180, 180, 180)
        light_gray = (220, 220, 220)
        black = (0, 0, 0)

        # Create buttons
        self.buttons = [
            # x, y, width, height
            Button((20, 30, 150, 40), f"Symbol: {self.player_symbol}", gray, light_gray, black, self.toggle_symbol),
            Button((20, 80, 250, 40), f"Mode: {self.mode}", gray, light_gray, black, self.change_mode),
            Button((20, 130, 150, 40), "Reset", gray, light_gray, black, self.game_reset),
            Button((430, 30, 150, 40), "Grid:", gray, light_gray, black, self.change_grid_size),
        ]

        # Initialize game state
        # If player chooses X, X goes first (turn_O=False)
        # If player chooses O, O goes first (turn_O=True)
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(board, turn_O=(self.player_symbol == "O"))

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = (self.size[0] - (self.GRID_SIZE + 1) * self.MARGIN) / self.GRID_SIZE
        self.HEIGHT = ((self.size[1] - self.HEADER_SIZE) / self.GRID_SIZE) - self.OFFSET

        # Initialize pygame display
        self.screen = pygame.display.set_mode(self.size)

    def draw_board(self):
        """
        Draws the static grid and header.
        """
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)

        # Draw header area
        header_rect = pygame.Rect(0, 0, self.size[0], self.HEADER_SIZE)
        pygame.draw.rect(self.screen, self.WHITE, header_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Draw grid cells
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = pygame.Rect(
                    col * (self.WIDTH + self.MARGIN) + self.MARGIN,
                    row * (self.HEIGHT + self.MARGIN) + self.HEADER_SIZE + self.MARGIN,
                    self.WIDTH,
                    self.HEIGHT,
                )
                pygame.draw.rect(self.screen, self.WHITE, rect)

        # Draw existing pieces on top
        self.update_pieces()
        pygame.display.update()

    def toggle_symbol(self):
        self.player_symbol = "O" if self.player_symbol == "X" else "X"
        print(f"Player symbol changed to {self.player_symbol}")
        self.buttons[0].text = f"Symbol: {self.player_symbol}"
        # Reset game when symbol changes to apply correct turn order
        self.game_reset()

    def change_mode(self):
        self.mode = "player_vs_player" if self.mode == "player_vs_ai" else "player_vs_ai"
        print(f"Game mode changed to {self.mode}")
        self.buttons[1].text = f"Mode: {self.mode}"
        self.draw_board()

    def change_grid_size(self):
        options = [3, 4, 5]
        
        current_index = options.index(self.GRID_SIZE)
        self.GRID_SIZE = options[(current_index + 1) % len(options)]
        GameStatus.win_length = self.GRID_SIZE  
        print(f"Grid size changed to {self.GRID_SIZE}x{self.GRID_SIZE}")
        # Reset game state with new grid size
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(board, turn_O=True)
        # Recalculate cell dimensions
        self.WIDTH = (self.size[0] - (self.GRID_SIZE + 1) * self.MARGIN) / self.GRID_SIZE
        self.HEIGHT = ((self.size[1] - self.HEADER_SIZE) / self.GRID_SIZE) - self.OFFSET
        self.buttons[3].text = f"Grid: {self.GRID_SIZE}"
        self.draw_board()
                                                            
    def update_pieces(self):
        """
        Redraws all crosses and circles from the board state.
        According to GameStatus: 1 = O, -1 = X
        """
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                val = self.game_state.board_state[row][col]
                if val == 1:   # O
                    self.draw_circle(row, col)
                elif val == -1:  # X
                    self.draw_cross(row, col)

    def draw_circle(self, row, col):
        # Calculate cell position
        x = col * (self.WIDTH + self.MARGIN) + self.MARGIN
        y = self.HEADER_SIZE + row * (self.HEIGHT + self.MARGIN) + self.MARGIN
        # Center and radius
        center = (int(x + self.WIDTH / 2), int(y + self.HEIGHT / 2))
        radius = int(min(self.WIDTH, self.HEIGHT) // 2 - 10)
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, center, radius, 8)

    def draw_cross(self, row, col):
        """
        Draws a thick, smooth X using polygons.
        """
        x = col * (self.WIDTH + self.MARGIN) + self.MARGIN
        y = self.HEADER_SIZE + row * (self.HEIGHT + self.MARGIN) + self.MARGIN
        w = self.WIDTH
        h = self.HEIGHT

        pad = 25         # distance from cell borders
        thickness = 18   # thickness of the X arms

        # Diagonal 1: top-left → bottom-right
        points1 = [
            (x + pad, y + pad + thickness),
            (x + pad + thickness, y + pad),
            (x + w - pad, y + h - pad - thickness),
            (x + w - pad - thickness, y + h - pad),
        ]

        # Diagonal 2: top-right → bottom-left
        points2 = [
            (x + w - pad - thickness, y + pad),
            (x + w - pad, y + pad + thickness),
            (x + pad + thickness, y + h - pad),
            (x + pad, y + h - pad - thickness),
        ]

        pygame.draw.polygon(self.screen, self.CROSS_COLOR, points1)
        pygame.draw.polygon(self.screen, self.CROSS_COLOR, points2)

    def change_turn(self):
        if self.game_state.turn_O:
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def is_game_over(self):
        return self.game_state.is_terminal()

    def get_winner_display(self):
        """
        Determines the actual winner based on player symbol choice.
        Returns (winner_text, color) tuple.
        """
        score = self.game_state.get_scores(terminal=True)
        
        if score == 0:
            return "Draw!", (255, 165, 0)  # Orange
        
        # Determine who won based on score and player symbol
        if self.player_symbol == "X":
            # Human is X (-1), AI is O (1)
            # Positive score = more X triplets = Human wins
            if score > 0:
                return "Human wins!", (0, 255, 0)  # Green
            else:
                return "AI wins!", (255, 0, 0)  # Red
        else:
            # Human is O (1), AI is X (-1)
            # Positive score = more X triplets = AI wins
            if score > 0:
                return "AI wins!", (255, 0, 0)  # Red
            else:
                return "Human wins!", (0, 255, 0)  # Green

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    # IMPLEMENT AI MOVE LOGIC HERE
    def play_ai(self):
        """AI makes a move using minimax or negamax algorithm."""
        if self.is_game_over():
            return

        possible_moves = self.game_state.get_moves()
        if not possible_moves:
            return
        
        use_minimax = True  # Change to False to use negamax

        if use_minimax:
            # Score is from human perspective: positive = human wins, negative = AI wins
            # AI always wants to MINIMIZE (get negative scores)
            # Human always wants to MAXIMIZE (get positive scores)
            # When it's AI's turn, we call minimax with maximizing_player=False
            _, best_move = minimax(self.game_state, depth=4, maximizing_player=False)
        else:
            # For negamax, we use turn_multiplier=-1 for AI (to minimize from human perspective)
            _, best_move = negamax(self.game_state, depth=4, turn_multiplier=-1)

        if best_move is not None:
            # Use get_new_state for cleaner state management
            self.game_state = self.game_state.get_new_state(best_move)
            
            self.update_pieces()
            self.change_turn()
        
        pygame.display.update()

    def game_reset(self):
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        # Reset game with proper turn based on player symbol
        self.game_state = GameStatus(board, turn_O=(self.player_symbol == "O"))
        self.draw_board()
        pygame.display.update()

    def play_game(self, mode="player_vs_ai"):
        done = False
        clock = pygame.time.Clock()
        self.draw_board()

        while not done:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                # Let buttons handle clicks first
                for button in self.buttons:
                    button.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Ignore clicks in the header (buttons live there)
                    if pos[1] < self.HEADER_SIZE:
                        continue

                    column = int(pos[0] // (self.WIDTH + self.MARGIN))
                    row = int((pos[1] - self.HEADER_SIZE) // (self.HEIGHT + self.MARGIN))
                    print(f"Click {pos} Grid coordinates: {row}, {column}")

                    # Check click validity
                    if 0 <= column < self.GRID_SIZE and 0 <= row < self.GRID_SIZE:
                        if self.game_state.board_state[row][column] == 0:
                            # Apply player move using get_new_state
                            self.game_state = self.game_state.get_new_state((row, column))
                            self.update_pieces()
                            pygame.display.update()

                            # Check if game ended after player move
                            if self.is_game_over():
                                print("Game Over")
                                score = self.game_state.get_scores(terminal=True)
                                winner_text, color = self.get_winner_display()
                                
                                # Display winner message
                                font = pygame.font.SysFont(None, 48)
                                text = font.render(f"{winner_text} Score: {score}", True, color)
                                self.screen.blit(text, (20, 80))
                                pygame.display.update()
                            else:
                                # AI's turn if in player vs AI mode
                                if self.mode == "player_vs_ai":
                                    self.play_ai()
                                    
                                    # Check if game ended after AI move
                                    if self.is_game_over():
                                        print("Game Over")
                                        score = self.game_state.get_scores(terminal=True)
                                        winner_text, color = self.get_winner_display()
                                        
                                        # Display winner message
                                        font = pygame.font.SysFont(None, 48)
                                        text = font.render(f"{winner_text} Score: {score}", True, color)
                                        self.screen.blit(text, (20, 80))
                                        pygame.display.update()
                        else:
                            print("Cell already occupied. Choose another cell.")
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
