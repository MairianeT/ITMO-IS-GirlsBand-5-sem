from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import numpy as np

from Func import *
from ColorSpaces import *
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def show_picture():
    global files_name
    global start_label
    global pixels
    try:
        image = Image.open(files_name)
        w = image.size[0]
        h = image.size[1]
        h_final = int((window.winfo_height()))
        img = ImageTk.PhotoImage(image.resize((int(h_final*w/h), h_final)))
        disp_img.config(image=img)
        disp_img.image = img
        start_label.destroy()
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except AttributeError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except Exception:
        messagebox.showerror("Ошибка", "Неверный формат файла")

def save_png_picture():
    global files_name
    try:
        h, f, k = read(files_name)
        convert(f, files_name[:len(files_name) - 4] + "_new")
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не найден")

def save_pnm_picture():
    global files_name
    try:
        h, f, k = read(files_name)
        write(files_name[:len(files_name) - 4] + "_new.pnm", f, k)
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не найден")

def save_as_picture(comboExample, new_files_name):
    global files_name
    try:
        h, f, k = read(files_name)
        if (comboExample.get() == ".png"):
            if (new_files_name.get() == ""):
                save_png_picture()
            else:
                convert(f, new_files_name.get())
        if (comboExample.get() == ".pnm"):
            if (new_files_name.get() == ""):
                save_pnm_picture()
            else:
                write(new_files_name.get() + ".pnm", f, k)
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не может быть создан")

def browse_files():
    global files_name
    filename = filedialog.askopenfilename(initialdir="/",
        title="Select a File",
        filetypes=(("PNM files", "*.pnm*"), ("PPM files", "*.ppm*"), ("PGM files", "*.pgm*"), ("all files", "*.*")))
    files_name = filename

def on_closing():
    window.destroy()

def open():
    global pixels
    browse_files()
    show_picture()
    pixels = read(files_name)[1]

def save_as():
    newWindow = Toplevel(window)
    newWindow.title("Сохранить как")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text = "Название файла: ")
    labelTop.grid(row=1, column=1)
    new_files_name = Entry(
        newFrame,
    )
    new_files_name.grid(row=1, column=2)
    labelTop = Label(newFrame, text = "Формат: ")
    labelTop.grid(row=1, column=3)
    comboExample = ttk.Combobox(newFrame, values=[".png", ".pnm"])
    comboExample.grid(row=1, column=4)
    save_as_btn = Button(
        newFrame,
        text='Cохранить',
        command=lambda: save_as_picture(comboExample, new_files_name)
    )
    save_as_btn.grid(row=1, column=5)

def save_as_canal(chanal):
    newWindow = Toplevel(window)
    newWindow.title("Сохранить отдкльный канал")
    newWindow.geometry('300x100')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text = "Название файла: ")
    labelTop.grid(row=1, column=1)
    new_files_name = Entry(
        newFrame,
    )
    new_files_name.grid(row=1, column=2)
    labelTop = Label(newFrame, text = "Формат: ")
    labelTop.grid(row=1, column=3)
    comboExample = ttk.Combobox(newFrame, values=[".png", ".pnm"])
    comboExample.grid(row=1, column=4)
    save_as_btn = Button(
        newFrame,
        text='Cохранить',
        command=lambda: save_as_picture(comboExample, new_files_name)
    )
    save_as_btn.grid(row=1, column=5)

def clean_picture():
    global start_label
    global files_name
    disp_img.config(image='')
    disp_img.image = ''
    files_name = ""
    start_label = Label(frame, text = "Для начала работы выберите изображение (Файл - Открыть)")
    start_label.grid(row=1, column=1)


def change_space(new_space):
    global pixels
    global current_space
    if new_space[0] != current_space[0]:
        if current_space[0] != "RGB":
            pixels = to_RGB(current_space[0], pixels)
            if new_space[0] != "RGB":
                pixels = from_RGB(new_space[0], pixels)
        else:
            pixels = from_RGB(new_space[0], pixels)
        current_space = new_space
    if current_space[0] != "RGB":
        pixels_to_show = to_RGB(current_space[0], pixels)
    else:
        pixels_to_show = pixels

    canals.delete(0, 3)
    canals.add_command(label=current_space[0], command=lambda: change_canal(0))
    canals.add_command(label=current_space[1], command=lambda: change_canal(1))
    canals.add_command(label=current_space[2], command=lambda: change_canal(2))
    canals.add_command(label=current_space[3], command=lambda: change_canal(3))
    plt.imshow(pixels_to_show.astype('uint8'))
    plt.show()

def change_canal(index):
    global current_space
    global pixels
    if (index == 0):
        pixels_to_show = pixels
    else:
        pixels_to_show = np.zeros((len(pixels[0]), len(pixels[0]), 3), dtype="float32")
        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                for k in range(3):
                    if k + 1 == index:
                        pixels_to_show[i, j][k] = pixels[i, j][k]

        if current_space[0] != "RGB":
            pixels_to_show = to_RGB(current_space[0], pixels_to_show)

    plt.imshow(pixels_to_show.astype('uint8'))
    plt.show()



window = Tk()
window.title('Графическое приложение')
window.geometry('800x600')
window.option_add("*tearOff", FALSE)
main_menu = Menu()
current_space = ["RGB", "R", "G", "B"]

file_menu = Menu()
file_menu.add_command(label="Открыть", command=open)
file_menu.add_command(label="Сохранить как", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Очистить", command=clean_picture)

color_spaces = Menu()
color_spaces.add_command(label="RGB", command=lambda: change_space(["RGB", "R", "G", "B"]))
color_spaces.add_command(label="HSL", command=lambda: change_space(["HSL", "H", "S", "L"]))
color_spaces.add_command(label="HSV", command=lambda: change_space(["HSV", "H", "S", "V"]))
color_spaces.add_command(label="YCbCr601", command=lambda: change_space(["YCbCr601", "Y", "Cb", "Cr"]))
color_spaces.add_command(label="YCbCr709", command=lambda: change_space(["YCbCr709", "Y", "Cb", "Cr"]))
color_spaces.add_command(label="TCoCg", command=lambda: change_space(["TCoCg", "T", "Co", "Cg"]))
color_spaces.add_command(label="CMY", command=lambda: change_space(["CMY", "C", "M", "Y"]))

canals = Menu()
canals.add_command(label=current_space[0], command=lambda: change_canal(0))
canals.add_command(label=current_space[1], command=lambda: change_canal(1))
canals.add_command(label=current_space[2], command=lambda: change_canal(2))
canals.add_command(label=current_space[3], command=lambda: change_canal(3))

change_menu = Menu()
change_menu.add_cascade(label="Цветовое пространство", menu=color_spaces)
change_menu.add_cascade(label="Каналы", menu=canals)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Изменить", menu=change_menu)

frame = Frame(
    window,
    padx=10,
    pady=10
)
frame.pack(expand=True)

files_name = ""

start_label = Label(frame, text="Для начала работы выберите изображение (Файл - Открыть)")
start_label.grid(row=1, column=1)

disp_img = Label()
disp_img.pack()

window.config(menu=main_menu)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()