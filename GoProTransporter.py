import os
import shutil
import threading
import json
from tkinter import Tk, Button, Label, filedialog, ttk
from appdirs import user_config_dir

CONFIG_DIR = user_config_dir(appname="GoProTransporter", appauthor=False)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


PROXY_EXT_ORIGINAL = ".lrv"
PROXY_EXT_TARGET = ".mov"
MEDIA_EXTENSIONS = (".jpg", ".wav", ".mp4")
ALL_EXTENSIONS = (*MEDIA_EXTENSIONS, PROXY_EXT_ORIGINAL, PROXY_EXT_TARGET)

class FileCopyApp:
    def __init__(self, master):
        self.master = master
        master.title("File Copy App")

        self.source_label = Label(master, text="Source Directory:")
        self.source_label.pack()

        self.source_button = Button(master, text="Select Source", command=self.select_source_directory)
        self.source_button.pack()

        self.destination_label = Label(master, text="Destination Directory:")
        self.destination_label.pack()

        self.destination_button = Button(master, text="Select Destination", command=self.select_destination_directory)
        self.destination_button.pack()

        self.copy_button = Button(master, text="Copy Files", command=self.copy_files)
        self.copy_button.pack()

        self.cancel_button = Button(master, text="Cancel", command=self.cancel_copy)
        self.cancel_button.pack()
        self.cancel_button.pack_forget()  # Hide the Cancel button initially

        self.close_button = Button(master, text="Close", command=self.close_app)
        self.close_button.pack()
        self.close_button.pack_forget()

        self.progress_label = Label(master, text="")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()


        # Shared variable to signal if copying should be canceled
        self.cancel_flag = False

        self.source_path = ""
        self.destination_path = ""

        self.load_config()


    def cancel_copy(self):
        self.cancel_flag = True

    def close_app(self):
        # Save selected folders to the configuration file before closing (optional)
        self.save_config()
        self.master.destroy()  # Close the Tkinter window


    def toggle_button(self, button, state):
        # Show or hide the Cancel button based on the given state
        if state:
            button.pack()
        else:
            button.pack_forget()

    def select_source_directory(self):
        self.source_path = filedialog.askdirectory()
        self.source_label.config(text=f"Source Directory: {self.source_path}")

    def select_destination_directory(self):
        self.destination_path = filedialog.askdirectory()
        self.destination_label.config(text=f"Destination Directory: {self.destination_path}")


    def copy_files(self):
        if  not (os.path.exists(self.source_path) and os.path.exists(self.destination_path)):
            print("Please select both source and destination directories.")
            return

        # Save selected folders to the configuration file
        self.save_config()

        # Run the file copy operation in a separate thread
        threading.Thread(target=self.copy_files_thread).start()


    def copy_files_thread(self):
       
        # Get the total number of files to copy
        total_files = sum(1 for file in os.listdir(self.source_path) if os.path.isfile(os.path.join(self.source_path, file)) and file.lower().endswith(ALL_EXTENSIONS))
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0

        proxy_subfolder = os.path.join(self.destination_path, "proxies")
        if not os.path.exists(proxy_subfolder):
            os.makedirs(proxy_subfolder)

        # Show the Cancel button
        self.toggle_button(self.cancel_button, True)
        self.toggle_button(self.copy_button, False)

        counts = {
            "copied": 0,
            "skipped": 0,
        }

        # Iterate through files in the source folder
        for filename in os.listdir(self.source_path):
            source_path = os.path.join(self.source_path, filename)

            # Check if it's a file and meets the criteria for copying
            if os.path.isfile(source_path):
                if self.cancel_flag:
                    self.progress_label.config(text="Copy operation canceled.")
                    return

                file_size = os.path.getsize(source_path)/float(1<<20)

                if filename.lower().endswith(MEDIA_EXTENSIONS):
                    destination_path = os.path.join(self.destination_path, filename)

                elif filename.lower().endswith(PROXY_EXT_ORIGINAL):
                    new_filename = filename.replace("GL", "GX").replace(PROXY_EXT_ORIGINAL.upper(), PROXY_EXT_TARGET)
                    destination_path = os.path.join(proxy_subfolder, new_filename)

                if os.path.exists(destination_path):
                    self.progress_bar["value"] += 1
                    counts["skipped"] += 1
                    self.progress_label.config(text=f"Skipping file {filename} (already exists)")
                    self.master.update()
                    continue

                
                self.progress_label.config(text=f"Copying file {filename} [{file_size:.2f} MB]")
                shutil.copy2(source_path, destination_path)
                self.progress_bar["value"] += 1
                counts["copied"] += 1
                self.master.update()

        # self.progress_bar["value"] = 0
        self.progress_label.config(text=f"Copy operation complete.\n Copied {counts['copied']} files.\n Skipped {counts['skipped']} files.")

        self.toggle_button(self.cancel_button, False)
        self.toggle_button(self.close_button, True)

    def save_config(self):
        # Save selected folders to the configuration file in JSON format
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

        config_data = {"SourcePath": self.source_path, "DestinationPath": self.destination_path}

        with open(CONFIG_PATH, "w") as config_file:
            json.dump(config_data, config_file)

    def load_config(self):
        # Load selected folders from the configuration file in JSON format
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as config_file:
                config_data = json.load(config_file)
                self.source_path = config_data.get("SourcePath", "")
                self.destination_path = config_data.get("DestinationPath", "")

                self.source_label.config(text=f"Source Directory: {self.source_path}")
                self.destination_label.config(text=f"Destination Directory: {self.destination_path}")


# Specify the source and destination paths
if __name__ == "__main__":
    root = Tk()
    app = FileCopyApp(root)
    root.mainloop()
