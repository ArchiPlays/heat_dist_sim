import tkinter as tk
import numpy as np

from integral_functions import compute_linear_integral

num_splits = 100
infty_prec = 50
length = 10
diffusivity = 0.1
visual_length = 500

max_temp = 15
min_temp = 0

time_per_change = 0.1
time_elapsed_in_seconds = 0

bar_part_length = visual_length // num_splits

z = np.zeros(num_splits)

def k(x):
    if 0.33 * length < x < 0.66 * length:
        return 10
    return 15

def get_temp_at_l_from_splits(z, l):
    return z[int(l * (num_splits / length))]

def get_x_from_split(split):
    return split * (length / num_splits)

def sum_internal(n, x, t):
    return (n * np.sin(n * np.pi * x / length) * np.exp(-diffusivity * (n * np.pi / length) ** 2 * t)) / (2 * n * np.pi - np.sin(2 * n * np.pi)) * compute_linear_integral(length, n, 2, 1)

def compute_at_x(x, t):
    return (4* np.pi / length) * np.sum([sum_internal(n, x, t) for n in range(1, infty_prec)])

def compute_z(t):
    global z
    z = np.array([compute_at_x(get_x_from_split(i), t) for i in range(num_splits)])
    
    # write z to a new line in a file
    with open("data.txt", "a") as f:
        f.write(" ".join([str(i) for i in z]) + "\n")
    
def compute_color(temp):
    # blue is min_temp, red is max_temp, middle is white
    if temp < min_temp:
        return "#0000FF"
    if temp > max_temp:
        return "#FF0000"
    
    # between (min_temp and (min_temp + max_temp) / 2), 0000FF is at min_temp, FFFFFF is at (min_temp + max_temp) / 2
    # between ((min_temp + max_temp) / 2 and max_temp), FFFFFF is at (min_temp + max_temp) / 2, FF0000 is at max_temp
    
    if temp < (min_temp + max_temp) / 2:
        return "#{:02X}{:02X}FF".format(int(255 * (temp - min_temp) / ((min_temp + max_temp) / 2 - min_temp)), int(255 * (temp - min_temp) / ((min_temp + max_temp) / 2 - min_temp)))
    return "#FF{:02X}{:02X}".format(int(255 * (1 - (temp - (min_temp + max_temp) / 2) / (max_temp - (min_temp + max_temp) / 2))), int(255 * (1 - (temp - (min_temp + max_temp) / 2) / (max_temp - (min_temp + max_temp) / 2))))

def increment_time():
    global time_elapsed_in_seconds
    time_elapsed_in_seconds += time_per_change

def draw_bar(canvas: tk.Canvas, root: tk.Tk, T: tk.Text):
    compute_z(time_elapsed_in_seconds)
    
    for i in range(num_splits):
        color = compute_color(z[i])
        canvas.create_rectangle(i * bar_part_length, 0, (i + 1) * bar_part_length, 50, fill=color, outline=color)
    
    increment_time()
    canvas.itemconfigure(T, text="Time: {}s".format(round(time_elapsed_in_seconds, 3)))

    root.after(int(time_per_change * 1000), lambda: draw_bar(canvas, root, T))

def start():
    root = tk.Tk()
    root.title("HDistSim")
    root.geometry("500x120")

    canvas = tk.Canvas(root, width=visual_length, height=0.7 * visual_length)
    canvas.pack()
    
    # draw a rectangle with temperature color legend
    for i in range(visual_length):
        color = compute_color(min_temp + (max_temp - min_temp) * i / visual_length)
        canvas.create_rectangle(i, 65, i + 1, 75, fill=color, outline=color)
    
    # draw min and max temperature text
    canvas.create_text(10, 90, text=str(min_temp))
    canvas.create_text(visual_length - 10, 90, text=str(max_temp))
    
    # display elapsed time
    T = canvas.create_text(35, 110, text="Time: 0s")
    
    canvas.create_text(visual_length // 2, 90, text="Temperature")
        
    draw_bar(canvas, root, T)

    root.mainloop() 

start()
