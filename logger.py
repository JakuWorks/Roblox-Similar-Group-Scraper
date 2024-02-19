from dataclasses import dataclass
from protocols import SupportsStr
from typing import Callable, Iterable

DEFAULT_DEBUG_MESSAGES_PREFIX: str = ":"
DEFAULT_ADDITIONAL_SPACES: int = 1
DEFAULT_IMPORTANCE_INDENT_MULTIPLIER: int = 2

LOGGER_ENABLE_MESSAGES: bool = True


@dataclass
class LoggerBuilder:
    messages_enabled: bool
    messages_prefix: str = DEFAULT_DEBUG_MESSAGES_PREFIX
    messages_additional_spaces: int = DEFAULT_ADDITIONAL_SPACES
    importance_indent_multiplier: int = DEFAULT_IMPORTANCE_INDENT_MULTIPLIER

    def build(self) -> "Logger":
        return Logger(builder=self)


class Logger:
    """
    This class is used to handle debug messages throughout the project
    'But why not just use print()?' - You ask'
    In case we want to implement more debug logging features - we could simply edit this class to do it
    instead of having to Ctrl+F and replace all these prints that would be scattered all throughout the code
    """

    def __init__(self, builder: LoggerBuilder) -> None:
        self.messages_enabled: bool = builder.messages_enabled
        self.messages_prefix: str = builder.messages_prefix
        self.messages_additional_spaces: int = builder.messages_additional_spaces
        self.importance_indent_multiplier: int = builder.importance_indent_multiplier

        self.log("Debug Messenger Initialized", 0)

    def write_message(self, message: str) -> None:
        # Better safe safe than sorry with the amount of abstraction I guess
        print(message)

    def log(self, message: str, importance: int, _is_child_of_logged_iterable: bool = False) -> None:
        """This is the main function to 'put' your log messages into. Use this function for every debug message you want to write
        Args:
            message (str): Message To Write (it will be formatted a bit)
            importance (int): 0 is max important; 1 is less important; 2 is even less important; and so on
            _is_child_of_logged_list (bool): Private argument to decide how the log is processed internally
        """
        # _is_child_of_logged_list is currently unused

        if self.messages_enabled:
            message_formatted_step1: str = self.messages_prefix + message
            additional_spaces: int = (importance + self.messages_additional_spaces) * self.importance_indent_multiplier
            message_formatted_step2: str = additional_spaces * " " + message_formatted_step1
            message_formatted: str = message_formatted_step2

            self.write_message(message=message_formatted)

    def log_iterable(self, iterable: Iterable[SupportsStr], importance: int) -> None:
        for value in iterable:
            message: str = " - " + str(value)
            self.log(message=message, importance=importance, _is_child_of_logged_iterable=True)


LOGGER_BUILDER: LoggerBuilder = LoggerBuilder(messages_enabled=LOGGER_ENABLE_MESSAGES)
LOGGER: Logger = LOGGER_BUILDER.build()
LOG: Callable[[str, int], None] = LOGGER.log
