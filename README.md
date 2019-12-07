# IRC application
#### [CS594 Internetworking Protocols Final Project]

A simple Internet Relay Chat (IRC) application using which multiple clients can communicate via text messages with each other in common "virtual" chatrooms. Chatrooms are groups of users that are subscribed to the same message stream. Any message sent to a chatroom is forwarded by a central server to all users currently in that room.

# Run the app
To change the server IP address and port, update `SERVER_IP_ADDR` and `SERVER_PORT` in server.py and client.py.

### Run server-side script:
`python3 server.py`

### Run client-side script:
`python3 client.py <username>`

### Available client commands:
```
create_room:<room name>
join_room:<room name>
leave_room:<room name>
list_rooms
list_users:<room name>
send_msg:<room name>:<a message>
send_pvt_msg:<receiver username>:<a message>
exit
```
