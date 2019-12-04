def send_packet(packet, conn):
    conn.sendall(packet.get_json_str().encode('utf-8'))


def print_list(title, list_to_print):
    print("-----------------------------\n" \
        + f"{title}\n" \
        + ".............................")
    for item in list_to_print:
        print(str(item))
    print("-----------------------------")


class ExitIRCApp(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)