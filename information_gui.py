import tkinter as tk
from tkinter import ttk
from custom_tkinter_styling import CustomTkinterStyles

from typing import Union
from dataclasses import dataclass

from logger import LOG


@dataclass
class InformationGuiAppearance:
    window_title: str
    text_heading: str
    text_main: str
    text_close_button: str = "Ok"
    window_size: str = "770x490"  # 550x350 is a good one if you have little text
    debug_title: Union[None, str] = None


# Note that the code runs completely FINE but my code editor still complains


class InformationGuiSingleton:
    _current_instance: Union["InformationGuiSingleton", None] = None
    _current_highest_id: int = 0

    def __init__(self, master: tk.Misc, appearance: InformationGuiAppearance) -> None:
        self.id: int = self.generate_unique_id()
        self.debug_title: str = appearance.debug_title or appearance.window_title
        self.debug_name: str = f"{appearance.debug_title} {self.id}"

        LOG(f"Initializing Help Gui - '{self.debug_name}'", 2)

        if self.__class__._current_instance is not None:
            LOG(f"Detected Already Existing Window - '{self.__class__._current_instance.debug_name}'", 3)
            self.__class__._current_instance.close_window()

        self.__class__._current_instance = self

        LOG(f"Creating GUI Root - '{self.debug_name}'", 3)
        self.root: tk.Toplevel = tk.Toplevel(master=master)

        self.CSF: CustomTkinterStyles = CustomTkinterStyles.get_instance()

        LOG(f"Setting Window Title - '{self.debug_name}'", 3)
        self.root.title(string=appearance.window_title)

        LOG(f"Setting Window Geometry - '{self.debug_name}'", 3)
        self.root.geometry(newGeometry=appearance.window_size)

        LOG(f"Creating MainFrame - '{self.debug_name}'", 3)
        self.mainframe: ttk.Frame = ttk.Frame(master=self.root)
        self.mainframe.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        LOG(f"Creating Heading Text Label - '{self.debug_name}'", 3)
        heading_label_text: str = appearance.text_heading
        self.heading_label: ttk.Label = ttk.Label(
            master=self.mainframe,
            anchor=tk.CENTER,
            text=heading_label_text,
            font=self.CSF.FONT_LABEL_HEADING_MEDIUM,
        )
        self.heading_label.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=15, pady=15)

        LOG(f"Creating Main Text Label - '{self.debug_name}'", 3)
        main_label_text: str = appearance.text_main

        self.main_label: ttk.Label = ttk.Label(
            master=self.mainframe,
            anchor=tk.NW,
            text=main_label_text,
            font=self.CSF.FONT_LABEL_NORMAL_SMALL,
        )
        self.main_label.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=50, pady=10)

        LOG(f"Creating '{appearance.text_close_button}' Button - '{self.debug_name}'", 3)
        self.close_button: ttk.Button = ttk.Button(
            master=self.mainframe,
            text=appearance.text_close_button,
            style=self.CSF.STYLE_BUTTON_MEDIUM_NAME,
            command=self.close_window,
        )

        self.close_button.pack(expand=False, fill=tk.NONE, side=tk.TOP, padx=15, pady=15, ipadx=3, ipady=3)

    def close_window(self) -> None:
        LOG(f"Closing Window '{self.debug_name}'", 4)
        self.__class__._current_instance = None
        self.root.destroy()

    @classmethod
    def generate_unique_id(cls) -> int:
        cls._current_highest_id = cls._current_highest_id + 1
        return cls._current_highest_id
