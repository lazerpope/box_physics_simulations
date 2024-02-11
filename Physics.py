from GameObject import GameObject
from decouple import config
import math

SCREEN_WIDTH = config("SCREEN_WIDTH", default=800, cast=int)
SCREEN_HEIGHT = config("SCREEN_HEIGHT", default=600, cast=int)


class Physics:
    @staticmethod
    def collide(this: GameObject, other: GameObject) -> None:
        """
        performs a collision between two GameObjects
        exchanging their speeds
        """
        total_mass = this.mass + other.mass
        diff_mass = this.mass - other.mass
        elasticity = (this.elasticity + other.elasticity) / 2

        print()

        tmp = this.speed.x
        this.speed.x = (diff_mass / total_mass) * this.speed.x + (
            ((other.mass * 2) / total_mass) * other.speed.x
        ) * elasticity
        other.speed.x = (-diff_mass / total_mass) * other.speed.x + (
            ((this.mass * 2) / total_mass) * tmp
        ) * elasticity
        tmp = this.speed.y
        this.speed.y = (diff_mass / total_mass) * this.speed.y + (
            ((other.mass * 2) / total_mass) * other.speed.y
        ) * elasticity
        other.speed.y = (-diff_mass / total_mass) * other.speed.y + (
            ((this.mass * 2) / total_mass) * tmp
        ) * elasticity

        if this.pos.x - other.pos.x > 0:
            this.pos.x += 1
            other.pos.x -= 1
        else:
            this.pos.x -= 1
            other.pos.x += 1
        if this.pos.y - other.pos.y > 0:
            this.pos.y += 1
            other.pos.y -= 1
        else:
            this.pos.y -= 1
            other.pos.y += 1



    @staticmethod
    def collideWallX(obj: GameObject):
        """
        performs a collision between a GameObject and a wall
        exchanging its speed in x direction
        """
        obj.speed.x *= -1 * obj.elasticity
        obj.speed.y *= obj.elasticity
        if obj.pos.x <= 0:
            obj.pos.x = 1
        if obj.right  >= SCREEN_WIDTH:
            obj.pos.x = SCREEN_WIDTH - obj.width - 1

    @staticmethod
    def collideWallY(obj: GameObject):
        """
        performs a collision between a GameObject and a wall
        exchanging its speed in y direction
        """
        obj.speed.y *= -1 * obj.elasticity
        obj.speed.x *= obj.elasticity

        if obj.pos.y <= 0:
            obj.pos.y = 1
        if obj.bottom  >= SCREEN_HEIGHT:
            obj.pos.y  =  SCREEN_HEIGHT- obj.height - 1

    @staticmethod
    def is_colliding(this: GameObject, other: GameObject, ) -> bool:
        """
        Check if any two SIDES of two objects are colliding
       
        returns True if colliding
        """
      
        x_collision = (math.fabs(this.center.x - other.center.x) * 2) < (this.width + other.width) 
        y_collision = (math.fabs(this.center.y - other.center.y) * 2) < (this.height + other.height) 
        return x_collision and y_collision


    @staticmethod
    def is_intersecting(obj1: GameObject, obj2: GameObject) -> bool:
        """
        Checks if any side of first object are inside
        with the second object

        returns True if intersecting
        """
        sides = (obj1.topleft, obj1.topright, obj1.bottomleft, obj1.bottomright, obj1.center)
       
        return any((
                (obj2.left < side.x < obj2.right)
                and (obj2.top < side.y < obj2.bottom)
                
            ) for side in sides)
