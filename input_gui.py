"""
This script handles the entire gui that gets the groups IDs
"""

# Code Sexiness Rules for this file:
# - When packing, always define arguments in this order: expand, fill, side
# - Stick to only one type of tkinter objects. Use either tk.Frame or ttk.Frame NOT BOTH. Unless you do it to make the gui look better

import tkinter as tk  # tk stands for 'Tkinter'
from tkinter import ttk  # tkk stands for 'Themed Tkinter'
from scrolledtext_with_hint import ScrolledTextWithHint
from custom_tkinter_styling import CustomTkinterStyles
from information_gui import InformationGuiSingleton, InformationGuiAppearance

from typing import Union, Set, Any
from dataclasses import dataclass, field
import re

from logger import LOG, LOGGER


# Tkinter makes guis so easy it feels like cheating

# Keep only the important variables here that a non-pythonist would like to edit


tab_raw_information_gui_data: InformationGuiAppearance = InformationGuiAppearance(
    window_title="Raw Input Guide",
    text_heading="Raw Input Guide",
    text_main="""In this tab you input the Groups IDs/URLs
and this script will attempt to find similar ones.
The script will:
1. Make a list of each player from within inputted groups
2. Make a list of each Roblox group these players are in
3. Count the occurrences of each group
4. Save the results to a file""",
)

tab_fancy_information_gui_data: InformationGuiAppearance = InformationGuiAppearance(
    window_title="Fancy Input Guide",
    text_heading="Fancy Input Guide",
    text_main="""TODO""",
)


@dataclass
class InputGuiBuilder:

    window_title: str = "Roblox ERP Groups Finder"
    window_size: str = "1000x800"  # Width x Height

    tab_raw_information_gui_data: InformationGuiAppearance = field(default_factory=lambda: tab_raw_information_gui_data)
    tab_raw_name: str = "Raw Input"
    tab_raw_button_import_from_fancy_name: str = "Import Content From Fancy Tab"
    tab_raw_button_scan_name: str = "Scan Using Raw Input"
    tab_raw_button_help_name: str = "Help"
    tab_raw_text_box_hint_text: str = """Input ID/URL for each Roblox Group you want to include in the search.
    You must separate them by either:
    1. New Line
    2. " " Space
    3. "," Comma
    4. ";" Semicolon

    Example:
3982592, 9760527 5211428 15772045; 10249200
3341679, https://www.roblox.com/groups/3059674/Badimo#!/about; https://www.roblox.com/groups/5126818/Interbyte-Studio#!/about
3870049
2748390
3755133 2856593"""

    tab_fancy_information_gui_class: InformationGuiAppearance = field(default_factory=lambda: tab_fancy_information_gui_data)
    tab_fancy_name: str = "Fancy Input"
    tab_fancy_button_import_from_raw_name: str = "Import Content From Raw Tab"
    tab_fancy_button_scan_name: str = "Scan Using Fancy Input"
    tab_fancy_button_help_name: str = "Help"

    def build(self) -> "InputGui":
        return InputGui(builder=self)


