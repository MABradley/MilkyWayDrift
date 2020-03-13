"""
UI Examples
================

A Place to document rendering practices and tinker
"""

from kivy.lang import Builder
import kivy.app
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh
from functools import partial
from math import cos, sin, pi

# this is one way to load from file, seems useful for things that don't change.
# we can manipulate this just like a widget we create in python - I think
presentation = Builder.load_file("resources/float_layout.kv")


# Here we make use of the loaded file
class TestApp(kivy.app.App):
    def build(self):
        return presentation


# Here we make a layout with a function
class RotationApp(kivy.app.App):
    def build(self):
        layout = FloatLayout(size=(300, 300))
        button = Button(
            text='Hello world',
            size_hint=(.5, .25),
            pos=(20, 20))
        button2 = Button(text='Hello world', size_hint=(.6, .6),
                         pos_hint={'x': .2, 'y': .2})
        rect = Image(source='resources/test.png', size=('400', '400'), size_hint=(None, None))
        layout.add_widget(button)
        layout.add_widget(button2)
        layout.add_widget(rect)
        return layout


# used for rendering more complicated shapes (we need this for hexes)
class MeshTestApp(App):

    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def build_mesh(self):
        """ returns a Mesh of a rough circle. """
        vertices = []
        indices = []
        step = 10
        istep = (pi * 2) / float(step)
        for i in range(step):
            x = 300 + cos(istep * i) * 100
            y = 300 + sin(istep * i) * 100
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        return Mesh(vertices=vertices, indices=indices)

    def build(self):
        wid = Widget()
        with wid.canvas:
            self.mesh = self.build_mesh()

        layout = BoxLayout(size_hint=(1, None), height=50)
        for mode in ('points', 'line_strip', 'line_loop', 'lines',
                     'triangle_strip', 'triangle_fan'):
            button = Button(text=mode)
            button.bind(on_release=partial(self.change_mode, mode))
            layout.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root


if __name__ == "__main__":
    TestApp().run()


