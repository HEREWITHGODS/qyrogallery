import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

root = tk.Tk()

selected_folder = None

root.title("My galleery")
root.geometry("900x600")

def choose_folder():
    global selected_folder

    folder_path = filedialog.askdirectory(
        title="Choose a folder with photos"
    )

    if not folder_path:
        return

    selected_folder = Path(folder_path)

    messagebox.showinfo(
        title = "Folder is selected",
        message = f"Selected folder: {selected_folder}"
    )

    find_images()

    print(f"Selected folder: {selected_folder}")


def find_images():
    global selected_folder

    if selected_folder is None:
        messagebox.showwarning("Error", "Please select a folder!")
        return

    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff'}

    image_files = []

    #ищем все фотки во всех подпапках
    for file_path in selected_folder.rglob("*"):
        if file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)

    print("\n"+ "="*50)
    print(f"Found {len(image_files)} images")
    print("="*50)

    for i, img in enumerate(image_files[:15], 1):
        print(f"{i:2d}. {img.name}→ {img.parent.name}")

    if len(image_files) > 15:
        print(f"... and more {len(image_files)-15} images")

choose_button = tk.Button(
    root,
    text="Choose a folder",
    font=("Arial", 12),
    width=30,
    height=2,
    command=choose_folder
)
choose_button.pack(pady=200)

find_button = tk.Button(
    root,
    text="Find images",
    font=("Arial", 12),
    width=30,
    height=2,
    command=find_images
)
find_button.pack(pady=20)

root.mainloop()