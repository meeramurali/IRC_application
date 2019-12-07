import json


CLIENT_OPCODES = [
	'REG_USER',
	'JOIN_ROOM',
	'LEAVE_ROOM',
	'CREATE_ROOM',
	'LIST_ROOMS',
	'LIST_USERS',
	'SEND_MSG',
	'SEND_PVT_MSG',
	'EXIT'
]

SERVER_OPCODES = [
	'WELCOME',
	'CREATE_ROOM_RES',
	'JOIN_ROOM_RES',
	'LEAVE_ROOM_RES',
	'LIST_ROOMS_RESP',
	'LIST_USERS_RESP',
	'TELL_MSG',
	'TELL_PVT_MSG',
	'ERROR',
	'DISCONNECT'
]


# Base Packet class
class Packet:
	def __init__(self, opcode, data=None, username=None, roomname=None, receiver=None):
		self.packet = {
			"opcode": opcode,
			"data": data,
			"username": username,
			"roomname": roomname,
			"receiver": receiver
		}

	def get_json_str(self):
		return json.dumps(self.packet)


# Client packets
class RegisterUserPacket(Packet):
	def __init__(self, username):
		super().__init__(opcode='REG_USER', username=username)


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


class SendPvtMessagePacket(Packet):
	def __init__(self, username, receiver, msg):
		super().__init__(opcode='SEND_PVT_MSG', data=msg, username=username, receiver=receiver)


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


class TellPvtMsgPacket(Packet):
	def __init__(self, username, msg):
		super().__init__(opcode='TELL_PVT_MSG', data=msg, username=username)


class ErrorMessagePacket(Packet):
	def __init__(self, error_msg):
		super().__init__(opcode='ERROR', data=error_msg)


class DisconnectUserPacket(Packet):
	def __init__(self):
		super().__init__(opcode='DISCONNECT')