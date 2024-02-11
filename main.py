import colorsys
import pygame as pg
from random import randint
from time import perf_counter_ns
from typing import Optional, Never, NoReturn
from random import choice, randint
from itertools import combinations, product
from decouple import config
from GameObject import GameObject
from Physics import Physics
import math


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = config("SCREEN_WIDTH", default=800, cast=int)
SCREEN_HEIGHT = config("SCREEN_HEIGHT", default=600, cast=int)
FPS = config("FPS", default=60, cast=int)
MINIMUM_NEW_OBJECT_MASS = config("MINIMUM_NEW_OBJECT_MASS", default=800, cast=int)
FPS_BUFFER_SIZE = config("FPS_BUFFER_SIZE", default=5, cast=int)
DEBUG_FONT_SIZE = config("DEBUG_FONT_SIZE", default=15, cast=int)
DEBUG = config("DEBUG", default=False, cast=bool)
LAUNCH_MULTIPLIER = config("LAUNCH_MULTIPLIER", default=1, cast=float)
SHOW_FPS = config("SHOW_FPS", default=True, cast=bool)


def line_intersection_on_rect(obj:GameObject , pos:tuple[float,float]) -> tuple[float,float]:
    xB, yB = obj.center.toTuple()
    w = obj.width / 2
    h = obj.height / 2

    xA,yA = pos
    dx = xA - xB
    dy = yA - yB

    if dx == 0 or dy == 0:
        return (xB, yB)

    tan_phi = h / w
    tan_theta = abs(dy / dx)
   
    qx = int(math.copysign(1, dx))
    qy = int(math.copysign(1, dy))

    if tan_theta > tan_phi:
        xI = xB + (h / tan_theta) * qx
        yI = yB + h * qy
    else:
        xI = xB + w * qx
        yI = yB + w * tan_theta * qy

    return (xI, yI)




def get_random_color(*args:Never, **kwargs:Never)-> pg.Color:
    color_hue = randint(0, 100) / 100
    rgb_color_as_float = colorsys.hsv_to_rgb(color_hue, 0.95, 0.95)
    rgb_color = [int(rgb_color_as_float[i] * 255) for i in range(3)]
    return pg.Color(*rgb_color)

def reverse_color(color:pg.Color) -> pg.Color:  
    rgb = color[:3]
    color_hue = abs(colorsys.rgb_to_hsv(*rgb) [0] - 1) #type:ignore
    rgb_color_as_float = colorsys.hsv_to_rgb(color_hue, 0.95, 0.95)
    rgb_color = [int(rgb_color_as_float[i] * 255) for i in range(3)]
    return pg.Color(*rgb_color)


