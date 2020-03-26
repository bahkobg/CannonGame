import pygame
import random

pygame.init()


class Cannon:
    """ Describe the cannon's attributes and methods """

    def __init__(self):
        self.WIDTH = 533
        self.pos_x = 200
        self.pos_y = 698
        self.imgs = [pygame.image.load('cannon' + str(x) + '.png') for x in range(1, 3)]
        self.direction = 'left'
        self.speed = 0
        self.cannon_sound = pygame.mixer.Sound('cart.wav')
        self.fire_sound = pygame.mixer.Sound('fire.wav')
        self.cannon_sound.set_volume(0.5)  # Set the volume
        self.animation_count = 0  # Used to animate movement

    def draw(self, surface):
        """
        This method is called from the Runtime class to draw the on the main surface.
        It calls the cannon move method
        :return:None
        """

        # Animation_count is used as index in the img list
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        # Check if the cannon is moving left or right
        if self.direction == 'right':
            # If the cannon is NOT moving -> don't animate
            if self.speed == 0:
                surface.blit(pygame.transform.flip(self.imgs[0], True, False), (self.pos_x, self.pos_y))
            # If the cannon is moving -> loop through the img list
            elif self.speed > 0:
                surface.blit(pygame.transform.flip(self.imgs[self.animation_count], True, False), (self.pos_x, self.pos_y))
        # Check if the cannon is moving left or right
        elif self.direction == 'left':
            # If the cannon is NOT moving -> don't animate
            if self.speed == 0:
                surface.blit(self.imgs[0], (self.pos_x, self.pos_y))
            # If the cannon is moving -> loop through the img list
            elif self.speed > 0:
                surface.blit(self.imgs[self.animation_count], (self.pos_x, self.pos_y))

        self.animation_count += 1
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
        if self.direction == 'left':
            self.pos_x -= self.speed
            if self.pos_x <= 3:
                self.pos_x = 3
        elif self.direction == 'right':
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
    def __init__(self):
        self.pos_x = random.randint(20, 520)
        self.pos_y = random.randint(50, 500)
        self.img = pygame.image.load('chest1.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)
        self.status = 'normal'

    def draw(self, surface):
        if self.status == 'normal':
            surface.blit(self.img, (self.pos_x, self.pos_y))

    @property
    def get_rect(self):
        """
        Returns
        :return:
        """
        return self.rect

    def set_hit(self):
        self.status = 'hit'


class Tnt(TreasureChest):

    def __init__(self):
        self.imgs = [pygame.image.load('tnt' + str(x) + '.png')
                     for x in range(1, 5)]


class CannonBall:
    def __init__(self, chest_list, menu):
        self.pos_x = 0
        self.pos_y = 708
        self.speed_y = 3
        self.speed_x = round(1.73 * self.speed_y)
        self.state = 'ready'
        self.orientation = ''
        self.img = pygame.image.load('ball.png')
        self.treasure_chests = chest_list
        self.hit_sound = pygame.mixer.Sound('hit.wav')
        self.bounce = pygame.mixer.Sound('bounce.wav')
        self.game_menu = menu
        self.ball_count = 12

    def set_ball_count_to_default(self):
        """
        Set the ball count to default value
        :return: None
        """
        self.ball_count = 12

    @property
    def get_ball_count(self):
        """
        Returns ball count
        :return: int
        """
        return self.ball_count

    def set_decrease_ball_count(self):
        """
        Decrease the ball count
        :return: None
        """
        self.ball_count -= 1

    def draw(self, surface):
        if self.state == 'moving':
            surface.blit(self.img, (self.pos_x, self.pos_y))
            self._move()

    def _move(self):
        if self.pos_y <= 0:
            self.speed_y = -1 * self.speed_y
            pygame.mixer.Sound.play(self.bounce)
        elif self.pos_y >= 800:
            self.state = 'ready'
            self.pos_y = 708
            self.speed_x = abs(self.speed_x)
            self.speed_y = abs(self.speed_y)

        if self.pos_x <= 0:
            self.speed_x = abs(self.speed_x)
            pygame.mixer.Sound.play(self.bounce)
        elif self.pos_x >= 581:
            self.speed_x = -1 * abs(self.speed_x)
            pygame.mixer.Sound.play(self.bounce)

        for i in range(len(self.treasure_chests) - 1, -1, -1):
            if self.treasure_chests[i].get_rect.colliderect(pygame.Rect(self.pos_x, self.pos_y, 16, 16)):
                pygame.mixer.Sound.play(self.hit_sound)
                self.treasure_chests[i].set_hit()
                self.game_menu.set_score()
                self.treasure_chests.remove(self.treasure_chests[i])

        self.pos_x += self.speed_x
        self.pos_y -= self.speed_y

    def set_position(self, x):
        if self.state != 'moving':
            if self.orientation == 'left':
                self.pos_x = x
            elif self.orientation == 'right':
                self.pos_x = x + 64

    def set_state(self, state):
        """
        Prevents multiple keypresses of SPACE key
        :param state: str -> TODO this may be int
        :return: None
        """
        if self.state != 'moving':
            self.state = state

    def set_orientation(self, orientation):
        if self.state != 'moving':
            self.orientation = orientation
            if self.orientation == 'left':
                self.speed_x = -1 * abs(self.speed_x)
            elif self.orientation == 'right':
                self.speed_x = abs(self.speed_x)

    def set_treasure_chests(self, chest_list):
        """
        Interface to set new treasure chest list
        :param chest_list: list
        :return: None
        """
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
        """
        Return the main surface area
        :return: Display object
        """
        return self.screen


class GameMenu:
    def __init__(self):
        self.score = 1
        self.level = 1
        self.text = pygame.font.Font(None, 18)
        self.main_menu_img = pygame.image.load('menu.png')
        self.score_menu = pygame.image.load('score.png')
        self.num_of_balls = pygame.image.load('bombs.png')
        self.level_img = pygame.image.load('level.png')
        self.game_over_img = pygame.image.load('game_over.png')
        self.game_over_sound = pygame.mixer.Sound('game_over.wav')

    @property
    def get_level(self):
        """
        Returns the current level
        :return: int
        """
        return self.level

    @property
    def get_score(self):
        """
        Returns the current score
        :return: int
        """
        return self.score

    def set_level(self):
        """
        Level up
        :return: None
        """
        self.level += 1

    def set_score(self):
        """
        Increase the score and the level
        :return: None
        """
        self.score += 1
        if self.score % (10 * self.level) == 0:
            self.set_level()

    def draw(self, surface, ball_count):
        surface.blit(self.score_menu, (460, 4))
        surface.blit(self.num_of_balls, (330, 4))
        surface.blit(self.level_img, (212, 10))
        surface.blit(self.text.render(str(ball_count), True, (255, 255, 255)), (412, 27))
        surface.blit(self.text.render(str(self.score), True, (255, 255, 255)), (540, 27))
        surface.blit(self.text.render(str(self.level), True, (255, 255, 255)), (282, 29))

    def display_main_menu(self, surface):
        surface.blit(self.main_menu_img, (0, 0))

    @property
    def get_new_game(self):
        """
        Returns the surface area of the new game button
        :return: Rect
        """
        return pygame.Rect(168, 346, 250, 80)

    @property
    def get_exit(self):
        """
        Returns the surface area of the exit button
        :return: Rect object
        """
        return pygame.Rect(168, 611, 250, 80)

    def set_game_over(self, surface):
        """
        Draws the game over image
        :param surface: Surface object
        :return: None
        """
        surface.blit(self.game_over_img, (150, 150))


class GameRuntime:
    def __init__(self):
        self.game_board = GameBoard()
        self.screen = self.game_board.get_surface()
        self.cannon = Cannon()
        self.game_menu = GameMenu()
        self.treasure_chests = [TreasureChest()]
        self.cannon_ball = CannonBall(self.treasure_chests, self.game_menu)
        self.game_state = 0  # Either 0 for main menu | 1 for in game | 2 for game over
        self.number_of_balls = self.cannon_ball.get_ball_count
        pygame.mixer.music.load('bg_music.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        self.clock = pygame.time.Clock()

    def set_treasure_chests(self):
        self.treasure_chests.extend([TreasureChest() for x in range(self.game_menu.get_level)])
        self.cannon_ball.set_treasure_chests(self.treasure_chests)

    def set_ball_count(self):
        """
        If the number of balls available get under 0 game over
        :return: None
        """
        self.number_of_balls -= 1
        if self.number_of_balls <= 0:
            self.game_state = 2



    @property
    def get_ball_count(self):
        """
        Returns the number of cannon balls left.
        :return: int
        """
        return self.number_of_balls

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
                            self.set_ball_count()
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
                self.game_menu.display_main_menu(self.screen)
                pygame.display.update()
            elif self.game_state == 1:
                self.game_board.draw()
                self.cannon.draw(self.screen)
                self.cannon_ball.draw(self.screen)
                self.game_menu.draw(self.screen, self.number_of_balls)

                for treasure_chest in self.treasure_chests:
                    treasure_chest.draw(self.screen)
                if len(self.treasure_chests) < 1:
                    self.set_treasure_chests()
                    if self.game_menu.get_score % (10 * self.game_menu.get_level) == 0:
                        self.number_of_balls = 12

                pygame.display.update()
            elif self.game_state == 2:
                self.game_board.draw()
                self.game_menu.set_game_over(self.screen)
                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    g = GameRuntime()
    g.run()
