import tkinter as tk
from PIL import Image, ImageTk
import os

last_clicked = None
first_click = None
is_first_click = True
image_dir = "klient/images"


def refresh_board(canvas, board_string):
    for i in range(len(board_string)):
        row = i // 4
        if row % 2 == 0:
            col = (i % 4) * 2 + 1
        else:
            col = (i % 4) * 2
        pawn_type = board_string[i]
        draw_pawn(canvas, row, col, pawn_type)


def draw_board(canvas):
    canvas.pawn_images = []
    for row in range(8):
        for col in range(8):
            color = "darkgreen" if (row + col) % 2 == 1 else "white"
            square_id = canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)
            if color == "darkgreen":
                canvas.tag_bind(square_id, "<Button-1>", lambda event, square_id=square_id: on_click(event, square_id))
            else:
                canvas.tag_bind(square_id, "<Button-1>", lambda event: reset_clicked())


def draw_pawn(canvas, row, col, pawn_type):
    if pawn_type == ".":
        return  # No image, just blank button

    color = "white" if pawn_type.lower() == "w" else "black"
    is_king = pawn_type.isupper()
    pawn_name = "king" if is_king else "pawn"
    filename = os.path.join(image_dir, f"{color}-{pawn_name}.png")

    image = Image.open(filename)
    image = image.resize((40, 40))
    pawn_image = ImageTk.PhotoImage(image)
    pawn_button = tk.Button(canvas, image=pawn_image, borderwidth=0, highlightthickness=0,
                            command=lambda row=row, col=col: on_pawn_click(row, col))
    pawn_button.image = pawn_image  # Keep a reference to prevent garbage collection
    canvas.create_window((col * 50 + 25, row * 50 + 25), window=pawn_button)
    canvas.pawn_buttons.append(pawn_button)


def on_click(event, square_id):
    global last_clicked, first_click, is_first_click
    col = event.x // 50
    row = event.y // 50
    if (row + col) % 2 == 1:  # Dark green square
        square_number = get_square_number(row, col)
        if is_first_click:
            first_click = square_number
            is_first_click = False
        else:
            # print("Clicked functional:", first_click, square_number)
            move_from_input(first_click, square_number)  # Call move_from_input function with clicked squares
            is_first_click = True
        if last_clicked:
            canvas.itemconfig(last_clicked, outline='')  # Clear previous highlighting
        canvas.itemconfig(square_id, outline='red')  # Highlight current dark green square
        last_clicked = square_id
    else:
        reset_clicked()
        # print("Clicked white")


def on_pawn_click(row, col):
    global last_clicked, first_click, is_first_click
    field_number = get_square_number(row, col)
    # print("Pawn clicked at field number:", field_number)
    reset_clicked()
    first_click = field_number
    is_first_click = False
    canvas.itemconfig(field_number, outline='red')
    last_clicked = field_number


def reset_clicked():
    global last_clicked, first_click, is_first_click
    if last_clicked:
        canvas.itemconfig(last_clicked, outline='')  # Clear previous highlighting
        last_clicked = None
        first_click = None
        is_first_click = True


def get_square_number(row, col):
    if row % 2 == 0:
        return (row * 4) + (col // 2) + 1
    else:
        return ((row - 1) * 4) + ((col - 1) // 2) + 6


def move_from_input(start, finish):
    # logic for handling the move from GUI input goes here
    print(f"Move from {start} to {finish}")


def main():
    global canvas
    root = tk.Tk()
    root.title("Checkers")

    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()
    canvas.pawn_images = []
    canvas.pawn_buttons = []

    draw_board(canvas)
    # Example: Draw pawns of different types
    # draw_pawn(canvas, 1, 0, "w")  # White pawn
    # draw_pawn(canvas, 1, 2, "b")  # Black pawn
    # draw_pawn(canvas, 2, 1, "W")  # White king
    # draw_pawn(canvas, 2, 3, "B")  # Black king

    board_string = "BBBBbbbbbbbb........wwwwwwwwWWWW"
    refresh_board(canvas, board_string)

    root.mainloop()


if __name__ == "__main__":
    main()