def main(*args:Never, **kwargs:Never):
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("My Game")
    clock = pg.time.Clock()
    font = pg.font.Font(None, DEBUG_FONT_SIZE)

    running = True

    fps_index = 0
    fps_list = [FPS for _ in range(FPS_BUFFER_SIZE)]

    game_objects: list[GameObject] = []

    a = GameObject(x=400, y=400, height=100, width=100, color=pg.Color(RED))
    a.speed.x = 77
    a.speed.y = -88
    a.mass_mul = 1
    game_objects.append(a)

    channeling_new_obj = False
    initial_mouse_pos = (0, 0)
    new_obj_color = get_random_color()

    channeling_launch = False
    selected_obj: GameObject = None  # type:ignore

    while running:
        screen.fill(BLACK)
        frame_start = perf_counter_ns()
        # print(channeling_new_obj,channeling_launch)
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == 114:
                game_objects = []

            if (
                event.type == pg.MOUSEBUTTONDOWN
                and pg.mouse.get_pressed()[0] == 1
                and not channeling_launch
            ):
                channeling_new_obj = True
                initial_mouse_pos = pg.mouse.get_pos()
                new_obj_color = get_random_color()

            if (
                event.type == pg.MOUSEBUTTONDOWN
                and pg.mouse.get_pressed()[2] == 1
                and not channeling_new_obj
                and not channeling_launch
            ):
                channeling_launch = True
                initial_mouse_pos = pg.mouse.get_pos()
                temp_obj = GameObject(
                    x=initial_mouse_pos[0],
                    y=initial_mouse_pos[1],
                )
                selected_obj = next(
                    (a for a in game_objects if Physics.is_intersecting(temp_obj, a)),
                    None,  # type:ignore
                )
                if not selected_obj:
                    channeling_launch = False

            if (
                event.type == pg.MOUSEBUTTONUP
                and pg.mouse.get_pressed()[2] == 0
                and channeling_launch
            ):
                channeling_launch = False
                if selected_obj:
                    selected_obj.speed.x = (
                        selected_obj.center.x - pg.mouse.get_pos()[0]
                    ) * LAUNCH_MULTIPLIER
                    selected_obj.speed.y = (
                        selected_obj.center.y - pg.mouse.get_pos()[1]
                    ) * LAUNCH_MULTIPLIER

            if (
                event.type == pg.MOUSEBUTTONUP
                and pg.mouse.get_pressed()[0] == 0
                and channeling_new_obj
            ):
                channeling_new_obj = False

                x = initial_mouse_pos[0] - abs(
                    (pg.mouse.get_pos()[0] - initial_mouse_pos[0])
                )

                y = initial_mouse_pos[1] - abs(
                    (pg.mouse.get_pos()[1] - initial_mouse_pos[1])
                )

                width = abs(initial_mouse_pos[0] - pg.mouse.get_pos()[0]) * 2
                height = abs(initial_mouse_pos[1] - pg.mouse.get_pos()[1]) * 2

                is_x_within_borders = 0 < x < SCREEN_WIDTH
                is_y_within_borders = 0 < y < SCREEN_HEIGHT
                is_width_within_borders = 0 < x + width < SCREEN_WIDTH
                is_height_within_borders = 0 < y + height < SCREEN_HEIGHT

                if (
                    is_x_within_borders
                    and is_y_within_borders
                    and is_width_within_borders
                    and is_height_within_borders
                ):
                    tempa = GameObject(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        color=new_obj_color,
                    )
                    is_colliding_with_others = any(
                        [Physics.is_intersecting(tempa, a) for a in game_objects]
                    )
                    if (
                        not is_colliding_with_others
                        and tempa.mass > MINIMUM_NEW_OBJECT_MASS
                    ):
                        
                        game_objects.append(tempa)

          

        # ----------------- collision between gameobjects
        coll_start = perf_counter_ns()
        [game_object.update(FPS) for game_object in game_objects]

        for a, b in combinations(game_objects, 2):
            if Physics.is_colliding(a, b):
                Physics.collide(a, b)

        # ----------------- collision between walls

        for a in game_objects:
            if a.left <= 0 or a.right >= SCREEN_WIDTH:
                Physics.collideWallX(a)
            if a.top <= 0 or a.bottom >= SCREEN_HEIGHT:
                Physics.collideWallY(a)

        coll_end = perf_counter_ns()

        coll_ms = (coll_end - coll_start) // 100_000 / 10
        # ----------------- drawing gameobjects
        draw_start = perf_counter_ns()
        [game_object.draw(screen) for game_object in game_objects]
        if DEBUG:
            [
                game_object.debugDraw(
                    screen,
                    game_object.speed.x,
                    game_object.speed.y,
                    game_object.mass / 1000,
                )
                for game_object in game_objects
            ]
        # ----------------- drawing new rect
        if channeling_new_obj:
            pg.draw.rect(
                screen,
                new_obj_color,
                (
                    initial_mouse_pos[0]
                    - abs((pg.mouse.get_pos()[0] - initial_mouse_pos[0])),
                    initial_mouse_pos[1]
                    - abs((pg.mouse.get_pos()[1] - initial_mouse_pos[1])),
                    abs(initial_mouse_pos[0] - pg.mouse.get_pos()[0]) * 2,
                    abs(initial_mouse_pos[1] - pg.mouse.get_pos()[1]) * 2,
                ),
            )
        # ----------------- drawing channeling_launch line
        if channeling_launch and selected_obj:

            denominator = pg.mouse.get_pos()[0] - selected_obj.center.x
            pg.draw.line(
                screen,
                selected_obj.color,
                selected_obj.center.toTuple(),
                pg.mouse.get_pos(),
                7,
            )
            if denominator != 0:
                slope = (pg.mouse.get_pos()[1] - selected_obj.center.y) / denominator
                
            else:
                slope = 0.01

            x_intersection , y_intersection = line_intersection_on_rect(selected_obj,pg.mouse.get_pos())

            pg.draw.line(
                screen,
                pg.Color(reverse_color(selected_obj.color)),
                selected_obj.center.toTuple(),
                (x_intersection, y_intersection),
                7,
            )

        draw_end = perf_counter_ns()
        draw_ms = (draw_end - draw_start) // 100_000 / 10

        # ----------------- fps measurement
        fps_index += 1
        if fps_index == FPS_BUFFER_SIZE:
            fps_index = 0
        fps_list[fps_index] = clock.get_fps()
        fps = sum(fps_list) / FPS_BUFFER_SIZE

        # ----------------- performance stats
        if DEBUG or SHOW_FPS:
            text = font.render(f"FPS: {fps:.1f}", True, WHITE)
            screen.blit(text, (10, 10))
        if DEBUG:
            frame_end = perf_counter_ns()
            frame_time_ms = (frame_end - frame_start) // 100_000 / 10
            text = font.render(
                f"{frame_time_ms=}  {coll_ms=}   {draw_ms=}", True, WHITE
            )
            screen.blit(text, (10, 40))

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
