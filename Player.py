import pygame
from utils import cut_picture

# Player Settings #
PLAYER_VELOCITY = pygame.math.Vector2(0, 0)
PLAYER_POSITION = pygame.math.Vector2(200, 200)
PLAYER_WALK_SPEED = 1
PLAYER_RUN_SPEED = 1.5


# Animation Settings #
WALK_ANIMATION_COOLDOWN = 200
RUN_ANIMATION_COOLDOWN = 150
SPRITE_SCALE = 1
BLOCKSIZE = 16


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the parent class (Sprite) constructor #
        super().__init__()

        # Load Player Animation #
        self.animations = self.get_animation()
        self.animation_type = "right"
        self.rect = self.animations["right"][0].get_rect()
        self.old_rect = self.rect
        # Load Player Settings #
        self.rect.midbottom = PLAYER_POSITION
        self.hitbox = self.rect.inflate(-10, -10)
        self.hitbox.midbottom = self.rect.midbottom
        self.old_hitbox = self.hitbox
        self.position = PLAYER_POSITION
        self.velocity = PLAYER_VELOCITY
        self.delta_position = pygame.math.Vector2(0, 0)
        self.animation_cooldown = WALK_ANIMATION_COOLDOWN

    def move(self, press_vector, pressed_run, island, dt):
        self.old_hitbox = self.hitbox.copy()
        self.old_rect = self.rect.copy()

        global ANIMATION_COOLDOWN
        if (pressed_run):
            self.velocity = press_vector * PLAYER_RUN_SPEED
        else:
            self.velocity = press_vector * PLAYER_WALK_SPEED

        dx = self.velocity.x * dt
        dy = self.velocity.y * dt
        self.update_position(dx, dy)

        # Check Collision #

        collisions = self.check_collision(island)

        for block in collisions:
            if self.velocity.x > 0 and self.hitbox.right+2 > block.left and self.old_hitbox.right <= block.left:
                self.hitbox.right = block.left
                self.position.x = self.hitbox.midbottom[0]
                self.rect.midbottom = self.hitbox.midbottom
                dx = 0
            elif self.velocity.x < 0 and self.hitbox.left-2 < block.right and self.old_hitbox.left >= block.right:
                self.hitbox.left = block.right
                self.position.x = self.hitbox.midbottom[0]
                self.rect.midbottom = self.hitbox.midbottom
                dx = 0
            elif self.velocity.y > 0 and self.hitbox.bottom+2 > block.top and self.old_hitbox.bottom <= block.top:
                self.hitbox.bottom = block.top
                self.position.y = self.hitbox.midbottom[1]
                self.rect.midbottom = self.hitbox.midbottom
                dy = 0
            elif self.velocity.y < 0 and self.hitbox.top-2 < block.bottom and self.old_hitbox.top >= block.bottom:
                self.hitbox.top = block.bottom
                self.position.y = self.hitbox.midbottom[1]
                self.rect.midbottom = self.hitbox.midbottom
                dy = 0

        self.delta_position = pygame.math.Vector2(dx, dy)
        if dx != 0 and dy != 0:
            d = pygame.math.Vector2(dx, dy).normalize() * \
                self.velocity.length()
            self.update_position(d.x, d.y)

        if (dx != 0 or dy != 0) and pressed_run:
            self.animation_cooldown = RUN_ANIMATION_COOLDOWN
        else:
            self.animation_cooldown = WALK_ANIMATION_COOLDOWN

    def update_position(self, dx, dy):
        self.position = pygame.math.Vector2(
            self.old_rect.midbottom[0], self.old_rect.midbottom[1]) + pygame.math.Vector2(dx, dy)
        self.rect.midbottom = (round(self.position.x), round(self.position.y))
        self.hitbox.midbottom = self.rect.midbottom

    def draw(self, screen):

        # Update Animation #
        if self.delta_position.x > 0:
            self.animation_type = "right"
        elif self.delta_position.x < 0:
            self.animation_type = "left"
        elif self.delta_position.y > 0:
            self.animation_type = "down"
        elif self.delta_position.y < 0:
            self.animation_type = "up"
        else:
            screen.blit(
                self.animations[self.animation_type][0], self.rect)

            # pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
            # for i in range(4):
            #     pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
            # pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 0)
            # for i in range(4):
            #     pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 1)
            return

        screen.blit(
            self.animations[self.animation_type][
                pygame.time.get_ticks()//self.animation_cooldown % 3 + 1], self.rect)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
        # for i in range(4):
        #     pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 0)
        # for i in range(4):
        #     pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 1)

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
                if island.block_map[i][j].id == -1 and self.hitbox.colliderect(island.block_map[i][j].rect):
                    collision_list.append(island.block_map[i][j].rect)
        return collision_list
