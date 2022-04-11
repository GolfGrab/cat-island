import pygame

from random import random

HP = 100
BLOCKSIZE = 16


class Townhall(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the parent class (Sprite) constructor #
        super().__init__()
        self.position = pygame.math.Vector2(400, 400)
        self.sprites = self.get_sprites()
        self.animation_cooldown = 100
        self.hp = HP
        self.rect = pygame.Rect(
            self.position.x, self.position.y, 2*BLOCKSIZE, 2*BLOCKSIZE)
        self.rect.center = self.position
        self.sprite_rect = self.sprites[0].get_rect()
        self.sprite_rect.midbottom = self.rect.midbottom

    def draw(self, screen) -> None:
        screen.blit(self.sprites[pygame.time.get_ticks(
        )//self.animation_cooldown % 11], self.sprite_rect)

    def get_sprites(self):
        picture_list = []
        for i in range(11):
            img = pygame.image.load(f"./Townhall/tile{i:03d}.png")
            picture_list.append(img)
        return picture_list
