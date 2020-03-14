"""
Main
================

Application launch point for end user
"""

import data
import ui

# Configuration Parameters
hex_rows = 28
hex_columns = 14
hex_width = 50
hex_height = 50
selection_mode = 'hex'  # 'square' (w s a d) or 'hex' (q w e a s d)
selection_color = [.1, .1, .4, 0.6]  # rgba used to construct kivy Color
grid_color = [.1, .1, .4, 1]  # rgba used to construct kivy Color
grid_width = 2

# "python __main__.py" to run in dev
if __name__ == "__main__":
    hex_app = ui.HexApp(hex_width, hex_height, hex_rows, hex_columns, selection_mode,
                        selection_color, grid_color, grid_width)
    hex_app.run()
