import pygame
from utils import cut_picture
import random

HP = 100
BLOCKSIZE = 16
TREE_RATE = 2
TREE_LIMIT = 20


class Tree_Group():
    def __init__(self, island) -> None:

        # Load Tree sprites #
        self.sprites = self.get_sprites()
        self.tree_list = []
        self.tree_activity = []

        # Load grass block list #
        self.grass_block_list = []
        for row in island.block_map:
            for block in row:
                if block.id == 0:
                    self.grass_block_list.append(block)
        self.n_grass = len(self.grass_block_list)

    def get_sprites(self):
        x = cut_picture("./Objects/Basic Grass Biom things 1.png")

        return [x[1], x[2], x[10], x[11]]

    def random_gen_tree(self):

        if pygame.time.get_ticks()//100 % 200 == 0 and len(self.tree_list) < TREE_LIMIT:
            self.tree_list.append(
                Tree(self.sprites, *self.grass_block_list[random.randint(0, self.n_grass-1)].rect.center))

    def kill_tree(self, tree):
        self.tree_list.remove(tree)


class Tree(pygame.sprite.Sprite):
    def __init__(self, sprites, x, y) -> None:
        # Call the parent class (Sprite) constructor #
        super().__init__()
        self.sprites = sprites
        self.position = pygame.math.Vector2(x, y)
        self.hp = HP

    def checkcut(self, player, tree_group, dt):
        if player.rect.collidepoint((self.position.x, self.position.y-8)):
            player.activity_list.append("cut_tree")
            self.hp -= dt

            if self.hp <= 0:
                player.inventory.add_item("normal_wood", random.randint(8, 12))
                player.activity_list.append("cut_done")
                tree_group.kill_tree(self)

    def draw(self, screen) -> None:
        screen.blit(self.sprites[0], self.position -
                    pygame.math.Vector2(BLOCKSIZE, 2*BLOCKSIZE))
        screen.blit(self.sprites[1], self.position -
                    pygame.math.Vector2(0, 2*BLOCKSIZE))
        screen.blit(self.sprites[2], self.position -
                    pygame.math.Vector2(BLOCKSIZE, BLOCKSIZE))
        screen.blit(self.sprites[3], self.position -
                    pygame.math.Vector2(0, BLOCKSIZE))
