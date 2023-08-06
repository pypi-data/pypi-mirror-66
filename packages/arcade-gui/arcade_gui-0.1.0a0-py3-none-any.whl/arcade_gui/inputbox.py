import arcade


class TextStorage:
    def __init__(self, box_width, font_size=24, theme=None):
        self.box_width = box_width
        self.font_size = font_size
        self.theme = theme
        if self.theme:
            self.font_size = self.theme.font_size
        self.char_limit = self.box_width / self.font_size
        self.text = ""
        self.cursor_index = 1
        self.cursor_symbol = "|"
        self.local_cursor_index = 0
        self.time = 0.0
        self.left_index = 0
        self.right_index = 1
        self.visible_text = ""

    def blink_cursor(self):
        seconds = self.time % 60
        if seconds > 0.1:
            if self.cursor_symbol == "_":
                self.cursor_symbol = "|"
            else:
                self.cursor_symbol = "_"
            self.time = 0.0

    def on_key_press(self, key: int, modifiers: int):
        if key in ALLOWED_KEYS:
            if key == arcade.key.BACKSPACE:
                if self.cursor_index < len(self.text):
                    text = self.text[:self.cursor_index - 1]
                    self.text = text + self.text[self.cursor_index:]
                else:
                    self.text = self.text[:-1]
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                if self.left_index > 0:
                    self.left_index -= 1
                if self.right_index > 1:
                    self.right_index -= 1
            elif key == arcade.key.LEFT:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                if 0 < self.left_index == self.cursor_index:
                    self.left_index -= 1
                    self.right_index -= 1
            elif key == arcade.key.RIGHT:
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
                if len(self.text) > self.right_index == self.cursor_index:
                    self.right_index += 1
                    self.left_index += 1
            else:
                if self.cursor_index < len(self.text):
                    self.text = self.text[:self.cursor_index] + chr(key) + self.text[self.cursor_index:]
                    self.cursor_index += 1
                    self.right_index += 1
                    if len(self.text) > self.char_limit:
                        self.left_index += 1
                else:
                    self.text += chr(key)
                    self.cursor_index += 1
                    self.right_index += 1
                    if len(self.text) >= self.char_limit:
                        self.left_index += 1

    def update(self, delta_time, key):
        self.time += delta_time
        # self.blink_cursor()
        self.visible_text = self.text[self.left_index:self.right_index]
        if self.cursor_index > self.left_index:
            self.local_cursor_index = self.cursor_index - self.left_index
        else:
            self.local_cursor_index = self.left_index
        return self.visible_text, self.cursor_symbol, self.local_cursor_index


class TextDisplay:
    def __init__(self, x, y, width=300, height=40, outline_color=arcade.color.BLACK,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.text = ""
        self.left_text = ""
        self.right_text = ""
        self.symbol = "|"
        self.cursor_index = 0
        self.theme = theme
        if self.theme:
            self.texture = self.theme.text_box_texture
            self.font_size = self.theme.font_size
            self.font_color = self.theme.font_color
            self.font_name = self.theme.font_name
        else:
            self.texture = None
            self.font_size = 24
            self.font_color = arcade.color.BLACK
            self.font_name = ('Calibri', 'Arial')

    def draw_text(self):
        if self.highlighted:
            arcade.draw_text(self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:],
                             self.x - self.width / 2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)
        else:
            arcade.draw_text(self.text, self.x - self.width / 2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)

    def color_theme_draw(self):
        if self.highlighted:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.highlight_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.shadow_color)
        self.draw_text()
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, 2)

    def texture_theme_draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
        self.draw_text()

    def draw(self):
        if self.texture == "":
            self.color_theme_draw()
        else:
            self.texture_theme_draw()

    def on_press(self):
        self.highlighted = True

    def on_release(self):
        pass

    def on_mouse_press(self, x, y, _button, _modifiers):
        if x > self.x + self.width / 2:
            self.highlighted = False
            return
        if x < self.x - self.width / 2:
            self.highlighted = False
            return
        if y > self.y + self.height / 2:
            self.highlighted = False
            return
        if y < self.y - self.height / 2:
            self.highlighted = False
            return
        self.on_press()

    def on_mouse_release(self, x, y, _button, _modifiers):
        if self.highlighted:
            self.on_release()

    def update(self, _delta_time, text, symbol, cursor_index):
        self.text = text
        self.symbol = symbol
        self.cursor_index = cursor_index


class UIInputBox:
    def __init__(self, x, y, width=300, height=40, theme=None, outline_color=arcade.color.BLACK, font_size=24,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE):
        self.theme = theme
        if self.theme:
            self.text_display = TextDisplay(x, y, width, height, theme=self.theme)
            self.text_storage = TextStorage(width, theme=self.theme)
        else:
            self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)
            self.text_storage = TextStorage(width, font_size)
        self.text = ""

    def draw(self):
        self.text_display.draw()

    def update(self, delta_time, key):
        if self.text_display.highlighted:
            self.text, symbol, cursor_index = self.text_storage.update(delta_time, key)
            self.text_display.update(delta_time, self.text, symbol, cursor_index)

    def check_mouse_press(self, x, y):
        self.text_display.check_mouse_press(x, y)

    def check_mouse_release(self, x, y):
        self.text_display.check_mouse_release(x, y)