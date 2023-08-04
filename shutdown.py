#!/home/lukas/player/venv/bin/python3


import zmq
import os


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    socket.recv()

    os.system("shutdown now")


if __name__ == "__main__":
    main()
