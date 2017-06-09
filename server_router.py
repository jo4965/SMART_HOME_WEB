import sys
import socket
import select
import time
import os
from threading import Timer, Thread

HOST = ''
SOCKET_LIST = []
PORT = 9009 

# Settable parameters
NUM_OF_NODES = 10 # The maximum number of nodes
MTU = 1000 # Maximum Transmit Unit for this medium (B)
RECV_BUFFER = 2*MTU # Receive buffer size


def connect_to_led(ip, pt, msg):
  host = ip # Local host address
  port = pt # Medium port number
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  s.settimeout(2)
  try:
    s.connect((host, port))
    s.send(msg.encode('utf-8'))

  except:
    print('Unable to connect')
    sys.exit()

  print('Connected. You can start sending packets')



def medium():

    medium_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    medium_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    medium_socket.bind((HOST, PORT))
    medium_socket.listen(NUM_OF_NODES)

    # Add medium socket object to the list of readable connections
    SOCKET_LIST.append(medium_socket)
    
    print("Medium is Activated (port:" + str(PORT) + ") ")

    smart_alarm_ip = "192.168.1.4"
    while 1:
      #try:
        # Get the list sockets which are ready to be read through select
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
          # A new connection request received
          if sock == medium_socket: # 0.0.0.0 : 9009 (sock)
            sockfd, addr = medium_socket.accept()
            SOCKET_LIST.append(sockfd)

            # naming the nodes an alphabet like A, B, C...
            print("Node (%s, %s) connected" % addr)

          # A message from a node, not a new connection
          else: # 127.0.0.1 : 9009 (sock)
            #try:
              # Receiving packet from the socket.
          #####################################
          #### JONGHAP SULGAE PROJECT PART ####
          #####################################
              packet = sock.recv(RECV_BUFFER)
              if packet:
                data = packet.decode('utf-8')
                if data == "alarm on Rain":
                  Thread(target=connect_to_led, args=(smart_alarm_ip, 9009, "3\n")).start()
                elif data == "alarm on Clear":
                  Thread(target=connect_to_led, args=(smart_alarm_ip, 9009, "4\n")).start()
                elif data == "alarm on Clouds":
                  Thread(target=connect_to_led, args=(smart_alarm_ip, 9009, "2\n")).start()
                print(data)
            ###################################
            ###################################
            ###################################
              else:
                if sock in SOCKET_LIST:
                  print("Node (%s, %s) disconnected" % sock.getpeername())
                  SOCKET_LIST.remove(sock)
                  continue

            # Exception
            #except:
            #  if sock in SOCKET_LIST:
            #    print("Error! Check Node (%s, %s)" % sock.getpeername())
            #    SOCKET_LIST.remove(sock)
            #  continue
      #except:
      #  print('\nMedium program is terminated')
      #  medium_socket.close()
      #  sys.exit()


if __name__ == "__main__":
    sys.exit(medium())
