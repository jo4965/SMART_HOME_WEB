import sys
import socket
import select
import os
import RPi.GPIO as Gpio
from time import sleep


Gpio.setmode(Gpio.BCM)

Gpio.setup(18, Gpio.OUT)
Gpio.setup(23, Gpio.OUT)
Gpio.setup(24, Gpio.OUT)

red = Gpio.PWM(18, 100)
green = Gpio.PWM(23, 100)
blue = Gpio.PWM(24, 100)

red.start(0)
blue.start(0)
green.start(0)



def changeLight(R,G,B,P):
    q = float(R+G+B)*float(P)/200000
    red.ChangeDutyCycle(int(R*q))
    green.ChangeDutyCycle(int(G*q))
    blue.ChangeDutyCycle(int(B*q))
    sleep(0.02)
    print(R,G,B,P)

def isProperData(arr):
    if  int(arr[4]) != 4 :
        print(" data_error")
        return 0
    if int(arr[5]) < 0 or int(arr[5]) > 255 :
        print (" red data error")
        return 0
    if int(arr[6]) < 0 or int(arr[6]) > 255 :
        print (" green data error")
        return 0
    if int(arr[7]) < 0 or int(arr[7]) > 255 :
        print (" blue data error")
        return 0
    if int(arr[8]) < 0 or int(arr[8]) > 100 :
        print (" power data error")
        return 0
    return 1

def control_mood_light(data, s):
  arr = data.split('_')
  err_message = "8_mood_resend_0"
  err_message = err_message.encode()
  if len(arr) > 4:
    if arr[1] == "8" and arr[2] == "mood" and arr[3] == "lighton":
      if isProperData(arr) == 1 :
        comp_message = "8_mood_complete_0"
        comp_message = comp_message.encode()
        s.send(comp_message)
        s.send(b"mood light on")
        print('light on ',arr[5],arr[6],arr[7],arr[8])
        changeLight(int(arr[5]),int(arr[6]),int(arr[7]),int(arr[8]))
      else :
        s.send(err_message)
    else :
      s.send(err_message)
  else :
    s.send(err_message)

def medium():

    medium_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    medium_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    medium_socket.bind((HOST, PORT))
    medium_socket.listen(NUM_OF_NODES)

    # Add medium socket object to the list of readable connections
    SOCKET_LIST.append(medium_socket)

    global STATUS # Status of Medium : I -> Idle, B -> Busy

    t=None; # Event Scheduler
    print("Medium is Activated (port:" + str(PORT) + ") ")

    global ascii_idx
    global ascii_sock_hash
    while 1:
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
            
              # Receiving packet from the socket.
          #####################################
          #### JONGHAP SULGAE PROJECT PART ####
          #####################################
              packet = sock.recv(RECV_BUFFER)
              data = packet.decode('utf-8')
              if packet:
                print(data)
                control_mood_light(data, sock)
                
            ###################################
            ###################################
            ###################################
              else:
                if sock in SOCKET_LIST:
                  print("Node (%s, %s) disconnected" % sock.getpeername())
                  SOCKET_LIST.remove(sock)
                  continue

"""
            except TypeError as e:
              if sock in SOCKET_LIST:
                print("Error! Check Node (%s, %s)" % sock.getpeername())
                SOCKET_LIST.remove(sock)
                print(e.args)
              continue
      except:
        print('\nMedium program is terminated')
        medium_socket.close()
        sys.exit()
"""
if __name__ == "__main__":
    sys.exit(medium())
