import tkinter as tk
import random

window = tk.Tk()
window.title("Minesweeper V2 - 416aab")

ROWS = 10
COLUMNS = 10
TOP_OFFSET = 5
BASE = "      "
FREQUENCY = 5

over = False
buttons = {}
revealed = set()
flags = set()
gamemap = []

top_frame = tk.Frame(window)
top_frame.pack()

game_frame = tk.Frame(window)
game_frame.pack()


def setup_grid():
    for c in range(COLUMNS):
        window.grid_columnconfigure(c, weight=0)

    for r in range(ROWS + TOP_OFFSET):
        window.grid_rowconfigure(r, weight=0)


def make_top_button():
    global rowsin, columnsin, frequencyin, reset_btn

    rowsin = tk.Entry(top_frame, width=5)
    rowsin.insert(0, str(ROWS))
    rowsin.grid(row=0, column=0)

    columnsin = tk.Entry(top_frame, width=5)
    columnsin.insert(0, str(COLUMNS))
    columnsin.grid(row=0, column=1)

    
    frequencyin = tk.Entry(top_frame, width=5)
    frequencyin.insert(0, str(FREQUENCY))
    frequencyin.grid(row=0, column=2)

    set_btn = tk.Button(top_frame, text="set", command=setconfig)
    set_btn.grid(row=0, column=3)

    reset_btn = tk.Button(top_frame, text="🙂", command=reset)
    reset_btn.grid(row=0, column=4)


def setconfig():
    global ROWS, COLUMNS, FREQUENCY

    try:
        rows = int(rowsin.get())
        columns = int(columnsin.get())
        frequency = int(frequencyin.get())
        
    except:
        #print("invalid input")
        return

    if rows < 5:
        rows = 5
    if columns < 5:
        columns = 5
    if frequency < 1:
        frequency = 1
    if frequency > 20:
        frequency = 20
        
    FREQUENCY = frequency

    ROWS = rows
    COLUMNS = columns

    rebuild()


def rebuild():
    for btn in buttons.values():
        btn.destroy()

    buttons.clear()
    revealed.clear()
    flags.clear()

    setup_grid()
    make_buttons()
    reset()


def make_buttons():
    for r in range(ROWS):
        for c in range(COLUMNS):
            button = tk.Button(game_frame, text=BASE, width=3, height=1)
            button.grid(row=r, column=c)

            button.config(command=lambda r=r, c=c: left_click(r, c))
            button.bind("<Button-3>", lambda event, r=r, c=c: right_click(r, c))

            buttons[(r, c)] = button


def make_map():
    new_map = []

    for r in range(ROWS):
        row = []

        for c in range(COLUMNS):
            if random.randint(0, FREQUENCY) == 1:
                row.append(1)
            else:
                row.append(0)

        new_map.append(row)

    return new_map


def count_neighbors(row, column):
    count = 0

    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if r == row and c == column:
                continue

            if r >= 0 and r < ROWS and c >= 0 and c < COLUMNS:
                if gamemap[r][c] == 1:
                    count += 1

    return count


def reveal(row, column):
    if (row, column) in revealed:
        return

    if (row, column) in flags:
        return

    revealed.add((row, column))

    button = buttons[(row, column)]
    count = count_neighbors(row, column)

    if count == 0:
        button.config(text=BASE, bg="grey")

        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if r >= 0 and r < ROWS and c >= 0 and c < COLUMNS:
                    reveal(r, c)
    else:
        button.config(text="  " + str(count) + "  ", bg="grey")


def left_click(row, column):
    global over

    if over:
        return

    if (row, column) in revealed:
        return

    if (row, column) in flags:
        return

    if gamemap[row][column] == 1:
        buttons[(row, column)].config(text="  X  ", bg="red")
        #print("LOSS")
        over = True
        return

    reveal(row, column)
    check_win()


def right_click(row, column):
    if over:
        return

    if (row, column) in revealed:
        return

    button = buttons[(row, column)]

    if (row, column) in flags:
        flags.remove((row, column))
        button.config(text=BASE, bg="SystemButtonFace")
    else:
        flags.add((row, column))
        button.config(text="  F  ", bg="yellow")


def check_win():
    
    global reset_btn
    safe_tiles = 0

    for r in range(ROWS):
        for c in range(COLUMNS):
            if gamemap[r][c] == 0:
                safe_tiles += 1

    if len(revealed) == safe_tiles:
        #print("WIN")
        reset_btn.config(text="🎉")


def reset():
    global gamemap, over, reset_btn
    
    reset_btn.config(text="🙂")
    
    over = False
    revealed.clear()
    flags.clear()

    gamemap = make_map()

    for button in buttons.values():
        button.config(text=BASE, bg="SystemButtonFace")


setup_grid()
make_top_button()
make_buttons()
reset()

window.mainloop()

