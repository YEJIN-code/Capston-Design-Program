# 2023 Capston Design Program
# Attendance
# 출결시스템

import socket
import sys
import threading
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> a13575e33c3df47ecdfe4207bf5866d41bf15954
import tkinter as tk
from threading import Thread
from time import sleep 
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
    self.win = tk.Tk()
    self.mode = mode

    # Add a title 
    self.win.title("Attendance")
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
    servAddr_str = input("서버 IP를 입력하여 연결하세요 ")
    self.cliSock.connect((servAddr_str, SocketChat_PortNumber)) 

    servAddr = self.cliSock.getpeername()
    self.scr_cliDisplay.insert(tk.INSERT,"*** 부정 출석 방지 시스템 서버와 연결되었습니다. \n")
    self.scr_cliDisplay.insert(tk.INSERT, "*** 강의 시작, 종료 시간을 24:00 형식으로 입력하세요.\n")
    self.servAddr_entry.insert(END, servAddr[0])
    
    
    while True:
      # 출석 초기화 메시지 수신
      cliRecvMsg = self.cliSock.recv(8192).decode()
      start = time.time()
      lock.acquire() # Lock 획득
      global count
      count = 0 # 출석 인원 초기화
      lock.release() # Lock 해제
      end = time.time()
      
      # time_diff = end - start # 성능 측정

      if not cliRecvMsg:
        break
      self.scr_cliDisplay.insert(tk.INSERT,">> " + cliRecvMsg) # 송신
      # print(time_diff)
    self.cliSock.close()

  def _quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

  def connect_server(self):
    self.scr_cliDisplay.insert(tk.INSERT,"Connecting to server ...")
    self.myIpAddr = self.myAddr.get()
    self.peerIpAddr = self.peerAddr.get()
    self.scr_cliDisplay.insert(tk.INSERT, "My IP Address : " + self.myIpAddr + '\n')
    self.scr_cliDisplay.insert(tk.INSERT, "Server's IP Address : " + self.peerIpAddr + '\n')
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.peerIpAddr, SocketChat_PortNumber)) 

  # 전송함수
  def cli_send(self):
    while True:
<<<<<<< HEAD
      now = datetime.now()
      nowHour = now.hour
      nowMinute = now.minute

      msgToServer = str(count)
      self.scr_cliDisplay.delete("1.0", "end")
      self.scr_cliDisplay.insert(tk.INSERT,"현재 출석: " + msgToServer + "명  (" + str(now.time()) + ")\n")
=======
      msgToServer = str(count)
      self.scr_cliDisplay.delete("1.0", "end")
      self.scr_cliDisplay.insert(tk.INSERT,"현재 출석: " + msgToServer + "명\n")
>>>>>>> a13575e33c3df47ecdfe4207bf5866d41bf15954
      self.cliSock.send(bytes(msgToServer.encode()))
      self.scr_cliInput.delete('1.0', END)
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
    self.scr_cliInput.delete('1.0', END) 

  def createWidgets(self):
    frame = ttk.LabelFrame(self.win, text="출결시스템")
    frame.grid(column=0, row=0, padx=8, pady=3)
    
    frame_addr_connect = ttk.LabelFrame(frame, text="")
    frame_addr_connect.grid(column=0, row=0, padx=40, pady=20, columnspan=2)

    myAddr_label = ttk.Label(frame_addr_connect, text="내 IP")
    myAddr_label.grid(column=0, row=0, sticky='W') #
    peerAddr_label = ttk.Label(frame_addr_connect, text="시스템 서버 IP")
    peerAddr_label.grid(column=1, row=0, sticky='W') #

    self.myAddr = tk.StringVar()
    self.myAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable=self.myAddr)
    self.myAddr_entry.insert(END, hostAddr)
    self.myAddr_entry.grid(column=0, row=1, sticky='W')
    
    self.servAddr = tk.StringVar()
    self.servAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable="")
    self.servAddr_entry.grid(column=1, row=1, sticky='W')
    

    # connect_button = ttk.Button(frame_addr_connect, text="연결하기",\
    # command=self.connect_server) 
    # connect_button.grid(column=3, row=1)
    # connect_button.configure(state='disabled')
    

    cliDisplay_label = ttk.Label(frame, text="현재 출석 인원")
    cliDisplay_label.grid(column=0, row=1 )
    scrol_w, scrol_h = 40, 7
    self.scr_cliDisplay = tk.Text(frame, width=scrol_w,height=scrol_h, wrap=tk.WORD)
    self.scr_cliDisplay.grid(column=0, row=2, sticky='WE') 
    
    cliInput_label = ttk.Label(frame, text="강의 시작/종료 시간 입력")
    cliInput_label.grid(column=0, row=3 )
    
    self.scr_cliInput = tk.Text(frame, width=40, height=3, wrap=tk.WORD)
    self.scr_cliInput.grid(column=0, row=4) 

    cli_send_button = ttk.Button(frame, text="실행", command=self.cli_send_thread) 
    cli_send_button.grid(column=0, row=5, sticky='E')

    cli_send_time_button = ttk.Button(frame, text="강의 시작/종료 시간 전송", command=self.cli_send_time_thread) 
    cli_send_time_button.grid(column=0, row=5, sticky='W')

    self.scr_cliInput.focus()


<<<<<<< HEAD
#======================
# Start GUI
#======================
=======
# Start 
>>>>>>> a13575e33c3df47ecdfe4207bf5866d41bf15954
print("출결 시스템 실행")
sockChat = Attendance('Attendance')
sockChat.win.mainloop()