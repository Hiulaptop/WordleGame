import pygame

class CellValue:
    def __init__(self, rn, cn, text, color):
        self.rn = rn
        self.cn = cn
        self.text = text
        self.color = color
    def set_text(self, text):
        self.text = text

class DataType:
    def __init__(self, tableData):
        self.tableData = tableData

class GameView:
    def __init__(self, screen, key_font):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = key_font
        self.current_row = 0
        self.current_column = 0
        self.tableData = []
        self.row = []
        self.key_color = []
        for i in range(100):
            self.key_color.append((100, 100, 100))
        for i in range(6):
            row = []
            for j in range(5):
                new_cell = CellValue(i, j, "", (100, 100, 100))
                row.append(new_cell)
            self.tableData.append(row)

    def next_row(self):
        if self.current_row <= 5:
            self.current_row += 1
            self.current_column = 0

    def add_text(self, text):
        # Accept only a single character, normalize to uppercase
        if not text:
            return
        ch = text[0].upper()
        if self.current_column == 5:
            return
        self.tableData[self.current_row][self.current_column].set_text(ch)
        self.current_column += 1

    def remove_text(self):
        """Backspace: remove the last character in the current row and move cursor left."""
        if self.current_column == 0:
            return
        self.current_column -= 1
        self.tableData[self.current_row][self.current_column].set_text("")

    def get_current_word(self):
        word = ""
        for j in range(5):
            word += self.tableData[self.current_row][j].text
        return word

    def set_key_color(self, key, color):
        self.key_color[ord(key)] = color

    def draw_cell(self, cellValue):
        width = 75
        height = 75
        gap = 10
        t_padding = 100
        l_padding = (self.screen_width - width * 5 - gap * 4) / 2
        x = l_padding + (width + gap) * cellValue.cn
        y = t_padding + (height + gap) * cellValue.rn
        pygame.draw.rect(self.screen, cellValue.color, (x, y, width, height), border_radius=5)
        if cellValue.text:
            text_surface = self.font.render(cellValue.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
            self.screen.blit(text_surface, text_rect)

    def draw_row(self, rowData):
        for cell in rowData:
            self.draw_cell(cell)

    def draw_table(self, tableData):
        for row in tableData:
            self.draw_row(row)


    def draw_keyboard(self):
        key = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        key_width = 50
        key_height = 65
        key_gap = 10
        start_y = 700

        for i, row in enumerate(key):
            row_width = len(row) * (key_width + key_gap) - key_gap
            start_x = (self.screen_width - row_width) / 2

            for j, char in enumerate(row):
                x = start_x + (key_width + key_gap) * j
                y = start_y + (key_height + key_gap) * i

                # Draw the key rectangle
                key_rect = pygame.Rect(x, y, key_width, key_height)
                pygame.draw.rect(self.screen, self.key_color[ord(char)], key_rect, border_radius=5)

                # Draw the letter on the key
                text_surface = self.font.render(char, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=key_rect.center)
                self.screen.blit(text_surface, text_rect)

    def render(self):
        # Clear the screen before drawing
        self.screen.fill((50, 50, 50))
        self.draw_table(self.tableData)
        self.draw_keyboard()