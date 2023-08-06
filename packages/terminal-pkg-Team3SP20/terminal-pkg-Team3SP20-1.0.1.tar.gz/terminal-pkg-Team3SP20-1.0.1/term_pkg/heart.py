import curses
import os
import pygame
import re
import socket
import sys
import threading
import time

from system_control import reboot, shutdown

# target server address
hostIP = "206.21.202.60"
# port to connect on
port = 1075

# specify file path name
path = "/home/pi/.local/lib/python3.7/site-packages/term_pkg/"

# get this device's IP
ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip.connect(("8.8.8.8", 80))
myHostname = ip.getsockname()[0]
ip.close()

# initialize audio player
pygame.mixer.init()
pygame.mixer.music.load(path + "classic_hurt.mp3")

# threading objects used to
# control the flow of msgs
send_pulse = threading.Event()
send_msg = threading.Semaphore()


# special request keys
# F1 - RESET
# F2 - MEAL TOTAL
# F3 - DEBIT
# F4 - EXCHANGE MEAL
# F5 - BALANCE

def keyentry(socket, display):
    read = ""
    while True:
        # read first key from user input
        read1 = display.getkey()
        # check if special cmd
        if read1 == "KEY_F(1)":
            read = "F1"
        elif read1 == "KEY_F(2)":
            read = "F2"
        elif read1 == "KEY_F(3)":
            read = "F3"
        elif read1 == "KEY_F(4)":
            read = "F4"
        elif read1 == "KEY_F(5)":
            read = "F5"
        else:
            read = read1 + display.getstr().decode(encoding="utf-8")

        if read == "shutdown":
            # initiate shutdown script
            shutdown()
        else:
            read = "KEY=" + read
            queue = True
            while queue:
                try:
                    # acquire socket
                    send_msg.acquire()
                    socket.send(bytes(read, "utf-8"))
                    # release socket
                    send_msg.release()
                    queue = False
                except (OSError, ConnectionResetError):
                    reboot()

def heartbeat(socket):
    # prepare message
    msg = bytes("MYIP=" + myHostname, "utf-8")
    while True:
        # wait for server
        send_pulse.wait()
        try:
            # acquire socket
            send_msg.acquire()
            socket.send(msg)
            # release socket
            send_msg.release()

        except (OSError, ConnectionResetError):
            reboot()
        
        # reset 
        send_pulse.clear()

def readmessage(socket, display):
    x, y = 0, 0
    while True:
        output = ""
        try:
            # recv msg from server
            msg = socket.recv(1024)
            msg = msg.decode("utf-8")

            if msg == "MYIP":
                send_pulse.set()

            # throw exception
            elif len(msg) == 0:
                raise OSError()

            else: 
                # break up & parse commands
                msgs = msg.split("\r")
                for cmd in msgs:

                    # remove newline character if in cmd
                    if "\n" in cmd:
                        cmd = cmd.replace("\n", "")

                    if cmd == "CLEAR":
                        display.clear()

                    elif "CURSOR" in cmd:
                        temp = re.findall(r'\d+', cmd) 
                        cords = list(map(int, temp)) 
                        if cords != []:
                            # only update coords if they exist
                            y = cords[0]
                            x = cords[1]

                    elif "DISPLAY" in cmd:
                        output = cmd[8:]
                        display.addstr(y, x, output)
                        # display.move(y+1, 1)
                        display.refresh()

                    elif cmd == "BELL":
                        pygame.mixer.music.play()
                        time.sleep(.25)

        except (OSError, ConnectionResetError):
            reboot()


def main(display):
    # initialize display
    curses.echo()
    
    # create IPv4, TCP socket
    while True:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # connect to host on port
            s.connect((hostIP, port))

            display.addstr(1, 1, "CONNECTED")
            display.move(2, 1)
            display.refresh()

            # start socket message reading thread
            read = threading.Thread(target = readmessage, args = [s, display])
            read.start()
            # start heartbeat thread
            heart = threading.Thread(target = heartbeat, args = [s], daemon = True)
            heart.start()

            # this loop keeps main method running so other threads
            # don't die
            while True:
                # start input thread
                key = threading.Thread(target = keyentry, args = [s, display])
                key.start()

                # wait for entry
                key.join()

        except (OSError, ConnectionResetError):
            # close socket
            s.close()
            # clear display
            display.clear()
            display.addstr(1, 1, "OFFLINE")
            display.move(2, 1)
            display.refresh()
            # wait 1 second
            time.sleep(1.0)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # occurs when user types ctrl + c
        print("Terminating program...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)