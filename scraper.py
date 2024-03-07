from typing import Union, TypedDict, Dict, Any, Mapping, Literal, TypeAlias, Set, List, FrozenSet
import urllib
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import inspect
from logger import LOG

group_users_step: TypeAlias = Literal[10, 25, 50, 100]
urlopen_timeout: TypeAlias = Union[None, float]
UrlopenRet: TypeAlias = Any

GET_GROUP_USERS_STEP: group_users_step = 100

# If the call times out - the script will probably throw an error
DEFAULT_TIMEOUT_GET_GROUP_MEMBERS: urlopen_timeout = None
DEFAULT_TIMEOUT_GET_USER_GROUPS_IDS: urlopen_timeout = None
DEFAULT_TIMEOUT_GET_GROUP_NAME: urlopen_timeout = None
DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS: int = 8
DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES: int = 3


class RobloxGetUsersOfGroupUrlParams(TypedDict):
    limit: int
    cursor: Union[None, str]


def urlopen_with_retries(max_tries: int = DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES, retry_interval_seconds: int = DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS, *args, **kwargs) -> UrlopenRet:
    """*args and **kwargs will be passed to the urlopen function"""

    urlopen_signature: inspect.Signature = inspect.signature(urllib.request.urlopen)
    urlopen_bound_args: inspect.BoundArguments = urlopen_signature.bind(*args, **kwargs)
    url_that_is_being_opened: str = urlopen_bound_args.arguments["url"]  # Trying to use .get will make mypy complain

    for i in range(max_tries):
        retry_number: int = i + 1
        tries_left: int = max_tries - retry_number

        try:
            raise RuntimeError("DEBUG")
            return urllib.request.urlopen(*args, **kwargs)
        except:
            # Usually the exception is either a rate limit or a bad gateway (502 status code)
            LOG(f"RECEIVED AN ERROR WHILE OPENING URL '{url_that_is_being_opened}'. The script will to retry in {retry_interval_seconds}, {tries_left} more times... (this is usually a rate limit or a bad gateway error)", 2)

            # I understand that this function will be called concurrently. This is (probably) not a problem. We will just make that concurrent thread sleep
            time.sleep(retry_interval_seconds)

            LOG(f"Retrying opening URL - '{url_that_is_being_opened}' - Retry number {retry_number}/{max_tries}", 2)

        LOG(f"Failed to open the URL. Skipping the call!!! - {url_that_is_being_opened}", 2)


def encode_url_with_params(url: str, params: Mapping[Any, Any]) -> str:
    # Note: the .urlencode function uses str() for all of the keys and values of the params dictionary
    return f"{url}?{urllib.parse.urlencode(query=params)}"


def get_group_members_count(group_id: int) -> int:
    group_info_api_url: str = rf"https://groups.roblox.com/v1/groups/{group_id}"
    response = urlopen_with_retries(max_tries=DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES, retry_interval_seconds=DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS, url=group_info_api_url)
    response_json: Dict = json.load(fp=response)
    members_count: int = int(response_json["memberCount"])
    return members_count


def union_group_members_ids_and_response(users_ids: Set[int], response_json: Dict) -> Set[int]:
    users_ids_of_this_response: Set[int] = {int(user_data["user"]["userId"]) for user_data in response_json["data"]}
    combined_users_ids: Set[int] = users_ids.union(users_ids_of_this_response)
    return combined_users_ids


