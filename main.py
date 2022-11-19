from PIL import Image, ImageEnhance, ImageDraw
import math
import concurrent.futures
import time

# opening file and creating image object
file = "input/kettering logo.png"
image = Image.open(file)
# convert to black and white and save for reference
image = image.convert("L")
image.save("bw.jpg")

px = image.load()

# set output scaling factor and create blank image
scale = 8
size = (image.size[0]*scale, image.size[1]*scale)
img = Image.new("L", size, "white")
draw = ImageDraw.Draw(img)
factor = size[0]/image.size[0]


# coordinate conversion functions from corner-based to center-based
def convert_source_coords(x, y):
    x = image.size[0]/2 + x
    y = image.size[1]/2 - y
    return x, y


def convert_output_coords(x, y):
    x = size[0] / 2 + x
    y = size[1] / 2 - y
    return x, y


def draw_circle(x, y, radius, max_width=100, min_width=2):
    # determine radial detail
    detail = 2
    angle = 0
    # calculate how many sections around the circle to draw
    sections = int(6.3*radius)*detail
    print(f"Radius: {radius}")

    for i in range(1,sections):
        # initialize list of
        color_list = []
        try:
            degree = math.radians(angle)
            for j in range(int(-max_width / 2), int(max_width / 2)):
                calc_coords = convert_source_coords((math.cos(degree) * (radius + j))/scale, (math.sin(degree) * (radius + j))/scale)
                color_list.append(px[int(calc_coords[0]/1), int(calc_coords[1]/1)])
            average = 256-(sum(color_list)/len(color_list))
            #
            average = (((average*max_width)/256.0))

            for j in range(int(-average/2), math.ceil(average/2)):
                calc_coords = convert_output_coords(math.cos(degree)*(radius+j), math.sin(degree)*(radius+j))
                draw.point(calc_coords, fill="black")

            angle += 360/sections
        except IndexError:
            print("out of range")


spacing = 3
width = 20
step = width+spacing

max = int((size[0]/width)/2)

print(max*(width+spacing))

threads = 8
start_time = time.time()
for i in range(int(max/threads)):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for j in range(threads):
            executor.submit(draw_circle, 0, 0, ((i*threads)+j)*step, width)
print(f"Execution time: {time.time()-start_time}")

"""
for i in range(max):
    print(f'Progress: {round((100*i)/max,2)}%')
    #print(i*step)
    #print(i*step)

    draw_circle(0,0,i*step, width)

print(f"Execution time: {time.time()-start_time}")"""
img.save("output.png")
img.show()




#image.show()