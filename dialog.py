# dialog.py
import pygame
from constants import *

class DialogBox:
    def __init__(self):
        self.font = pygame.font.SysFont('Verdana', 30)
        self.dialog_rect = pygame.Rect(dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height)
        self.options = ['Exit', 'Restart']
        self.selected_option = 0

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_WHITE, self.dialog_rect)
        pygame.draw.rect(screen, COLOR_BLACK, self.dialog_rect, 3)
        text_y = self.dialog_rect.y + 20
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, COLOR_BLACK)
            text_x = self.dialog_rect.x + (self.dialog_rect.width - text.get_width()) // 2
            text_y += 40
            screen.blit(text, (text_x, text_y))
            if i == self.selected_option:
                pygame.draw.rect(screen, COLOR_BLUE, (text_x - 10, text_y, text.get_width() + 20, text.get_height()), 3)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None
