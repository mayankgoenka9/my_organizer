import os
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox


def select_folder():
    try:
        filename = filedialog.askdirectory()
        folder_path = StringVar()
        folder_path.set(filename)
        current_path = folder_path.get()
        path_var = StringVar()
        os.chdir(current_path)
        path_var.set("Folder selected :" + current_path)
        root.geometry('500x200')
        selected_folder_label = Label(root, textvariable=path_var, relief="solid")
        selected_folder_label.grid(row=0, column=0, pady=10)
        files = False
        for entry in os.scandir():
            if entry.is_file():
                files = True
                continue
        if not files:
            messagebox.showinfo('My Sorter','No files in this folder.Please select another folder or Press the EXIT button')
            selected_folder_label.grid_remove()
            root.geometry('100x50')
        else:
            get_name_btn = Button(root, text='NEXT', command=get_name)
            get_name_btn.grid(row=11, column=1)
            get_name_btn.focus_set()
    except:
        pass


scanned = []
folder_dict = {}

def get_name():
    root.geometry('500x450')
    for entry in os.scandir():
        if entry.is_dir():
            continue
        file_path = Path(entry)
        file_format = file_path.suffix.lower()
        if file_format not in scanned:
            scanned.append(file_format)
    extension_entries = [Entry(scrollable_frame) for _ in range(len(scanned))]

    def set_name():
        global last_row
        for i in range(len(scanned)):
            if not extension_entries[i].get():
                folder_dict.update({scanned[i]: scanned[i][1:]})
            else:
                folder_dict.update({scanned[i]: extension_entries[i].get()})
        messagebox.showinfo('My Organizer', 'Folder names saved Successfully. Press the PROCEED Button')
        organize_btn = Button(root, text='PROCEED', command=organize)
        organize_btn.grid(row=11, column=1)

    container.grid(row=2, column=0)
    canvas.grid(row=2, column=3)
    scrollbar.grid(row=2, column=4, sticky=N + S)
    global last_row
    for i in range(len(scanned)):
        Label(scrollable_frame, text=scanned[i]).grid(row=i+1, column=0, sticky=W, padx=10)
        extension_entries[i].grid(row=i+1, column=1, pady=1.5)

    Label(root, text='NOTE: If no name is provided,a new folder\nwith file extension as name will be created!').grid(row=13, column=0, sticky=S)
    set_name_btn = Button(root, text="OK", command=set_name)
    set_name_btn.grid(row=10, column=0, sticky=S, pady=10)
    set_name_btn.focus_set()


def organize():
    root.geometry('400x450')
    for file in os.scandir():
        if file.is_dir():
            continue
        file_path2 = Path(file)
        file_format2 = file_path2.suffix.lower()
        if file_format2 in folder_dict:
            directory_path = Path(folder_dict[file_format2])
            directory_path.mkdir(exist_ok=True)
            file_path2.rename(directory_path.joinpath(file_path2))
    for dir in os.scandir():
        try:
            os.rmdir(dir)
        except:
            pass
    messagebox.showinfo('My Organizer', 'The Selected Folder Organized Successfully.Press the EXIT button.')


def exit():
    root.destroy()
    folder_dict.clear()
    scanned.clear()


if __name__ == "__main__":
    root = Tk()
    root.title("MY SORTER")
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 3 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 2)
    container=Frame(root)
    canvas=Canvas(container)
    scrollbar=Scrollbar(container,orient='vertical',command=canvas.yview)
    scrollable_frame=Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0,0),window=scrollable_frame,anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    sel_folder_btn = Button(root, text='Browse Folder', command=select_folder)
    sel_folder_btn.grid(row=11, column=0)
    exit = Button(root, text='EXIT', command=exit)
    exit.grid(row=12, column=0)
    root.geometry('+{}+{}'.format(positionRight,positionDown))
    root.mainloop()