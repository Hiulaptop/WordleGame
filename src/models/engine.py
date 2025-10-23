import pygame
from src.views.game_view import GameView
from src.models.words import Words


class Engine:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 1000
        self.key_font = pygame.font.Font(None, 50)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Word Game")
        self.clock = pygame.time.Clock()

        self.game_view = GameView(self.screen, self.key_font)

        self.word = Words()

        self.running = True
        self.restart = False

    def handleInput(self, event):
        if event.type == pygame.QUIT:
            self.running = False
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
                            self.game_view.tableData[self.game_view.current_row][j].color = (0, 255, 0)
                            self.game_view.set_key_color(cur[j], (0, 255, 0))
                        elif res[j] == "YELLOW":
                            self.game_view.tableData[self.game_view.current_row][j].color = (255, 255, 0)
                            self.game_view.set_key_color(cur[j], (255, 255, 0))
                        else:
                            self.game_view.tableData[self.game_view.current_row][j].color = (128, 128, 128)
                            self.game_view.set_key_color(cur[j], (0, 0, 0))
                    self.game_view.render()
                    if cnt == 5:
                        print("You Win!")
                        self.running = False
                    self.game_view.next_row()
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if not self.running:
                    break
                self.handleInput(event)
            self.game_view.render()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
