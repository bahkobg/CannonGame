import pygame
import random

pygame.init()


class Cannon:
    """ Describe the cannon's attributes and methods """

    def __init__(self, surface):
        self.WIDTH = 533
        self.pos_x = 200
        self.pos_y = 698
        self.img = pygame.image.load('cannon.png')
        self.direction = 'left'
        self.screen = surface
        self.speed = 0
        self.cannon_sound = pygame.mixer.Sound('cart.wav')
        self.fire_sound = pygame.mixer.Sound('fire.wav')
        self.cannon_sound.set_volume(0.5)

    def draw(self):
        """
        This method is called from the Runtime class to draw the on the main surface.
        It calls the cannon move method
        :return:None
        """
        if self.direction == 'right':
            self.screen.blit(pygame.transform.flip(self.img, True, False), (self.pos_x, self.pos_y))
        elif self.direction == 'left':
            self.screen.blit(self.img, (self.pos_x, self.pos_y))
        self._move()

    def set_direction(self, direction):
        """
        Set cannon direction
        :param direction: str 'left' or 'right'
        :return: None
        """
        self.direction = direction

    def set_speed(self, speed):
        """
        Set cannon speed.
        :param speed: int
        :return: None
        """
        self.speed = speed

    def _move(self):
        if self.direction is 'left':
            self.pos_x -= self.speed
            if self.pos_x <= 3:
                self.pos_x = 3
        elif self.direction is 'right':
            self.pos_x += self.speed
            if self.pos_x >= self.WIDTH:
                self.pos_x = self.WIDTH

    @property
    def get_direction(self):
        """
        Returns cannon's horizontal orientation.
        :return:
        """
        return self.direction

    @property
    def get_position(self):
        """
        Returns cannon's horizontal position.
        :return:
        """
        return self.pos_x

    def get_sound(self):
        """
        Plays sound effect.
        :return: None
        """
        pygame.mixer.Sound.play(self.cannon_sound, -1)

    def set_sound_stop(self):
        """
        Plays sound effect.
        :return: None
        """
        pygame.mixer.Sound.stop(self.cannon_sound)

    def set_sound_fire(self):
        """
        Plays sound effect
        :return: None
        """
        pygame.mixer.Sound.play(self.fire_sound)


