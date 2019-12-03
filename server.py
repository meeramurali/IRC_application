import socket 
import select 
import json
from chatroom import Chatroom, User
from message import SERVER_OPCODE, Message, ErrorMessage


class Server:
    def __init__(self, IP_addr, port):
        self.rooms = {}
        self.IP_addr = IP_addr
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.IP_addr, self.port)) 

        self.socket.listen(100)


    def create_new_chatroom(self, room_name):
        self.rooms[room_name] = Chatroom(room_name)


    def display_all_rooms(self, verbose=False):
        for _, room in self.rooms.items():
            room.display_room(verbose)


    def display_room(self, room_name):
        if room_name in self.rooms:
            self.rooms[room_name].display_room()
        else:
            return None


    def add_user_to_room(self, user, room_name):
        self.rooms[room_name].add_user(user)


    def remove_user_from_room(self, username, room_name):
        self.rooms[room_name].remove_user(username)


    def process_client_msg(self, msg_json_str):
        msg = json.loads(msg_json_str)

        if msg["opcode"] not in SERVER_OPCODE:
            print("Invalid Opcode!")
            return None

        else:
            print(msg["opcode"])
            print(msg["data"])



test = Server(IP_addr="0.0.0.0", port=8000)
test.create_new_chatroom("CS590")
test.create_new_chatroom("CS530")
test.add_user_to_room(User("mmurali", "0.0.0.0", None), "CS590")
test.add_user_to_room(User("diganta", "1.0.0.0", None), "CS590")
test.add_user_to_room(User("mahesh", "2.0.0.0", None), "CS530")
test.display_all_rooms()
test.remove_user_from_room("mmurali", "CS590")
test.remove_user_from_room("mmurali", "CS530")
test.display_all_rooms()
print("--------------")
test.display_room("CS540")

print("--------------")
test.process_client_msg(ErrorMessage("some error").get_json_str())
test.process_client_msg(Message(opcode="WELCOME", data="Hello").get_json_str())





