import tkinter as tk
from tkinter import PhotoImage

def button_click(row, col):
    print(f"Button clicked: Row {row}, Column {col}")

def additional_button_click(button_name):
    print(f"Additional button clicked: {button_name}")

def create_gui():
    root = tk.Tk()
    root.title("8x8 Button Array")

    # Title above the buttons
    title_label = tk.Label(root, text="Rzucanie szablą :D", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8, pady=10)

    # Load the image
    image_path = "../images/red-pawn.png"  # Replace with the actual path to your .png file
    img = PhotoImage(file=image_path)
    img = img.subsample(3, 3)

    button_array = [[tk.Button(root, width=5, height=2, command=lambda r=row, c=col: button_click(r, c))
                     for col in range(8)] for row in range(8)]

    for row in range(8):
        for col in range(8):
            color = "yellow" if (row + col) % 2 == 0 else "green"
            button_array[row][col].config(bg=color)
            button_array[row][col].grid(row=row + 1, column=col, padx=2, pady=2)

    # Attach the image to the middle two buttons in the top and bottom rows
    button_array[1][3].config(image=img, compound=tk.TOP, command=lambda: button_click(1, 3))
    button_array[1][4].config(image=img, compound=tk.TOP, command=lambda: button_click(1, 4))
    button_array[6][3].config(image=img, compound=tk.TOP, command=lambda: button_click(6, 3))
    button_array[6][4].config(image=img, compound=tk.TOP, command=lambda: button_click(6, 4))

    # Additional buttons at the right side
    button1 = tk.Button(root, text="Refresh", width=10, height=2, command=lambda: additional_button_click("Button 1"))
    button1.grid(row=1, column=8, padx=10, pady=2)

    button2 = tk.Button(root, text="Exit", width=10, height=2, command=lambda: additional_button_click("Button 2"))
    button2.grid(row=2, column=8, padx=10, pady=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()




    button_array[7][0].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[7][2].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[7][4].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[7][6].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[6][1].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[6][3].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[6][5].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[6][7].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[5][0].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[5][2].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[5][4].config(image=img, compound=tk.TOP, width=70, height=70)
    button_array[5][6].config(image=img, compound=tk.TOP, width=70, height=70)
