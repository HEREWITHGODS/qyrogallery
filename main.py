from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

root = tk.Tk()

selected_folder = None
image_files = []
thumbnails = [] # сюда будем сохранять PhotoImage, чтобы они не исчезали

root.title("My galleery")
root.geometry("1280x800")
root.minsize(800, 600)

def choose_folder():
    global selected_folder

    folder_path = filedialog.askdirectory(
        title="Choose a folder with photos"
    )

    if not folder_path:
        return

    selected_folder = Path(folder_path)

    # messagebox.showinfo(
    #     title = "Folder is selected",
    #     message = f"Selected folder: {selected_folder}"
    # )
    #
    # print(f"Selected folder: {selected_folder}")
    find_button.config(state="normal")

def find_images():
    global selected_folder, image_files

    if selected_folder is None:
        messagebox.showwarning("Error", "Please select a folder!")
        return

    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff'}

    local_files = []

    #ищем все фотки во всех подпапках
    for file_path in selected_folder.rglob("*"):
        if file_path.suffix.lower() in image_extensions:
            local_files.append(file_path)

    image_files = local_files

    print("\n"+ "="*50)
    print(f"Found {len(image_files)} images")
    print("="*50)

    for i, img in enumerate(image_files[:15], 1):
        print(f"{i:2d}. {img.name}→ {img.parent.name}")

    if len(image_files) > 15:
        print(f"... and more {len(image_files)-15} images")
    show_thumbnail()

def show_thumbnail():
    global thumbnails
    thumbnails = [] # очищаем старые миниатюры

    # Очищаем предыдущее содержимое

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if not image_files:
        tk.Label(scrollable_frame, text="No images found!", font = ("Arial", 12)).pack(pady = 20)
        return

    # Размер миниатюры
    thumb_size = (300, 300)

    # Создаём сетку (4 колонки)
    columns = 6
    for index, img_path in enumerate(image_files):
        try:
            # Открываем изображение и создаём миниатюру
            img = Image.open(img_path)
            img.thumbnail(thumb_size)

            # Конвертируем в формат для Tkinter
            photo = ImageTk.PhotoImage(img)
            thumbnails.append(photo) # сохраняем, чтобы не удалилось

            # Создаём Label с картинкой
            label = tk.Label(scrollable_frame, image=photo, relief="solid", bd = 1)
            label.grid(row = index // columns, column = index % columns, padx=5, pady=5)

            # При клике на миниатюру — потом откроем большое фото
            label.bind("<Button-1>", lambda e, path=img_path: show_full_image(path))

        except Exception as e:
            print(f'Не удалось загрузить {img_path.name}: {e}')

def show_full_image(image_path):
    global current_index, full_window

    # Находим индекс текущего фото
    try:
        current_index = image_files.index(image_path)
    except ValueError:
        return

    # Создаём новое окно для просмотра
    full_window = tk.Toplevel(root)
    full_window.title("Full image")
    full_window.geometry("1000x700")
    full_window.state("zoomed")

    # Label для большой картинки
    global full_label
    full_label = tk.Label(full_window, bg="black")
    full_label.pack(fill="both", expand=True)

    # Показываем текущее фото
    show_image_in_full(current_index)

    #Привязываем клавиши
    full_window.bind("<Left>", lambda e: change_image(-1))
    full_window.bind("<Right>", lambda e: change_image(1))
    full_window.bind("<Escape>", lambda e: full_window.destroy())

    full_window.bind("<A>", lambda e: change_image(-1))
    full_window.bind("<D>", lambda e: change_image(1))

    full_window.bind("<a>", lambda e: change_image(-1))
    full_window.bind("<d>", lambda e: change_image(1))

def show_image_in_full(index):
    global full_label, current_index
    current_index = index

    if index < 0 or index >= len(image_files):
        return

    try:
        img_path = image_files[index]
        img = Image.open(img_path)

        # Подгоняем под размер окна
        img.thumbnail((1000, 700), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        full_label.config(image=photo)
        full_label.image = photo # сохраняем ссылку

        full_window.title(f'Viewed: {img_path.name} ({index+1}/{len(image_files)})')
    except Exception as e:
        print(f"Error while loading: {e}")

def change_image(direction):
    global current_index

    if not image_files:
        return

    current_index = (current_index + direction) % len(image_files)

    show_image_in_full(current_index)

top_frame = tk.Frame(root, height=60)
top_frame.pack(fill="x", padx=10, pady=5)

choose_button = tk.Button(
    top_frame,
    text="Choose a folder",
    font=("Arial", 11),
    width=20,
    height=2,
    command=choose_folder
)
choose_button.pack(side="left", padx=5)

find_button = tk.Button(
    top_frame,
    text="Find images",
    font=("Arial", 11),
    width=20,
    height=2,
    state="disabled",
    command=find_images
)
find_button.pack(side="left", padx=5)

# Создаём область с прокруткой
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Внутри main_frame будет Canvas + Scrollbar
canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()