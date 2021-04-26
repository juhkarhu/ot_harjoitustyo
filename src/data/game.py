import sys
import os
import pygame
import pygame.locals
from pygame.constants import MOUSEBUTTONDOWN

from data.assets import lemminki, world

import data.settings
import data.points
from data.map import Map


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        # Font for rendering text
        self.game_font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.Font(None, 65)
        self.intro_text_font = pygame.font.Font(None, 45)
        self.map = Map()

        # Starts the intro loop
        self.clock = pygame.time.Clock()
        self.intro = True
        self.intro_loop()

        # Pylint error handling
        self.player = None
        self.player_id = None
        self.throw_cooldown = None
        self.control = None
        self.left = None
        self.right = None
        self.jump = None
        self.shoot = None
        self.interval = None
        self.add_lemming = None
        self.grass_image = None
        self.dirt_image = None
        self.max_players = None
        self.points = None
        self.counter = None
        self.text = None
        self.thrown_rocks = None
        self.player_sprites = None
        self.tile_rects = None
        self.door_list = None
        self.map_sprites = None
        self.npc_list = None
        self.window_size = None
        self.height = None
        self.width = None
        self.screen = None
        self.x = None
        self.y = None
        self.all_players_spawned = None
        self.num_of_players_spawned = None
        self.controlled_player_list = None

    def set_player_variables(self):
        self.player = None
        self.player_id = 0

        self.throw_cooldown = 0
        self.control = False
        self.left = False
        self.right = False
        self.jump = False
        self.shoot = False
        self.interval = 1600
        self.add_lemming = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_lemming, self.interval)


    def load_tile_images(self):
        self.grass_image = self.map.load_grass_image()
        self.dirt_image = self.map.load_dirt_image()

    def set_game_variables(self):
        self.max_players = 3
        self.points = 0
        # Countdown timer for level
        self.counter, self.text = 80, '80'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        # Variables for sprite lists and seeing if all players have spawned
        self.all_players_spawned = False
        self.thrown_rocks = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.num_of_players_spawned = 0
        self.controlled_player_list = []

        # Related to map, so they are handled in map.py
        self.npc_list = self.map.get_npc_list()
        self.map_sprites = self.map.get_map_sprites()
        self.door_list = self.map.get_door_list()
        self.tile_rects = self.map.read_map_data()


    def set_gamedisplay_settings(self):
        '''
        Sets the display settings for game.
        '''
        self.height = len(self.map.get_game_map())
        self.width = len(self.map.get_game_map())
        print(self.height, self.width)
        data.settings.SCREEN_HEIGHT = data.settings.SCALA * self.height
        data.settings.SCREEN_WIDTH = data.settings.SCALA * self.width
        self.window_size = (data.settings.SCREEN_HEIGHT,
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
        self.window_size = (data.settings.SCREEN_HEIGHT,
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
                    sys.exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        sys.exit()
                    if tapahtuma.key == pygame.K_RETURN:
                        self.set_game_variables()
                        self.set_player_variables()
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
                    self.intro_loop()
                if self.control:
                    if event.key == pygame.K_a:
                        self.left = True
                    if event.key == pygame.K_d:
                        self.right = True
                    if event.key == pygame.K_SPACE:
                        if self.throw_cooldown == 0:
                            self.throw_cooldown = 25
                            rock = world.Rock(self.player.rect.centerx + (
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
                #TODO What happens if the time runs out before the player is done?

            if event.type == MOUSEBUTTONDOWN:
                self.x, self.y = event.pos
                for unit in self.player_sprites:
                    if unit.rect.collidepoint(self.x, self.y):
                        self.check_control_conditions(unit)

            if event.type == self.add_lemming:
                if self.num_of_players_spawned == self.max_players:
                    self.all_players_spawned = True
                if self.num_of_players_spawned < self.max_players:
                    identifier = os.urandom(16).hex()
                    new_player = lemminki.Lemminki(
                        'player', data.settings.CHARACTER_SCALE , (self.map.get_starting_position()), identifier)
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
                    self.points += 100
                    self.player.kill()
                    self.check_control_conditions(self.player)
                    if self.all_players_spawned and len(self.player_sprites) == 0:
                        # TODO Ask for the username
                        self.clock.tick(0)
                        self.points += (self.counter * 100)
                        data.points.write_points('testaaja', self.points)
                        print('LÄPI')
                        self.intro_loop()

        for rock in self.thrown_rocks:
            for npc in self.npc_list:
                if rock.rect.colliderect(npc.rect):
                    rock.kill()
                    npc.get_hit_enemy()
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

    