import json

SERVER_OPCODE = {
	'ERROR' : 0,
	'WELCOME' : 1,
	'LIST_ROOMS_RESP' : 3,
	'LIST_USER_RESP' : 5,
	'TELL_MSG' : 9
}

CLIENT_OPCODE = {
	'JOIN_ROOM': 10,
	'LEAVE_ROOM': 11,
	'CREATE_ROOM': 12,
	'LIST_ROOMS' : 2,
	'LIST_USERS' : 4,
	'SEND_MSG' : 8,
	'EXIT': 13
}

class Packet:
	def __init__(self, opcode, data, username, roomname):
		self.packet = {
			"opcode": opcode,
			"data": data,
			"username": username,
			"roomname": roomname
		}

	def get_json_str(self):
		return json.dumps(self.packet)


# Server packets
class ErrorMessagePacket(Packet):
	def __init__(self, error_code):
		super().__init__(opcode='ERROR', data=error_code)


class WelcomeMessagePacket(Packet):
	def __init__(self):
		super().__init__(opcode='WELCOME', data=None)


# Client packets
class JoinRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='JOIN_ROOM', data=None, username=username, roomname=roomname)


class LeaveRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='LEAVE_ROOM', data=None, username=username, roomname=roomname)


class CreateRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='CREATE_ROOM', data=None, username=username, roomname=roomname)


class SendMessagePacket(Packet):
	def __init__(self, username, roomname, data):
		super().__init__(opcode='SEND_MSG', data=data, username=username, roomname=roomname)


class ListRoomsPacket(Packet):
	def __init__(self, username):
		super().__init__(opcode='LIST_ROOMS', data=None, username=username, roomname=None)


class ListUsersPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='LIST_USERS', data=None, username=username, roomname=roomname)


class ExitPacket(Packet):
	def __init__(self, username):
		super().__init__(opcode='EXIT', data=None, username=username, roomname=None)