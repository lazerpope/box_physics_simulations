from decouple import config
DEBUG_FONT_SIZE_2 = config("DEBUG_FONT_SIZE_2",default=30, cast=int)
SPEED_THRESHOLD = config("SPEED_THRESHOLD",default=0.01, cast=float)
WHITE = (255, 255, 255)

import pygame as pg


class Point:
    """
    Define a x and y point on 2d space
    Attributes:
        x: float
        y: float
    """    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    def toTuple(self):
        return (self.x, self.y)




class GameObject:    
    
    """
    GameObject that exists in game
    Attributes:
        pos: Point
        speed: Point
        height: int
        width: int
        color: pg.Color
        mass_mul: float
        elasticity: float
    """
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        sx: float = 0,
        sy: float = 0,
        height: int = 1,
        width: int = 1,
        color: pg.Color = pg.Color(255, 255, 255),
        mass_mul: float = 1,
        elasticity: float = 0.97,
    ) -> None:
        self.pos = Point(x, y)
        self.speed = Point(sx, sy)
        self.height = height
        self.width = width
        self.color = color
        self.mass_mul = mass_mul
        self.elasticity = elasticity

    @property
    def center(self):
        return Point(self.pos.x + self.width / 2, self.pos.y + self.height / 2)

    @property
    def mass(self):
        return self.height * self.width * self.mass_mul

    @property
    def right(self):
        return self.pos.x + self.width

    @property
    def left(self):
        return self.pos.x

    @property
    def top(self):
        return self.pos.y

    @property
    def bottom(self):
        return self.pos.y + self.height

    @property
    def topleft(self):
        return Point(self.pos.x, self.pos.y)

    @property
    def topright(self):
        return Point(self.pos.x + self.width, self.pos.y)

    @property
    def bottomleft(self):
        return Point(self.pos.x, self.pos.y + self.height)

    @property
    def bottomright(self):
        return Point(self.pos.x +self.width, self.pos.y+ self.height)

    def draw(self, screen):
        """
        Draw the object on the screen
        """
        pg.draw.rect(
            screen, self.color, (self.pos.x, self.pos.y, self.width, self.height)
        )

    def debugDraw(self, screen, *args):
        """
        Draw debug info about the object on the screen
        Info to draw must be specified as *args
        """
        
        i = -DEBUG_FONT_SIZE_2
        for arg in args:
            i += DEBUG_FONT_SIZE_2
            if isinstance(arg, int) or isinstance(arg, float):
                t = round(arg, 1)
            else:
                t = arg
            s = str(t) 
            font = pg.font.Font(None, DEBUG_FONT_SIZE_2)
            text = font.render(s, True, WHITE)
            screen.blit(text, (self.pos.x + 5, self.pos.y+i + 5))

    def update(self, fps):
        """
        Update the position of the object (fps-dependant)
        
        speed_threshold determines the speed 
        at which the speed will reset to zero
        """
        if abs(self.speed.x) < SPEED_THRESHOLD:
            self.speed.x = 0
        if abs(self.speed.y) < SPEED_THRESHOLD:
            self.speed.y = 0
        self.pos.x += self.speed.x / fps
        self.pos.y += self.speed.y / fps
