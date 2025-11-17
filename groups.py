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

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)