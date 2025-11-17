from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class TransitionSprite(Sprite):
    def __init__(self, pos, size, target_map, current_map, group):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, group)
        self.target_map = target_map
        self.current_map = current_map

class CollisionSprite(Sprite):
    def __init__(self, pos, size, group):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, group)