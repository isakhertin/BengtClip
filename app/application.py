import rumps
import pyperclip
import os
import json
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF

HISTORY_FILE = os.path.expanduser("~/.clipboard_history.json")
MAX_ROW_OPTIONS = [5, 10, 20, 30]

class Application(rumps.App):
    def __init__(self) -> None:
        super().__init__(
            name="",
            icon="resources/BengtClip_white.icns",
            menu=[]
        )

        # Load from file
        self.history, self.max_row = self.load_data()
        self.last_clipboard = self.history[0] if self.history else ""

        # Pre-create the clipboard row submenu before inserting clipboard items
        self.row_menu = rumps.MenuItem("Max Rows")
        for row in MAX_ROW_OPTIONS:
            self.row_menu.add(
                rumps.MenuItem(
                    f"Show {row}",
                    callback=self.make_row_setter(row)
                )
            )
        self.menu.add(self.row_menu)

        self.clipboard_items = []
        self.setup_clipboard_items()

        self.timer = rumps.Timer(self.check_clipboard, 1)
        self.timer.start()

    def setup_clipboard_items(self) -> None:
        # First, remove all previously added clipboard items and the separator
        for item in self.clipboard_items:
            try:
                del self.menu[item.title]
            except KeyError:
                pass

        # Remove any lingering separator (None) if it exists
        keys_to_remove = [key for key, val in self.menu.items() if val is None]
        for key in keys_to_remove:
            del self.menu[key]

        # Clear internal list
        self.clipboard_items.clear()

        # Add fresh clipboard items
        for i in range(self.max_row):
            shortcut = f"@{i+1}" if i < 9 else None
            item = rumps.MenuItem(f"{i+1}. (empty)", 
                                  callback=self.make_copy_callback(i), 
                                  key=shortcut)
            
            self.clipboard_items.append(item)
            self.menu.insert_before("Max Rows", item)

        # Add a new separator
        self.menu.insert_before("Max Rows", None)

        self.refresh_menu_titles()

    def make_copy_callback(self, index: int) -> None:
        def copy_item(_):
            if index < len(self.history):
                pyperclip.copy(self.history[index])
                rumps.notification("Clipboard Copied", "", f"Copied item {index + 1}")
        return copy_item

    def make_row_setter(self, row_count: int) -> None:
        def set_rows(_):
            self.max_row = row_count
            self.history = self.history[:self.max_row]
            self.setup_clipboard_items()
            self.save_data()
        return set_rows

    def check_clipboard(self, _) -> None:

        def is_image_in_clipboard() -> bool:
            clipboard = NSPasteboard.generalPasteboard()
            image_types = [NSPasteboardTypePNG, NSPasteboardTypeTIFF]
            return clipboard.availableTypeFromArray_(image_types) is not None
    
        if is_image_in_clipboard():
            #is image -> do nothing
            return

        content = pyperclip.paste().strip()
        try:        
            if content and content != self.last_clipboard:
                self.last_clipboard = content
                self.add_to_history(content)
        
        except ValueError as e:
            print(f"Error: {e}")
            return
        

    def add_to_history(self, content) -> None:
        if content in self.history:
            self.history.remove(content)
        self.history.insert(0, content)
        self.history = self.history[:self.max_row]
        self.refresh_menu_titles()
        self.save_data()

    def refresh_menu_titles(self) -> None:
        for i in range(self.max_row):
            text = self.history[i] if i < len(self.history) else "(empty)"
            if len(text) > 50:
                text = text[:47] + "..."
            self.clipboard_items[i].title = f"{i+1}. {text}"

    def load_data(self) -> tuple:
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    data = json.load(f)
                    history = data.get("history", [])
                    max_row = data.get("max_row", MAX_ROW_OPTIONS[-1])
                    return history[:max_row], max_row
            except Exception:
                pass
        return [], MAX_ROW_OPTIONS[-1]

    def save_data(self) -> None:
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump({"history": self.history, "max_row": self.max_row}, f)
        except Exception as e:
            rumps.alert("Error saving data", str(e))

    def quit_app(self, _):
        print("Quitting application...")
        self.save_data()
        rumps.quit_application()


