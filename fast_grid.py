

class Grid:
    def __init__(self, *cells_size):
        self.sells_sum = sum(cells_size)
    
    def __call__(self, all_size, cell_size):
        return (all_size/self.sells_sum)*cell_size