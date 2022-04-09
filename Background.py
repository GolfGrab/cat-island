
import pygame
from utils import cut_picture

BLOCKSIZE = 16
TEXTURE_PATH = "Water.png"
ANIMATION_COOLDOWN = 1000


class Background():
    def __init__(self, map_path) -> None:
        super().__init__()
        self.textures = cut_picture(TEXTURE_PATH)
        self.block_map = []
        with open(map_path) as f:
            text = f.read()
            data = [t.split(",")for t in text.split("\n")]
        for y_idx, row in enumerate(data):
            self.block_map.append([])
            for x_idx, data in enumerate(row):
                self.block_map[-1].append(
                    Block(int(data), pygame.math.Vector2(x_idx*BLOCKSIZE, y_idx*BLOCKSIZE)))

        self.width = len(self.block_map[0])*BLOCKSIZE
        self.height = len(self.block_map)*BLOCKSIZE
        self.canvas = pygame.Surface((self.width, self.height))

        self.animations = self.getframes()

    def getframes(self):
        animations = []
        for n_frame in range(len(self.textures)):
            frame = self.canvas.copy()
            for row in self.block_map:
                for block in row:
                    if block.id != -1:
                        frame.blit(self.textures[(pygame.time.get_ticks(
                        )//ANIMATION_COOLDOWN) % len(self.textures)], block.position)
            animations.append(frame)
        return animations

    def draw(self, screen) -> None:
        screen.blit(
            self.animations[(pygame.time.get_ticks()//ANIMATION_COOLDOWN) % 4], (0, 0))


class Block(pygame.sprite.Sprite):
    def __init__(self, id, position) -> None:
        super().__init__()
        self.id = id
        self.position = position
