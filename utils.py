import pygame


def cut_picture(path):
    surface = pygame.image.load(path)
    # surface = surface.convert_alpha()
    tile_num_x = surface.get_size()[0] // 16
    tile_num_y = surface.get_size()[1] // 16
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 16
            y = row * 16
            new_surface = pygame.Surface((16, 16))
            new_surface.set_colorkey((0, 0, 0))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, 16, 16))
            cut_tiles.append(new_surface)

    return cut_tiles
