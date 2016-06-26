import requests
import json
import os

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

# ERROR DECLARATIONS
# XXX Stick these in a map to simplify lookup
GS_ERROR_GAME_OR_EVENT_UNSPECIFIED = (0, "Game or event string not specified")
GS_ERROR_GAME_UNSPECIFIED = (1, "Game string not specified")
GS_ERROR_GAME_OR_EVENT_MALFORMED = (2, "Game or event string contains disallowed characters. Allowed are upper-case A-Z, 0-9, hyphen, and underscore")
GS_ERROR_GAME_MALFORMED = (3, "Game string contains disallowed characters. Allowed are upper-case A-Z, 0-9, hyphen, and underscore")
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

class GameSense(object):
	def __init__(self, game, game_display_name):
		super(GameSense, self).__init__()
		self.__address = self.__find_gamesense_data()
		self.game = game
		self.game_display_name = game_display_name

	def __find_gamesense_data(self):
		platform = os.name
		prop_path = ""

		if platform == "nt":
			prop_path = os.path.expandvars(GS_CORE_PROPS_WINDOWS)
		elif platform == "mac":
			prop_path = os.path.expandvars(GS_CORE_PROPS_OSX)
		else:
			raise GameSenseNotPresentException("GameSense is not supported on platform '{}'".format(platform))

		if os.path.isfile(prop_path):
			prop_file = None

			try:
				prop_file = open(prop_path)
			except OSError as e:
				raise GameSenseNotPresentException("Could not open GameSense properties file")

			prop_data = json.loads(prop_file.read())
			unsecure_address = "http://{address}".format(address=prop_data["address"])
			return unsecure_address
		else:
			raise GameSenseNotPresentException("GameSense properties file missing")
		
	def create_message(self, endpoint):
		message = GameSenseMessage(self.game, endpoint)
		message["game"] = self.game
		return message

	def post(self, message):
		url = "{address}{endpoint}".format(address=self.__address, endpoint=message.endpoint)

		if "game" not in message:
			raise KeyError("Mandatory key 'game' missing")

		api_response = requests.post(url, json=message.message_data)
		response = GameSenseResponse(success=api_response.status_code == 200, data=api_response.json())
		return response

	def register_game(self, icon_color_id=GS_ICON_ORANGE):
		message = self.create_message(GS_ENDPOINT_GAME_METADATA)
		message["game"] = self.game
		message["game_display_name"] = self.game_display_name
		message["icon_color_id"] = icon_color_id
		return self.post(message)

	def register_event(self, event_name, min_value=0, max_value=100, icon_id=GS_ICON_ORANGE):
		message = self.create_message(GS_ENDPOINT_REGISTER_EVENT)
		message["event"] = event_name
		message["min_value"] = min_value
		message["max_value"] = max_value
		message["icon_id"] = icon_id
		return self.post(message)

	def send_event(self, event_name, data):
		message = self.create_message(GS_ENDPOINT_GAME_EVENT)
		message["event"] = event_name
		message["data"] = data
		return self.post(message)

class GameSenseMessage(object):
	def __init__(self, game, endpoint):
		super(GameSenseMessage, self).__init__()
		self.endpoint = endpoint
		self.__data = {}

	@property
	def message_data(self):
		return self.__data
	
	def __getitem__(self, index):
		return self.__data[index]

	def __setitem__(self, index, value):
		self.__data[index] = value

	def __contains__(self, value):
		return value in self.__data

	def __repr__(self):
		return "ENDPOINT: {endpoint}, DATA: {data}".format(endpoint=self.endpoint, data=json.dumps(self.__data))

class GameSenseResponse(object):
	def __init__(self, success, data):
		super(GameSenseResponse, self).__init__()
		self.success = success
		self.data = data

def main():
	gs = GameSense("PYTHON_SDK", "Python SDK")
	gs.register_game(icon_color_id=GS_ICON_GOLD)

	response = gs.register_event("DID_STUFF")
	if response.success:
		print(response.data)

	response = gs.send_event("DID_STUFF", {"value": 22})
	if response.success:
		print(response.data)

if __name__ == '__main__':
	main()