"""
util.py

Utility functions and exception classes.

Author: Meera Murali
Course: CS594 Internetworking Protocols
Date: 12/6/2019
Final Project: A simple IRC application 
"""


# Utility functions
def send_packet(packet, conn):
    conn.sendall(packet.get_json_str().encode('utf-8'))


def print_list(title, list_to_print):
    print("-------------------------------------\n" \
        + f"{title}\n" \
        + ".....................................")
    for item in list_to_print:
        print(str(item))
    print("-------------------------------------")


def print_dict(title, dict_to_print):
    print("-------------------------------------\n" \
        + f"{title}\n" \
        + ".....................................")
    for (item, val) in dict_to_print.items():
        if val:
            print(f"{str(item)}:{str(val)}")
        else:
            print(str(item))
    print("-------------------------------------")


# Custom Exceptions
class ExitIRCApp(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class ServerCrashError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class DuplicateUsernameError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)