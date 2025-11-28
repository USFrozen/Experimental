from settings import *
from sprites import Sprite, TransitionSprite, CollisionSprite, AnimatedSprite, MonsterEnv, MapObject
from entities import *
from groups import AllSprites
from helpers import *

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
            #self.tmx_maps['world'], 'player_house'
            self.tmx_maps['player_house'], 'spawn'
            )


    # Uses load_pygame from pytmx.util_pygame to load the Tiled .mtx maps in ./assets/TMX
    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame(world),
            'player_house': load_pygame(player_house)
            }

        self.world_animations = {
            'characters': import_characters(characters),
        }

    # Generates object class instances based on data in Tiled maps
    # Each map layer is being looked at individually by name so names need to be consistent between maps
    def setup(self, tmx_map, player_start_pos):
        for layer in ['BG', 'BG2', 'BG3']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    group = self.all_sprites,
                    layer = WORLD_DRAW_ORDER['bg']
                )

        # Monster environment objects, areas and tiles where monsters can spawn
        for obj in tmx_map.get_layer_by_name('Monsters'):
            self.monster_env = MonsterEnv(
                pos = (obj.x, obj.y),
                group = self.all_sprites,
                obj = obj,
                tmx_data = tmx_map
            )

        # Collision objects, stops player from walking in area
        for obj in tmx_map.get_layer_by_name('Collisions'):
            self.collision = CollisionSprite(
                pos = (obj.x, obj.y),
                size = (obj.width, obj.height),
                group = self.collision_sprites,
                layer = WORLD_DRAW_ORDER['bg']
            )

        # Transition objects, warps player to target map
        for obj in tmx_map.get_layer_by_name('Transitions'):
            if obj.name == 'transition':
                self.transition = TransitionSprite(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    target_map = obj.properties['target_map'],
                    current_map = obj.properties['current_map'],
                    group = self.transition_sprites,
                    layer = WORLD_DRAW_ORDER['bg']
                )

        # All remaining entities in layer that are not player or NPC objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name != 'player' and obj.name != 'npc':
                self.entities = MapObject(
                    pos = (obj.x, obj.y),
                    group = self.all_sprites,
                    obj = obj,
                    tmx_data = tmx_map,
                    layer=WORLD_DRAW_ORDER['main']
                )

        # Player and NPCs
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                if obj.pos == player_start_pos:
                    self.player = Player(
                        pos = (obj.x, obj.y),
                        frames = self.world_animations['characters'][player_sprite],
                        group = self.all_sprites,
                        collision_sprites = self.collision_sprites,
                        facing_direction = obj.properties['direction'],
                    )
            elif obj.name == 'npc':
                self.NPCs(
                    pos=(obj.x, obj.y),
                    frames = self.world_animations['characters'][obj.properties['sprite']],
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    facing_direction = obj.properties['direction'],
                )


    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            for sprite in sprites:
                target_map = sprite.target_map
                current_map = sprite.current_map
                print(f"Transition triggered: {sprite.current_map} -> {sprite.target_map}")

                #fade out
                screen_fade(self, fade_in=False)

                # unload all groups
                self.all_sprites.empty()
                self.collision_sprites.empty()
                self.transition_sprites.empty()

                # load new map
                new_tmx = self.tmx_maps[target_map]

                # extract player_start_pos from player spawn object
                for obj in new_tmx.get_layer_by_name('Entities'):
                    if obj.name == 'player':
                        player_start_pos = obj.pos
                        break

                if player_start_pos:
                    self.setup(new_tmx, player_start_pos)

                # fade in
                screen_fade(self, fade_in=True)


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