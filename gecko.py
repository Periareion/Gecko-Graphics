"""
Anton Oresten Sollman

Created Oct 2021

@COPYLEFT ALL WRONGS RESERVED
"""

import sys, os
import time
import math

# To avoid the start-up message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np

pygame.font.init()

# An empty color with zero alpha
empty = pygame.Color(0,0,0,0)

BACKGROUND_COLOR = pygame.Color(255,255,255)
WIDTH, HEIGHT = 800, 600
HALF_SCREEN = [WIDTH/2, HEIGHT/2]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gecko Graphics')

try:
    pygame.display.set_icon(pygame.image.load('images/gecko.png'))
except:
    pass

screen.fill(BACKGROUND_COLOR)
pygame.display.update()

path_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

def screen_pos(position):
    return position*[1,-1]+HALF_SCREEN

# Update screen
def update():
    screen.fill(BACKGROUND_COLOR)
    screen.blit(path_surface, (0,0))
    
    for gecko in geckos:
        gecko.draw_body()
        screen.blit(gecko.surf, (0,0))
        
    pygame.display.update()

def draw_line(color, start, end, width=1, surf=path_surface):
    pygame.draw.line(surf, color, start, end, width)

geckos = []

class Gecko:
    
    def __init__(self, position=[0,0], angle=0):
        geckos.append(self)
        
        self.position = np.array(position, dtype=np.float64)
        self.angle = angle

        self.shape = 'triangle'
        self.color = pygame.Color(0,0,0)
        self.size = 4
        self.pencolor = self.color
        self.pensize = 1

        self.trace_gecko = True
        self.show_gecko = True

        # Update screen when gecko moves (will make it slower)
        self.auto_update = True

        self.first_position = self.position.copy()
        self.set_last_position()

        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self._update()

    def _update(self):

        if self.auto_update:
            update()

    @property
    def properties(self):
        p = {
            'position': self.position,
            'angle': self.angle,
            'shape': self.shape,
            'color': self.color,
            'size': self.size,
            'pencolor': self.pencolor,
            'pensize': self.pensize,
            'trace_gecko': self.trace_gecko,
            'show_gecko': self.show_gecko,
        }
        
        return p

    # Write some text    
    def write(self, text):
        font = pygame.font.SysFont('Calibri', 12)
        screen_position = screen_pos(self.position)
        self.surf.blit(font.render(text, True, self.pencolor), (screen_position[0]+8, screen_position[1]-5))
        self._update()

    def clear(self, update=True):
        self.surf.fill(empty)
        if update:
            self._update()

    # Whether to draw path
    def pendown(self):
        self.trace_gecko = True

    def penup(self):
        self.trace_gecko = False
        
    def set_last_position(self):
        self.last_position = self.position.copy()

    def show(self):
        self.show_gecko = True
        self._update()

    def hide(self):
        self.show_gecko = False
        self._update()

    def set_color(self, color):
        self.color = pygame.Color(color)
        self._update()

    def set_pencolor(self, color):
        self.pencolor = pygame.Color(color)
        self._update()

    def set_angle(self, angle):
        self.angle = angle

    def rotate(self, angle):
        self.angle += angle

    def left(self, angle):
        self.rotate(angle)

    def right(self, angle):
        self.rotate(-angle)

    def set_position(self, position, draw_line=True):
        if len(position) == 1:
            position = np.array(*position, dtype=np.float64)
        elif len(position) == 2:
            position = np.array(position, dtype=np.float64)
        else:
            raise ValueError
        self.position = position
        if draw_line:
            self.draw_path_line()
        self._update()

    # Aliases for set_position
    setpos = set_pos = goto = setposition = set_position

    def move(self, *offset):
        if len(offset) == 1:
            offset = np.array(*offset, dtype=np.float64)
        elif len(offset) == 2:
            offset = np.array(offset, dtype=np.float64)
        else:
            raise ValueError
        self.position += offset
        self.draw_path_line()
        self._update()

    def forward(self, distance):
        self.move([distance*math.cos(math.radians(self.angle)), distance*math.sin(math.radians(self.angle))])

    def backward(self, distance):
        self.move([-distance*math.cos(math.radians(self.angle)), -distance*math.sin(math.radians(self.angle))])

    fd, bk = forward, backward

    def draw_body(self):
        if self.show_gecko:
            if self.shape == 'circle':
                pygame.draw.circle(screen, self.color, screen_pos(self.position)+1, self.size)
            elif self.shape == 'square':
                pygame.draw.rect(screen, self.color, pygame.Rect(screen_pos(self.position)-self.size+1, (2*self.size, 2*self.size)))
            elif self.shape == 'triangle':

                # These positions form a triangle that points in the direction of the Gecko
                pos0 = screen_pos(self.position + [6*math.cos(math.radians(self.angle)), 6*math.sin(math.radians(self.angle))])
                pos1 = screen_pos(self.position + [6*math.cos(math.radians(self.angle+150)), 6*math.sin(math.radians(self.angle+120))])
                pos2 = screen_pos(self.position + [6*math.cos(math.radians(self.angle+210)), 6*math.sin(math.radians(self.angle+240))])

                pygame.draw.polygon(screen, self.color, [pos0,pos1,pos2])
                
                pygame.draw.line(screen, '#000000', pos0, pos1, 1)
                pygame.draw.line(screen, '#000000', pos0, pos2, 1)
                pygame.draw.line(screen, '#000000', pos1, pos2, 2)

    def draw_path_line(self):
        if self.trace_gecko:
            draw_line(self.pencolor, screen_pos(self.last_position), screen_pos(self.position), self.pensize, self.surf)
        self.set_last_position()

    # Clone a gecko save it in a variable
    def clone(self, name):
        clone = Gecko()
        globals().update({name: clone})
        clone.penup()
        
        clone.position = self.position
        clone.angle = self.angle
        clone.shape = self.shape
        clone.color = self.color
        clone.size = self.size
        clone.pencolor = self.pencolor
        clone.pensize = self.pensize

        clone.pendown()

        return clone

    def __repr__(self):
        return f"Gecko object at [{round(self.position[0],1)}, {round(self.position[1],1)}]"

    __str__ = __repr__

def q():
    pygame.quit()

def main():

    # This is a complete mess, but produces a nice looking animation and an even nicer result.

    g = Gecko()
    g.right(90)
    g.set_color(pygame.Color(255,0,0))
    g.set_pencolor(pygame.Color(0,255,255))
    g.pensize = 2
    g.auto_update = False
    test = 0
    g.hide()

    # num > 7
    num = 6
        
    for k in range(2**(8+num)-1):
        if not k % 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:import sys;pygame.quit(); sys.exit()
        for i in range(2):
            if i == 0:
                g.set_pencolor((0,128-k//2**(1+num),255-k//2**num))
            else:
                g.set_pencolor((255-k//2**num,128-k//2**(1+num),0))
            for n in range(180):
                test += 1
                g.forward((k+1)/3000)
                g.rotate(2*(2*(i%2)-1))

        # update after every 20 loops (when k is divisible by 20)
        if not k % 20:
            update()
            
    print(test)

if __name__ == '__main__':
    print("Enter 'q()' to close the window")
    main()
else:
    print("Gecko has been loaded. Enter 'gecko.q()' to close the window")
