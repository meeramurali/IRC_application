import socket 
import select 
import sys 
from packet import *
from util import send_packet, print_list, ExitIRCApp
  

SERVER_IP_ADDR = "127.0.0.1" 
SERVER_PORT = 8080 
CLIENT_COMMANDS = [
    "create_room",
    "join_room",
    "leave_room",
    "list_rooms",
    "list_users",
    "send_msg",
    "exit"
]


def process_packet(packet_json_str):
    # convert packet string to JSON
    packet = json.loads(packet_json_str)

    if packet['opcode'] == 'WELCOME':
        print(packet['data'])

    elif packet['opcode'] == 'CREATE_ROOM_RES':
        print(f"#[{packet['roomname']}] room created!")

    elif packet['opcode'] == 'JOIN_ROOM_RES':
        print(f"#[{packet['roomname']}] <{packet['username']}> joined the room.")

    elif packet['opcode'] == 'LEAVE_ROOM_RES':
        print(f"#[{packet['roomname']}] <{packet['username']}> left the room.")

    elif packet['opcode'] == 'LIST_USERS_RES':
        print_list(title=f"#{packet['roomname']} users", list_to_print=packet['data'])

    elif packet['opcode'] == 'LIST_ROOMS_RES':
        print_list(title="Chatrooms", list_to_print=packet['data'])

    elif packet['opcode'] == 'TELL_MSG':
        print(f"#[{packet['roomname']}] <{packet['username']}>: {packet['data']}")

    elif packet['opcode'] == 'ERROR':
        print(f"*** {packet['data']} ***")


def process_command(command):
    command_split = command.replace('\n', '').split(':')

    if command_split[0] == "list_rooms":
        send_packet(ListRoomsPacket(username=username), server_socket)

    elif command_split[0] == "create_room":
        send_packet(CreateRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "join_room":
        send_packet(JoinRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "leave_room":
        send_packet(LeaveRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "list_users":
        send_packet(ListUsersPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "send_msg":
        send_packet(SendMessagePacket(username=username, roomname=command_split[1], msg=command_split[2]), server_socket)

    elif command_split[0] == "exit":
        raise ExitIRCApp()

    else:
        sys.stdout.write("Invalid command!\n")


# Get username from command line arg
if len(sys.argv) != 2: 
    print ("Correct usage: python3 client.py <username>")
    exit() 
username = str(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.connect((SERVER_IP_ADDR, SERVER_PORT)) 
  
    try:
        while True: 
            # list of possible input streams 
            sockets_list = [sys.stdin, server_socket] 
            read_sockets, _, _ = select.select(sockets_list,[],[]) 
          
            for socket in read_sockets: 
                # get packet from server
                if socket == server_socket: 
                    packet_json_str = socket.recv(2048)
                    process_packet(packet_json_str)

                # get command from standard input
                else: 
                    command = sys.stdin.readline()
                    process_command(command)

    except ExitIRCApp:
        send_packet(ExitPacket(username=username), server_socket)
        server_socket.close()
        print("Exiting...")


