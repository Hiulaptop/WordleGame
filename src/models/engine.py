import pygame
from src.views.game_view import GameView
from src.models.words import Words


class Engine:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 1000

        self.key_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 70)
        self.button_font = pygame.font.Font(None, 40)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Word Game")
        self.clock = pygame.time.Clock()

        self.game_view = GameView(self.screen, self.key_font)
        self.word = Words()

        self.running = True
        self.state = "PLAYING"
        self.game_result = ""

        self.restart_button = pygame.Rect(0, 0, 180, 50)
        self.quit_button = pygame.Rect(0, 0, 180, 50)

    def restart_game(self):
        print("Restarting game...")
        self.word.get_random_word()
        self.game_view = GameView(self.screen, self.key_font)
        self.state = "PLAYING"
        self.game_result = ""

    def handle_play_input(self, event):
        if event.type == pygame.KEYDOWN:
            k = event.key
            if pygame.K_a <= k <= pygame.K_z:
                self.game_view.add_text(chr(k).upper())
            if k == pygame.K_BACKSPACE:
                self.game_view.remove_text()
            if k == pygame.K_RETURN and self.game_view.current_column == 5:
                print(self.game_view.get_current_word())
                cur = self.game_view.get_current_word()
                res = self.word.check_word(cur)
                cnt = 0

                if res != False:
                    for j in range(5):
                        if res[j] == "GREEN":
                            cnt += 1
                            self.game_view.tableData[self.game_view.current_row][j].color = (0, 150, 0)
                            self.game_view.set_key_color(cur[j], (0, 150, 0))
                        elif res[j] == "YELLOW":
                            self.game_view.tableData[self.game_view.current_row][j].color = (200, 200, 0)
                            self.game_view.set_key_color(cur[j], (200, 200, 0))
                        else:
                            self.game_view.tableData[self.game_view.current_row][j].color = (128, 128, 128)
                            if self.game_view.key_color[ord(cur[j])] == (100, 100, 100):
                                self.game_view.set_key_color(cur[j], (50, 50, 50))

                    self.game_view.render()

                    if cnt == 5:
                        print("You Win!")
                        self.state = "GAME_OVER"
                        self.game_result = "WIN"
                    else:
                        self.game_view.next_row()
                        if self.game_view.current_row == 6:
                            print("You Lose!")
                            self.state = "GAME_OVER"
                            self.game_result = "LOSE"

    def handle_end_screen_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.restart_button.collidepoint(pos):
                self.restart_game()
            if self.quit_button.collidepoint(pos):
                self.running = False

    def draw_end_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 180))
        self.screen.blit(overlay, (0, 0))

        if self.game_result == "WIN":
            message = "You Win!"
            color = (0, 255, 0)
        else:
            message = f"You Lose! The word was: {self.word._word}"
            color = (255, 0, 0)

        text_surf = self.title_font.render(message, True, color)
        text_rect = text_surf.get_rect(center=(self.screen_width / 2, 300))
        self.screen.blit(text_surf, text_rect)

        center_x = self.screen_width / 2
        self.restart_button.center = (center_x - 110, 400)
        self.quit_button.center = (center_x + 110, 400)

        pygame.draw.rect(self.screen, (0, 150, 0), self.restart_button, border_radius=10)
        restart_text = self.button_font.render("Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, restart_text.get_rect(center=self.restart_button.center))

        pygame.draw.rect(self.screen, (150, 0, 0), self.quit_button, border_radius=10)
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if self.state == "PLAYING":
                    self.handle_play_input(event)
                elif self.state == "GAME_OVER":
                    self.handle_end_screen_input(event)

            if not self.running:
                break

            self.game_view.render()

            if self.state == "GAME_OVER":
                self.draw_end_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()