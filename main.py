import tkinter
import tkinter.filedialog
from tkinter import ttk
import os
import csv_parser
import pastebin
#import settings
from dotenv import load_dotenv, set_key

#from settings import Settings

load_dotenv()
#DEV_KEY = os.getenv("DEV_KEY")



root = tkinter.Tk()

file_path = ""
file_name = tkinter.StringVar()
pastebin_link = tkinter.StringVar()
ban_reason = tkinter.StringVar()
test_mode = tkinter.BooleanVar()
#print(os.getenv("DEV_KEY"))
dev_key_displayed = tkinter.StringVar(root, value=os.getenv("DEV_KEY"))
#DEV_KEY = os.getenv("DEV_KEY")
#if DEV_KEY is None:
   # dev_key_displayed.set("")
#else:
   # dev_key_displayed.set(DEV_KEY)


def save_settings():
    if dev_key_displayed.get() != os.getenv("DEV_KEY"):
        set_key(dotenv_path=".env", key_to_set="DEV_KEY", value_to_set=dev_key_displayed.get())
        #load_dotenv()
        os.environ["DEV_KEY"] = dev_key_displayed.get()
    print("test" + os.getenv("DEV_KEY"))

def open_settings():
    settings = tkinter.Toplevel()
    settings.title("Settings")
    settings.focus_set()

    key_label = ttk.Label(settings, text="api_dev_key:")
    key_label.grid(row=0, column=0, padx=5, pady=5)

    key_entry = ttk.Entry(settings, width=35, textvariable=dev_key_displayed)
    #key_entry.insert(index=0, string=DEV_KEY)
    key_entry.grid(row=0, column=1, pady=5, padx=5)

    testmode_checkbox = ttk.Checkbutton()

    save_button = ttk.Button(settings, text="Save", command=save_settings)
    save_button.grid(row=2, column=1, sticky="e", padx=5, pady=5)

    # settings.geometry("200x200")
    settings.mainloop()

def open_file():
    global file_path
    file_path = tkinter.filedialog.askopenfilename(title="Open File",
                                                   filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
    file_name.set(os.path.basename(file_path))


def generate_link():
    if file_path != "":
        link = ""
        filesay = csv_parser.parse(file_path, ban_reason.get())
        print(test_mode.get())
        if test_mode.get():
            pastebin_link.set("Test Mode is active!")
            print(filesay)
        else:
            link = pastebin.paste(filesay)

        pastebin_link.set(link)


def copy_link():
    if pastebin_link.get() != "":
        root.clipboard_append(pastebin_link.get())


def main():
    root.title("filesay")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # MENU ############

    menu = tkinter.Menu(root)
    root.config(menu=menu)
    file_menu = tkinter.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Settings", command=open_settings)
    file_menu.add_checkbutton(label="Test Mode", variable=test_mode)
    file_menu.add_command(label="Exit", command=quit)

    #settings_button = ttk.Button(text="Set", command=open_settings)
    #settings_button.grid(row=0, column=0, sticky="e", padx=5)

    # UPPER LABELFRAME ############

    labelframe1 = ttk.LabelFrame(text="Select File: ")
    labelframe1.grid(row=1, column=0, padx=5, pady=5, sticky="we")
    labelframe1.columnconfigure(1, weight=1)

    file_label1 = ttk.Label(labelframe1, text="Filename:", width=10)
    file_label1.grid(row=0, column=0, padx=5)

    file_label2 = ttk.Label(labelframe1, textvariable=file_name, width=50)
    file_label2.grid(row=0, column=1)

    open_btn = ttk.Button(labelframe1, text="Open File", command=open_file)
    open_btn.grid(row=0, column=2, pady=5, padx=5, sticky="e")

    # LOWER LABELFRAME ##############

    labelframe2 = ttk.LabelFrame(text="Pastebin Link:")
    labelframe2.grid(row=3, column=0, padx=5, pady=5, sticky="we")
    labelframe2.columnconfigure(1, weight=1)

    link_label = ttk.Label(labelframe2, text="Link:", width=10)
    link_label.grid(row=0, column=0, padx=5, pady=5)

    link_label2 = ttk.Label(labelframe2, textvariable=pastebin_link, width=50)
    link_label2.grid(row=0, column=1)

    copy_btn = ttk.Button(labelframe2, text="Copy", command=copy_link)
    copy_btn.grid(row=0, column=2, pady=5, padx=5, sticky="e")

    # MIDDLE FRAME ################

    frame1 = ttk.Frame()
    frame1.grid(row=2, column=0)

    reason_label = ttk.Label(frame1, text="Ban Reason:")
    reason_label.grid(row=0, column=0, padx=5)

    generate_btn = ttk.Button(frame1, text="Generate Link", command=generate_link)
    generate_btn.grid(row=0, column=2, pady=5, padx=5, sticky="we")

    reason_entry = ttk.Entry(frame1, textvariable=ban_reason)
    reason_entry.grid(row=0, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
