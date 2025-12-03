from settings import *
from pygame.time import get_ticks

# Import Functions
# Used for importing single image files
def import_image(*path, alpha=True, ext="png"):
    full_path = os.path.join(*path) + f'.{ext}'
    image = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return image

# Imports all images in a specified directory without preserving name data
# Thanks to Copilot, it also makes it so files with names that aren't numbers won't crash the game
def import_dirs(*path):
    frames = []
    for directory, subdirectory, image_names in os.walk(*path):
        def num_key(name):
            try:
                return int(name)
            except:
                return float("inf")

        for image_name in sorted(image_names, key=num_key):
            full_path = os.path.join(directory, image_name)
            image = pygame.image.load(full_path).convert_alpha()
            frames.append(image)
    return frames

# Imports all images but preserves names
def import_dir_dict(*path):
    frames = {}
    for directory, subdirectory, image_names in os.walk(os.path.join(*path)):
        for image_name in image_names:
            full_path = os.path.join(directory, image_name)
            image = pygame.image.load(full_path).convert_alpha()
            frames[image_name.split('.')[0]] = image
    return frames

# Looks for images in multiple subdirs and imports them all
def import_subdirs(*path):
    frames = {}
    for _, subdirs, __ in os.walk(os.path.join(*path)):
        if subdirs:
            for subdir in subdirs:
                frames[subdir] = import_dirs(*path, subdir)
    return frames

# imports and slices tilemaps
def import_tilemaps(cols, rows, *path):
    frames = {}
    surface = import_image(*path)
    tile_width = surface.get_width() / cols
    tile_height = surface.get_height() / rows
    for col in range(cols):
        for row in range(rows):
            cut_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            cut_surf = pygame.Surface((tile_width, tile_height))
            cut_surf.fill("magenta")
            cut_surf.set_colorkey("magenta")
            cut_surf.blit(surface, (0,0), cut_rect)
            frames[(col, row)] = cut_surf
    return frames

def import_character(cols, rows, *path):
    frame_dict = import_tilemaps(cols, rows, *path)
    new_dict = {}
    for row, direction in enumerate(('down', 'left', 'right', 'up')):
        new_dict[direction] = [frame_dict[(col, row)] for col in range(cols)]
        new_dict[f'{direction}_idle'] = [frame_dict[(1, row)]]
    return new_dict

def import_characters(*path):
    new_dict = {}
    for _, __, image_names in os.walk(os.path.join(*path)):
        for image_name in image_names:
            image_name = image_name.split('.')[0]
            new_dict[image_name] = import_character(4,4,*path,image_name)
    return new_dict

def import_tmx(*path):
    tmx_dict = {}
    for directory, subdirectory, files in os.walk(os.path.join(*path)):
        for file in files:
            tmx_dict[file.split('.')[0]] = load_pygame(os.path.join(directory, file))
    return tmx_dict

# Game Functions
# Transition screen effect used before and after all sprites unload and load from new map
def screen_fade(self, fade_in=True, speed=15):
    fade_surface = pygame.Surface(self.screen.get_size())
    fade_surface.fill(BACKGROUND_COLOR)
    if fade_in:
        for alpha in range(255, -1, -speed):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    else:
        for alpha in range(0, 256, speed):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

def check_connections(distance, entity, target, tollerance = 16):
    relationship = vector(target.rect.center) - vector(entity.rect.center)
    if relationship.length() < distance:
        if (
            entity.facing_direction == 'left' and relationship.x < 0 and abs(relationship.y) < tollerance or
            entity.facing_direction == 'right' and relationship.x > 0 and abs(relationship.y) < tollerance or
            entity.facing_direction == 'up' and relationship.y < 0 and abs(relationship.x) < tollerance or
            entity.facing_direction == 'down' and relationship.y > 0 and abs(relationship.x) < tollerance
        ):
            return True

# Timer for use in battle system
class Timer:
    def __init__(self, duration, repeat = False, autostart = False, func = None):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.func = func
        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                if self.func: self.func()
                self.deactivate()