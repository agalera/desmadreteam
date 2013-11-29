class casilla:
    def __init__ (self, tile):
        self.tile = tile

    def get_tile(self):
        return self.tile
    def set_tile(self, tile):
        self.tile = tile
    def block(self):
        if self.tile == -1:
            return False
        else:
            if self.tile == 4 or self.tile == 5:
                return False
            return True
