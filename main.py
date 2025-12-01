from settings import *
from sprites import Sprite, TransitionSprite, CollisionSprite, AnimatedSprite, MonsterEnv, MapObject
from entities import *
from groups import AllSprites
from helpers import *
from dialogue import DialogueTree
from game_data import *


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
        self.npc_sprites = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        # Stores current dialogue tree
        self.dialogue_tree = None

        # Cooldown variables for interaction (prevents instant restart)
        self.can_interact = True
        self.interaction_cooldown = 200  # 200 milliseconds
        self.last_interaction_time = 0

        self.import_assets()
        self.setup(
            # self.tmx_maps['world'], 'player_house'
            self.tmx_maps['player_house'], 'spawn'
        )

    # Dictionaries used to load assets
    def import_assets(self):
        self.tmx_maps = import_tmx(MAP_DIRECTORY)

        self.world_animations = {
            'characters': import_characters(characters),
        }

        self.fonts = {
            'dialogue': pygame.font.Font(dialogue_font, dialogue_font_size),
        }

    # Generates object class instances based on data in Tiled maps
    # Each map layer is being looked at individually by name so names need to be consistent between maps
    def setup(self, tmx_map, player_start_pos):
        # Makes sure all groups are empty before adding new sprites to groups
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.npc_sprites, self.ui_group):
            group.empty()

        # Sets up all background items like floor/wall tiles and non-interactive decorations
        for layer in ['BG', 'BG2', 'BG3']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    group=self.all_sprites,
                    layer=WORLD_DRAW_ORDER['bg']
                )

        # Monster environment objects, areas and tiles where monsters can spawn
        for obj in tmx_map.get_layer_by_name('Monsters'):
            self.monster_env = MonsterEnv(
                pos=(obj.x, obj.y + 3),
                group=self.all_sprites,
                obj=obj,
                tmx_data=tmx_map,
                layer=WORLD_DRAW_ORDER['main']
            )

        # Collision objects, stops player from walking in area
        for obj in tmx_map.get_layer_by_name('Collisions'):
            self.collision = CollisionSprite(
                pos=(obj.x, obj.y),
                size=(obj.width, obj.height),
                group=self.collision_sprites,
                layer=WORLD_DRAW_ORDER['bg']
            )

        # Transition objects, warps player to target map
        for obj in tmx_map.get_layer_by_name('Transitions'):
            if obj.name == 'transition':
                self.transition = TransitionSprite(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    target_map=obj.properties['target_map'],
                    current_map=obj.properties['current_map'],
                    group=self.transition_sprites,
                    layer=WORLD_DRAW_ORDER['bg']
                )

        # All remaining entities in layer that are not player or NPC objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name != 'player' and obj.name != 'npc':
                self.entities = MapObject(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    obj=obj,
                    tmx_data=tmx_map,
                    layer=WORLD_DRAW_ORDER['main']
                )

        # Player and NPCs
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                if obj.pos == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.world_animations['characters'][player_sprite],
                        group=self.all_sprites,
                        collision_sprites=self.collision_sprites,
                        facing_direction=obj.properties['direction'],
                    )
            elif obj.name == 'npc':
                self.npc = NPC(
                    pos=(obj.x, obj.y),
                    frames=self.world_animations['characters'][obj.properties['sprite']],
                    group=(self.all_sprites, self.npc_sprites, self.collision_sprites),
                    facing_direction=obj.properties['direction'],
                    npc_data=NPC_DATA[obj.properties['npc_id']]
                )

    # Checks if player is in contact with a transition sprite, loads new map
    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.block()
            for sprite in sprites:
                target_map = sprite.target_map
                current_map = sprite.current_map
                print(f"Transition triggered: {sprite.current_map} -> {sprite.target_map}")

                # fade out
                screen_fade(self, fade_in=False)

                # unload all groups
                self.all_sprites.empty()
                self.collision_sprites.empty()
                self.transition_sprites.empty()

                # load new map
                new_tmx = self.tmx_maps[target_map]

                # extract player_start_pos from player spawn object
                player_start_pos = None
                # noinspection PyTypeChecker
                for obj in new_tmx.get_layer_by_name('Entities'):
                    if obj.name == 'player':
                        player_start_pos = obj.pos
                        break

                if player_start_pos:
                    self.setup(new_tmx, player_start_pos)

                # fade in
                screen_fade(self, fade_in=True)
                self.player.unblock()

    # Allows player input otherwise blocked, used for special events like advancing dialogue
    def input(self, current_time):
        keys = pygame.key.get_just_pressed()

        # Advance dialogue, close when no more dialogue present
        if self.dialogue_tree:
            if keys[pygame.K_SPACE] and self.can_interact:
                self.dialogue_tree.advance_dialogue()

                # Reset cooldown immediately upon action
                self.can_interact = False
                self.last_interaction_time = current_time

            return

        # Initiate new dialogue window only if current dialogue is closed
        if keys[pygame.K_SPACE] and self.can_interact:
            for npc in self.npc_sprites:
                if check_connections(32, self.player, npc):

                    # Make NPC face player when talking
                    npc.change_facing_direction(self.player.rect.center)

                    # Create dialogue
                    self.create_dialogue(npc)

                    # Reset cooldown immediately upon starting dialogue
                    self.can_interact = False
                    self.last_interaction_time = current_time

                    # Break out of loop after desired NPC is found
                    break

    def create_dialogue(self, npc):
        self.dialogue_tree = DialogueTree(npc, self.player, self.ui_group, self.fonts['dialogue'])

    # Main logic loop function
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            current_time = pygame.time.get_ticks()

            # Cooldown logic, checks cooldown state
            if not self.can_interact and current_time - self.last_interaction_time >= self.interaction_cooldown:
                self.can_interact = True

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw game
            self.input(current_time)

            if self.dialogue_tree:
                self.dialogue_tree.update(dt)
                if not self.dialogue_tree.active:
                    self.dialogue_tree = None  # Dialogue is closed here!

            self.all_sprites.update(dt)
            self.ui_group.update(dt)
            self.transition_check()
            self.screen.fill(BACKGROUND_COLOR)
            self.all_sprites.draw_stuff(self.player.hitbox.topleft)
            self.ui_group.draw(self.screen)
            pygame.display.update()

            # Debug: prints delta time to console so we can see if I did something dumb that is slowing down the game
            # print(dt)


if __name__ == "__main__":
    game = Game()
    game.run()