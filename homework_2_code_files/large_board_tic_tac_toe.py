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
HEADER_SIZE = 240

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
        # Define a modern, professional color palette (Modern Dark)
        self.DARK_BG = (34, 40, 49)       # Dark charcoal
        self.BOARD_BG = (57, 62, 70)      # Medium gray
        self.LINE_COLOR = (78, 86, 98)    # Lighter gray for lines
        self.WHITE = (238, 238, 238)      # Off-white for text
        self.SUCCESS_GREEN = (85, 173, 85) # Muted green
        self.ERROR_RED = (217, 83, 79)    # Muted red
        self.WARNING_ORANGE = (240, 173, 78) # Muted orange
        self.ACCENT_BLUE = (52, 152, 219) # Bright blue for highlights

        # Grid Size
        self.GRID_SIZE = 3
        self.OFFSET = 5
        self.HEADER_SIZE = 240
        self.MARGIN = 8
        self.CIRCLE_COLOR = (70, 171, 219) # A slightly different blue for O
        self.CROSS_COLOR = (217, 83, 79)   # Muted red for X
        
        self.player_symbol = "X"
        self.mode = "player_vs_ai"
        self.game_ended = False
        
        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0

        # Modern button styling
        button_color = (50, 55, 65)
        button_hover = self.ACCENT_BLUE
        button_text = self.WHITE

        self.buttons = [
            Button((20, 20, 160, 45), f"Symbol: {self.player_symbol}", button_color, button_hover, button_text, self.toggle_symbol_button, font_size=24),
            Button((200, 20, 220, 45), f"Mode: {self.mode.replace('_', ' ').title()}", button_color, button_hover, button_text, self.change_mode_button, font_size=24),
            Button((440, 20, 140, 45), f"Grid: {self.GRID_SIZE}x{self.GRID_SIZE}", button_color, button_hover, button_text, self.change_grid_size_button, font_size=24),
            Button((self.width/2 - 50, 75, 100, 40), "Reset", self.ERROR_RED, (192, 57, 43), button_text, self.game_reset_button, font_size=26),
        ]

        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(board, turn_O=(self.player_symbol == "O"), human_symbol=self.player_symbol)

        self.WIDTH = (self.size[0] - (self.GRID_SIZE + 1) * self.MARGIN) / self.GRID_SIZE
        self.HEIGHT = ((self.size[1] - self.HEADER_SIZE) / self.GRID_SIZE) - self.OFFSET

        self.screen = pygame.display.set_mode(self.size)

    def draw_board(self):
        pygame.display.set_caption("Tic Tac Toe - AI Challenge")
        self.screen.fill(self.DARK_BG)
        
        pygame.draw.rect(self.screen, self.BOARD_BG, (0, 0, self.width, self.HEADER_SIZE))

        for button in self.buttons:
            button.draw(self.screen)
        
        self.draw_scoreboard()

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = pygame.Rect(
                    col * (self.WIDTH + self.MARGIN) + self.MARGIN,
                    row * (self.HEIGHT + self.MARGIN) + self.HEADER_SIZE + self.MARGIN,
                    self.WIDTH,
                    self.HEIGHT,
                )
                pygame.draw.rect(self.screen, self.BOARD_BG, rect, border_radius=8)
                pygame.draw.rect(self.screen, self.LINE_COLOR, rect, 2, border_radius=8)

        self.update_pieces()
        pygame.display.update()
    
    def draw_scoreboard(self):
        scoreboard_y = 130
        
        score_bg = pygame.Rect(10, scoreboard_y, self.width - 20, 60)
        pygame.draw.rect(self.screen, self.LINE_COLOR, score_bg, border_radius=12)
        pygame.draw.rect(self.screen, self.BOARD_BG, score_bg.inflate(-4, -4), border_radius=10)
        
        title_font = pygame.font.SysFont('Arial', 22, bold=True)
        title_text = title_font.render("SCOREBOARD", True, self.ACCENT_BLUE)
        title_rect = title_text.get_rect(center=(self.width // 2, scoreboard_y + 20))
        self.screen.blit(title_text, title_rect)
        
        score_font = pygame.font.SysFont('Arial', 26, bold=True)
        scores_text = f"Human: {self.human_wins}    |    AI: {self.ai_wins}    |    Draws: {self.draws}"
        scores_surface = score_font.render(scores_text, True, self.WHITE)
        scores_rect = scores_surface.get_rect(center=(self.width // 2, scoreboard_y + 45))
        self.screen.blit(scores_surface, scores_rect)

    def toggle_symbol_button(self):
        self.player_symbol = "O" if self.player_symbol == "X" else "X"
        self.buttons[0].text = f"Symbol: {self.player_symbol}"
        
        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0
        
        self.game_ended = False
        self.game_reset()

    def change_mode_button(self):
        self.mode = "player_vs_player" if self.mode == "player_vs_ai" else "player_vs_ai"
        self.buttons[1].text = f"Mode: {self.mode.replace('_', ' ').title()}"
        
        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0
        
        self.game_ended = False
        self.game_reset()

    def change_grid_size_button(self):
        options = [3, 4, 5]
        
        current_index = options.index(self.GRID_SIZE)
        self.GRID_SIZE = options[(current_index + 1) % len(options)]
        GameStatus.win_length = 3 # Keep win condition as 3-in-a-row
        
        self.game_ended = False
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(board, turn_O=(self.player_symbol == "O"), human_symbol=self.player_symbol)
        
        self.WIDTH = (self.size[0] - (self.GRID_SIZE + 1) * self.MARGIN) / self.GRID_SIZE
        self.HEIGHT = ((self.size[1] - self.HEADER_SIZE) / self.GRID_SIZE) - self.OFFSET
        self.buttons[2].text = f"Grid: {self.GRID_SIZE}x{self.GRID_SIZE}"
        self.draw_board()

    def game_reset_button(self):
        print("Game reset")
        self.game_ended = False
        self.game_reset()
                                                            
    def update_pieces(self):
        pygame.draw.rect(self.screen, self.BOARD_BG, (0, 0, self.width, self.HEADER_SIZE))
        for button in self.buttons:
            button.draw(self.screen)
        self.draw_scoreboard()
        
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                val = self.game_state.board_state[row][col]
                if val == 1:   # O
                    self.draw_circle(row, col)
                elif val == -1:  # X
                    self.draw_cross(row, col)

    def draw_circle(self, row, col):
        x = col * (self.WIDTH + self.MARGIN) + self.MARGIN
        y = self.HEADER_SIZE + row * (self.HEIGHT + self.MARGIN) + self.MARGIN
        center = (int(x + self.WIDTH / 2), int(y + self.HEIGHT / 2))
        radius = int(min(self.WIDTH, self.HEIGHT) // 2 - 15)
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, center, radius, 10)

    def draw_cross(self, row, col):
        x = col * (self.WIDTH + self.MARGIN) + self.MARGIN
        y = self.HEADER_SIZE + row * (self.HEIGHT + self.MARGIN) + self.MARGIN
        w = self.WIDTH
        h = self.HEIGHT

        pad = 30
        thickness = 20

        points1 = [
            (x + pad, y + pad + thickness / 2),
            (x + pad + thickness / 2, y + pad),
            (x + w - pad, y + h - pad - thickness / 2),
            (x + w - pad - thickness / 2, y + h - pad),
        ]

        points2 = [
            (x + w - pad - thickness / 2, y + pad),
            (x + w - pad, y + pad + thickness / 2),
            (x + pad + thickness / 2, y + h - pad),
            (x + pad, y + h - pad - thickness / 2),
        ]

        pygame.draw.polygon(self.screen, self.CROSS_COLOR, points1)
        pygame.draw.polygon(self.screen, self.CROSS_COLOR, points2)

    def find_all_triplets(self):
        """Scan the current board and return all length-3 triplets.

        Returns a list of tuples: (ttype, start_row, start_col, value)
        where ttype is one of 'horizontal', 'vertical', 'diagonal_dr', 'diagonal_dl'
        and value is 1 (O) or -1 (X).
        """
        B = self.game_state.board_state
        R = self.GRID_SIZE
        C = self.GRID_SIZE
        L = 3
        triplets = []

        # horizontal
        for r in range(R):
            for c in range(C - L + 1):
                vals = [B[r][c + k] for k in range(L)]
                if vals[0] != 0 and all(v == vals[0] for v in vals):
                    triplets.append(('horizontal', r, c, vals[0]))

        # vertical
        for c in range(C):
            for r in range(R - L + 1):
                vals = [B[r + k][c] for k in range(L)]
                if vals[0] != 0 and all(v == vals[0] for v in vals):
                    triplets.append(('vertical', r, c, vals[0]))

        # diagonal down-right
        for r in range(R - L + 1):
            for c in range(C - L + 1):
                vals = [B[r + k][c + k] for k in range(L)]
                if vals[0] != 0 and all(v == vals[0] for v in vals):
                    triplets.append(('diagonal_dr', r, c, vals[0]))

        # diagonal down-left
        for r in range(R - L + 1):
            for c in range(L - 1, C):
                vals = [B[r + k][c - k] for k in range(L)]
                if vals[0] != 0 and all(v == vals[0] for v in vals):
                    triplets.append(('diagonal_dl', r, c, vals[0]))

        return triplets

    def draw_win_highlight(self):
        """Draw a semi-transparent highlight over winning triplet(s) for 3x3 games."""
        # Only apply for 3x3
        if self.GRID_SIZE != 3:
            return
        triplets = self.find_all_triplets()
        if not triplets:
            return
        # Use accent color with transparency
        highlight_color = (*self.ACCENT_BLUE, 120) if len(self.ACCENT_BLUE) == 3 else self.ACCENT_BLUE
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for t in triplets:
            ttype, r, c, val = t
            # compute rectangle covering the triplet
            if ttype == 'horizontal':
                x1 = c * (self.WIDTH + self.MARGIN) + self.MARGIN
                y1 = self.HEADER_SIZE + r * (self.HEIGHT + self.MARGIN) + self.MARGIN
                w = self.WIDTH * 3 + self.MARGIN * 2
                h = self.HEIGHT
                rect = pygame.Rect(int(x1), int(y1), int(w), int(h))
            elif ttype == 'vertical':
                x1 = c * (self.WIDTH + self.MARGIN) + self.MARGIN
                y1 = self.HEADER_SIZE + r * (self.HEIGHT + self.MARGIN) + self.MARGIN
                w = self.WIDTH
                h = self.HEIGHT * 3 + self.MARGIN * 2
                rect = pygame.Rect(int(x1), int(y1), int(w), int(h))
            elif ttype == 'diagonal_dr':
                # Draw a thick diagonal rectangle by drawing a rotated polygon
                start_x = c * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 2
                start_y = self.HEADER_SIZE + r * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 2
                end_x = (c + 2) * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 2
                end_y = self.HEADER_SIZE + (r + 2) * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 2
                pygame.draw.line(s, (*self.ACCENT_BLUE, 140), (int(start_x), int(start_y)), (int(end_x), int(end_y)), 20)
                continue
            else:  # diagonal_dl
                start_x = c * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 2
                start_y = self.HEADER_SIZE + r * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 2
                end_x = (c - 2) * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 2
                end_y = self.HEADER_SIZE + (r + 2) * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 2
                pygame.draw.line(s, (*self.ACCENT_BLUE, 140), (int(start_x), int(start_y)), (int(end_x), int(end_y)), 20)
                continue
            # fill semi-transparent rectangle
            pygame.draw.rect(s, (*self.ACCENT_BLUE, 80), rect, border_radius=8)
        self.screen.blit(s, (0, 0))

    def change_turn(self):
        if self.game_state.turn_O:
            pygame.display.set_caption("Tic Tac Toe - O's Turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's Turn")

    def is_game_over(self):
        return self.game_state.is_terminal()

    def update_persistent_score(self):
        score = self.game_state.get_scores(terminal=True)
        
        if score == 0:
            self.draws += 1
        elif score > 0:
            self.human_wins += 1
        else:
            self.ai_wins += 1
    
    def get_winner_display(self):
        score = self.game_state.get_scores(terminal=True)
        
        if score == 0:
            return "It's a Draw!", self.WARNING_ORANGE
        elif score > 0:
            return "Human Wins!", self.SUCCESS_GREEN
        else:
            return "AI Wins!", self.ERROR_RED

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        print(f"AI turn: turn_O={self.game_state.turn_O}, player_symbol={self.player_symbol}")
        
        if self.is_game_over():
            return

        possible_moves = self.game_state.get_moves()
        if not possible_moves:
            return
        
        # Let's use Negamax for the AI player
        use_minimax = False

        if use_minimax:
            _, best_move = minimax(self.game_state, depth=4, maximizing_player=False)
        else:
            # For negamax, turn_multiplier is -1 for AI, 1 for human
            turn_multiplier = 1 if self.game_state.turn_O == (self.player_symbol == "O") else -1
            _, best_move = negamax(self.game_state, depth=4, turn_multiplier=turn_multiplier)

        if best_move is not None:
            print(f"AI chose move: {best_move}")
            self.game_state = self.game_state.get_new_state(best_move)
            
            self.update_pieces()
            self.change_turn()
        
        pygame.display.update()

    def game_reset(self):
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(board, turn_O=(self.player_symbol == "O"), human_symbol=self.player_symbol)
        self.draw_board()
        pygame.display.update()

    def play_game(self, mode="player_vs_ai"):
        done = False
        clock = pygame.time.Clock()
        self.draw_board()
        
        if self.mode == "player_vs_ai" and self.player_symbol == "O":
            self.play_ai()

        while not done:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                for button in self.buttons:
                    button.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if pos[1] < self.HEADER_SIZE:
                        continue

                    if self.game_ended:
                        print("Game is over. Please reset to play again.")
                        continue

                    column = int(pos[0] // (self.WIDTH + self.MARGIN))
                    row = int((pos[1] - self.HEADER_SIZE) // (self.HEIGHT + self.MARGIN))
                    
                    if 0 <= column < self.GRID_SIZE and 0 <= row < self.GRID_SIZE:
                        if self.game_state.board_state[row][column] == 0:
                            is_player_turn = (self.player_symbol == "X" and not self.game_state.turn_O) or \
                                           (self.player_symbol == "O" and self.game_state.turn_O)
                            
                            if not is_player_turn and self.mode == "player_vs_ai":
                                print("Not your turn! Wait for AI...")
                                continue
                                
                            self.game_state = self.game_state.get_new_state((row, column))
                            self.update_pieces()
                            pygame.display.update()

                            # Check if game is over after player move
                            terminal = self.game_state.is_terminal()
                            if terminal:
                                score = self.game_state.get_scores(terminal)
                                self.game_ended = True
                                self.update_persistent_score()
                                # Highlight winning triplet(s) immediately for 3x3
                                self.draw_win_highlight()
                                winner_text, color = self.get_winner_display()
                                self.draw_scoreboard()
                                
                                font = pygame.font.SysFont('Arial', 52, bold=True)
                                text = font.render(winner_text, True, color)
                                text_rect = text.get_rect(center=(self.width // 2, self.HEADER_SIZE / 2 + 20))
                                
                                # Add a subtle shadow effect
                                shadow = font.render(winner_text, True, (0,0,0,50))
                                self.screen.blit(shadow, text_rect.move(2,2))
                                self.screen.blit(text, text_rect)
                                
                                pygame.display.update()
                            else:
                                if self.mode == "player_vs_ai":
                                    pygame.time.wait(500) # Add a small delay for realism
                                    self.play_ai()
                                    
                                    # Check if game is over after AI move
                                    terminal = self.game_state.is_terminal()
                                    if terminal:
                                        score = self.game_state.get_scores(terminal)
                                        self.game_ended = True
                                        self.update_persistent_score()
                                        # Highlight winning triplet(s) immediately for 3x3
                                        self.draw_win_highlight()
                                        winner_text, color = self.get_winner_display()
                                        self.draw_scoreboard()
                                        
                                        font = pygame.font.SysFont('Arial', 52, bold=True)
                                        text = font.render(winner_text, True, color)
                                        text_rect = text.get_rect(center=(self.width // 2, self.HEADER_SIZE / 2 + 20))
                                        
                                        shadow = font.render(winner_text, True, (0,0,0,50))
                                        self.screen.blit(shadow, text_rect.move(2,2))
                                        self.screen.blit(text, text_rect)
                                        
                                        pygame.display.update()
                        else:
                            print("Cell already occupied. Choose another cell.")
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
