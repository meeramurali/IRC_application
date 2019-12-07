import socket 
import select 
import sys 
from packet import *
from util import send_packet, print_list, print_dict, ExitIRCApp, ServerCrashError
  

SERVER_IP_ADDR = "127.0.0.1" 
SERVER_PORT = 8080 
CLIENT_COMMANDS = {
    "create_room": "<room name>",
    "join_room": "<room name>",
    "leave_room": "<room name>",
    "list_rooms": None,
    "list_users": "<room name>",
    "send_msg": "<room name>:<a message>",
    "exit": None
}


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
        if len(packet['data']):
            print_list(title=f"#{packet['roomname']} users", list_to_print=packet['data'])
        else:
            print(f"*** No users currently in room {packet['roomname']}! ***")

    elif packet['opcode'] == 'LIST_ROOMS_RES':
        if len(packet['data']):
            print_list(title="Chatrooms", list_to_print=packet['data'])
        else:
            print("*** No chatrooms created! ***")

    elif packet['opcode'] == 'TELL_MSG':
        print(f"#[{packet['roomname']}] <{packet['username']}>: {packet['data']}")

    elif packet['opcode'] == 'ERROR':
        print(f"*** {packet['data']} ***")

    elif packet['opcode'] == 'DISCONNECT':
        raise ExitIRCApp()


def process_command(command):
    command_split = command.replace('\n', '').split(':')

    if command_split[0] == "list_rooms":
        send_packet(ListRoomsPacket(username=username), server_socket)

    elif command_split[0] == "create_room":
        if (len(command_split) != 2):
            print((
                '*** Invalid command! Do you want to create a new chatroom?' 
                ' Try \"create_room:<room name>\". ***'))
        else:
            send_packet(CreateRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "join_room":
        if (len(command_split) != 2):
            print((
                '*** Invalid command! Do you want to join a chatroom?' 
                ' Try \"join_room:<room name>\". ***'))
        else:
            send_packet(JoinRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "leave_room":
        if (len(command_split) != 2):
            print((
                '*** Invalid command! Do you want to leave a chatroom?' 
                ' Try \"leave_room:<room name>\". ***'))
        else:
            send_packet(LeaveRoomPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "list_users":
        if (len(command_split) != 2):
            print((
                '*** Invalid command! Do you want to list users in a chatroom?' 
                ' Try \"list_users:<room name>\". ***'))
        else:
            send_packet(ListUsersPacket(username=username, roomname=command_split[1]), server_socket)

    elif command_split[0] == "send_msg":
        if (len(command_split) != 3):
            print((
                '*** Invalid command! Do you want to send a message?' 
                ' Try \"send_msg:<room name>:<some message>\". ***'))
        else:
            send_packet(SendMessagePacket(username=username, roomname=command_split[1], msg=command_split[2]), server_socket)

    elif command_split[0] == "exit":
        raise ExitIRCApp()

    else:
        print('*** Invalid command! Here\'s a list of available commands: ***')
        print_dict(title="User commands", dict_to_print=CLIENT_COMMANDS)


# Get username from command line arg
if len(sys.argv) != 2: 
    print ("Correct usage: python3 client.py <username>")
    exit() 
username = str(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.connect((SERVER_IP_ADDR, SERVER_PORT))
  
    try:
        send_packet(RegisterUserPacket(username=username), server_socket)

        while True: 
            # list of possible input streams 
            sockets_list = [sys.stdin, server_socket] 
            read_sockets, _, _ = select.select(sockets_list,[],[]) 
          
            for socket in read_sockets: 
                # get packet from server
                if socket == server_socket: 
                    packet_json_str = socket.recv(2048)
                    if packet_json_str:
                        process_packet(packet_json_str)
                    else:
                        raise ServerCrashError()

                # get command from standard input
                else: 
                    command = sys.stdin.readline()
                    process_command(command)

    except ExitIRCApp:
        send_packet(ExitPacket(username=username), server_socket)
        server_socket.close()
        print("Exiting...")

    except ServerCrashError:
        server_socket.close()
        print("Oops! Something went wrong. Connection with server lost. Exiting...")


