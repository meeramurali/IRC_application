"""
user.py

User class that handles info about a single user 
connected to the IRC server. 

Author: Meera Murali
Course: CS594 Internetworking Protocols
Date: 12/6/2019
Final Project: A simple IRC application 
"""


class User:
    def __init__(self, username, IP_addr, connection):
        self.username = username
        self.IP_addr = IP_addr
        self.connection = connection

    def display_user(self, verbose=False):
        if verbose:
            print(f"[{self.username}] <{self.IP_addr}>")
        else:
            print(f"[{self.username}]")