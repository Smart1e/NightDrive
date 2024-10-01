import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from threading import Thread
import time
import funkyDisk

SCREEN_SIZE = {'width': 1920, 'height': 1080}

dark_theme = {
    'bg': '#1a1a1a', 'menu_bg': '#282828', 'widget_bg': '#2a2a2a',
    'text': '#ffffff', 'generalFont': ('Arial', 20), 'largerFont': ('Arial', 45),
    'accent': '#49D2FF'
}

light_theme = {
    'bg': '#ffffff', 'menu_bg': '#C4C4C4', 'widget_bg': '#ABABAB',
    'text': '#000000', 'generalFont': ('Arial', 20), 'largerFont': ('Arial', 45),
    'accent': '#49D2FF'
}

theme = dark_theme

# Sizes and types based on the given guide
sizes_hdd = ["160GB", "250GB", "320GB", "500GB", "750GB", "1TB", "2TB", "3TB", "4TB"]
sizes_ssd = ["128GB", "256GB", "512GB", "1TB", "2TB", "4TB"]
physical_sizes_hdd = ["2.5\"", "3.5\""]
physical_sizes_ssd = ["2.5\""]
drive_types = ["HDD", "SSD", "Unknown"]
test_statuses = ["Not Started", "In Progress", "Completed"]
erase_statuses = ["Not Started", "In Progress", "Completed"]

