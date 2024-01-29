import tkinter as tk
from tkinter import PhotoImage


def wyjdz(root):
    print("Bye!")
    root.destroy()


def refresh(root, pozycja):
    print("REFRESHING...")

    if len(pozycja) != 32:
        print("BŁĄD W DŁUGOŚCI ODCZYTANEJ POZYCJI!")

    pozycja = pozycja[::-1]

    # Load the image
    image_path = "../images/red-pawn.png"
    img = PhotoImage(file=image_path)

    image_path2 = "../images/black-pawn.png"
    img2 = PhotoImage(file=image_path2)

    image_path = "../images/black-king.png"
    img_2d = PhotoImage(file=image_path)

    image_path = "../images/red-king.png"
    img_d = PhotoImage(file=image_path)

    # Pozycja, ale już w 8. stringach
    poz = []
    for row in range(8):
        if row % 2 == 1:
            pom = pozycja[0] + "o" + pozycja[1] + "o" + pozycja[2] + "o" + pozycja[3] + "o"
        else:
            pom = "o" + pozycja[0] + "o" + pozycja[1] + "o" + pozycja[2] + "o" + pozycja[3]
        pozycja = pozycja[4::]
        poz.append(pom)

    # print(poz)

        # Load the image
        image_path = "../images/red-pawn.png"  # Replace with the actual path to your .png file
        img = PhotoImage(file=image_path)

        image_path2 = "../images/black-pawn.png"  # Replace with the actual path to your .png file
        img2 = PhotoImage(file=image_path2)

        image_path = "../images/black-king.png"  # Replace with the actual path to your .png file
        img_2d = PhotoImage(file=image_path)

        image_path = "../images/red-king.png"  # Replace with the actual path to your .png file
        img_d = PhotoImage(file=image_path)


    for row in range(8):
        for col in range(8):
            # print("inloop", row, col )
            if poz[row][col] == 'c':
                button_array[row][col].config(image=img2, width=70, height=70)
            elif poz[row][col] == 'b':
                button_array[row][col].config(image=img, width=70, height=70)
            elif poz[row][col] == 'C':
                button_array[row][col].config(image=img_2d, width=70, height=70)
            elif poz[row][col] == 'B':
                button_array[row][col].config(image=img_d, width=70, height=70)
            elif poz[row][col] == 'o':
                button_array[row][col].config(image="")

    print("REFRESHED!")


def send():
    print("Move sent!")


def button_click(row, col):
    print(f"Button clicked: Row {row}, Column {col}")


def play():
    print("Szukaj gracza > rozmawiaj z serwerem")


def create_start_gui():
    pass


def create_gui():
    global root
    root = tk.Tk()
    root.title("Kocie_Warcaby - klient")
    global button_array
    button_array = [[tk.Button(root, width=10, height=4, command=lambda r=row, c=col: button_click(r, c))
                     for col in range(8)] for row in range(8)]

    # Title above the buttons
    title_label = tk.Label(root, text="Warcaby :D", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8, pady=10)

    # Load the image
    image_path = "../images/red-pawn.png"  # Replace with the actual path to your .png file
    img = PhotoImage(file=image_path)

    image_path2 = "black-pawn.png"  # Replace with the actual path to your .png file
    img2 = PhotoImage(file=image_path2)

    image_path = "../images/black-king.png"  # Replace with the actual path to your .png file
    img_2d = PhotoImage(file=image_path)

    image_path = "../images/red-king.png"  # Replace with the actual path to your .png file
    img_d = PhotoImage(file=image_path)

    for row in range(8):
        for col in range(8):
            color = "khaki" if (row + col) % 2 == 0 else "green"
            button_array[row][col].config(bg=color)
            button_array[row][col].grid(row=row + 1, column=col, padx=2, pady=2)

    pozycja = "ccccccbbccccoooooooobbbbbccbbbbb"
    # refresh(pozycja)

    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                button_array[row][col].config(image=img2, width=70, height=70)
            else:
                button_array[7 - row][col].config(image=img, width=70, height=70)

    # Additional buttons on the right side
    button1 = tk.Button(root, text="Refresh", width=10, height=2, command=lambda: refresh(root, pozycja))
    button1.grid(row=1, column=8, padx=10, pady=2)

    button2 = tk.Button(root, text="EXIT", width=10, height=2, command=lambda: wyjdz(root))
    button2.grid(row=2, column=8, padx=10, pady=2)

    button3 = tk.Button(root, text="Confirm move", width=10, height=2, command=lambda: send())
    button3.grid(row=3, column=8, padx=10, pady=2)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
