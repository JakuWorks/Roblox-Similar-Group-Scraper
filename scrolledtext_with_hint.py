import tkinter as tk
from tkinter import scrolledtext
from typing import Any


class ScrolledTextWithHint(scrolledtext.ScrolledText):
    # Your code editor will not like this way of extending a class
    # It will not hint most of the argument names when creating an instance of ScrolledTextWithHint
    # It will only hint the hint_text and hint_color arguments

    def __init__(self, hint_text: str, hint_color: str, *args, **kwargs) -> None:
        """Constructor of the extended ScrolledText class

        Example usage:
        ScrolledTextWithHint(hint_tex"="ab", hint_color="red", master=root, bg="blue", width=500, padx=50)
        You can pass other arguments like if you were creating a normal ScrolledText

        Args:
            hint_text (str): Hint Text
            hint_color (str): Color of Hint Text
            *args: Represents all the Positional Arguments of the original ScrolledText element
            **kwargs: Represents all the Keyword Arguments of the original ScrolledText element
        """

        super().__init__(*args, **kwargs)
        self.hint_text: str = hint_text
        self.hint_foreground_color: str = hint_color
        self.hint_is_displayed: bool = False
        self.normal_foreground: Any = self.cget(key="foreground")

        self.bind(sequence="<FocusIn>", func=self.on_focus_in)
        self.bind(sequence="<FocusOut>", func=self.on_focus_out)
        self.on_focus_out()

    def on_focus_in(self, *args) -> None:
        # These *args are here because the .bind function will call this function and give it additional data
        # by using the arguments of this function. We don't care about their data, so we dump all of it into the args tuple.
        current_text: str = self.get_current_text()

        if current_text == self.hint_text:
            # Note Tkinter's code: _TextIndex: TypeAlias = _tkinter.Tcl_Obj | str | float | Misc
            # Tip: Ctrl+Click on a class/object/instance/whatever to go to its definition
            self.hint_is_displayed = False
            self.delete(index1="1.0", index2="end-1c")
            self.configure(foreground=self.normal_foreground)

    def on_focus_out(self, *args) -> None:
        # . *args is here for the same reason as above
        current_text: str = self.get_current_text()

        if current_text == "":
            self.hint_is_displayed = True
            self.insert(index=tk.END, chars=self.hint_text)
            self.configure(foreground=self.hint_foreground_color)

    def get_current_text(self) -> str:
        # Just some handy method to avoid using the more complicated get method.
        return self.get(index1="1.0", index2="end-1c")