class TreasureChest:
    def __init__(self, surface):
        self.pos_x = random.randint(20, 520)
        self.pos_y = random.randint(50, 500)
        self.img = pygame.image.load('chest1.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)
        self.screen = surface
        self.status = 'normal'

    def draw(self):
        if self.status == 'normal':
            self.screen.blit(self.img, (self.pos_x, self.pos_y))

    @property
    def get_rect(self):
        """
        Returns
        :return:
        """
        return self.rect

    def set_hit(self):
        self.status = 'hit'
        self.screen.blit(pygame.transform.rotozoom(self.img, 0, 1.2), (self.pos_x, self.pos_y))


class CannonBall:
    def __init__(self, surface, chest_list, menu):
        self.pos_x = 0
        self.pos_y = 708
        self.speed_x = 4.5
        self.speed_y = 3
        self.state = 'ready'
        self.orientation = ''
        self.screen = surface
        self.img = pygame.image.load('ball.png')
        self.treasure_chests = chest_list
        self.hit_sound = pygame.mixer.Sound('hit.wav')
        self.game_menu = menu

    def draw(self):
        if self.state == 'moving':
            self.screen.blit(self.img, (self.pos_x, self.pos_y))
            self._move()

    def _move(self):
        if self.pos_y <= 0:
            self.speed_y = -1 * self.speed_y
        elif self.pos_y >= 800:
            self.state = 'ready'
            self.pos_y = 708
            self.speed_x = abs(self.speed_x)
            self.speed_y = abs(self.speed_y)

        if self.pos_x <= 0:
            self.speed_x = abs(self.speed_x)
        elif self.pos_x >= 581:
            self.speed_x = -1 * abs(self.speed_x)

        for i in range(len(self.treasure_chests) - 1, -1, -1):
            if self.treasure_chests[i].get_rect.colliderect(pygame.Rect(self.pos_x, self.pos_y, 16, 16)):
                pygame.mixer.Sound.play(self.hit_sound)
                self.treasure_chests[i].set_hit()
                self.game_menu.set_score()
                self.treasure_chests.remove(self.treasure_chests[i])

        self.pos_x += self.speed_x
        self.pos_y -= self.speed_y

    def set_position(self, x):
        if self.state is not 'moving':
            if self.orientation == 'left':
                self.pos_x = x
            elif self.orientation == 'right':
                self.pos_x = x + 64

    def set_state(self, state):
        if self.state is not 'moving':
            self.state = state

    def set_orientation(self, orientation):
        if self.state is not 'moving':
            self.orientation = orientation
            if self.orientation == 'left':
                self.speed_x = -1 * abs(self.speed_x)
            elif self.orientation == 'right':
                self.speed_x = abs(self.speed_x)

    def set_treasure_chests(self, chest_list):
        self.treasure_chests = chest_list

    @property
    def get_state(self):
        """
        Returns the state of the cannon ball -> 'ready' or 'moving'
        :return: str
        """
        return self.state


class GameBoard:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.bg = pygame.image.load('bg1.png')
        self.icon = pygame.image.load('icon.png')

    def draw(self):
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Cannon Game Designed by Ivan Ivanov')
        self.screen.blit(self.bg, (0, 0))

    def get_surface(self):
        return self.screen


class GameMenu:
    def __init__(self, surface):
        self.score = 1
        self.level = 1
        self.screen = surface
        self.text = pygame.font.Font(None, 36)
        self.main_menu_img = pygame.image.load('menu.png')

    @property
    def get_level(self):
        return self.level

    def set_level(self):
        self.level += 1

    def set_score(self):
        self.score += 1
        if self.score % 10 == 0:
            self.set_level()

    def draw(self):
        self.screen.blit(self.text.render('SCORE: {}'.format(self.score), True, (255, 255, 255)), (460, 20))

    def display_main_menu(self):
        self.screen.blit(self.main_menu_img, (0, 0))

    @property
    def get_new_game(self):
        return pygame.Rect(168, 346, 250, 80)

    @property
    def get_exit(self):
        return pygame.Rect(168, 611, 250, 80)


class GameRuntime:
    def __init__(self):
        self.game_board = GameBoard()
        self.screen = self.game_board.get_surface()
        self.cannon = Cannon(self.screen)
        self.game_menu = GameMenu(self.screen)
        self.treasure_chests = [TreasureChest(self.screen)]
        self.cannon_ball = CannonBall(self.screen, self.treasure_chests, self.game_menu)
        self.game_state = 0  # Either 0 for Main menu or 1 for in game
        pygame.mixer.music.load('bg_music.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

    def set_treasure_chests(self):
        self.treasure_chests.extend([TreasureChest(self.screen) for x in range(self.game_menu.get_level)])
        self.cannon_ball.set_treasure_chests(self.treasure_chests)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # KEY IS PRESSED
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cannon.set_direction('left')
                        self.cannon.set_speed(1)
                        self.cannon.get_sound()
                    if event.key == pygame.K_RIGHT:
                        self.cannon.set_direction('right')
                        self.cannon.set_speed(1)
                        self.cannon.get_sound()
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_SPACE:
                        if self.cannon_ball.get_state == 'ready':
                            self.cannon.set_sound_fire()
                        self.cannon_ball.set_orientation(self.cannon.get_direction)
                        self.cannon_ball.set_position(self.cannon.get_position)
                        self.cannon_ball.set_state('moving')

                # KEY IS RELEASED
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.cannon.set_speed(0)
                        self.cannon.set_sound_stop()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        pass

                # MOUSE EVENTS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                    if self.game_menu.get_new_game.collidepoint(pygame.mouse.get_pos()):
                        self.game_state = 1
                    if self.game_menu.get_exit.collidepoint(pygame.mouse.get_pos()):
                        running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pass

            if self.game_state == 0:
                self.game_menu.display_main_menu()
                pygame.display.update()
            elif self.game_state == 1:
                self.game_board.draw()
                self.cannon.draw()
                self.cannon_ball.draw()
                self.game_menu.draw()

                for treasure_chest in self.treasure_chests:
                    treasure_chest.draw()
                if len(self.treasure_chests) < 1:
                    self.set_treasure_chests()
                pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    g = GameRuntime()
    g.run()
