from settings import *
from sprites import Sprite, TransitionSprite, CollisionSprite
from entities import *
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()

        # Game tick, used for FPS and delta time (dt)
        self.clock = pygame.time.Clock()

        # Initial screen surface, W and H set in settings.py
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Sets pygame window title
        pygame.display.set_caption("NET-202 Final Project Demo")

        # Object groups, used in drawing objects to screen
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        self.import_assets()
        self.setup(
            self.tmx_maps['world'], 'player_house'
            #self.tmx_maps['player_house'], 'world'
            )


    # Uses load_pygame from pytmx.util_pygame to load the Tiled .mtx maps in ./assets/TMX
    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame(world),
            'player_house': load_pygame(player_house)
            }

    # Generates object class instances based on data in Tiled maps
    # Each map layer is being looked at individually by name so names need to be consistent between maps
    def setup(self, tmx_map, player_start_pos):
        for layer in ['BG', 'BG2', 'BG3']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Monsters'):
            self.monster_env = Monster_env((obj.x, obj.y), self.all_sprites, obj, tmx_map)

        for obj in tmx_map.get_layer_by_name('Collisions'):
            self.collision = CollisionSprite((obj.x, obj.y), (obj.width, obj.height), self.collision_sprites)

        for obj in tmx_map.get_layer_by_name('Transitions'):
            if obj.name == 'transition':
                self.transition = TransitionSprite((obj.x, obj.y), (obj.width, obj.height), obj.properties['target_map'], obj.properties['current_map'], self.transition_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name != 'player':
                self.entities = Entity((obj.x, obj.y), self.all_sprites, obj, tmx_map)

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player' and obj.pos == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.rect)]
        if sprites:
            for sprite in sprites:
                return sprite.target_map, sprite.current_map
                #print(f"Transition Check Successful, target: {sprite.target_map}, current: {sprite.current_map}")

    # Main logic loop function
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw game
            self.all_sprites.update(dt)
            self.transition_check()
            self.screen.fill(BACKGROUND_COLOR)
            self.all_sprites.draw_stuff(self.player.rect.topleft)
            pygame.display.update()

            # Debug: prints delta time to console so we can see if I did something dumb that is slowing down the game
            #print(dt)



if __name__ == "__main__":
    game = Game()
    game.run()