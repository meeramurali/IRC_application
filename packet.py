import json


CLIENT_OPCODE = {
	'JOIN_ROOM': 10,
	'LEAVE_ROOM': 11,
	'CREATE_ROOM': 12,
	'LIST_ROOMS' : 2,
	'LIST_USERS' : 4,
	'SEND_MSG' : 8,
	'EXIT': 13
}

SERVER_OPCODE = {
	'WELCOME' : 1,
	'CREATE_ROOM_RES': 14,
	'JOIN_ROOM_RES': 15,
	'LEAVE_ROOM_RES': 16,
	'LIST_ROOMS_RESP' : 3,
	'LIST_USERS_RESP' : 5,
	'TELL_MSG' : 9,
	'ERROR' : 0
}


# Base Packet class
class Packet:
	def __init__(self, opcode, data=None, username=None, roomname=None):
		self.packet = {
			"opcode": opcode,
			"data": data,
			"username": username,
			"roomname": roomname
		}

	def get_json_str(self):
		return json.dumps(self.packet)


# Client packets
class JoinRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='JOIN_ROOM', username=username, roomname=roomname)


class LeaveRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='LEAVE_ROOM', username=username, roomname=roomname)


class CreateRoomPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='CREATE_ROOM', username=username, roomname=roomname)


class SendMessagePacket(Packet):
	def __init__(self, username, roomname, msg):
		super().__init__(opcode='SEND_MSG', data=msg, username=username, roomname=roomname)


class ListRoomsPacket(Packet):
	def __init__(self, username):
		super().__init__(opcode='LIST_ROOMS', username=username)


class ListUsersPacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='LIST_USERS', username=username, roomname=roomname)


class ExitPacket(Packet):
	def __init__(self, username):
		super().__init__(opcode='EXIT', username=username)


# Server packets
class WelcomeMessagePacket(Packet):
	def __init__(self, msg):
		super().__init__(opcode='WELCOME', data=msg)


class CreateRoomResponsePacket(Packet):
	def __init__(self, roomname):
		super().__init__(opcode='CREATE_ROOM_RES', roomname=roomname)


class JoinRoomResponsePacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='JOIN_ROOM_RES', username=username, roomname=roomname)


class LeaveRoomResponsePacket(Packet):
	def __init__(self, username, roomname):
		super().__init__(opcode='LEAVE_ROOM_RES', username=username, roomname=roomname)


class ListRoomsResponsePacket(Packet):
	def __init__(self, room_list):
		super().__init__(opcode='LIST_ROOMS_RES', data=room_list)


class ListUsersResponsePacket(Packet):
	def __init__(self, roomname, users_list):
		super().__init__(opcode='LIST_USERS_RES', data=users_list, roomname=roomname)


class TellMsgPacket(Packet):
	def __init__(self, username, roomname, msg):
		super().__init__(opcode='TELL_MSG', data=msg, username=username, roomname=roomname)


class ErrorMessagePacket(Packet):
	def __init__(self, error_msg):
		super().__init__(opcode='ERROR', data=error_msg)