import socket 
import select 
import sys 
from packet import *

  

SERVER_IP_ADDR = "127.0.0.1" 
SERVER_PORT = 8000 
USERNAME = "mmurali"
CLIENT_COMMANDS = [
    "create_room",
    "join_room",
    "leave_room",
    "list_rooms",
    "list_users",
    "send_msg",
    "exit"
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.connect((SERVER_IP_ADDR, SERVER_PORT)) 
  
    try:
        while True: 
            # list of possible input streams 
            sockets_list = [sys.stdin, server_socket] 
            read_sockets, _, _ = select.select(sockets_list,[],[]) 
          
            for socket in read_sockets: 
                # get message from server
                if socket == server_socket: 
                    message = socket.recv(2048)
                    print(message.decode('utf-8'))

                # read command from standard input
                else: 
                    command = sys.stdin.readline()
                    command_split = command.replace('\n', '').split(':')

                    if command_split[0] == "list_rooms":
                        packet = ListRoomsPacket(username=USERNAME).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "create_room":
                        packet = CreateRoomPacket(username=USERNAME, roomname=command_split[1]).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "join_room":
                        packet = JoinRoomPacket(username=USERNAME, roomname=command_split[1]).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "leave_room":
                        packet = LeaveRoomPacket(username=USERNAME, roomname=command_split[1]).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "list_users":
                        packet = ListUsersPacket(username=USERNAME, roomname=command_split[1]).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "send_msg":
                        packet = SendMessagePacket(username=USERNAME, roomname=command_split[1], data=command_split[2]).get_json_str()
                        server_socket.sendall(packet.encode('utf-8'))

                    elif command_split[0] == "exit":
                        raise Exception()

                    else:
                        sys.stdout.write("Invalid command!\n")

    except:
        packet = ExitPacket(username=USERNAME).get_json_str()
        server_socket.sendall(packet.encode('utf-8'))
        server_socket.close()
        print("Exiting...")


