import tkinter
import tkinter.filedialog
from tkinter import ttk
import os
import csv_parser
import pastebin
from dotenv import load_dotenv, set_key
import configparser

load_dotenv()

config = configparser.ConfigParser()
config.read("config.ini")


root = tkinter.Tk()

file_path = ""
file_name = tkinter.StringVar()
pastebin_link = tkinter.StringVar()
ban_reason = tkinter.StringVar()
test_mode = tkinter.BooleanVar(root, value=config["settings"]["testmode"])
dark_mode = tkinter.BooleanVar(root, value=config["settings"]["darkmode"])
prefix = tkinter.BooleanVar(root, value=config["settings"]["prefix"])
key_visible = tkinter.BooleanVar(root, False)
dev_key = tkinter.StringVar(root, value=os.getenv("DEV_KEY"))
TEST_MODE_MESSAGE = "Test Mode is active!"


def save_settings():
    if dev_key.get() != os.getenv("DEV_KEY"):
        set_key(dotenv_path=".env", key_to_set="DEV_KEY", value_to_set=dev_key.get())
        os.environ["DEV_KEY"] = dev_key.get()

    toggle_test_mode()
    toggle_dark_mode()
    toggle_prefix()

    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def toggle_entry_visibility(entry: ttk.Entry):
    if key_visible.get():
        entry.config(show="")
    else:
        entry.config(show="*")


def toggle_prefix():
    if prefix.get():
        config["settings"]["prefix"] = "on"
    else:
        config["settings"]["prefix"] = "off"


def toggle_test_mode():
    if test_mode.get():
        config["settings"]["testmode"] = "on"
    else:
        config["settings"]["testmode"] = "off"


def toggle_dark_mode():
    if dark_mode.get():
        config["settings"]["darkmode"] = "on"
        root.tk.call("set_theme", "dark")
    else:
        config["settings"]["darkmode"] = "off"
        root.tk.call("set_theme", "light")


def open_settings():
    settings = tkinter.Toplevel()
    settings.title("Settings")
    settings.focus_set()
    settings.resizable(False, False)

    key_label = ttk.Label(settings, text="api_dev_key:")
    key_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    key_entry = ttk.Entry(settings, width=31, textvariable=dev_key, show="*")
    key_entry.grid(row=0, column=1, pady=5, padx=5)

    key_visible.set(False)
    key_visible_checkbox = ttk.Checkbutton(settings, style='Switch.TCheckbutton', variable=key_visible,
                                           command=lambda: toggle_entry_visibility(key_entry))
    key_visible_checkbox.grid(row=0, column=2, padx=5)

    test_mode_label = ttk.Label(settings, text="Test Mode:")
    test_mode_label.grid(row=1, column=0, sticky="w", padx=5)

    test_mode.set(config["settings"]["testmode"])
    test_mode_checkbox = ttk.Checkbutton(settings, style='Switch.TCheckbutton', variable=test_mode)
    test_mode_checkbox.grid(row=1, column=1, padx=5, sticky="w")

    dark_mode_label = ttk.Label(settings, text="Dark Mode:")
    dark_mode_label.grid(row=2, column=0, sticky="w", padx=5)

    dark_mode.set(config["settings"]["darkmode"])
    dark_mode_checkbox = ttk.Checkbutton(settings, style='Switch.TCheckbutton', variable=dark_mode)
    dark_mode_checkbox.grid(row=2, column=1, padx=5, sticky="w")

    prefix_label = ttk.Label(settings, text="!filesay Prefix:")
    prefix_label.grid(row=3, column=0, sticky="w", padx=5)

    prefix.set(config["settings"]["prefix"])
    prefix_checkbox = ttk.Checkbutton(settings, style='Switch.TCheckbutton', variable=prefix)
    prefix_checkbox.grid(row=3, column=1, padx=5, sticky="w")

    save_button = ttk.Button(settings, text="Save", width=5, command=save_settings)
    save_button.grid(row=4, column=2, sticky="e", padx=5, pady=5)

    settings.mainloop()


def open_file():
    global file_path
    file_path = tkinter.filedialog.askopenfilename(title="Open File",
                                                   filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
    file_name.set(os.path.basename(file_path))


def generate_link():
    if file_path != "":
        filesay = csv_parser.parse(file_path, ban_reason.get())
        if test_mode.get():
            pastebin_link.set(TEST_MODE_MESSAGE)
            print(filesay)
        else:
            response = pastebin.paste(filesay, dev_key.get())
            if response.status_code == 200:
                if prefix.get():
                    pastebin_link.set("!filesay " + response.text)
            else:
                pastebin_link.set(response.text)


def copy_link():
    if pastebin_link.get() != "" and pastebin_link.get() != TEST_MODE_MESSAGE:
        root.clipboard_clear()
        root.clipboard_append(pastebin_link.get())


def main():
    root.title("filesay")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    root.tk.call("source", "Azure-ttk-theme-2.1.0/azure.tcl")
    if dark_mode.get():
        root.tk.call("set_theme", "dark")
    else:
        root.tk.call("set_theme", "light")

    # UPPER LABELFRAME ############

    upper_frame = ttk.LabelFrame(text="Select File: ")
    upper_frame.grid(row=1, column=0, padx=5, pady=5, sticky="we")
    upper_frame.columnconfigure(1, weight=1)

    file_label1 = ttk.Label(upper_frame, text="Filename:", width=10)
    file_label1.grid(row=0, column=0, padx=5)

    file_label2 = ttk.Label(upper_frame, textvariable=file_name, width=50)
    file_label2.grid(row=0, column=1)

    open_btn = ttk.Button(upper_frame, text="Open File", command=open_file)
    open_btn.grid(row=0, column=2, pady=5, padx=5, sticky="e")

    # MIDDLE FRAME ################

    middle_frame = ttk.Frame()
    middle_frame.grid(row=2, column=0)

    reason_label = ttk.Label(middle_frame, text="Ban Reason:")
    reason_label.grid(row=0, column=0, padx=5)

    reason_entry = ttk.Entry(middle_frame, textvariable=ban_reason)
    reason_entry.grid(row=0, column=1, padx=5)

    generate_btn = ttk.Button(middle_frame, text="Generate Link", command=generate_link)
    generate_btn.grid(row=0, column=2, pady=5, padx=5, sticky="we")

    settings_button = ttk.Button(middle_frame, text="Settings", command=open_settings, width=7)
    settings_button.grid(row=0, column=3, padx=5, pady=5)

    # LOWER LABELFRAME ##############

    lower_frame = ttk.LabelFrame(text="Pastebin:")
    lower_frame.grid(row=3, column=0, padx=5, pady=5, sticky="we")
    lower_frame.columnconfigure(1, weight=1)

    link_label = ttk.Label(lower_frame, text="Link:", width=10)
    link_label.grid(row=0, column=0, padx=5, pady=5)

    link_label2 = ttk.Label(lower_frame, textvariable=pastebin_link, width=50)
    link_label2.grid(row=0, column=1)

    copy_btn = ttk.Button(lower_frame, text="Copy", command=copy_link)
    copy_btn.grid(row=0, column=2, pady=5, padx=5, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
