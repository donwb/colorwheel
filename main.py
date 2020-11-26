import time
from phue import Bridge

def rgb_to_xy(red, green, blue):
 
    # gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

    # convert rgb to xyz
    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    # convert xyz to xy
    x = x / (x + y + z)
    y = y / (x + y + z)

    # TODO check color gamut if known
     
    return [x, y]

# this is the rotating position on the color wheel
# based on the "primary" color 
# the primary is the one on the tree
def color_position(idx):
    color_array = []
    if idx == 0:
        color_array = [0, 1, 2, 3]
    elif idx == 1:
        color_array = [1, 2, 3, 0]
    elif idx == 2:
        color_array = [2, 3, 0, 1]
    else:
        color_array = [3, 0, 1, 2]
    
    return color_array

# this will change all the lights at one time
# the idx is the primary dcolor on the tree
def change_light(lights, colors, idx):
    c_array = color_position(idx)
    color_count = 0
    
    for l in lights:
        l.xy = colors[c_array[color_count]]
        color_count+=1

sleep_time = 5

b = Bridge('192.168.1.16')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()
b.get_api()

# red, gree, yellow, blue
r_xy = rgb_to_xy(1.0, 0, 0)
g_xy = rgb_to_xy(0, 1.0, 0)
y_xy = rgb_to_xy(1.0, 0.45, 0)
b_xy = rgb_to_xy(0, 0, 1.0)

colors = [r_xy, g_xy, y_xy, b_xy]

# lights
light_names = b.get_light_objects('name')
fan2 = light_names['Fan 2']
fan1 = light_names['Fan 1']
desk = light_names['Desk lamp']
sixties = light_names['60s lamp']
office_lights = [fan2, fan1, sixties, desk]


# Turn on all the lights
for l in office_lights:
    l.on = True
    if l.name == 'Fan 2':
        l.brightness = 254
    else:
        l.brightness = 127
    
    
time.sleep(3)

count = 0
while(True):
    print('Light change! primary is: ', count)

    change_light(office_lights, colors, count)
    time.sleep(sleep_time)

    if count < 3:
        count+=1
    else:
        count = 0
    

# will never get here lol
print('done!')