def get_group_members(group_id: int, timeout: urlopen_timeout = DEFAULT_TIMEOUT_GET_GROUP_MEMBERS) -> Set[int]:
    # This is not a normal group link. It's an url call to the Roblox's API
    # Here is example output: https://groups.roblox.com/v1/groups/2731732/users

    LOG(f"Getting current amount of group members - '{group_id}'", 2)

    group_users_api_url: str = f"https://groups.roblox.com/v1/groups/{group_id}/users"

    group_members_count: int = get_group_members_count(group_id=group_id)

    step_users: group_users_step = GET_GROUP_USERS_STEP
    current_page_cursor: Union[None, str] = ""
    current_params: RobloxGetUsersOfGroupUrlParams = {"limit": step_users, "cursor": current_page_cursor}
    users_ids: Set[int] = set()

    while True:
        elapsed_users_ids: int = len(users_ids)
        elapsed_percent: float = elapsed_users_ids / group_members_count * 100
        elapsed_percent_rounded: float = round(elapsed_percent, 2)

        LOG(f"Scraping '{group_id}' - Elapsed Users: {elapsed_users_ids}/{group_members_count} ({elapsed_percent_rounded}%) - Cursor: '{current_page_cursor}'", 4)

        if elapsed_users_ids == group_members_count:
            break

        url_with_params: str = encode_url_with_params(url=group_users_api_url, params=current_params)
        response = urlopen_with_retries(max_tries=DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES, retry_interval_seconds=DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS, url=url_with_params, timeout=timeout)
        status_code: int = response.getcode()

        if status_code != 200:
            raise RuntimeError(f"RESPONSE IS NOT 200!!! It's '{status_code}' - Getting Group '{group_id}'")

        response_json: Dict = json.load(fp=response)
        users_ids = union_group_members_ids_and_response(users_ids=users_ids, response_json=response_json)

        # Setting new cursor
        current_page_cursor = response_json["nextPageCursor"]
        current_params["cursor"] = current_page_cursor

    return users_ids


class GettingUsersGroupsIdsOperation:
    def __init__(self, total_users_count: int) -> None:
        LOG("Starting the getting groups of players operation", 2)

        self.total_users_count: int = total_users_count
        self.processed_users_count: int = 0

    def get_user_groups_ids(self, user_id: int, timeout: urlopen_timeout = DEFAULT_TIMEOUT_GET_USER_GROUPS_IDS) -> FrozenSet[int]:
        self.processed_users_count = self.processed_users_count + 1
        current_processed_users_decimal: float = self.processed_users_count / self.total_users_count
        current_processed_users_percent: float = current_processed_users_decimal * 100
        current_processed_users_percent_rounded: float = round(current_processed_users_percent, 2)

        LOG(f"Getting groups IDs - user '{user_id}' - {self.processed_users_count}/{self.total_users_count} ({current_processed_users_percent_rounded}%)", 3)

        user_groups_api_url: str = rf"https://groups.roblox.com/v1/users/{user_id}/groups/roles"  # v2 has rate limit! (note: v2 has a rate limit of 50 per [unknown delay]. v1 seems to have a higher limit)

        response: urllib.request._UrlopenRet = urlopen_with_retries(max_tries=DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES, retry_interval_seconds=DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS, url=user_groups_api_url, timeout=timeout)
        status_code: int = response.getcode()

        if status_code != 200:
            raise RuntimeError(f"RESPONSE IS NOT 200!!! It's '{status_code}' - Getting User Groups '{user_id}'")

        response_json: Dict = json.load(fp=response)
        groups: List[Dict] = response_json["data"]
        groups_ids: FrozenSet[int] = frozenset({int(group["group"]["id"]) for group in groups})

        return groups_ids


def get_group_name_from_id(group_id: int, timeout: urlopen_timeout = DEFAULT_TIMEOUT_GET_GROUP_NAME):
    LOG(f"Getting group name - '{group_id}'", 4)

    api_url: str = rf"https://groups.roblox.com/v1/groups/{group_id}"

    response = urlopen_with_retries(max_tries=DEFAULT_URL_GET_ERROR_MAXIMUM_TRIES, retry_interval_seconds=DEFAULT_URL_GET_ERROR_RETRY_INTERVAL_SECONDS, url=api_url, timeout=timeout)
    status_code: int = response.getcode()

    if status_code != 200:
        raise RuntimeError(f"RESPONSE IS NOT 200!!! It's '{status_code}' - Getting Group Name ''{group_id}")

    response_json: Dict = json.load(fp=response)
    group_name: str = response_json["name"]
    return group_name
