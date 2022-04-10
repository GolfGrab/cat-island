import pygame
from utils import cut_picture

BLOCKSIZE = 16
TEXTURE_PATH = "texture.png"


class Map():
    def __init__(self, map_path,) -> None:
        super().__init__()
        self.textures = cut_picture(TEXTURE_PATH)
        self.block_map = []
        with open(map_path) as f:
            text = f.read().strip()
            data = [t.split(",")for t in text.split("\n")]
        for y_idx, row in enumerate(data):
            self.block_map.append([])
            for x_idx, data in enumerate(row):
                self.block_map[-1].append(
                    Block(int(data), pygame.math.Vector2(x_idx*BLOCKSIZE, y_idx*BLOCKSIZE)))

        self.width = len(self.block_map[0])*BLOCKSIZE
        self.height = len(self.block_map)*BLOCKSIZE

    def draw(self, screen) -> None:
        for i, row in enumerate(self.block_map):
            for j, block in enumerate(row):
                if block.id != -1:
                    screen.blit(self.textures[block.id], block.position)
                    if i != len(self.block_map)-1 and self.block_map[i+1][j].id == -1:
                        screen.blit(
                            self.textures[6+block.id], block.position+pygame.math.Vector2(0, BLOCKSIZE))


class Block(pygame.sprite.Sprite):
    def __init__(self, id, position) -> None:
        super().__init__()
        self.id = id
        self.position = position
        self.rect = pygame.Rect(self.position, (BLOCKSIZE, BLOCKSIZE))
