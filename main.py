"""
Roblox ERP & Fetish Groups Finder
"""

# Example group: 3070057
# Example link:  https://www.roblox.com/groups/3070057/Doges-fangroup#!/about

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from input_gui import InputGui, InputGuiBuilder
from typing import Set, FrozenSet, Iterator, Iterable, Tuple
from logger import LOG
import scraper


# DO NOT USE ANY MODULES THAT REQUIRE MANUAL INSTALLATION
# USE __ONLY__ VANILLA MODULES THAT ARE INCLUDED WITH PYTHON
# CODE MUST SUPPORT PYTHON 3.10 AND UP
# USE TYPE HINTS
# WRITE CLEAN, GOOD AND OPTIMIZED CODE

# Linters used while writing:
#   VSCode Extensions
# Code spell checker (checks orthography)
# Python
# Pylance
# Mypy (the original extension made by Matan Gover NOT THE MICROSOFT VERSION)

# Formatters used while writing:
# Black Formatter (by Microsoft)
# Custom formatter settings: (just add this line to your settings.json)
"""
"black-formatter.args": [
  "--line-length",
  "150"
]
"""


# Do not increase - Roblox will rate limit you
DEFAULT_PARALLEL_MAX_WORKERS_GET_GROUPS_MEMBERS_IDS: int = 2
DEFAULT_PARALLEL_MAX_WORKERS_GET_RELATED_GROUPS_IDS: int = 1
DEFAULT_PARALLEL_MAX_WORKERS_GET_GROUPS_NAMES: int = 1

DEFAULT_OUTPUT_ADD_GROUP_NAMES: bool = False  # This will extend the scraping time twice
DEFAULT_OUTPUT_HEADING: str = "Occurrences - Group Id"


def get_groups_ids(our_input_gui: InputGui) -> Set[int]:
    user_input: str = our_input_gui.wait_for_user_answer()
    ids: Set[int] = our_input_gui.convert_raw_input(user_input=user_input)
    our_input_gui.close()
    return ids


def get_groups_members_ids(groups_ids: Set[int], parallel_max_workers: int = DEFAULT_PARALLEL_MAX_WORKERS_GET_GROUPS_MEMBERS_IDS) -> Set[int]:
    with ThreadPoolExecutor(max_workers=parallel_max_workers) as executor:
        groups_members_ids_map: Iterator = executor.map(scraper.get_group_members, groups_ids)

    groups_members_ids: Set[int] = set().union(*groups_members_ids_map)
    return groups_members_ids


def get_related_groups_to_users(users_ids: Set[int], parallel_max_workers: int = DEFAULT_PARALLEL_MAX_WORKERS_GET_RELATED_GROUPS_IDS) -> Iterable[Tuple[int, int]]:
    with ThreadPoolExecutor(max_workers=parallel_max_workers) as executor:
        users_groups_map: Iterator = executor.map(scraper.get_user_groups_ids, users_ids)
        users_groups: Set[FrozenSet[int]] = {*users_groups_map}

    LOG("Counting Occurrences!", 1)
    counter: Counter = Counter(group for groups_set in users_groups for group in groups_set)

    LOG("Sorting Occurrences!", 1)
    counter_sorted: Iterable[Tuple[int, int]] = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    return counter_sorted


def get_file_name_from_time(time: datetime) -> str:
    return f"Y-{time.year} M-{time.month} D-{time.day} H-{time.hour} M-{time.minute} S-{time.second}"


def convert_group_occurrence_to_human_readable_string(occurrence: Tuple[int, int], add_group_name: bool = DEFAULT_OUTPUT_ADD_GROUP_NAMES) -> str:
    text: str = f"{occurrence[1]} - {occurrence[0]}"

    if add_group_name:
        group_name: str = scraper.get_group_name_from_id(group_id=occurrence[0])
        text = f"{text} ({group_name})"

    return text


def save_groups_occurrences_data_to_file(occurrences: Iterable[Tuple[int, int]], output_heading: str = DEFAULT_OUTPUT_HEADING, parallel_max_workers: int = DEFAULT_PARALLEL_MAX_WORKERS_GET_GROUPS_NAMES) -> None:
    current_time: datetime = datetime.now()
    name_from_time: str = get_file_name_from_time(time=current_time)
    filename: str = f"SCAN {name_from_time}"

    LOG(f"SAVING SCAN AS '{filename}'", 1)

    output_text_heading: str = output_heading

    with ThreadPoolExecutor(max_workers=DEFAULT_PARALLEL_MAX_WORKERS_GET_GROUPS_NAMES) as executor:
        output_text_groups_map: Iterator = executor.map(convert_group_occurrence_to_human_readable_string, occurrences)

    output_text_groups: str = "\n".join(output_text_groups_map)

    output_text: str = "\n".join([output_text_heading, output_text_groups])

    path = rf".\results\{filename}.txt"

    with open(file=path, mode="wt") as file:
        file.write(output_text)


def main() -> None:
    LOG("Main Script Start", 0)

    LOG("Creating Input Gui", 1)

    our_input_gui_builder: InputGuiBuilder = InputGuiBuilder()

    our_input_gui: InputGui = our_input_gui_builder.build()

    groups_ids: Set[int] = get_groups_ids(our_input_gui=our_input_gui)
    users_ids: Set[int] = get_groups_members_ids(groups_ids=groups_ids)
    related_groups_scored: Iterable[Tuple[int, int]] = get_related_groups_to_users(users_ids=users_ids)
    save_groups_occurrences_data_to_file(occurrences=related_groups_scored)

    LOG("Main Script End", 0)

    try:
        input("Press Enter To Exit!\n")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
