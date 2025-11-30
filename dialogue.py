from settings import *

# Note: Gemini re-wrote this to add the text scrolling animation and significantly changed the draw logic

class DialogueTree:
    def __init__(self, npc, player, ui_group, font):
        self.npc = npc
        self.player = player
        self.ui_group = ui_group
        self.font = font

        # Dialogue Data
        self.dialogue_lines = npc.get_dialogue()
        self.dialogue_index = 0
        self.active = True

        # Lock player and create the first text box
        self.player.block()
        self.current_box = TextBox(self.dialogue_lines[self.dialogue_index], self.ui_group, self.font)

    def advance_dialogue(self):
        if self.current_box.is_scrolling:
            # Skip the scrolling animation and show full text
            self.current_box.finish_scroll()
        else:
            # Text is finished, move to next line or close
            self.dialogue_index += 1
            self.current_box.kill()  # Remove current box sprite

            if self.dialogue_index < len(self.dialogue_lines):
                # Start the next line
                self.current_box = TextBox(self.dialogue_lines[self.dialogue_index], self.ui_group, self.font)
            else:
                # End of dialogue tree
                self.active = False
                self.player.unblock()
                self.current_box = None

    def update(self, dt):
        if self.active and self.current_box:
            self.current_box.update(dt)


class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, group, font):
        super().__init__(group)
        self.font = font
        self.full_text = text

        # Scrolling properties
        self.char_index = 0
        self.is_scrolling = True
        self.scroll_speed = TEXT_SPEED
        self.time_delay = 1.0 / self.scroll_speed
        self.time_counter = 0

        # UI Visual Constants (Pulled from settings)
        screen_width = WINDOW_WIDTH
        screen_height = WINDOW_HEIGHT
        box_height = int(screen_height * 0.25)  # Bottom 1/4 of screen

        # Image creation (Baked onto surface for performance)
        self.image = pygame.Surface((screen_width, box_height), pygame.SRCALPHA)
        self.rect = self.image.get_frect(bottomleft=(0, screen_height))
        self.padding = 15

        # Draw the static background (White box with black border)
        pygame.draw.rect(self.image, 'white', self.image.get_rect())
        pygame.draw.rect(self.image, 'black', self.image.get_rect(), width=4)

        self.render_current_text()

    def render_current_text(self):
        # 1. Get the text currently displayed
        current_text = self.full_text[:int(self.char_index)]

        # 2. Clear the previous text area (inside border)
        # We need to re-blit the background over the text area.
        text_area = self.image.get_rect().inflate(-8, -8)  # Shrink rect by border thickness
        pygame.draw.rect(self.image, 'white', text_area)

        # 3. Render the scrolling text
        text_surf = self.font.render(current_text, False, 'black')

        # 4. Blit text onto the box surface
        self.image.blit(text_surf, (self.padding, self.padding))

    def finish_scroll(self):
        self.char_index = len(self.full_text)
        self.is_scrolling = False
        self.render_current_text()

    def update(self, dt):
        if self.is_scrolling:
            self.time_counter += dt

            # Check if enough time has passed to show the next character
            if self.time_counter >= self.time_delay:

                self.char_index += 1
                self.time_counter -= self.time_delay  # Subtract time, don't reset

                # --- FIX: Check if text is completed and lock the index ---
                if self.char_index >= len(self.full_text):
                    self.char_index = len(self.full_text)
                    self.finish_scroll()

            # Always re-render if scrolling to show the new character
            self.render_current_text()