from life_core import LifeGrid


class LifeGridCairo(LifeGrid):

    def _set_scale(self, cr, width, height):
        shape_ratio = self.rows / self.cols
        box_ratio = height / width

        if shape_ratio > box_ratio:
            scale = height / self.rows
        else:
            scale = width / self.cols
        cr.translate(0, 0)
        cr.scale(scale, scale)

    def draw(self, cr, width, height):
        self._set_scale(cr, width, height)
        cr.set_line_width(0.02)

        cr.set_source_rgb(0.0, 0.5, 1.0)
        cr.rectangle(0, 0, self.cols, self.rows)
        cr.stroke()

        cr.set_line_width(0.01)
        for row in range(self.rows):
            for col in range(self.cols):
                if self[row, col]:
                    cr.set_source_rgb(0.0, 1.0, 0.0)
                    cr.rectangle(col+0.1, row+0.1, 0.8, 0.8)
                    cr.fill()
