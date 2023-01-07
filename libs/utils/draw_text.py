import pygame as pg

# -------------------------------------------------------------------------------------------

class Text:

    # -------------------------------------------------------------------------------------------

    def __init__(self, FontName=None, FontSize=30):

        pg.font.init()
        self.font = pg.font.Font(FontName, FontSize)
        self.size = FontSize

    # -------------------------------------------------------------------------------------------

    # def render(self, surface, text, color, pos):
    def render(self, surface, text, pos, color, bg_color = None):

        # x, y = pos
        # for i in text.split("\r"):
        #     surface.blit(self.font.render(i, 1, color), (x, y))
        #     y += self.size
        x, y = pos
        for i in text.split('\r'):
            text_surf= self.font.render(i,True,color,bg_color)
            text_rect = text_surf.get_rect()
            text_rect.move_ip(x,y)
            surface.blit(text_surf,text_rect)
