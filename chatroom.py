"""
chatroom.py

Defines the Chatroom class that handles a group of users 
subscribing to a single message stream.

Author: Meera Murali
Course: CS594 Internetworking Protocols
Date: 12/6/2019
Final Project: A simple IRC application 
"""


from user import User

class Chatroom:
    def __init__(self, room_name):
        self.name = room_name
        self.users = {}


    def add_user(self, user):
        self.users[user.username] = user


    def remove_user(self, username):
        if username in self.users:
            del self.users[username]


    def display_room(self, verbose=False):
        print(f"#{self.name}")
        for _, user in self.users.items():
            user.display_user(verbose)


    def broadcast(self, packet): 
        for _, user in self.users.items(): 
            try: 
                user.connection.sendall(packet.get_json_str().encode('utf-8')) 
            except: 
                user.connection.close() 
                self.remove_user(user.username) 