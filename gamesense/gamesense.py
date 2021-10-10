
import json
import os
import platform

try:
    import requests
    sync_enabled = True
except ImportError:
    sync_enabled = False

try:
    import aiohttp
    async_enabled = True
except ImportError:
    async_enabled = False

# URL DECLARATIONS
GS_CORE_PROPS_WINDOWS = "%ProgramData%\SteelSeries\SteelSeries Engine 3\coreProps.json"
GS_CORE_PROPS_OSX = "/Library/Application Support/SteelSeries Engine 3/coreProps.json"

# ENDPOINT DECLARATIONS
GS_ENDPOINT_GAME_METADATA = "/game_metadata"
GS_ENDPOINT_REGISTER_EVENT = "/register_game_event"
GS_ENDPOINT_BIND_EVENT = "/bind_game_event"
GS_ENDPOINT_GAME_EVENT = "/game_event"
GS_ENDPOINT_REMOVE_EVENT = "/remove_game_event"
GS_ENDPOINT_REMOVE_GAME = "/remove_game"
GS_ENDPOINT_GAME_HEARTBEAT = "/game_heartbeat"

# ICON_DECLARATIONS
GS_ICON_ORANGE = 0
GS_ICON_GOLD = 1
GS_ICON_YELLOW = 2
GS_ICON_GREEN = 3
GS_ICON_TEAL = 4
GS_ICON_LIGHT_BLUE = 5
GS_ICON_BLUE = 6
GS_ICON_PURPLE = 7
GS_ICON_FUSCHIA = 8
GS_ICON_PINK = 9
GS_ICON_RED = 10
GS_ICON_SILVER = 11

# EVENT ICON DECLARATIONS
EVENT_BLANK = 0
EVENT_HEALTH = 1
EVENT_ARMOR = 2
EVENT_AMMO = 3
EVENT_MONEY = 4
EVENT_FLASHBANG = 5
EVENT_KILLS = 6
EVENT_HEADSHOT = 7
EVENT_HELMET = 8
EVENT_HUNGER = 10
EVENT_AIR = 11
EVENT_COMPASS = 12
EVENT_TOOL = 13
EVENT_MANA = 14
EVENT_CLOCK = 15
EVENT_LIGHTNING = 16
EVENT_BACKPACK = 17

# ERROR DECLARATIONS
# XXX Stick these in a map to simplify lookup
GS_ERROR_GAME_OR_EVENT_UNSPECIFIED = (0, "Game or event string not specified")
GS_ERROR_GAME_UNSPECIFIED = (1, "Game string not specified")
GS_ERROR_GAME_OR_EVENT_MALFORMED = (
    2, "Game or event string contains disallowed characters. Allowed are upper-case A-Z, 0-9, hyphen, and underscore")
GS_ERROR_GAME_MALFORMED = (
    3, "Game string contains disallowed characters. Allowed are upper-case A-Z, 0-9, hyphen, and underscore")
GS_ERROR_GAME_EVENT_DATA_EMPTY = (4, "GameEvent data member is empty")
GS_ERROR_TOO_MANY_REGISTRATIONS = (5, "Events for too many games have been registered recently, please try again later")
GS_ERROR_NO_HANDLERS = (6, "One or more handlers must be specified for binding")
GS_ERROR_RESERVED_EVENT = (7, "That event for that game is reserved")
GS_ERROR_RESERVED_GAME = (8, "That game is reserved")
GS_ERROR_UNREGISTERED_EVENT = (9, "That event is not registered")
GS_ERROR_UNREGISTERED_GAME = (10, "That game is not registered")


class GameSenseNotPresentException(Exception):
    def __init__(self, message):
        super(GameSenseNotPresentException, self).__init__(message)


class GameSenseAPIException(Exception):
    def __init__(self, message):
        super(GameSenseAPIException, self).__init__(message)


def gamesense_url():
    plat = platform.system()

    if plat == "Windows":
        prop_path = os.path.expandvars(GS_CORE_PROPS_WINDOWS)
    elif plat == "Darwin":
        prop_path = os.path.expandvars(GS_CORE_PROPS_OSX)
    else:
        raise GameSenseNotPresentException("GameSense is not supported on platform '{}'".format(platform))

    if os.path.isfile(prop_path):
        try:
            with open(prop_path) as prop_file:
                prop_data = json.loads(prop_file.read())
        except OSError:
            raise GameSenseNotPresentException("Could not open GameSense properties file")

        return "http://{address}".format(address=prop_data["address"])
    else:
        raise GameSenseNotPresentException("GameSense properties file missing")


