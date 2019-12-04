class User:
    def __init__(self, username, IP_addr, connection):
        self.username = username
        self.IP_addr = IP_addr
        self.connection = connection

    # def display_user(self, verbose=False):
    #     if verbose:
    #         print(f"[{self.username}] <{self.IP_addr}>")
    #     else:
    #         print(f"[{self.username}]")