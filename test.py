import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty
import random

kivy.require('2.1.0')  # replace with your version

class GameWidget(Widget):
    square_pos = ListProperty([200, 200])
    square_size = ListProperty([50, 50])
    circle_radius = 25
    map_size = (50 * 10, 50 * 10)
    circles = []
    print(Window.height)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.keys_pressed = set()
        self.create_circles()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keys_pressed.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        self.keys_pressed.discard(keycode[1])

    def create_circles(self):
        for _ in range(20):
            x = random.randint(0, self.map_size[0] // 50 - 1) * 50 + 25
            y = random.randint(0, self.map_size[1] // 50 - 1) * 50 + 25
            self.circles.append((x, y))

    def update(self, dt):
        step = 5
        moved = False
        if 'w' in self.keys_pressed:
            self.move_square(0, step)
            moved = True
        if 's' in self.keys_pressed:
            self.move_square(0, -step)
            moved = True
        if 'a' in self.keys_pressed:
            self.move_square(-step, 0)
            moved = True
        if 'd' in self.keys_pressed:
            self.move_square(step, 0)
            moved = True
        if 'spacebar' in self.keys_pressed:
            self.hit_circles()

        if moved:
            print(f"Square position: {self.square_pos}")  # Debug print

        self.canvas.clear()
        self.draw_background()
        self.draw()

    def draw_background(self):
        with self.canvas.before:
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.pos, size=self.size)

    def move_square(self, dx, dy):
        new_pos = [self.square_pos[0] + dx, self.square_pos[1] + dy]
        if not self.detect_collision(new_pos):
            self.square_pos = new_pos

    def detect_collision(self, new_pos):
        for cx, cy in self.circles:
            if abs(new_pos[0] - cx) < self.circle_radius + self.square_size[0] / 2 and \
               abs(new_pos[1] - cy) < self.circle_radius + self.square_size[1] / 2:
                return True
        return False

    def hit_circles(self):
        to_remove = []
        for cx, cy in self.circles:
            if abs(self.square_pos[0] - cx) <= 50 and abs(self.square_pos[1] - cy) <= 50:
                to_remove.append((cx, cy))
        for circle in to_remove:
            self.circles.remove(circle)

    def draw(self):
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=self.square_pos, size=self.square_size)
            Color(1, 0, 0)
            for cx, cy in self.circles:
                Ellipse(pos=(cx - self.circle_radius, cy - self.circle_radius), size=(self.circle_radius * 2, self.circle_radius * 2))

class GameApp(App):
    def build(self):
        game = GameWidget()
        game.bind(size=self._update_rect, pos=self._update_rect)
        return game

    def _update_rect(self, instance, value):
        instance.pos = (Window.width - instance.width) / 2, (Window.height - instance.height) / 2

if __name__ == '__main__':
    GameApp().run()
