class Settings:

    def __init__(self):
        # Display settings
        self.display_width = 1280
        self.display_size = (self.display_width,
                             int(9 * self.display_width / 16))

        # Map settings
        self.weight = 255
        self.bias = 127
        self.pixel_size = 40

        # Bug settings
        self.bug_size = 20
        self.bug_color = (200, 200, 200)
        self._x = 300
        self._y = 300
        self._movement = (-0.08, -0.01)
        self._rotation = 0.1