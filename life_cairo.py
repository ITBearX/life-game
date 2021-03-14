import life_core
from life_core import LifeGrid

class LifeGridCairo(LifeGrid):

    def setScale(self, cr, width, height):
        shape_ratio = self.size[0] / self.size[1]
        box_ratio = height / width

        if shape_ratio > box_ratio:
            scale = height / self.size[0]
        else:
            scale = width / self.size[1]
        cr.translate(0, 0)
        cr.scale(scale, scale)

    def draw(self, cr, width, height):
        self.setScale(cr, width, height)
        cr.set_line_width(0.02)

        cr.set_source_rgb(0.0, 0.5, 1.0)
        cr.rectangle(0, 0, self.size[1], self.size[0])
        cr.stroke()

        cr.set_line_width(0.01)
        for row in range(0, self.size[0]):
            for col in range(0, self.size[1]):
                if self.getCellState((row, col)):
                    cr.set_source_rgb(0.0, 1.0, 0.0)
                    cr.rectangle(col+0.1, row+0.1, 0.8, 0.8)
                    cr.fill()
#                    print('X', end='')
#                else:
#                    print('_', end='')
            print()
        print()
