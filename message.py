import json

SERVER_OPCODE = {
	'ERROR' : 0,
	'WELCOME' : 1,
	'LIST_ROOMS_RESP' : 3,
	'LIST_USER_RESP' : 5,
	'TELL_MSG' : 9
}

CLIENT_OPCODE = {
	'LIST_ROOMS' : 2,
	'LIST_USERS' : 4,
	'SEND_MSG' : 8
}


class Message:
	def __init__(self, opcode, data):
		self.message = {
			"opcode": opcode,
			"data": data
		}

	def get_json_str(self):
		return json.dumps(self.message)


class ErrorMessage(Message):
	def __init__(self, error_code):
		super().__init__(opcode='ERROR', data=error_code)


class WelcomeMessage(Message):
	def __init__(self, error_code):
		super().__init__(opcode='WELCOME', data=None)