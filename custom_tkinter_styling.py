from typing import Callable, Union

from tkinter import ttk
from tkinter import font as tkfont

from logger import LOG


class CustomTkinterStyles:
    def __init__(self) -> None:
        if self.__class__._instance is not None:
            raise RuntimeError(f"Attempted to create a second instance of the singleton {self.__class__.__name__}." f" Don't do that! Use the {self.__class__.singleton_get_method.__name__} method!")

        self.__class__._instance = self

        LOG(f"Creating Custom Styles And Fonts", 2)

        if self.__class__._style_instance is None:
            self.__class__._style_instance = ttk.Style()

        # Before using a custom font, check is it pre-installed on Windows, Linux and MacOs!!!
        # Useful article about this: https://web.mit.edu/jmorzins/www/fonts.html
        # From my research I found these fonts should be shared between Windows and MacOS 70% of the time:
        # of course the more popular the font the higher is the chance that it will work
        # ['Arial', 'Courier New', 'Georgia', 'Candara', 'Tahoma', 'Times New Roman', 'Verdana', 'Consolas', 'Trebuchet MS', 'Impact']
        # But there may be other working fonts besides these

        # Special font just for the x and + text in fancy label buttons
        self.STYLE_BUTTON_SYMBOL_BIG_NAME: str = "Custom_Symbol_Big.TButton"
        self.STYLE_BUTTON_SYMBOL_BIG_FONT: tkfont.Font = tkfont.Font(family="Courier New", size=26, weight=tkfont.BOLD)
        self.__class__._style_instance.configure(
            style=self.STYLE_BUTTON_SYMBOL_BIG_NAME,
            font=self.STYLE_BUTTON_SYMBOL_BIG_FONT,
        )

        self.STYLE_BUTTON_SMALLEST_NAME: str = "Custom_Smallest.TButton"
        self.STYLE_BUTTON_SMALLEST_FONT: tkfont.Font = tkfont.Font(family="Arial", size=8, weight=tkfont.BOLD)
        self.__class__._style_instance.configure(style=self.STYLE_BUTTON_SMALLEST_NAME, font=self.STYLE_BUTTON_SMALLEST_FONT)

        self.STYLE_BUTTON_SMALL_NAME: str = "Custom_Small.TButton"
        self.STYLE_BUTTON_SMALL_FONT: tkfont.Font = tkfont.Font(family="Arial", size=10, weight=tkfont.BOLD)
        self.__class__._style_instance.configure(style=self.STYLE_BUTTON_SMALL_NAME, font=self.STYLE_BUTTON_SMALL_FONT)

        self.STYLE_BUTTON_MEDIUM_NAME: str = "Custom_Medium.TButton"
        self.STYLE_BUTTON_MEDIUM_FONT: tkfont.Font = tkfont.Font(family="Arial", size=12, weight=tkfont.BOLD)
        self.__class__._style_instance.configure(style=self.STYLE_BUTTON_MEDIUM_NAME, font=self.STYLE_BUTTON_MEDIUM_FONT)

        self.FONT_SCROLLED_TEXT_MEDIUM: tkfont.Font = tkfont.Font(family="Courier New", size=12, weight=tkfont.BOLD)
        self.FONT_LABEL_HEADING_MEDIUM: tkfont.Font = tkfont.Font(family="Arial", size=16, weight=tkfont.BOLD)
        self.FONT_LABEL_NORMAL_SMALL: tkfont.Font = tkfont.Font(family="Courier New", size=12, weight=tkfont.BOLD)

    @classmethod
    def get_instance(cls) -> "CustomTkinterStyles":
        """
        If a CustomTkinterStyles instance is already present - this function will return it
        If it is not already present - this function will create it and then return it
        """
        if cls._instance is None:
            cls._instance = CustomTkinterStyles()
        return cls._instance

    _instance: Union["CustomTkinterStyles", None] = None
    _style_instance: Union[ttk.Style, None] = None
    singleton_get_method: Callable[..., "CustomTkinterStyles"] = get_instance
