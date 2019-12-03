import socket 
import select 
import json
import _thread
from chatroom import Chatroom, User
from packet import SERVER_OPCODE, CLIENT_OPCODE


class Server:
    def __init__(self, IP_addr, port):
        self.rooms = {}

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((IP_addr, port)) 
            s.listen(100)
            # conn, addr = s.accept() 
            # with conn:
            #     print(addr[0], " connected")
            #     _thread.start_new_thread(self.client_thread,(conn, addr))
            while True:
                conn, addr = s.accept()
                print(addr[0], " connected")
                _thread.start_new_thread(self.client_thread,(conn, addr))
            conn.close()


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


    def get_rooms_list(self):
        room_list = ""
        for roomname in self.rooms.keys():
             room_list = room_list + roomname + '\n'
        return room_list

    def get_users_list(self, roomname):
        if roomname in self.rooms:
            return self.rooms[roomname].get_users_list()
        else:
            return "No such room found."        


    def process_client_msg(self, msg_json_str, conn, addr):
        msg = json.loads(msg_json_str)

        if msg['opcode'] == 'CREATE_ROOM':
            print(f"<{msg['username']}> {msg['opcode']}:{msg['roomname']}")
            self.create_new_chatroom(msg['roomname'])
            return f"New chatroom {msg['roomname']} created!"

        elif msg['opcode'] == 'LIST_ROOMS':
            print(f"<{msg['username']}> {msg['opcode']}")
            return self.get_rooms_list() or "No rooms created!"

        elif msg['opcode'] == 'JOIN_ROOM':
            print(f"<{msg['username']}> {msg['opcode']}:{msg['roomname']}")
            self.add_user_to_room(User(msg['username'], addr, conn), msg['roomname'])
            return f"{msg['username']} joined room {msg['roomname']}!"

        elif msg['opcode'] == 'LIST_USERS':
            print(f"<{msg['username']}> {msg['opcode']}:{msg['roomname']}")
            return self.get_users_list(msg['roomname'])

        elif msg['opcode'] == 'LEAVE_ROOM':
            print(f"<{msg['username']}> {msg['opcode']}:{msg['roomname']}")
            self.remove_user_from_room(msg['username'], msg['roomname'])
            return f"{msg['username']} left room {msg['roomname']}!"

        elif msg['opcode'] == 'EXIT':
            print(f"{msg['username']} disconnected")

        else:
            return "Invalid Opcode!"


    def client_thread(self, conn, addr):   
        conn.sendall(b"Welcome to IRC chat app!")    
        while True:
            message = conn.recv(2048) 
            if not message:
                break
            else: 
                response_str = self.process_client_msg(message, conn, addr)
                print(response_str)
                conn.sendall(response_str.encode('utf-8'))


test = Server(IP_addr="127.0.0.1", port=8000)
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





