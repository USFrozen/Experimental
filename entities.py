from settings import *

# Player class, handles inputs, collisions, and movement
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)
        self.direction = vector()
        self.target_pos = vector(self.rect.topleft)
        self.speed = 125
        self.collision_sprites = collision_sprites

    def input(self, collision_sprites):
        buttons = pygame.key.get_pressed()
        input_vector = vector()
        if buttons[pygame.K_LEFT]:
            input_vector.x -= 1
        elif buttons[pygame.K_RIGHT]:
            input_vector.x += 1
        elif buttons[pygame.K_UP]:
            input_vector.y -= 1
        elif buttons[pygame.K_DOWN]:
            input_vector.y += 1
        elif buttons[pygame.K_z]:
            pass
        elif buttons[pygame.K_x]:
            pass

        # Used to get rid of floaty movement and restricts player object to grid
        # Only set new target if we're already at the current target
        if vector(self.rect.topleft) == self.target_pos and input_vector.length_squared() > 0:
            # Set up new rect for checking collisions
            new_rect = self.rect.copy()
            new_rect.x += input_vector.x * TILE_SIZE
            new_rect.y += input_vector.y * TILE_SIZE

            if not any(new_rect.colliderect(sprite.rect) for sprite in collision_sprites):
                self.target_pos = vector(new_rect.topleft)

        self.direction = input_vector

    def move(self, dt):
        current = vector(self.rect.topleft)
        if current != self.target_pos:
            direction = (self.target_pos - current).normalize()
            step = direction * self.speed * dt
            if step.length() >= (self.target_pos - current).length():
                self.rect.topleft = self.target_pos
            else:
                self.rect.topleft = current + step

    def update(self, dt):
        self.input(self.collision_sprites)
        self.move(dt)

# From .mtx Monsters layer, environment objects where monsters can appear
class Monster_env(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obj, tmx_data):
        super().__init__(groups)

        if obj.gid:
            self.image = tmx_data.get_tile_image_by_gid(obj.gid)
        else:
            self.image = pygame.Surface((16, 16))
            self.image.fill('magenta')

        self.rect = self.image.get_frect(topleft=pos)

# From .mtx Entities layer, used for objects that can be interacted with
class MapEntity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obj, tmx_data):
        super().__init__(groups)

        if obj.gid:
            self.image = tmx_data.get_tile_image_by_gid(obj.gid)
        else:
            self.image = pygame.Surface((16, 16))
            self.image.fill('magenta')

        self.rect = self.image.get_frect(topleft=pos)