class GameSenseBase(object):
    """
    See https://github.com/SteelSeries/gamesense-sdk/tree/master/doc/api for more information
    """
    def __init__(self, game, game_display_name):
        super(GameSenseBase, self).__init__()
        self._address = gamesense_url()
        self.game = game
        self.game_display_name = game_display_name

    def post(self, endpoint, message):
        pass

    def _register_game_payload(self, icon_color_id):
        return {
            'game': self.game,
            'game_display_name': self.game_display_name,
            'icon_color_id': icon_color_id
        }

    def register_game(self, icon_color_id=GS_ICON_ORANGE):
        """
        Registers this GameSense object with the GameSense API.

        :param icon_color_id: The ID of the icon to use
        :return: The response from the API
        """
        pass

    def _register_event_payload(self, event_name, min_value, max_value, icon_id):
        return {
            'game': self.game,
            'event': event_name,
            'min_value': min_value,
            'max_value': max_value,
            'icon_id': icon_id,
        }

    def register_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK):
        """
        Registers an event under the game that this GameSense object represents.

        :param event_name: The name of the event to register
        :param min_value: The minimum value of this event
        :param max_value: The maximum value of this event
        :param icon_id: The ID of the icon for this event
        :return: The response from the API
        """
        pass

    def _bind_event_payload(self, event_name, min_value, max_value, icon_id, handlers):
        return {
            'game': self.game,
            'event': event_name,
            'min_value': min_value,
            'max_value': max_value,
            'icon_id': icon_id,
            'handlers': handlers
        }

    def bind_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK, handlers=None):
        """
        Binds an event under the game that this GameSense object represents.

        :param event_name: The name of the event to register
        :param min_value: The minimum value of this event
        :param max_value: The maximum value of this event
        :param icon_id: The ID of the icon for this event
        :param handlers: Handlers to bind for this event
        :return: The response from the API
        """
        pass

    def _send_event_payload(self, event_name, data):
        return {
            'game': self.game,
            'event': event_name,
            'data': data
        }

    def send_event(self, event_name, data):
        """
        Sends an event to the GameSense API. The event must have been previously registered or bound.

        :param event_name: The name of the event to send
        :param data: Any data related to the event being sent, should be a dict containing at least 'value'
        :return: The response from the API
        """
        pass

    def _heartbeat_payload(self):
        return {
            'game': self.game,
        }

    def send_heartbeat(self):
        """
        Sends a heartbeat/keepalive event

        :return: The response from the API
        """
        pass


if sync_enabled:
    class GameSense(GameSenseBase):
        def __init__(self, game, game_display_name):
            super(GameSense, self).__init__(game, game_display_name)

        def post(self, endpoint, message):
            url = "{address}{endpoint}".format(address=self._address, endpoint=endpoint)
            api_response = requests.post(url, json=message)
            response = GameSenseResponse(status_code=api_response.status_code, data=api_response.json())
            return response

        def register_game(self, icon_color_id=GS_ICON_ORANGE):
            message = self._register_game_payload(icon_color_id)
            return self.post(GS_ENDPOINT_GAME_METADATA, message)

        def register_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK):
            message = self._register_event_payload(event_name, min_value, max_value, icon_id)
            return self.post(GS_ENDPOINT_REGISTER_EVENT, message)

        def bind_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK, handlers=None):
            message = self._bind_event_payload(event_name, min_value, max_value, icon_id, handlers or [])
            return self.post(GS_ENDPOINT_BIND_EVENT, message)

        def send_event(self, event_name, data):
            message = self._send_event_payload(event_name, data)
            return self.post(GS_ENDPOINT_GAME_EVENT, message)

        def send_heartbeat(self):
            message = self._heartbeat_payload()
            return self.post(GS_ENDPOINT_GAME_HEARTBEAT, message)


if async_enabled:
    class AioGameSense(GameSenseBase):
        def __init__(self, game, game_display_name, session=None):
            super(AioGameSense, self).__init__(game, game_display_name)
            self.session = session or aiohttp.ClientSession()

        async def post(self, endpoint, data):
            url = f'{self._address}{endpoint}'
            async with self.session.post(url, json=data) as resp:
                t = await resp.text()
                resp_json = json.loads(t)  # Wrong content type being returned by GameSense API, manually deserialize
                response = GameSenseResponse(status_code=resp.status, data=resp_json)
                return response

        async def register_game(self, icon_color_id=GS_ICON_ORANGE):
            message = self._register_game_payload(icon_color_id)
            return await self.post(GS_ENDPOINT_GAME_METADATA, message)

        async def register_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK):
            message = self._register_event_payload(event_name, min_value, max_value, icon_id)
            return await self.post(GS_ENDPOINT_REGISTER_EVENT, message)

        async def bind_event(self, event_name, min_value=0, max_value=100, icon_id=EVENT_BLANK, handlers=None):
            message = self._bind_event_payload(event_name, min_value, max_value, icon_id, handlers or [])
            return await self.post(GS_ENDPOINT_BIND_EVENT, message)

        async def send_event(self, event_name, data):
            message = self._send_event_payload(event_name, data)
            return await self.post(GS_ENDPOINT_GAME_EVENT, message)

        async def send_heartbeat(self):
            message = self._heartbeat_payload()
            return await self.post(GS_ENDPOINT_GAME_HEARTBEAT, message)


class GameSenseResponse(object):
    def __init__(self, status_code, data):
        super(GameSenseResponse, self).__init__()
        self.status_code = status_code
        self.data = data

    @property
    def success(self):
        return 200 <= self.status_code < 300
