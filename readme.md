# Colliding Rects Game 

## How to Run
install dependencies with `pip install -r requirements.txt`

run with `python main.py`

## How to Play

Drag Left Mouse Button to create a rect

Drag Right Mouse Button to launch a rect

R - to destroy all rects

## Settings

### Game related settings

__LAUNCH_MULTIPLIER__ = 2 - multiplier for the RMB launch speed

__MINIMUM_NEW_OBJECT_MASS__ - mass (product of x and y) of a new rect cannot be less than this

__SCREEN_WIDTH__  - width of the screen in pixels

__SCREEN_HEIGHT__ - height of the screen in pixels

__FPS__ - frames per second (movement speed not affected by this)

__SPEED_THRESHOLD__ - the speed at which the movement stops

### Other settings

__DEBUG__ - will show you the debug info when set to True. Showing total frame time, time to calculate collisions and time to update the screen. As well as speed and mass of each rect.

__SHOW_FPS__ - will show you the fps when set to True

__FPS_BUFFER_SIZE__  - number of frames to average the fps over 

__DEBUG_FONT_SIZE__ - font size for the debug info

__DEBUG_FONT_SIZE_2__ - font size for the debug info displayed on a rects





