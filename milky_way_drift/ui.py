"""
UI
================

Display of grid-space and user inputs
"""

import kivy.app
from kivy.graphics.vertex_instructions import Mesh
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.graphics import Line, Color
from kivy.core.window import Window
import hexgrid
import morton


# takes square coordinates and outputs a hexgrid.Hex that hexgrid-py would identify as being at that location
def hex_at(x, y):
    return hexgrid.Hex(x, y - x//2)  # // is floor division (integer division)


# takes a hexgrid.Hex and gives you its y coordinate in square coordinates
def hex_y(h):
    return h[0]//2 + h[1]


def hex_vertices(grid, h):
    c = grid.hex_corners(h)
    return [c[0][0], c[0][1], 0, 0, c[1][0], c[1][1], 0, 0, c[2][0], c[2][1], 0, 0,
            c[3][0], c[3][1], 0, 0, c[4][0], c[4][1], 0, 0, c[5][0], c[5][1], 0, 0]


class HexCanvas(kivy.app.Widget):
    def __init__(self, width, height, rows, columns, selection_color, grid_color, grid_width):
        super(HexCanvas, self).__init__()
        self.grid = hexgrid.Grid(hexgrid.OrientationFlat, hexgrid.Point(0, 0),
                                 hexgrid.Point(width, height), morton.Morton(2, 32))
        self.hexes = []
        for x in range(0, rows):
            for y in range(0, columns):
                self.hexes.append(hex_at(x, y))
        lines_dict = {}  # dictionary of Point() to Point()[]
        for h in range(0, len(self.hexes)):
            corners = self.grid.hex_corners(self.hexes[h])
            for i in range(0, 6):
                if corners[i] not in lines_dict.keys():
                    lines_dict[corners[i]] = []
                if not corners[(i + 1) % 6] in lines_dict[corners[i]]:
                    if corners[(i + 1) % 6] not in lines_dict.keys() \
                            or corners[i] not in lines_dict[corners[(i + 1) % 6]]:
                        lines_dict[corners[i]].append(corners[(i + 1) % 6])
        with self.canvas:
            Color(selection_color[0], selection_color[1], selection_color[2], selection_color[3])
            self.selection_mesh = Mesh(vertices=hex_vertices(self.grid, self.hexes[0]),
                                       indices=[0, 1, 2, 3, 4, 5], mode='triangle_fan')
            Color(grid_color[0], grid_color[1], grid_color[2], grid_color[3])
            for key in lines_dict.keys():
                lines = []
                for point in lines_dict[key]:
                    lines.append([key.x, key.y, point.x, point.y])
                Line(points=lines, width=grid_width, cap='square')


class HexApp(kivy.app.App):
    def __init__(self, width, height, rows, columns, selection_mode, selection_color, grid_color, grid_width):
        super(HexApp, self).__init__()
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.selection_mode = selection_mode
        self.selection_color = selection_color
        self.grid_color = grid_color
        self.grid_width = grid_width
        self.selected_hex = hexgrid.Hex(0, 0)
        self.selection_mesh = None
        self.grid = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def build(self):
        layout = RelativeLayout(size=(2000, 2000))

        hex_grid = HexCanvas(self.width, self.height, self.rows, self.columns,
                             self.selection_color, self.grid_color, self.grid_width)
        hex_grid.selection_mesh.vertices = hex_vertices(hex_grid.grid, self.selected_hex)
        self.selection_mesh = hex_grid.selection_mesh
        grid = hex_grid.grid
        self.grid = grid
        # label the hexes with square coordinates for developer reference
        for i in range(0, len(hex_grid.hexes)):
            h = hex_grid.hexes[i]
            label = Label(text=str(h[0]) + ',' + str(hex_y(h)), width=10, height=10, color=(0.3, 0.3, 0.3, 1),
                          x=grid.hex_center(h).x - 5, y=grid.hex_center(h).y - 5)
            hex_grid.add_widget(label)
        layout.add_widget(hex_grid)
        return layout

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.selection_mode == 'hex':
            if keycode[1] == 'w':
                self.select_adjacent(0, 1, True)
            if keycode[1] == 's':
                self.select_adjacent(0, -1, True)
            if keycode[1] == 'a':
                self.select_adjacent(-1, 0, True)
            if keycode[1] == 'd':
                self.select_adjacent(1, -1, True)
            if keycode[1] == 'q':
                self.select_adjacent(-1, 1, True)
            if keycode[1] == 'e':
                self.select_adjacent(1, 0, True)
        elif self.selection_mode == 'square':
            if keycode[1] == 'w':
                self.select_adjacent(0, 1, False)
            if keycode[1] == 's':
                self.select_adjacent(0, -1, False)
            if keycode[1] == 'a':
                self.select_adjacent(-1, 0, False)
            if keycode[1] == 'd':
                self.select_adjacent(1, 0, False)
        return True

    # updates selected hex by adding x and y to current square coordinate (or hex coord if use_hex is true)
    def select_adjacent(self, x, y, use_hex):
        if use_hex:
            requested_hex = hexgrid.Hex(self.selected_hex[0] + x, self.selected_hex[1] + y)
            square_y = hex_y(requested_hex)
            if square_y < 0 or square_y >= self.height:
                return
            else:
                self.select_hex(requested_hex[0], requested_hex[1], True)
                return
        else:
            self.select_hex(max(min(self.selected_hex[0] + x, self.width - 1), 0),
                            max(min(hex_y(self.selected_hex) + y, self.height - 1), 0), False)

    # Select a hex using square coordinates, unless use_hex is passed as true
    def select_hex(self, x, y, use_hex):
        if use_hex:
            self.selected_hex = hexgrid.Hex(x, y)
        else:
            self.selected_hex = hex_at(x, y)
        self.selection_mesh.vertices = hex_vertices(self.grid, self.selected_hex)
