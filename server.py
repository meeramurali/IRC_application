import socket 
import select 
import json
import _thread
from chatroom import Chatroom, User
from packet import SERVER_OPCODE, CLIENT_OPCODE


SERVER_IP_ADDR = "127.0.0.1"
SERVER_PORT = 8000


class Server:
    def __init__(self, IP_addr, port):
        self.rooms = {}

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((IP_addr, port)) 
            s.listen(100)

            while True:
                conn, addr = s.accept()
                print(addr[0], " connected")
                _thread.start_new_thread(self.client_conn_thread,(conn, addr))
            conn.close()


    def client_conn_thread(self, conn, addr):   
        conn.sendall(b"Welcome to IRC chat app!")    
        while True:
            packet_json_str = conn.recv(2048) 
            if not packet_json_str:
                break
            else: 
                self.process_packet(packet_json_str, conn, addr)


    def process_packet(self, packet_json_str, conn, addr):
        # convert packet string to JSON
        packet = json.loads(packet_json_str)

        # logging info on server side
        log_str = f"<{packet['username']}> {packet['opcode']}"
        if packet['opcode'] in CLIENT_OPCODE:
            if packet['opcode'] != 'LIST_ROOMS':
                log_str = log_str + f":{packet['roomname']}"
        else:
            log_str = log_str + f"Invalid Opcode!"
        print(log_str)

        # dispatch to corresponding handlers based on opcode
        if packet['opcode'] == 'CREATE_ROOM':
            self.create_new_chatroom(packet['roomname'], conn)

        elif packet['opcode'] == 'LIST_ROOMS':
            self.send_rooms_list(conn) or "No rooms created!"

        elif packet['opcode'] == 'JOIN_ROOM':
            self.add_user_to_room(packet['username'], packet['roomname'], conn, addr)

        elif packet['opcode'] == 'LEAVE_ROOM':
            self.remove_user_from_room(packet['username'], packet['roomname'])

        elif packet['opcode'] == 'LIST_USERS':
            self.send_users_list(packet['roomname'], conn)

        elif packet['opcode'] == 'SEND_MSG':
            self.send_msg(packet['username'], packet['roomname'], packet['data'], conn)

        elif packet['opcode'] == 'EXIT':
            print(f"{packet['username']} disconnected")

        else:
            return "Invalid Opcode!"


    # def display_all_rooms(self, verbose=False):
    #     for _, room in self.rooms.items():
    #         room.display_room(verbose)


    # def display_room(self, room_name):
    #     if room_name in self.rooms:
    #         self.rooms[room_name].display_room()
    #     else:
    #         return None


    def create_new_chatroom(self, room_name, conn):
        # Create new room
        self.rooms[room_name] = Chatroom(room_name)

        # Send success message to user
        success_msg = f"New chatroom {room_name} created!" 
        conn.sendall(success_msg.encode('utf-8'))


    def add_user_to_room(self, username, room_name, conn, addr):
        # Add to room's user list
        self.rooms[room_name].add_user(User(username, addr, conn))

        # Announce to all users in room 
        broadcast_msg = f"{username} joined room {room_name}!"
        self.rooms[room_name].broadcast(broadcast_msg)


    def remove_user_from_room(self, username, room_name):
        # Remove from room's user list
        self.rooms[room_name].remove_user(username)

        # Announce to all users in room
        broadcast_msg = f"{username} left room {room_name}!"
        self.rooms[room_name].broadcast(broadcast_msg)


    def send_rooms_list(self, conn):
        # Build room list
        room_list = ""
        for roomname in self.rooms.keys():
             room_list = room_list + roomname + '\n'
        
        # Send to asking user
        conn.sendall(room_list.encode('utf-8'))


    def send_users_list(self, roomname, conn):
        # Get users list from room
        if roomname in self.rooms:
            users_list = self.rooms[roomname].get_users_list()
        else:
            users_list = "No such room found."        

        # Send to asking user
        conn.sendall(users_list.encode('utf-8'))


    def send_msg(self, username, room_name, message, conn):
        # Check if room exists
        if room_name not in self.rooms.keys():
            conn.sendall(b'No such room found!')

        # Check if user is in room
        elif username not in self.rooms[room_name].users.keys():
            conn.sendall(b'You must first join the room to send a message to it!')
            
        # Broadcast message to all users in room
        else:
            broadcast_msg = f"#[{room_name}] <{username}>: {message}"
            self.rooms[room_name].broadcast(broadcast_msg)



server = Server(IP_addr=SERVER_IP_ADDR, port=SERVER_PORT)





