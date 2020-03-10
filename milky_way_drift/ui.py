'''
UI Examples
================

A Place to document rendering practices and tinker
'''


from kivy.lang import Builder
from kivy.app import App
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

# this is one way to load from file, seems useful for things that don't change.
# we can manipulate this just like a widget we create in python - I think
presentation = Builder.load_file("resources/float_layout.kv")


# Here we make use of the loaded file
class TestApp(App):
    def build(self):
        return presentation


# Here we make a layout with a function
class RotationApp(App):
    def build(self):
        layout = FloatLayout(size=(300,300))
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


TestApp().run()
