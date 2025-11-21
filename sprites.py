from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, group):
        self.frame_index, self.frames = 0, frames
        super().__init__(pos, frames[self.frame_index], group)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)


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