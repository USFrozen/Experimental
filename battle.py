from settings import *

class Battle:
    def __init__(self, player_equipment, enemy, monster_frames, bg_surf, fonts):
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.monster_frames = monster_frames
        self.fonts = fonts
        self.monster_data = {'opponent': enemy}
        self.player_data = {'player': player_equipment}