## 2023 Capston Design Progect
## Attendance
## 출결시스템

import socket
import sys
import threading
import tkinter as tk
from threading import Thread  # for testing multi-thread
from time import sleep  # for sleep in thread
from tkinter import END, scrolledtext, ttk
import time

LocalHost = "127.0.0.1"
SocketChat_PortNumber = 24000
count = 30
time_diff = 0 
lock=threading.Lock()

class Attendance:

  def __init__(self, mode):
    global hostAddr
    # Create instance
    self.win = tk.Tk()
    self.mode = mode # server or client

    # Add a title 
    self.win.title("Multi-thread-based Socket Chatting (TCP Client)")
    hostname = socket.gethostname()
    hostAddr = socket.gethostbyname(hostname)
    print("My (client) IP address = {}".format(hostAddr))
    self.myAddr = hostAddr
    self.createWidgets()

    cli_thread = Thread(target=self.TCPClient, daemon=True)
    cli_thread.start()

    # TCP client
  def TCPClient(self):
    self.cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servAddr_str = input("Server IP Addr (e.g., '127.0.0.1') = ")
    self.cliSock.connect((servAddr_str, SocketChat_PortNumber)) 
    # send connect request to TCP server
    servAddr = self.cliSock.getpeername()
    print("TCP Client is connected to server ({})\n".format(servAddr))
    self.scr_cliDisplay.insert(tk.INSERT,"TCP client is connected to server \n")
    self.scr_cliDisplay.insert(tk.INSERT,"TCP server IP address : {}\n".format(servAddr[0]) )
    self.scr_cliDisplay.insert(tk.INSERT, "*** 강의 시작, 종료 시간을 24:00 형식으로 입력하세요\n")
    self.servAddr_entry.insert(END, servAddr[0])
    
    
    while True:
      
      cliRecvMsg = self.cliSock.recv(8192).decode() # 수신
      start = time.time()
      lock.acquire() # Lock 획득
      global count
      count = 0
      lock.release() # Lock 해제
      end = time.time()
      
      time_diff = end - start

      if not cliRecvMsg:
        break
      self.scr_cliDisplay.insert(tk.INSERT,">> " + cliRecvMsg) # 송신
      print(time_diff)
    self.cliSock.close()

#Exit GUI cleanly; definition of quit()
  def _quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

  # Modified Button Click Function
  def connect_server(self):
    self.scr_cliDisplay.insert(tk.INSERT,"Connecting to server ....")
    self.myIpAddr = self.myAddr.get()
    self.peerIpAddr = self.peerAddr.get()
    self.scr_cliDisplay.insert(tk.INSERT, "My IP Address : " + self.myIpAddr + '\n')
    self.scr_cliDisplay.insert(tk.INSERT, "Server's IP Address : " + self.peerIpAddr + '\n')
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.peerIpAddr, SocketChat_PortNumber)) 
      # send connect request to TCP server 

  #define callback for myMsg_enter()

  # 전송함수
  def cli_send(self): #from mySelf to peer/server
    while True:
      msgToServer = str(count)
      self.scr_cliDisplay.insert(tk.INSERT,"<< " + msgToServer + "\n")
      self.cliSock.send(bytes(msgToServer.encode()))
      self.scr_cliInput.delete('1.0', END) #clear scr_msgInput scrolltext
      sleep(1)
  
  # 전송 스레드 생성 함수
  def cli_send_thread(self):
    cli_send_thread = Thread(target=self.cli_send, daemon=True)
    cli_send_thread.start()

  # 강의실 시작 시간 전송 함수
  def cli_send_time_thread(self):
    msgToServer = str(self.scr_cliInput.get(1.0, END))
    self.scr_cliDisplay.insert(tk.INSERT,"<< " + msgToServer + "\n")
    self.cliSock.send(bytes(msgToServer.encode()))
    self.scr_cliInput.delete('1.0', END) #clear scr_msgInput scrolltext

  def createWidgets(self):
  # Add a frame in self.win
    frame = ttk.LabelFrame(self.win, text="강의실 내 인원 파악 프로그램 - 출결시스템 (Client)")
    frame.grid(column=0, row=0, padx=8, pady=3)
    #Add a LabelFrame of myAddr, peerAddr, Connect Button in frame
    frame_addr_connect = ttk.LabelFrame(frame, text="")
    frame_addr_connect.grid(column=0, row=0, padx=40, pady=20, columnspan=2)
    # Add labels (myAddr, peerAddr) in the frame_addr_connect
    myAddr_label = ttk.Label(frame_addr_connect, text="MyAddr (Client)")
    myAddr_label.grid(column=0, row=0, sticky='W') #
    peerAddr_label = ttk.Label(frame_addr_connect, text="Server Addr")
    peerAddr_label.grid(column=1, row=0, sticky='W') #

    # Add a Textbox Entry widgets (myAddr, peerAddr) in the frame_addr_connect
    self.myAddr = tk.StringVar()
    self.myAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable=self.myAddr)
    self.myAddr_entry.insert(END, hostAddr)
    self.myAddr_entry.grid(column=0, row=1, sticky='W')
    
    self.servAddr = tk.StringVar()
    self.servAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable="")
    #self.servAddr_entry.insert(END, LocalHost)
    self.servAddr_entry.grid(column=1, row=1, sticky='W')
    
    # Add a connect_button
    connect_button = ttk.Button(frame_addr_connect, text="Connect",\
    command=self.connect_server) 
    connect_button.grid(column=3, row=1)
    connect_button.configure(state='disabled') # for local 
    
    # Add ScrolledText fields of display and input 
    cliDisplay_label = ttk.Label(frame, text="전송 내역")
    cliDisplay_label.grid(column=0, row=1 )
    scrol_w, scrol_h = 40, 20
    self.scr_cliDisplay = scrolledtext.ScrolledText(frame, width=scrol_w,\
      height=scrol_h, wrap=tk.WORD)
    self.scr_cliDisplay.grid(column=0, row=2, sticky='WE') #, columnspan=3
    
    cliInput_label = ttk.Label(frame, text="강의 시작/종료 시간 입력 (Client) :")
    cliInput_label.grid(column=0, row=3 )
    
    self.scr_cliInput = scrolledtext.ScrolledText(frame, width=40, height=3, wrap=tk.WORD)
    self.scr_cliInput.grid(column=0, row=4) #, columnspan=3

    # Add Buttons (cli_send, serv_send)
    cli_send_button = ttk.Button(frame, text="인원 체크 시작", command=self.cli_send_thread) 
    cli_send_button.grid(column=0, row=5, sticky='E')

    cli_send_time_button = ttk.Button(frame, text="강의 시작/종료 시간 전송", command=self.cli_send_time_thread) 
    cli_send_time_button.grid(column=0, row=5, sticky='W')

    
    #Place cursor into the message input scrolled text
    self.scr_cliInput.focus()


#======================
# Start GUI
#======================
print("Running TCP Client")
sockChat = Attendance('client')
sockChat.win.mainloop()