class InputGui:
    _raw_input_conversion_url_search_regex: Union[re.Pattern[str], None] = None
    _raw_input_conversion_digits_search_regex: Union[re.Pattern[str], None] = None

    def __init__(self, builder: InputGuiBuilder) -> None:
        self.tab_raw_information_gui_data: InformationGuiAppearance = builder.tab_raw_information_gui_data
        self.tab_fancy_information_gui_data: InformationGuiAppearance = builder.tab_fancy_information_gui_class

        self.tab_raw_separator_characters: Set[str] = {"\n", ",", ";", " "}

        LOG("Creating Input GUI Root", 2)
        self.root: tk.Tk = tk.Tk()

        self.input_callback: tk.StringVar = tk.StringVar(master=self.root)

        LOG(f"Creating Custom Styles And Fonts", 2)
        self.CSF: CustomTkinterStyles = CustomTkinterStyles.get_instance()  # CSF - stands for 'Custom Styles and Fonts'

        LOG("Setting Window Title", 2)
        self.root.title(string=builder.window_title)

        LOG("Setting Window Geometry", 2)
        self.root.geometry(newGeometry=builder.window_size)

        LOG("Creating MainFrame", 2)
        self.mainframe: ttk.Frame = ttk.Frame(master=self.root)
        self.mainframe.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        LOG("Creating Window Tabs Notebook", 3)
        self.tabs_notebook: ttk.Notebook = ttk.Notebook(master=self.mainframe)
        self.tabs_notebook.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        # UNCOMMENT LATER TODO AFTER DOING BACKEND
        # self.initialize_tab_fancy(builder=builder)

        self.initialize_tab_raw(builder=builder)

    def initialize_tab(self, tab_name: str) -> ttk.Frame:
        LOG(f"Creating Frame - '{tab_name}'", 5)
        tab_frame: ttk.Frame = ttk.Frame(master=self.tabs_notebook)

        LOG(f"Adding Tab To Tabs Notebook - '{tab_name}'", 5)
        self.tabs_notebook.add(child=tab_frame, text=tab_name)

        return tab_frame

    def initialize_tab_raw(self, builder: InputGuiBuilder) -> None:
        self.tab_raw_name: str = builder.tab_raw_name

        LOG(f"Initializing Tab '{self.tab_raw_name}'", 4)
        self.tab_raw: ttk.Frame = self.initialize_tab(tab_name=self.tab_raw_name)

        LOG(f"Creating 1'st Subframe - '{self.tab_raw_name}'", 5)
        self.tab_raw_subframe1: ttk.Frame = ttk.Frame(master=self.tab_raw)
        self.tab_raw_subframe1.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=15, pady=15)

        # UNCOMMENT AND FIX LATER TODO WHEN FANCY TAB IS MADE
        # LOG(f"Creating '{TAB_RAW_BUTTON_IMPORT_FROM_FANCY_NAME}' Button - '{self.tab_raw_name}'", 6)
        # self.tab_raw_button_import_from_fancy: ttk.Button = ttk.Button(master=self.tab_raw_subframe1,
        #                                                                text=TAB_RAW_BUTTON_IMPORT_FROM_FANCY_NAME,
        #                                                                style=self.CSF.STYLE_BUTTON_SMALL_NAME,
        #                                                                command=self.tab_raw_import_ids_from_fancy)
        # self.tab_raw_button_import_from_fancy.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT,
        #                                            ipadx=10, ipady=10)

        LOG(f"Creating 2'nd Subframe - '{self.tab_raw_name}'", 5)
        self.tab_raw_subframe2: ttk.Frame = ttk.Frame(master=self.tab_raw)
        self.tab_raw_subframe2.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        LOG(f"Creating Input Box - '{self.tab_raw_name}'", 6)
        self.tab_raw_text_box: ScrolledTextWithHint = ScrolledTextWithHint(
            master=self.tab_raw_subframe2,
            hint_text=builder.tab_raw_text_box_hint_text,
            hint_color="grey",
            font=self.CSF.FONT_SCROLLED_TEXT_MEDIUM,
        )
        self.tab_raw_text_box.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=70, pady=30)

        LOG(f"Creating 3'rd Subframe - '{self.tab_raw_name}'", 5)
        self.tab_raw_subframe3: ttk.Frame = ttk.Frame(master=self.tab_raw)
        self.tab_raw_subframe3.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=15, pady=15)

        LOG(f"Creating '{builder.tab_raw_button_help_name}' Button - '{self.tab_raw_name}'", 6)
        self.tab_raw_button_help: ttk.Button = ttk.Button(
            master=self.tab_raw_subframe3,
            text=builder.tab_raw_button_help_name,
            style=self.CSF.STYLE_BUTTON_MEDIUM_NAME,
            command=self.tab_raw_display_help,
        )
        self.tab_raw_button_help.pack(expand=False, fill=tk.BOTH, side=tk.LEFT, ipadx=10, ipady=10)

        LOG(f"Creating '{builder.tab_raw_button_scan_name}' Button - '{self.tab_raw_name}'", 6)
        self.tab_raw_button_scan: ttk.Button = ttk.Button(
            master=self.tab_raw_subframe3,
            text=builder.tab_raw_button_scan_name,
            style=self.CSF.STYLE_BUTTON_MEDIUM_NAME,
            command=self.tab_raw_return,
        )
        self.tab_raw_button_scan.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT, ipadx=10, ipady=10)

    def initialize_tab_fancy(self, builder: InputGuiBuilder) -> None:
        self.tab_fancy_name: str = builder.tab_fancy_name

        LOG(f"Initializing Tab '{self.tab_fancy_name}'", 4)
        self.tab_fancy: ttk.Frame = self.initialize_tab(tab_name=self.tab_fancy_name)

        LOG(f"Creating 1'st Subframe - '{self.tab_fancy_name}'", 5)
        self.tab_fancy_subframe1: ttk.Frame = ttk.Frame(master=self.tab_fancy)
        self.tab_fancy_subframe1.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=15, pady=15)

        LOG(f"Creating '{builder.tab_fancy_button_import_from_raw_name}' Button - '{self.tab_fancy_name}'", 6)
        self.tab_fancy_button_import_from_raw: ttk.Button = ttk.Button(
            master=self.tab_fancy_subframe1,
            text=builder.tab_fancy_button_import_from_raw_name,
            style=self.CSF.STYLE_BUTTON_SMALL_NAME,
            command=self.tab_fancy_import_ids_from_raw,
        )
        self.tab_fancy_button_import_from_raw.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT, ipadx=10, ipady=10)

        LOG(f"Creating 2'nd Subframe - '{self.tab_fancy_name}'", 5)
        self.tab_fancy_subframe2: ttk.Frame = ttk.Frame(master=self.tab_fancy)
        self.tab_fancy_subframe2.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        LOG(f"Creating Fancy Label Subframe inside 2'nd Subframe - '{self.tab_fancy_name}'", 6)
        self.tab_fancy_label_subframe: ttk.Frame = ttk.Frame(master=self.tab_fancy_subframe2)
        self.tab_fancy_label_subframe.pack(expand=False, fill=tk.BOTH, side=tk.TOP)

        # self.tab_fancy_label_manager: fancy_labels.FancyLabelManager = fancy_labels.FancyLabelManager(master=self.tab_fancy_label_subframe)
        # self.tab_fancy_label_manager.add()

        LOG(f"Creating 3'rd Subframe - '{self.tab_fancy_name}'", 5)
        self.tab_fancy_subframe3: ttk.Frame = ttk.Frame(master=self.tab_fancy)
        self.tab_fancy_subframe3.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=15, pady=15)

        LOG(f"Creating '{builder.tab_fancy_button_help_name}' Button - '{self.tab_fancy_name}'", 6)
        self.tab_fancy_button_help: ttk.Button = ttk.Button(
            master=self.tab_fancy_subframe3,
            text=builder.tab_fancy_button_help_name,
            style=self.CSF.STYLE_BUTTON_MEDIUM_NAME,
            command=self.tab_fancy_display_help,
        )
        self.tab_fancy_button_help.pack(expand=False, fill=tk.BOTH, side=tk.LEFT, ipadx=10, ipady=10)

        LOG(f"Creating '{builder.tab_fancy_button_scan_name}' Button - '{self.tab_fancy_name}'", 6)
        self.tab_fancy_button_scan: ttk.Button = ttk.Button(
            master=self.tab_fancy_subframe3,
            text=builder.tab_fancy_button_scan_name,
            style=self.CSF.STYLE_BUTTON_MEDIUM_NAME,
            command=self.tab_fancy_return,
        )
        self.tab_fancy_button_scan.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT, ipadx=10, ipady=10)

    def tab_raw_import_ids_from_fancy(self) -> None:
        # Separate the conversion and the importing, so you can reuse the conversion in tab_fancy_return
        pass

    def tab_fancy_import_ids_from_raw(self) -> None:
        pass

    def tab_raw_return(self) -> None:
        self.input_callback.set(value=self.tab_raw_text_box.get_current_text())

    def tab_fancy_return(self) -> None:
        # Convert data from fancy to raw using the function
        # Then handle it just as raw input data
        pass

    def convert_raw_input(self, user_input: str) -> Set[int]:
        LOG("Converting User Input!", 2)

        with_commas_replaced: str = user_input

        for char in self.tab_raw_separator_characters:
            with_commas_replaced = with_commas_replaced.replace(char, "\n")

        lines: Set[str] = set(with_commas_replaced.splitlines())

        ids_map: map[int] = map(self.convert_line_of_raw_input, lines)
        ids: Set[int] = set(ids_map)

        if 0 in ids:
            ids.remove(0)

        LOG(f"Received IDs:", 1)
        LOGGER.log_iterable(iterable=ids, importance=2)

        return ids

    @classmethod
    def get_raw_input_conversion_url_search_pattern_compiled(cls) -> re.Pattern[str]:
        if cls._raw_input_conversion_url_search_regex is None:
            cls._raw_input_conversion_url_search_regex = re.compile(pattern=r"(?<=groups/)\d+")

        return cls._raw_input_conversion_url_search_regex

    @classmethod
    def get_raw_input_conversion_digits_search_pattern_compiled(cls) -> re.Pattern[str]:
        if cls._raw_input_conversion_digits_search_regex is None:
            cls._raw_input_conversion_digits_search_regex = re.compile(pattern=r"\d+")

        return cls._raw_input_conversion_digits_search_regex

    def convert_line_of_raw_input(self, line: str) -> int:
        LOG(f"Converting Line: '{line}'", 3)

        # Try check if line isdigit
        if line.isdigit():
            return int(line)

        # Try to match the url
        url_id_search_pattern: re.Pattern[str] = self.__class__.get_raw_input_conversion_url_search_pattern_compiled()
        url_id_search_match: Union[re.Match, None] = url_id_search_pattern.search(string=line)
        if url_id_search_match is not None:
            return int(url_id_search_match.group(0))

        # Select the biggest int (last resort) (a group id is usually a big number)
        digits_search_pattern: re.Pattern[str] = self.__class__.get_raw_input_conversion_digits_search_pattern_compiled()
        digits_search_matches: list[str] = digits_search_pattern.findall(string=line)
        if len(digits_search_matches) > 0:
            digits_search_results: Set[int] = {int(x) for x in digits_search_matches if x.isdigit()}
            return max(digits_search_results)

        # Fallback
        return 0

    def tab_raw_display_help(self) -> None:
        InformationGuiSingleton(master=self.tab_raw, appearance=self.tab_raw_information_gui_data)

    def tab_fancy_display_help(self) -> None:
        InformationGuiSingleton(master=self.tab_fancy, appearance=self.tab_fancy_information_gui_data)

    def wait_for_user_answer(self) -> str:
        LOG("Waiting For User Answer!", 1)
        self.root.wait_variable(name=self.input_callback)
        return self.input_callback.get()

    def close(self) -> None:
        self.root.destroy()
