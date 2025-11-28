from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, group, facing_direction):
        super().__init__(group)

        # Graphics
        self.draw_layer = WORLD_DRAW_ORDER['main']
        self.frame_index = 0
        self.frames = frames
        self.facing_direction = facing_direction

        # Movement
        self.direction = vector()
        self.speed = 100

        # Sprite
        self.hitbox = pygame.FRect(pos, (16, 16))
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(midbottom = self.hitbox.midbottom)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'

        return f"{self.facing_direction}{'' if moving else '_idle'}"



# Player class, handles inputs, collisions, and movement
class Player(Entity):
    def __init__(self, pos, frames, group, collision_sprites, facing_direction):
        super().__init__(pos, frames, group, facing_direction)
        self.target_pos = vector(self.hitbox.topleft)
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
        if vector(self.hitbox.topleft) == self.target_pos and input_vector.length_squared() > 0:
            # Set up new rect for checking collisions
            new_rect = self.hitbox.copy()
            new_rect.x += input_vector.x * TILE_SIZE
            new_rect.y += input_vector.y * TILE_SIZE

            if not any(new_rect.colliderect(sprite.rect) for sprite in collision_sprites):
                self.target_pos = vector(new_rect.topleft)

        self.direction = input_vector

    def move(self, dt):
        current = vector(self.hitbox.topleft)
        if current != self.target_pos:
            direction = (self.target_pos - current).normalize()
            step = direction * self.speed * dt
            if step.length() >= (self.target_pos - current).length():
                self.hitbox.topleft = self.target_pos
            else:
                self.hitbox.topleft = current + step

            self.rect.midbottom = self.hitbox.midbottom

    def update(self, dt):
        self.input(self.collision_sprites)
        self.move(dt)
        self.animate(dt)

# NPC class
class NPCs(Entity):
    def __init__(self, pos, frames, group, collision_sprites, facing_direction):
        super().__init__(pos, frames, group, facing_direction)