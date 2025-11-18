from settings import *

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


# takes sprite png and splits it into frames for animations
def load_sprite_sheet(sheet_path, frame_width, frame_height, rows, cols):
    pass