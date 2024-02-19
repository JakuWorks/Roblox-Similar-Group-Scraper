# TODO: IMPROVE THE CODE QUALITY BEFORE YOU CONTINUE THIS CODE

import tkinter as tk
from tkinter import ttk
from custom_tkinter_styling import CustomTkinterStyles

from logger import LOG


FANCY_LABEL_DEBUG_NAME: str = "Fancy Label"


class FancyLabelManager:
    def __init__(self, master: tk.Misc) -> None:
        LOG(f"Creating a Fancy Label Manager", 2)
        self.master: tk.Misc = master

    def add(self) -> None:
        LOG(f"Adding a Fancy Label", 3)
        FancyLabel(master=self.master)


class FancyLabel:
    # 🞫 Special Unicode Cross U+1F5D9 - https://en.wikipedia.org/wiki/X_mark
    # ＋ Special Unicode Plus U+FF0B

    _current_highest_id: int = 0

    def __init__(self, master: tk.Misc) -> None:
        self.id: int = self.generate_unique_id()
        self.debug_name: str = f"{FANCY_LABEL_DEBUG_NAME} {self.id}"
        self.CSF: CustomTkinterStyles = CustomTkinterStyles.get_instance()

        self.char_x: str = ""
        self.char_plus: str = ""

        LOG(f"Initializing - '{self.debug_name}'", 3)

        LOG(f"Creating Frame - '{self.debug_name}'", 4)
        self.frame: ttk.Frame = ttk.Frame(master=master)
        self.frame.pack(expand=False, fill=tk.BOTH, side=tk.TOP)

        LOG(f"Adding Removal Button - '{self.debug_name}'", 4)
        self.button: ttk.Button = ttk.Button(master=master, text=self.char_x, style=self.CSF.STYLE_BUTTON_SYMBOL_BIG_NAME)
        self.button.pack(expand=False, fill=tk.BOTH, side=tk.TOP)

    @classmethod
    def generate_unique_id(cls) -> int:
        cls._current_highest_id = cls._current_highest_id + 1
        return cls._current_highest_id
