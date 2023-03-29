# 2023 Capston Design Program
# ServerCompare
# 서버 - 인원 비교 기능

import socket, sys, threading
from threading import Thread 
from time import sleep 
import tkinter as tk
from tkinter import ttk, scrolledtext, END
LocalHost = "127.0.0.1"
SocketChat_PortNumber = 24000


class ServerCompare:
  def __init__(self, mode):
    global hostAddr
    # Create instance
    self.win = tk.Tk()
    self.mode = mode # server or client

    self.win.title("Multi-thread-based Socket Chatting (TCP Server)")
    hostname = socket.gethostname()
    hostAddr = socket.gethostbyname(hostname)
    print("My (server) IP address = {}".format(hostAddr))
    self.myAddr = hostAddr
    self.createWidgets()

# Start TCP/IP server in its own thread
    serv_thread = Thread(target=self.TCPServer, daemon=True) 
    serv_thread.start()

# TCP server
  def TCPServer(self):

    global lecture_start_time # 강의 시작 시, 분
    global lecture_end_time # 강의 종료 시, 분
    global time_serv # 강의 시작, 종료 시간 수신 여부 표시
    time_serv= 0
    lecture_start_time=0
    lecture_end_time=0

    self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.servSock.bind((hostAddr, SocketChat_PortNumber)) 
    # bind socket to (IP_addr(local_host), port_number)
    self.scr_servDisplay.insert(tk.INSERT,"TCP server is waiting for a client .... \n" )
    self.servSock.listen(1)
    self.conn, self.cliAddr = self.servSock.accept() # cliAddr : (IPaddr, port_no)
    print("TCP Server is connected to client ({})\n".format(self.cliAddr))
    self.scr_servDisplay.insert(tk.INSERT,"TCP server is connected to client\n" )
    self.scr_servDisplay.insert(tk.INSERT, "TCP client IP address : {}\n".format(self.cliAddr[0]))
    self.peerAddr_entry.insert(END, self.cliAddr[0])
    while True:
      servRecvMsg = self.conn.recv(512).decode()
      if time_serv==0: # 시작시간 먼저 입력 받음
        lecture_start_time = servRecvMsg.split(':') # : 기준으로 문자열 자름. (ex, '4:30' -> ['4', '30'])
        lecture_start_time = lecture_start_time[1].replace("\n", "")
        time_serv+=1
        print(time_serv, lecture_start_time) # 디버그

      elif time_serv==1: # 종료시간을 입력받음
        lecture_end_time = servRecvMsg.split(':')
        lecture_end_time = lecture_end_time[1].replace("\n", "")
        time_serv+=1
        print(time_serv, lecture_end_time) # 디버그

      if not servRecvMsg: # 강의 시작/종료를 모두 받았으면 강의실 인원 수신
        break
      self.scr_servDisplay.insert(tk.INSERT,">> " + servRecvMsg+"\n")
    self.conn.close()

# Exit GUI cleanly; definition of quit()
  def _quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

  def serv_send(self): # from server send message to client
    msgToCli = str(self.scr_servInput.get(1.0, END))
    self.scr_servDisplay.insert(tk.INSERT,"<< " + msgToCli)
    self.conn.send(bytes(msgToCli.encode()))
    self.scr_servInput.delete('1.0', END) #clear scr_msgInput scrolltext

  def createWidgets(self):
    # Add a frame in self.win
    frame = ttk.LabelFrame(self.win, text="강의실 내 인원 파악 프로그램 - 서버 (Server)")
    frame.grid(column=0, row=0, padx=8, pady=4)
    
    #Add a LabelFrame of myAddr, peerAddr, Connect Button in frame
    frame_addr_connect = ttk.LabelFrame(frame, text="")
    frame_addr_connect.grid(column=0, row=0, padx=40, pady=20, columnspan=2)

    # Add labels (myAddr, peerAddr) in the frame_addr_connect
    myAddr_label = ttk.Label(frame_addr_connect, text="MyAddr(Server)")
    myAddr_label.grid(column=0, row=0, sticky='W') #
    peerAddr_label = ttk.Label(frame_addr_connect, text="Peer(CLient)Addr")
    peerAddr_label.grid(column=1, row=0, sticky='W') #

    # Add a Textbox Entry widgets (myAddr, peerAddr) in the frame_addr_connect
    self.myAddr = tk.StringVar()
    self.myAddr_entry = ttk.Entry(frame_addr_connect, width=15,\
      textvariable=self.myAddr)
    self.myAddr_entry.insert(END, hostAddr)
    self.myAddr_entry.grid(column=0, row=1, sticky='W')

    self.peerAddr = tk.StringVar()
    self.peerAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable="")
    #self.peerAddr_entry.insert(END, LocalHost)
    self.peerAddr_entry.grid(column=1, row=1, sticky='W')

    # Add ScrolledText fields of display and input 
    scrol_w, scrol_h = 40, 20
    servDisplay_label = ttk.Label(frame, text="전송 내역")
    servDisplay_label.grid(column=0, row=1 )
    self.scr_servDisplay = scrolledtext.ScrolledText(frame, width=scrol_w, height=scrol_h, wrap=tk.WORD)
    self.scr_servDisplay.grid(column=0, row=2, sticky='E') #, columnspan=3

    servInput_label = ttk.Label(frame, text="전송 테스트 :")
    servInput_label.grid(column=0, row=3 )

    self.scr_servInput = scrolledtext.ScrolledText(frame, width=40, height=3, wrap=tk.WORD)
    self.scr_servInput.grid(column=0, row=4) #, columnspan=3

    # Add Buttons (cli_send, serv_send)
    serv_send_button = ttk.Button(frame, text="전송", command=self.serv_send) 
    serv_send_button.grid(column=0, row=5, sticky='E')

    #Place cursor into the message input scrolled text
    self.scr_servInput.focus()


#======================
# Start GUI
#======================
print("Running TCP server")
sockChat = ServerCompare("server")
sockChat.win.mainloop()