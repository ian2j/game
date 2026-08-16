import pygame


class Player:

    def __init__(self):
        self.name = "Player"
        self.position = None
        self.sprite_sheet = None
        self.frame_width = None
        self.frame_height = None
        self.scale = 6

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def set_sprite_sheet(self, sprite_sheet):
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

    def set_frame_width(self, frame_width):
        self.frame_width = frame_width

    def set_frame_height(self, frame_height):
        self.frame_height = frame_height

    def set_scale(self, scale):
        self.scale = scale
