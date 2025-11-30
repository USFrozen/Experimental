from settings import *

# Gets called in main
# Cleans up draw function in main by grouping all draw calls for sprites together
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = vector()

    def draw_stuff(self, player_topleft):
        self.offset.x = -(player_topleft[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_topleft[1] - WINDOW_HEIGHT / 2)

        bg_sprites = [sprite for sprite in self if sprite.draw_layer < WORLD_DRAW_ORDER['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.draw_layer == WORLD_DRAW_ORDER['main']], key = lambda sprite: sprite.y_sort)
        fg_sprites = [sprite for sprite in self if sprite.draw_layer > WORLD_DRAW_ORDER['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)