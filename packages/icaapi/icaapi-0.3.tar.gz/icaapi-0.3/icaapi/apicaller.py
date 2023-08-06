
import requests


from .const import (
    AUTH_URL,
    AUTH_TICKET,
    SHOPPING_URL,
    LIST_NAME,  
    ITEM_LIST,
    ITEM_NAME,
    AUTH_URL,
    SHOPPING_URL,
    GET_LISTS,
    IS_CHECKED
)


def get_auth_key(user, psw):
    url = AUTH_URL
    auth = (user, psw)
    response = requests.get(url, auth = auth)
    if response:
        return response.headers[AUTH_TICKET]
    return None

def get_shopping_list(auth_key):
    url = SHOPPING_URL
    headers = {AUTH_TICKET:auth_key}
    response = requests.get(url, headers=headers)
    if response:
        return response.json()
    print(response.headers)
    return None

class ICAapi:
    ### Class to retrieve and hold the data for a Shopping list from ICA ###
    def __init__(self, user, psw):
        self._auth_key = get_auth_key(user, psw)
        self._raw_shopping_list = get_shopping_list(self._auth_key).get(GET_LISTS)

    @property
    def lists(self):
        lists = []
        for item in self._raw_shopping_list:
            lists.append(item[LIST_NAME])
        return lists

    @property
    def items(self):
        items = []
        for item_list in self._raw_shopping_list:
            for item in item_list.get(ITEM_LIST):
                if item[IS_CHECKED] == False:
                    items.append(item[ITEM_NAME])
        return items

    def items_in_list(self, list_name):
        items = []
        for item_list in self._raw_shopping_list:
            if item_list[LIST_NAME] == list_name:
                for item in item_list.get(ITEM_LIST):
                    if item[IS_CHECKED] == False:
                        items.append(item[ITEM_NAME])
        return items

    def update(self):
        self._raw_shopping_list = get_shopping_list(self._auth_key).get(GET_LISTS)