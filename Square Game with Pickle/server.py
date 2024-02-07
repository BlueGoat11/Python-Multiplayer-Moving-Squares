import socket
from _thread import *
from player import Player
import pickle

#Put your local IPv4 address here. (For Windows in terminal type in ipconfig)
server = "192.168.1.164"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("CodeGoats server started. Waiting for connection...")

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(26,163,255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected from CodeGoats servers.")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Connection Lost")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1