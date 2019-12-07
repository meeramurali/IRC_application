import socket 
import select 
import json
import _thread
from chatroom import Chatroom, User
from packet import *
from util import send_packet


SERVER_IP_ADDR = "127.0.0.1"
SERVER_PORT = 8000


class Server:
    def __init__(self, IP_addr, port):
        self.rooms = {}
        self.connections = {}

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((IP_addr, port)) 
            s.listen(100)

            while True:
                conn, addr = s.accept()
                print(f"{addr} connected")
                _thread.start_new_thread(self.client_conn_thread,(conn, addr))
            conn.close()


    def client_conn_thread(self, conn, addr):
        # Send welcome message to the newly connected user
        welcome_msg = "Welcome to IRC chat app!"
        welcome_packet = WelcomeMessagePacket(msg=welcome_msg)
        conn.sendall(welcome_packet.get_json_str().encode('utf-8'))

        while True:
            packet_json_str = conn.recv(2048) 
            # Handle client crashes/lost connection 
            if not packet_json_str:
                print(f"{addr} disconnected")
                self.disconnect_user(conn)
                break
            else: 
                self.process_packet(packet_json_str, conn, addr)


    def process_packet(self, packet_json_str, conn, addr):
        # convert packet string to JSON
        packet = json.loads(packet_json_str)

        # logging info on server side
        log_str = f"<{packet['username']} {addr}> {packet['opcode']}"
        if packet['opcode'] in CLIENT_OPCODES:
            if packet['opcode'] not in ['REG_USER', 'LIST_ROOMS']:
                log_str = log_str + f":{packet['roomname']}"
        else:
            log_str = log_str + f"Invalid Opcode!"
        print(log_str)

        # dispatch to corresponding handlers based on opcode
        if packet['opcode'] == 'REG_USER':
            self.connections[conn] = User(packet['username'], addr, conn)

        elif packet['opcode'] == 'CREATE_ROOM':
            self.create_new_chatroom(packet['roomname'], conn)

        elif packet['opcode'] == 'LIST_ROOMS':
            self.send_rooms_list(conn) or "No rooms created!"

        elif packet['opcode'] == 'JOIN_ROOM':
            self.add_user_to_room(packet['username'], packet['roomname'], conn, addr)

        elif packet['opcode'] == 'LEAVE_ROOM':
            self.remove_user_from_room(packet['username'], packet['roomname'], conn)

        elif packet['opcode'] == 'LIST_USERS':
            self.send_users_list(packet['roomname'], conn)

        elif packet['opcode'] == 'SEND_MSG':
            self.send_msg(packet['username'], packet['roomname'], packet['data'], conn)

        elif packet['opcode'] == 'EXIT':
            print(f"{addr} disconnected")

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
        # Check if there's already a room of that name
        if room_name in self.rooms:
            error_msg = f"A room with name {room_name} already exists!"
            send_packet(ErrorMessagePacket(error_msg), conn)
        else:    
            # Create new room
            self.rooms[room_name] = Chatroom(room_name)

            # Send success message to user
            send_packet(CreateRoomResponsePacket(room_name), conn)


    def add_user_to_room(self, username, room_name, conn, addr):
        # Check if room exists
        if room_name not in self.rooms.keys():
            error_msg = f"No room called {room_name} found!"
            send_packet(ErrorMessagePacket(error_msg), conn)
        else:
            # Check if username is already in room's list:
            if username in self.rooms[room_name].users.keys():
                error_msg = f"Username {username} already taken!" \
                            + " Join a different room or reconnect with a new username."
                send_packet(ErrorMessagePacket(error_msg), conn)

            else:
                # Add to room's user list
                self.rooms[room_name].add_user(User(username, addr, conn))

                # Announce to all users in room 
                self.rooms[room_name].broadcast(
                    JoinRoomResponsePacket(username, room_name))


    def remove_user_from_room(self, username, room_name, conn):
        # Check if room exists
        if room_name not in self.rooms.keys():
            error_msg = f"No room called {roomname} found!"
            send_packet(ErrorMessagePacket(error_msg), conn)
        # Check if user is in room
        elif username not in self.rooms[room_name].users.keys():
            error_msg = f"You have not joined room {room_name}!"
            send_packet(ErrorMessagePacket(error_msg), conn)
        else:
            # Remove from room's user list
            self.rooms[room_name].remove_user(username)

            # Announce to all users in room
            self.rooms[room_name].broadcast(
                LeaveRoomResponsePacket(username, room_name))


    def send_rooms_list(self, conn):
        # Get room list
        room_list = list(self.rooms.keys())
        
        # Send to asking user
        send_packet(ListRoomsResponsePacket(room_list), conn)


    def send_users_list(self, roomname, conn):
        # Get users list from room
        if roomname in self.rooms:
            users_list = list(self.rooms[roomname].users.keys())
            send_packet(
                ListUsersResponsePacket(roomname, users_list), conn)
        else:
            error_msg = f"No room called {roomname} found!"
            send_packet(ErrorMessagePacket(error_msg), conn)      


    def send_msg(self, username, room_name, message, conn):
        # Check if room exists
        if room_name not in self.rooms.keys():
            error_msg = f"No room called {room_name} found!"
            send_packet(ErrorMessagePacket(error_msg), conn)

        # Check if user is in room
        elif username not in self.rooms[room_name].users.keys():
            error_msg = f"You must first join room {room_name} " \
                + "to send a message to it!"
            send_packet(ErrorMessagePacket(error_msg), conn)

        # Broadcast message to all users in room
        else:
            self.rooms[room_name].broadcast(
                TellMsgPacket(username, room_name, message))


    def disconnect_user(self, conn):
        username = self.connections[conn].username
        for room_name, room in self.rooms.items():
            if username in room.users.keys():
                # Remove user from room list
                room.remove_user(username)
                # Broadcast to all remaining in room that the user has left
                room.broadcast(LeaveRoomResponsePacket(username, room_name))
                



server = Server(IP_addr=SERVER_IP_ADDR, port=SERVER_PORT)





