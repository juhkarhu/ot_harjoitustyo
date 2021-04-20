import sys
import os
import pygame
import pygame.locals
from pygame.constants import MOUSEBUTTONDOWN
import data.lemminki
import data.settings
import data.world
import data.points


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        # Font for rendering text
        self.game_font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.Font(None, 65)
        self.intro_text_font = pygame.font.Font(None, 45)

        self.clock = pygame.time.Clock()
        self.intro = True
        self.intro_loop()

    def set_player_variables(self):
        self.character_scale = 3
        self.throw_cooldown = 0
        self.control = False
        self.left = False
        self.right = False
        self.jump = False
        self.shoot = False
        self.interval = 1600
        self.ADD_LEMMING = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_LEMMING, self.interval)

    def load_tile_images(self):
        self.grass_image = pygame.image.load('img/ground_tiles/top_ground.png')
        self.dirt_image = pygame.image.load(
            'img/ground_tiles/middle_ground.png')

    def set_game_variables(self):
        self.max_players = 3
        self.player = None
        self.player_id = 0
        self.points = 0
        # Countdown timer for level
        self.counter, self.text = 80, '80'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.all_players_spawned = False

    def load_game_data(self):
        self.controlled_player_list = []
        self.npc_list = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.thrown_rocks = pygame.sprite.Group()
        self.num_of_players_spawned = 0
        self.load_tile_images()

        self.game_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
            [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 3, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 1, 2, 2, 2, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 10, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def read_map_data(self):
        '''
        Reads the map array and assigns objects depending on the value on the array. 
        1 and 2 are ground tiles,
        3 is an enemy,
        10 is the starting locations for the player,
        8 is the door that finishes the level.
        '''
        self.tile_rects = []
        for row_num, row in enumerate(self.game_map):
            for col_num, tile in enumerate(row):
                if tile == 10:
                    self.starting_pos = None
                    self.starting_position = (
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE)
                if tile in [1, 2]:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                if tile == 1:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                    tile = data.world.Tile(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        self.dirt_image)
                    self.map_sprites.add(tile)
                if tile == 2:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                    tile = data.world.Tile(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        self.grass_image)
                    self.map_sprites.add(tile)
                if tile == 3:
                    identifier = os.urandom(16).hex()
                    new_npc = data.lemminki.Lemminki('enemy', self.character_scale, (
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE), identifier)
                    self.npc_list.add(new_npc)
                if tile == 8:
                    door = data.world.Door(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE)
                    self.map_sprites.add(door)
                    self.door_list.add(door)

    def set_gamedisplay_settings(self):
        '''
        Sets the display settings for game.
        '''
        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        print(self.height, self.width)
        data.settings.SCREEN_HEIGHT = data.settings.SCALA * self.height
        data.settings.SCREEN_WIDTH = data.settings.SCALA * self.width
        self.WINDOW_SIZE = (data.settings.SCREEN_HEIGHT,
                            data.settings.SCREEN_WIDTH)
        self.screen = pygame.display.set_mode(
            (data.settings.SCREEN_WIDTH, data.settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Lemminki')

    def set_introdisplay_settings(self):
        '''
        Sets the display settings for menu.
        '''
        # Screen size is the same as the game map.
        # This would be different but then the winwos position shifts when game is started and
        # that's no good.
        data.settings.SCREEN_HEIGHT = data.settings.SCALA * 19
        data.settings.SCREEN_WIDTH = data.settings.SCALA * 20
        self.WINDOW_SIZE = (data.settings.SCREEN_HEIGHT,
                            data.settings.SCREEN_WIDTH)
        self.screen = pygame.display.set_mode(
            (data.settings.SCREEN_WIDTH, data.settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Lemminki')

    def intro_loop(self):
        '''
        Intro - the main menu at the moment - is processed here. 
        High score displays in the menu.
        '''
        self.set_introdisplay_settings()
        points_list = data.points.read_points()
        while self.intro:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                    if tapahtuma.key == pygame.K_RETURN:
                        self.set_game_variables()
                        self.set_player_variables()
                        self.load_game_data()
                        self.read_map_data()
                        self.set_gamedisplay_settings()
                        self.game_loop()

            self.screen.fill(data.settings.SKYBLUE)

            game_name = self.title_font.render(
                'Lemminki', True, data.settings.RED)
            help_text = self.intro_text_font.render(
                'Press enter to start playing.', True, data.settings.RED)
            tutorial_text = self.intro_text_font.render(
                'Control with A and S keys and jump with W.', True, data.settings.RED)
            tutorial2_text = self.intro_text_font.render(
                'Select a controllable character with your mouse and', True, data.settings.RED)
            tutorial3_text = self.intro_text_font.render(
                'click him to start controlling.', True, data.settings.RED)
            tutorial4_text = self.intro_text_font.render(
                'Guide as many as you can to the finish!', True, data.settings.RED)

            game_name_text_rect = game_name.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2-80))
            help_text_rect = help_text.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2))
            tutorial_text_rect = tutorial_text.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+50))
            tutorial2_text_rect = tutorial2_text.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+80))
            tutorial3_text_rect = tutorial3_text.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+110))
            tutorial4_text_rect = tutorial4_text.get_rect(
                center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+140))

            if (len(points_list)) >= 3:
                top_score_text = self.intro_text_font.render(
                    'Top 3 High Scores', True, data.settings.RED)
                top_scorers = []
                offset = 250
                for i in range(3):
                    username = points_list[i][0]
                    points = points_list[i][1]
                    top_text = self.intro_text_font.render(
                        f'{username, points}', True, data.settings.RED)
                    top_text_rect = top_text.get_rect(
                        center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+offset))
                    top_scorers.append((top_text, top_text_rect))
                    offset += 30

                top_score_text_rect = top_score_text.get_rect(
                    center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2+220))
                for text, rect in top_scorers:
                    self.screen.blit(text, rect)

                self.screen.blit(top_score_text, top_score_text_rect)

            # you_died_text_rect = top_score_text.get_rect(
            #     center=(data.settings.SCREEN_WIDTH/2, data.settings.SCREEN_HEIGHT/2-100))

            self.screen.blit(game_name, game_name_text_rect)
            self.screen.blit(help_text, help_text_rect)
            self.screen.blit(tutorial_text, tutorial_text_rect)
            self.screen.blit(tutorial2_text, tutorial2_text_rect)
            self.screen.blit(tutorial3_text, tutorial3_text_rect)
            self.screen.blit(tutorial4_text, tutorial4_text_rect)

            pygame.display.flip()
            self.clock.tick(15)

    def check_events(self):
        '''
        Checks for events and keystrokes.
        '''
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    # self.intro_loop()
                    pygame.quit()
                    sys.exit()
                if self.control:
                    if event.key == pygame.K_a:
                        self.left = True
                    if event.key == pygame.K_d:
                        self.right = True
                    if event.key == pygame.K_SPACE:
                        if self.throw_cooldown == 0:
                            self.throw_cooldown = 25
                            rock = data.world.Rock(self.player.rect.centerx + (
                                self.player.direction * self.player.rect.width),
                                self.player.rect.centery, self.player.direction)
                            self.thrown_rocks.add(rock)
                        self.shoot = True
                    if event.key == pygame.K_w and not self.jump:
                        self.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False
                if event.key == pygame.K_SPACE:
                    self.shoot = False
                if event.key == pygame.K_w:
                    self.jump = False

            if event.type == pygame.USEREVENT:
                self.counter -= 1
                if self.counter > 0:
                    self.text = str(self.counter).rjust(3)
                # else:

            if event.type == MOUSEBUTTONDOWN:
                self.x, self.y = event.pos
                for unit in self.player_sprites:
                    if unit.rect.collidepoint(self.x, self.y):
                        self.check_control_conditions(unit)

            if event.type == self.ADD_LEMMING:
                if self.num_of_players_spawned == self.max_players:
                    self.all_players_spawned = True
                if self.num_of_players_spawned < self.max_players:
                    identifier = os.urandom(16).hex()
                    new_player = data.lemminki.Lemminki(
                        'player', self.character_scale, (self.starting_position), identifier)
                    self.player_sprites.add(new_player)
                    self.num_of_players_spawned += 1



    def check_control_conditions(self, entity):
        '''Check whether the clicked character may be controlled or not.
        The Player can have only one controllable character at a time.'''
        if len(self.controlled_player_list) > 0:
            if entity.get_id() == self.player.get_id():
                self.player_id = None
                self.player = None
                self.controlled_player_list.clear()
                self.control = False
                entity.give_control()
        else:
            self.player_id = entity.get_id()
            self.player = entity
            self.controlled_player_list.append(entity)
            self.control = True
            entity.take_control()

    def game_loop(self):
        while True:
            if self.throw_cooldown > 0:
                self.throw_cooldown -= 1
            self.clock.tick(60)
            self.draw_screen()
            self.check_events()
            pygame.display.flip()

    def draw_screen(self):
        self.screen.fill(data.settings.SKYBLUE)
        self.map_sprites.draw(self.screen)
        self.thrown_rocks.update()
        self.thrown_rocks.draw(self.screen)
        if self.control:
            for door in self.door_list:
                if self.player.rect.colliderect(door.rect):
                    self.points += 1000
                    self.player.kill()
                    self.check_control_conditions(self.player)
                    if self.all_players_spawned and len(self.player_sprites) == 0:
                        self.clock.tick(0)
                        self.points += (self.counter * 1000)
                        data.points.write_points('testaaja', self.points)
                        self.intro_loop()
                        # TODO Ask for the username and write to file using points.py
                        print('LÄPI')
        for rock in self.thrown_rocks:
            for npc in self.npc_list:
                if rock.rect.colliderect(npc.rect):
                    rock.kill()
                    self.points += 100
                    print(
                        'point for hitting enemy. Enemy goes to sleep for X \
                        amount of time before he wakes back up.')

        for player in self.player_sprites:
            player.update(self.screen, self.tile_rects, self.left,
                          self.right, self.jump, self.shoot)
        for npc in self.npc_list:
            npc.ai_movement(self.screen, self.tile_rects, self.left,
                   self.right, self.jump, self.shoot)

        score = self.game_font.render(
            f'Score: {self.points}', True, data.settings.BLACK)
        time = self.game_font.render(
            f'Time: {self.text}', True, data.settings.BLACK)
        self.screen.blit(score, (60, 50))
        self.screen.blit(time, (790, 50))
