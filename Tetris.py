from tkinter import *
from tkinter import messagebox
from random import choice, randrange
from copy import deepcopy
фвлв import time
import pygame


W, H = 10, 20
TILE = 35
GAME_RES = W * TILE, H * TILE
RES = 1200, 800
FPS = 10

pygame.mixer.init()
pygame.mixer.music.load("C:/Program Files (x86)/tetris/sound.mp3")
pygame.mixer.music.play(-1) 



def on_closing():
    global app_running
    if messagebox.askokcancel("Exiting the application", "Do you want to exit the application?"):
        app_running = False
       


tk = Tk()
app_running = True
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Tetris")   
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)


sc = Canvas(tk, width=RES[0], height=RES[1], bg="black", highlightthickness=0)
sc.pack()



def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
        return "0"
    


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))
        


game_sc = Canvas(tk, width=W*TILE+1, height=H*TILE+1, bg="yellow", highlightthickness=0)
game_sc.place(x=20, y=20, anchor=NW)


img_obj1 = PhotoImage(file="C:/Program Files (x86)/tetris/bg.png")
sc.create_image(0, 0, anchor=NW, image=img_obj1)


img_obj2 = PhotoImage(file="C:/Program Files (x86)/tetris/img2.png")
game_sc.create_image(0, 0, anchor=NW, image=img_obj2)


grid = [game_sc.create_rectangle(x * TILE, y * TILE, x * TILE+TILE, y * TILE+TILE) for x in range(W) for y in range(H)]


figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


figures = [[[x + W // 2, y + 1, 1, 1] for x, y in fig_pos] for fig_pos in figures_pos]

field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000


score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
record = "0"

sc.create_text(400, 30,text="Atsasaki Huyse", font=("Bicubik", 55),fill="red", anchor=NW)
sc.create_text(400, 360,text="your score:", font=("Bicubik", 35),fill="red", anchor=NW)
_score = sc.create_text(773, 360,text=str(score), font=("Bicubik", 35),fill="white", anchor=NW)
sc.create_text(400, 430,text="record:", font=("Bicubik", 35),fill="red", anchor=NW)
_record = sc.create_text(640, 430,text=record, font=("Bicubik", 35),fill="white", anchor=NW)


get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))


figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

color, next_color = get_color(), get_color()


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb




def check_borders():
    if figure[i][0] < 0 or figure[i][0] > W - 1:
        return False
    elif figure[i][1] > H - 1 or field[figure[i][1]][figure[i][0]]:
        return False
    return True
def move_obj(event):
    global rotate, anim_limit, dx
    if event.keysym == 'Up':
        rotate = True
    elif event.keysym == 'Down':
        anim_limit = 100
    elif event.keysym == 'Left':
        dx = -1
    elif event.keysym == 'Right':
        dx = 1
game_sc.bind_all("<KeyPress-Up>",move_obj)
game_sc.bind_all("<KeyPress-Down>",move_obj)
game_sc.bind_all("<KeyPress-Left>",move_obj)
game_sc.bind_all("<KeyPress-Right>",move_obj)
dx, rotate = 0, False
while app_running:
    if app_running:
        record = get_record()
        
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i][0] += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i][1] += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i][1]][figure_old[i][0]] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i][1] - center[1]
                y = figure[i][0] - center[0]
                figure[i][0] = center[0] - x
                figure[i][1] = center[1] + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        
        score += scores[lines]

        fig = []
        
        for i in range(4):
            figure_rect_x = figure[i][0] * TILE
            figure_rect_y = figure[i][1] * TILE
            fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE, fill=rgb_to_hex(color)))


        
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect_x, figure_rect_y = x * TILE, y * TILE
                    fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE,
                                                        figure_rect_y + TILE, fill=rgb_to_hex(col)))

        fig2 = []
        
        for i in range(4):
            figure_rect_x = next_figure[i][0] * TILE + 348
            figure_rect_y = next_figure[i][1] * TILE + 185
            fig2.append(sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE,
                                            fill=rgb_to_hex(next_color)))
        
        sc.itemconfigure(_score, text=str(score))
        sc.itemconfigure(_record, text=record)

        
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                
                for item in grid:
                    game_sc.itemconfigure(item, fill=rgb_to_hex(get_color()))
                    time.sleep(0.005)
                    tk.update_idletasks()
                    tk.update()
                
                for item in grid:
                    game_sc.itemconfigure(item, fill="")
        dx, rotate = 0, False
        tk.update_idletasks()
        tk.update()
        for id_fig in fig: game_sc.delete(id_fig)
        for id_fig in fig2: sc.delete(id_fig)
    time.sleep(0.005)

tk.destroy()
