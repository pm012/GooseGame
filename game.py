# game.py
import pygame
import random
from entities import Player, Enemy, Bonus
from dialog import DialogBox
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Verdana', 60)
        self.bg = pygame.transform.scale(pygame.image.load('res/background.png'), (WIDTH, HEIGHT))
        self.bg_x1 = 0
        self.bg_x2 = self.bg.get_width()
        self.bg_move = 3
        self.player = Player(50, HEIGHT // 2)
        self.enemies = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.score = 0
        self.create_entities()
        self.dialog_box = DialogBox()
        self.show_dialog = False  # Initialize show_dialog

    def create_entities(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
        pygame.time.set_timer(pygame.USEREVENT + 2, 1500)
        pygame.time.set_timer(pygame.USEREVENT + 3, 200)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.USEREVENT + 1:
                self.enemies.add(Enemy(WIDTH, random.randint(30, HEIGHT - 35)))
            elif event.type == pygame.USEREVENT + 2:
                self.bonuses.add(Bonus(random.randint(0, WIDTH - 90), -230))
            elif event.type == pygame.USEREVENT + 3:
                self.player.change_image()

             # Handle dialog box input events
            if self.show_dialog:
                if event.type == pygame.KEYDOWN:
                    option = self.dialog_box.handle_input(event)
                    if option == 'Exit':
                        return False
                    elif option == 'Restart':
                        self.reset_game()
                        self.show_dialog = False  # Hide dialog after choosing option
        return True

    def update_entities(self):
        if self.show_dialog:
            return True


        self.bg_x1 -= self.bg_move
        self.bg_x2 -= self.bg_move
        if self.bg_x1 < -self.bg.get_width():
            self.bg_x1 = self.bg.get_width()
        if self.bg_x2 < -self.bg.get_width():
            self.bg_x2 = self.bg.get_width()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.player.rect.bottom < HEIGHT:
            self.player.move(0, 4)
        if keys[pygame.K_RIGHT] and self.player.rect.right < WIDTH:
            self.player.move(4, 0)
        if keys[pygame.K_UP] and self.player.rect.top > 0:
            self.player.move(0, -4)
        if keys[pygame.K_LEFT] and self.player.rect.left > 0:
            self.player.move(-4, 0)

        for enemy in self.enemies:
            enemy.move()
            if enemy.rect.left < 0:
                enemy.kill()
            if pygame.sprite.collide_rect(self.player, enemy):
                self.show_dialog = True
                break

        # Handle dialog box
        if self.show_dialog:
            self.show_dialog = self.handle_dialog()

        for bonus in self.bonuses:
            bonus.move()
            if bonus.rect.bottom > HEIGHT:
                bonus.kill()
            if pygame.sprite.collide_rect(self.player, bonus):
                self.score += 1
                bonus.kill()
        return True

    def handle_dialog(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                option = self.dialog_box.handle_input(event)
                if option == 'Exit':
                    return False
                elif option == 'Restart':
                    self.reset_game()
                    return True
        return True

    def reset_game(self):
        self.score = 0
        self.player.rect.topleft = (50, HEIGHT // 2)
        self.enemies.empty()
        self.bonuses.empty()

    def run(self):
        running = True
        while running:
            self.clock.tick(120)
            running = self.handle_events()
            if not running:
                break

            running = self.update_entities()
            if not running:
                break

            self.screen.blit(self.bg, (self.bg_x1, 0))
            self.screen.blit(self.bg, (self.bg_x2, 0))
            self.enemies.draw(self.screen)
            self.bonuses.draw(self.screen)
            self.screen.blit(self.font.render(str(self.score), True, COLOR_RED), (WIDTH - 80, 60))
            self.screen.blit(self.player.image, self.player.rect)

            # Display dialog box if show_dialog is True
            if self.show_dialog:
                self.dialog_box.draw(self.screen)
                pygame.display.flip()

            pygame.display.flip()

        pygame.quit()
