import pygame
from utils import cut_picture

# Player Settings #
PLAYER_VELOCITY = pygame.math.Vector2(0, 0)
PLAYER_POSITION = pygame.math.Vector2(200, 200)
PLAYER_ACCELERATION = pygame.math.Vector2(0, 0)
PLAYER_WALK_ACCELERATION = 0.5
PLAYER_MAX_WALK_SPEED = 0.8

# Physics Settings #
FRICTION = 0.4

# Animation Settings #
ANIMATION_COOLDOWN = 200
SPRITE_SCALE = 1
BLOCKSIZE = 16


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the parent class (Sprite) constructor #
        super().__init__()

        # Load Player Animation #
        self.animations = self.get_animation()
        self.animation_type = "right"
        self.rect = self.animations["left"][0].get_rect()
        self.rect.topleft = PLAYER_POSITION

        # Load Player Settings #
        self.velocity = PLAYER_VELOCITY
        self.position = PLAYER_POSITION
        self.acceleration = PLAYER_ACCELERATION

    def move(self, press_vector, pressed_run, island, dt):
        global ANIMATION_COOLDOWN

        old_position = self.position.copy()
        if (pressed_run and self.velocity.length() > 0):

            PLAYER_MAX_WALK_SPEED = 1.5

            ANIMATION_COOLDOWN = 150
        else:
            PLAYER_MAX_WALK_SPEED = 0.8
            ANIMATION_COOLDOWN = 200

        if press_vector.x != 0 and press_vector.y != 0:
            press_vector = press_vector.normalize()
        # Update acceleration #
        self.acceleration = press_vector * PLAYER_WALK_ACCELERATION

        # Update Velocity #
        self.velocity += self.acceleration * dt

        # friction #
        if press_vector.length() == 0:
            self.velocity = self.velocity*(1-FRICTION)

        # min vel to 0 #
        if self.velocity.x < 0.005 and press_vector.x == 0:
            self.velocity.x = 0
        if self.velocity.y < 0.005 and press_vector.y == 0:
            self.velocity.y = 0

        # limit Velocity #
        if self.velocity.length() > PLAYER_MAX_WALK_SPEED:
            if self.velocity.x == 0:
                self.velocity.y = PLAYER_MAX_WALK_SPEED * \
                    self.velocity.y/abs(self.velocity.y)
            elif self.velocity.y == 0:
                self.velocity.x = PLAYER_MAX_WALK_SPEED * \
                    self.velocity.x/abs(self.velocity.x)
            else:
                self.velocity = (self.velocity.normalize(
                )+press_vector)/2 * PLAYER_MAX_WALK_SPEED

        # Update Position #
        self.position += self.velocity * dt
        self.position = pygame.math.Vector2(
            round(self.position.x), round(self.position.y))
        self.rect.topleft = self.position

        # Check Collision #
        collision_list = self.check_collision(island)

        for block in collision_list:
            if self.velocity.y > 0 and press_vector.y > 0:
                self.rect.y = old_position.y
                self.velocity.y = 0
                self.position.y = self.rect.topleft[1]
            if self.velocity.y < 0 and press_vector.y < 0:
                self.rect.y = old_position.y
                self.velocity.y = 0
                self.position.y = self.rect.topleft[1]

        collision_list = self.check_collision(island)

        for block in collision_list:
            if self.velocity.x > 0 and press_vector.x > 0:
                self.rect.x = old_position.x
                self.velocity.x = 0
                self.position.x = self.rect.topleft[0]
            if self.velocity.x < 0 and press_vector.x < 0:
                self.rect.x = old_position.x
                self.velocity.x = 0
                self.position.x = self.rect.topleft[0]

    def draw(self, screen):
        # Update Animation #
        if self.velocity.x > 0:
            self.animation_type = "right"
        elif self.velocity.x < 0:
            self.animation_type = "left"
        elif self.velocity.y > 0:
            self.animation_type = "down"
        elif self.velocity.y < 0:
            self.animation_type = "up"
        else:
            screen.blit(
                self.animations[self.animation_type][0], self.rect)
            return

        screen.blit(
            self.animations[self.animation_type][
                pygame.time.get_ticks()//ANIMATION_COOLDOWN % 3 + 1], self.rect)

    def get_animation(self):
        pics = cut_picture("Characters/walk.png")
        animations = {"down": [], "up": [], "left": [], "right": []}
        n = 13
        for i, animation_type in enumerate(animations):
            for j in range(4):
                animations[animation_type].append(pygame.transform.scale(
                    pics[n+i*36+j*3], (pics[n+i*36+j*3].get_width()*SPRITE_SCALE, pics[n+i*36+j*3].get_height()*SPRITE_SCALE)))
        return animations

    def check_collision(self, island):
        collision_list = []
        block_y = int(self.position.y/BLOCKSIZE)
        block_x = int(self.position.x/BLOCKSIZE)
        for i in range(block_y-2, block_y+3):
            for j in range(block_x-2, block_x+3):
                if i < 0 or j < 0 or i >= len(island.block_map) or j >= len(island.block_map[0]):
                    continue
                if island.block_map[i][j].id == -1 and self.rect.colliderect(island.block_map[i][j].rect):
                    collision_list.append(island.block_map[i][j].rect)
        return collision_list
