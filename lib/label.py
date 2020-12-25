import math

class BarStyle():
  SOLID             = 0
  DIAGONAL_FORWARD  = 1
  DIAGONAL_BACKWARD = 2
  ARROW_FORWARD     = 3
  ARROW_BACKWARD    = 4

class LabelBase():

  def __init__(self, x, y, width, height, oled):
    self.inited = False

    self.x = x
    self.y = y
    self.height = height
    self.width = width
    self.oled = oled
    self.text = None
    self.text_color = 1
    self.show_text_mask = True

    self.update()
    self.inited = True

  def update(self):
    # print the text out
    self.draw_text()

  def set_text(self, text, color=1):
    self.text = text
    self.text_color = color
    self.update()

  def draw_text(self):
    if self.text == None:
      return

    # All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
    text_width = len(self.text) * 8
    block_padding = 1 # 1 pixel padding around text mask
    text_x = math.floor(self.x + (self.width - text_width) / 2)
    text_y = math.floor(self.y + (self.height - 6) / 2)
    self.oled.fill_rect(
        text_x - block_padding,
        text_y - block_padding,
        text_width + block_padding * 2,
        8 + block_padding * 2,
        not self.text_color
      )
    self.oled.text(self.text, text_x, text_y, self.text_color)
    self.oled.show()

class Label(LabelBase):
  def __init__(self, x, y, width, height, oled):
    super().__init__(x, y, width, height, oled)
    self.inited = True

  def redraw(self):
    self.inited = False
    super().update()
    self.inited = True

  def update(self):
    if not self.inited:
      # update unoptimized the first time (paint all pixels)
      return super().update()
    # print the text out
    self.draw_text()
