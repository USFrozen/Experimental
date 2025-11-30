from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, layer = WORLD_DRAW_ORDER['main']):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.draw_layer = layer
        self.y_sort = self.rect.centery

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, group, layer = WORLD_DRAW_ORDER['main']):
        self.frame_index, self.frames = 0, frames
        super().__init__(pos, frames[self.frame_index], group, layer)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)

class TransitionSprite(Sprite):
    def __init__(self, pos, size, target_map, current_map, group, layer = WORLD_DRAW_ORDER['main']):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, group, layer)
        self.target_map = target_map
        self.current_map = current_map

class CollisionSprite(Sprite):
    def __init__(self, pos, size, group, layer = WORLD_DRAW_ORDER['main']):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, group, layer)

# From .mtx Monsters layer, environment objects where monsters can appear
class MonsterEnv(Sprite):
    def __init__(self, pos, group, obj, tmx_data, layer = WORLD_DRAW_ORDER['main']):
        surf = pygame.Surface((16, 16))
        super().__init__(pos, surf, group, layer)

        if obj.gid:
            self.image = tmx_data.get_tile_image_by_gid(obj.gid)
        else:
            self.image = pygame.Surface((16, 16))
            self.image.fill('magenta')

        self.rect = self.image.get_frect(topleft=pos)
        self.draw_layer = layer
        self.y_sort -= 2

# From .mtx Entities layer, used for objects that can be interacted with
class MapObject(Sprite):
    def __init__(self, pos, group, obj, tmx_data, layer = WORLD_DRAW_ORDER['main']):
        surf = pygame.Surface((16, 16))
        super().__init__(pos, surf, group, layer)

        if obj.gid:
            self.image = tmx_data.get_tile_image_by_gid(obj.gid)
        else:
            self.image = pygame.Surface((16, 16))
            self.image.fill('magenta')

        self.rect = self.image.get_frect(topleft=pos)
        self.draw_layer = layer