from blessed import Terminal

term = Terminal()

regular = term.on_color_rgb(40, 40, 40) + term.color_rgb(255, 169, 0)
reverse = term.color_rgb(40, 40, 40) + term.on_color_rgb(255, 169, 0)
