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


class ExitIRCApp(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)