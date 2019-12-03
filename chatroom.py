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


    def broadcast(self, message, sending_user): 
        for user in self.users: 
            if user != sending_user: 
                try: 
                    user.connection.send(message) 
                except: 
                    user.connection.close() 
                    self.remove_user(user.username) 


# test = Chatroom("CS590")
# test.add_user(User("mmurali", "0.0.0.0", None))
# test.add_user(User("diganta", "1.0.0.0", None))
# test.add_user(User("mahesh", "2.0.0.0", None))
# test.display_room()
# print("------------------------")
# test.remove_user("mahesh")
# test.display_room(verbose=True)