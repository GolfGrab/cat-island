import pygame
from utils import cut_picture, cut_picture_3x

# Player Settings #
PLAYER_VELOCITY = pygame.math.Vector2(0, 0)
PLAYER_POSITION = pygame.math.Vector2(400, 450)
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
        self.rect = pygame.Rect(
            PLAYER_POSITION.x, PLAYER_POSITION.y, BLOCKSIZE, BLOCKSIZE)
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
        self.inventory = Inventory()
        self.activity = "idle"

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

        # # Check Collision #

        collisions = self.check_collision_point(island)

        if collisions["right"]:
            dx = 0
        if collisions["left"]:
            dx = 0
        if collisions["up"]:
            dy = 0
        if collisions["down"]:
            dy = 0

        self.delta_position = pygame.math.Vector2(dx, dy)
        if dx != 0 and dy != 0:
            dx = dx / 1.414
            dy = dy / 1.414
        self.update_position(dx, dy)

        self.velocity = pygame.math.Vector2(dx, dy)

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

        if (self.activity == "idle"):
            if self.delta_position == pygame.math.Vector2(0, 0):
                screen.blit(
                    self.animations[self.activity][self.animation_type][0], (self.rect.x-BLOCKSIZE, self.rect.y-BLOCKSIZE))
            else:
                screen.blit(
                    self.animations[self.activity][self.animation_type][
                        pygame.time.get_ticks()//self.animation_cooldown % 3 + 1], (self.rect.x-BLOCKSIZE, self.rect.y-BLOCKSIZE))
        else:
            screen.blit(
                self.animations[self.activity][self.animation_type][
                    pygame.time.get_ticks()//self.animation_cooldown % 2], (self.rect.x-BLOCKSIZE, self.rect.y-BLOCKSIZE))

        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
        # for i in range(4):
        #     pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 0)
        # for i in range(4):
        #     pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 1)

    def get_animation(self):
        walk = cut_picture_3x("Characters/walk.png")
        activity = cut_picture_3x("Characters/activity.png")
        animations = {"idle": {"down": [], "up": [], "left": [], "right": []},
                      "cut_tree": {"down": [], "up": [], "left": [], "right": []},
                      "dig": {"down": [], "up": [], "left": [], "right": []},
                      "watering": {"down": [], "up": [], "left": [], "right": []}}
        for i, animation_type in enumerate(animations["idle"]):
            for j in range(4):
                animations["idle"][animation_type].append(pygame.transform.scale(
                    walk[i*4+j], (walk[i*4+j].get_width()*SPRITE_SCALE, walk[i*4+j].get_height()*SPRITE_SCALE)))
        for n, activity_type in enumerate(["dig", "cut_tree", "watering"]):
            for i, animation_type in enumerate(animations[activity_type]):
                for j in range(2):
                    animations[activity_type][animation_type].append(pygame.transform.scale(
                        activity[n*8+i*2+j], (activity[n*8+i*2+j].get_width()*SPRITE_SCALE, activity[n*8+i*2+j].get_height()*SPRITE_SCALE)))

        return animations

    def check_collision_point(self, island):
        collisions = {"left": False, "right": False,
                      "up": False, "down": False}
        block_y = int(self.position.y/BLOCKSIZE)
        block_x = int(self.position.x/BLOCKSIZE)
        for i in range(block_y-2, block_y+3):
            for j in range(block_x-2, block_x+3):
                if i < 0 or j < 0 or i >= len(island.block_map) or j >= len(island.block_map[0]):
                    continue
                # test left
                if island.block_map[i][j].id == -1 and island.block_map[i][j].rect.collidepoint(self.hitbox.midleft):
                    collisions["left"] = True
                if island.block_map[i][j].id == -1 and island.block_map[i][j].rect.collidepoint(self.hitbox.midright):
                    collisions["right"] = True
                if island.block_map[i][j].id == -1 and island.block_map[i][j].rect.collidepoint(self.hitbox.midtop):
                    collisions["up"] = True
                if island.block_map[i][j].id == -1 and island.block_map[i][j].rect.collidepoint(self.hitbox.midbottom):
                    collisions["down"] = True
        return collisions


class Inventory():
    def __init__(self) -> None:
        self.items = dict()

    def add_item(self, item, amount):
        if item in self.items:
            self.items[item] += amount
        else:
            self.items[item] = amount
        print("Added " + str(amount) + " " + item)

    def remove_item(self, item_name, amount):
        if item_name in self.items and self.items[item_name] - amount < 0:
            self.items[item_name] -= amount
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        return False
