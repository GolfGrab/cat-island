import pygame
from Player import Player
from Map import Map
from Background import Background
import time
from Tree import Tree_Group, Tree
from Townhall import Townhall


# Game Settings #
SCREEN_WIDTH = 1024*2
SCREEN_HEIGHT = int(1024 * 9 / 16)*2
BG_COLOR = ("#9bd4c3")
TARGET_FPS = 60
BLOCKSIZE = 16
ZOOM = 2

# Load basic window and clock #
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyCraft")
clock = pygame.time.Clock()

# Load Player #
p1 = Player()

# Load Townhall #
townhall = Townhall()


# Load Map #
water = Background("testmap_water.csv")
island = Map("testmap5_island.csv")

background = pygame.Surface((water.width, water.height))

water.draw(background)
island.draw(background)

# Load tree group #
tree_group = Tree_Group(island)

now_time = time.time()

# Game loop #
game_run = True
while game_run:
    # tick #
    clock.tick(TARGET_FPS)
    dt = (time.time() - now_time) * 100
    now_time = time.time()

    # Event handling #
    press_vector = pygame.math.Vector2(0, 0)
    pressed_run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_run = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        press_vector.x -= 1
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        press_vector.x += 1
    if pressed[pygame.K_w] or pressed[pygame.K_UP]:
        press_vector.y -= 1
    if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
        press_vector.y += 1
    if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
        pressed_run = True

    # Move player #
    p1.move(press_vector, pressed_run, island, dt)

    # Random generation #
    tree_group.random_gen_tree()

    # cut tree #
    for tree in tree_group.tree_list:
        tree.checkcut(p1, tree_group, dt)

    # update player activity #
    p1.update_activity()

    # Draw background #s
    canvas = background.copy()
    island.draw(canvas)

    # Draw y sort #
    y_sort = []
    y_sort.append(p1)
    y_sort.append(townhall)
    y_sort.extend(tree_group.tree_list)
    y_sort.sort(key=lambda x: x.position.y)

    for obj in y_sort:
        obj.draw(canvas)

    # Zoom #
    canvas = pygame.transform.scale(
        canvas, (water.width*ZOOM, water.height*ZOOM))
    # Draw to screen #
    screen.blit(canvas, (-p1.position*ZOOM +
                (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

# Show position #
    screen.blit(pygame.font.Font(None, 32).render(
        f'POS(X,Y) = {p1.position.x:.2f} , {p1.position.y:.2f}', True, (255, 255, 255)), (20, 20))
    # Show velocity #
    screen.blit(pygame.font.Font(None, 32).render(
        f'VEL(X,Y) = {p1.velocity.x:.2f} , {p1.velocity.y:.2f}', True, (255, 255, 255)), (20, 60))
    # Show FPS #
    screen.blit(pygame.font.Font(None, 32).render(
        f'FPS = {clock.get_fps():.2f}', True, (255, 255, 255)), (20, 100))

    # Show Items #
    screen.blit(pygame.font.Font(None, 32).render(
        f'{list(p1.inventory.items.items())}', True, (255, 255, 255)), (20, 1000))
    # Update screen #
    pygame.display.update()

    # Clear screen #
    screen.fill(BG_COLOR)
pygame.quit()
