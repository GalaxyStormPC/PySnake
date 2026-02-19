from tkinter import *
import random
from tkinter import messagebox, colorchooser

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 90
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

def new_game():
    global snake, food, direction, score
    canvas.delete(ALL)
    direction = "down"
    score = 0
    lbl.config(text='Score: {}'.format(score))
    snake = Snake()
    food = Food()
    next_turn(snake, food)

def exit_game():
    window.destroy()

def show_settings():
    def choose_snake_color():
        nonlocal snake_color
        color = colorchooser.askcolor(title="Choose Snake Color")
        if color[1]:
            snake_color = color[1]
            color_lbl.config(text=snake_color, bg=snake_color)

    settings_win = Toplevel(window)
    settings_win.title("Settings")
    settings_win.geometry("300x300")

    snake_color = SNAKE_COLOR

    speed_var = IntVar(value=SPEED)
    space_var = IntVar(value=SPACE_SIZE)
    parts_var = IntVar(value=BODY_PARTS)

    Label(settings_win, text="Speed of snake (delay in ms)").pack()
    Entry(settings_win, textvariable=speed_var).pack()

    Label(settings_win, text="Size of space").pack()
    Entry(settings_win, textvariable=space_var).pack()

    Label(settings_win, text="Initial snake size").pack()
    Entry(settings_win, textvariable=parts_var).pack()

    Label(settings_win, text="Snake color").pack()
    Button(settings_win, text="Choose color", command=choose_snake_color).pack()
    color_lbl = Label(settings_win, text=snake_color, bg=snake_color, fg="white")
    color_lbl.pack(pady=5)

    def save_settings():
        global SPEED, SPACE_SIZE, BODY_PARTS, SNAKE_COLOR
        SPEED = speed_var.get()
        SPACE_SIZE = space_var.get()
        BODY_PARTS = parts_var.get()
        SNAKE_COLOR = snake_color
        messagebox.showinfo("Saved", "Settings are saved. Restart the game.")
        settings_win.destroy()

    Button(settings_win, text="Save settings", command=save_settings).pack(pady=10)

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, -i * SPACE_SIZE])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        lbl.config(text='Score: {}'.format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=("JetBrains Mono", 60), text="GAME OVER!", fill="red", tag="gameover")

window = Tk()
window.title("Python Snake")
window.resizable(False, False)

menubar = Menu(window)
window.config(menu=menubar)

main_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Main", menu=main_menu)
main_menu.add_command(label="New game", command=new_game)
main_menu.add_command(label="Exit game", command=exit_game)

settings_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Open settings", command=show_settings)

score = 0
direction = "down"

lbl = Label(window, text="Score: {}".format(score), font=("JetBrains Mono", 24))
lbl.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y-50}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()