class NightDriveApp:
    def __init__(self, root):
        self.root = root
        self.root.title('NightDrive')
        self.root.attributes('-fullscreen', True)
        self.drive_frames = {}

        self.menuFrame = ctk.CTkFrame(self.root, fg_color=theme['menu_bg'], width=SCREEN_SIZE['width'], height=80)
        self.menuTitle = ctk.CTkLabel(self.menuFrame, text='NightDrive', fg_color=theme['menu_bg'], text_color=theme['text'], font=theme['largerFont'])
        self.menuFrame.place(x=0, y=0)
        self.menuTitle.place(x=10, y=10)

        self.canvas = tk.Canvas(self.root, bg=theme['bg'])
        self.canvas.place(x=0, y=100, relwidth=1, relheight=0.9)

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=SCREEN_SIZE['width'] - 20, y=100, height=SCREEN_SIZE['height'] - 100)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=theme['bg'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.update_drives()

    def update_drives(self):
        current_drives = funkyDisk.getAllInfo()
        current_identifiers = {drive['identifier'] for drive in current_drives}
        existing_identifiers = set(self.drive_frames.keys())

        # Remove missing drives
        for identifier in existing_identifiers - current_identifiers:
            frame = self.drive_frames.pop(identifier)
            frame.destroy()

        # Add new drives
        for drive in current_drives:
            if drive['identifier'] not in self.drive_frames:
                self.create_drive_frame(drive)

        self.root.after(5000, self.update_drives)

    def create_drive_frame(self, drive_info):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color=theme['widget_bg'], height=250)
        frame.pack(fill=tk.X, padx=5, pady=5)
        self.drive_frames[drive_info['identifier']] = frame

        # Identifier
        label_identifier = ctk.CTkLabel(frame, text=f"Identifier: {drive_info['identifier']}", text_color=theme['text'], font=theme['generalFont'])
        label_identifier.pack(anchor=tk.W, padx=10, pady=5)

        # Physical Size Dropdown
        label_physical_size = ctk.CTkLabel(frame, text="Physical Size:", text_color=theme['text'], font=theme['generalFont'])
        label_physical_size.pack(anchor=tk.W, padx=10, pady=5)
        combobox_physical_size = ttk.Combobox(frame, values=physical_sizes_hdd + physical_sizes_ssd)
        combobox_physical_size.set(drive_info['physical_size'])
        combobox_physical_size.pack(anchor=tk.W, padx=10, pady=5)

        # Type Dropdown
        label_type = ctk.CTkLabel(frame, text="Type:", text_color=theme['text'], font=theme['generalFont'])
        label_type.pack(anchor=tk.W, padx=10, pady=5)
        combobox_type = ttk.Combobox(frame, values=drive_types)
        combobox_type.set(drive_info['type'])
        combobox_type.pack(anchor=tk.W, padx=10, pady=5)

        # Size Dropdown
        label_size = ctk.CTkLabel(frame, text="Size:", text_color=theme['text'], font=theme['generalFont'])
        label_size.pack(anchor=tk.W, padx=10, pady=5)
        combobox_size = ttk.Combobox(frame, values=sizes_hdd + sizes_ssd)
        combobox_size.set(drive_info['size'])
        combobox_size.pack(anchor=tk.W, padx=10, pady=5)

        # Now bind the type combobox to update physical size and size comboboxes
        combobox_type.bind("<<ComboboxSelected>>", lambda event, cb_size=combobox_size, cb_type=combobox_type, cb_physical_size=combobox_physical_size: self.update_size_and_physical_size_options(cb_size, cb_type, cb_physical_size))

        # Test Status Label
        label_test_status_text = ctk.CTkLabel(frame, text="Test Status:", text_color=theme['text'], font=theme['generalFont'])
        label_test_status_text.pack(anchor=tk.W, padx=10, pady=5)
        label_test_status = ctk.CTkLabel(frame, text=drive_info.get('test_status', 'Not Started'), text_color=theme['text'], font=theme['generalFont'])
        label_test_status.pack(anchor=tk.W, padx=10, pady=5)

        # Erase Status Label
        label_erase_status_text = ctk.CTkLabel(frame, text="Erase Status:", text_color=theme['text'], font=theme['generalFont'])
        label_erase_status_text.pack(anchor=tk.W, padx=10, pady=5)
        label_erase_status = ctk.CTkLabel(frame, text=drive_info.get('erase_status', 'Not Started'), text_color=theme['text'], font=theme['generalFont'])
        label_erase_status.pack(anchor=tk.W, padx=10, pady=5)

        # Start Test Button
        button_test = ctk.CTkButton(frame, text="Start Test", command=lambda: self.start_test(drive_info['identifier'], label_test_status))
        button_test.pack(side=tk.LEFT, padx=10, pady=10)

        # Start Erase Button
        button_erase = ctk.CTkButton(frame, text="Start Erase", command=lambda: self.start_erase(drive_info['identifier'], label_erase_status))
        button_erase.pack(side=tk.LEFT, padx=10, pady=10)

    def update_size_and_physical_size_options(self, combobox_size, combobox_type, combobox_physical_size):
        type_value = combobox_type.get()
        if type_value == "SSD":
            combobox_physical_size.set("2.5\"")
            combobox_physical_size['values'] = physical_sizes_ssd
            combobox_size['values'] = sizes_ssd
        elif type_value == "HDD":
            combobox_physical_size['values'] = physical_sizes_hdd
            combobox_size['values'] = sizes_hdd
        else:
            combobox_physical_size['values'] = physical_sizes_hdd #  + physical_sizes_ssd Commented out because otherwise there will be dupe values
            combobox_size['values'] = sizes_hdd + sizes_ssd

    def start_test(self, identifier, label_test_status):
        frame = self.drive_frames[identifier]
        label_test_status.configure(text="In Progress")

        def update_status(diskNumber, result):
            status = "Passed" if result else "Failed"
            self.root.after(0, lambda: label_test_status.configure(text=status))

        test_thread = Thread(target=funkyDisk.surfaceScan, args=(identifier, update_status))
        test_thread.start()

    def start_erase(self, identifier, label_erase_status):
        print(f"This would start an erase on {identifier}")

def constantDiskCheck():
    while True:
        funkyDisk.getAllInfo()
        time.sleep(5)

if __name__ == "__main__":
    root = ctk.CTk()
    app = NightDriveApp(root)
    constantDiskCheckThread = Thread(target=constantDiskCheck)
    constantDiskCheckThread.daemon = True
    constantDiskCheckThread.start()
    root.mainloop()
    # This comment is meaningless