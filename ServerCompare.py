# 2023 Capston Design Program
# ServerCompare
# 서버 - 인원 비교 기능

import socket, sys, threading
from threading import Thread 
from time import sleep 
import tkinter as tk
from tkinter import ttk, scrolledtext, END
SocketChat_PortNumber = 24000

CameraCount = 50 # 카메라로 확인한 재실 인원
AttendaceCount = 0 # 출결시스템 내 출석 인원
registerStudentCount = 50 # 수강 인원

class ServerCompare:
  def __init__(self, mode):
    global hostAddr
    self.win = tk.Tk()
    self.win.title("ServerCompare")
    self.mode = mode
    
    # 호스트 이름과 IP 추출
    hostname = socket.gethostname()
    hostAddr = socket.gethostbyname(hostname)
    print("IP address = {}".format(hostAddr))
    self.myAddr = hostAddr
    self.createWidgets()
    
    # TCP 스레드 생성
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
    self.scr_servDisplay.insert(tk.INSERT,"** 출결시스템과 연결하세요. \n" )
    self.servSock.listen(1)
    self.conn, self.cliAddr = self.servSock.accept() # cliAddr : (IPaddr, port_no)

    print("** 출결시스템과 연결되었습니다. ({})\n".format(self.cliAddr))
    self.scr_servDisplay.insert(tk.INSERT,"** 출결시스템과 연결되었습니다.\n" )
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

      else:
        self.compare()

      if not servRecvMsg: # 수신한 메시지 없음
        break

      else: # 수신한 메시지 있음
        self.scr_servDisplay.delete("1.0", "end")
        self.scr_servDisplay.insert(tk.INSERT,">> " + servRecvMsg+"\n")
      
    self.conn.close()

  def compare(self): # 재실 인원과 출결시스템 인원을 비교하는 함수
    gap = CameraCount - 0.85 * registerStudentCount
    if (gap<0): # 음수일 경우 부정출석
      self.serv_send()
      print("부정 출석이 의심됩니다!")

  def _quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

  def serv_send(self):
    msgToCli = "출결 초기화\n"
    self.scr_servDisplay.insert(tk.INSERT,"<< " + msgToCli)
    self.conn.send(bytes(msgToCli.encode()))


  def createWidgets(self):
    frame = ttk.LabelFrame(self.win, text="부정 출석 방지 시스템 서버")
    frame.grid(column=0, row=0, padx=8, pady=4)
    
    frame_addr_connect = ttk.LabelFrame(frame, text="")
    frame_addr_connect.grid(column=0, row=0, padx=40, pady=20, columnspan=2)

    myAddr_label = ttk.Label(frame_addr_connect, text="내 IP")
    myAddr_label.grid(column=0, row=0, sticky='W') #
    peerAddr_label = ttk.Label(frame_addr_connect, text="출결시스템 IP")
    peerAddr_label.grid(column=1, row=0, sticky='W') #

    self.myAddr = tk.StringVar()
    self.myAddr_entry = ttk.Entry(frame_addr_connect, width=15,textvariable=self.myAddr)
    self.myAddr_entry.insert(END, hostAddr)
    self.myAddr_entry.grid(column=0, row=1, sticky='W')

    self.peerAddr = tk.StringVar()
    self.peerAddr_entry = ttk.Entry(frame_addr_connect, width=15, textvariable="")
    self.peerAddr_entry.grid(column=1, row=1, sticky='W')

    scrol_w, scrol_h = 40, 5
    servDisplay_label = ttk.Label(frame, text="전송 내역")
    servDisplay_label.grid(column=0, row=1 )
    self.scr_servDisplay = tk.Text(frame, width=scrol_w, height=scrol_h, wrap=tk.WORD)
    self.scr_servDisplay.grid(column=0, row=2, sticky='E') #, columnspan=3

    # Add Buttons (cli_send, serv_send)
    serv_send_button = ttk.Button(frame, text="초기화", command=self.serv_send) 
    serv_send_button.grid(column=0, row=5, sticky='E')


#======================
# Start GUI
#======================
print("부정 출석 방지 시스템 실행")
sockChat = ServerCompare("ServerCompare")
sockChat.win.mainloop()