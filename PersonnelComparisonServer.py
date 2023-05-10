<<<<<<< HEAD

import cv2
import numpy as np
import threading
from datetime import datetime
import socket
from time import sleep
import tkinter as tk
from tkinter import ttk, END
from tkinter import messagebox
from enum import Enum
from threading import Thread 
start = False

SocketChat_PortNumber = 24000

CameraCount = 30 # 카메라로 확인한 재실 인원
AttendanceCount = 0 # 출결시스템 내 출석 인원
#registerStudentCount = 200 # 수강 인원

class LectureTime(Enum):
  START = 0
  END = 1

class ServerCompare:
  def __init__(self, mode):
    global CameraCount
    global hostAddr

=======
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
>>>>>>> d54fa8f0f95d534503d981fdad381459f4890949
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
<<<<<<< HEAD
    serv_thread = Thread(target=self.RecvCompare, daemon=True) 
    serv_thread.start()

    send_thread = Thread(target=self.SendCompare, daemon=True) 
    send_thread.start()
    print("send 스레드 생성")

  def init_time(self, servRecvMsg, time):
      time = servRecvMsg.split(':') # : 기준으로 문자열 자름. (ex, '4:30' -> ['4', '30'])
      time[1] = time[1].replace("\n", "")
      print(time) # 디버그

      return time

    
  # TCP server
  def RecvCompare(self):
    global CameraCount
    global AttendanceCount
    global lecture_start_time # 강의 시작 시, 분
    global lecture_end_time # 강의 종료 시, 분
    global time_serv # 강의 시작, 종료 시간 수신 여부 표시
    global flag
    flag = False
    time_serv= 0
    lecture_start_time=(0, 0)
    lecture_end_time=(0, 0)
    count = 0
    TIME = False
=======
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
>>>>>>> d54fa8f0f95d534503d981fdad381459f4890949

    self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.servSock.bind((hostAddr, SocketChat_PortNumber)) 
    self.scr_servDisplay.insert(tk.INSERT,"** 출결시스템과 연결하세요. \n" )
    self.servSock.listen(1)
    self.conn, self.cliAddr = self.servSock.accept() # cliAddr : (IPaddr, port_no)

    print("** 출결시스템과 연결되었습니다. ({})\n".format(self.cliAddr))
    self.scr_servDisplay.insert(tk.INSERT,"** 출결시스템과 연결되었습니다.\n" )
    self.peerAddr_entry.insert(END, self.cliAddr[0])

    while True:
<<<<<<< HEAD
      # ================= 수신 ======================

      #print("일해욧")
      servRecvMsg = self.conn.recv(512).decode()

      now = datetime.now()
      nowHour = now.hour
      nowMinute = now.minute

      if (TIME == False):
        if (count == 0): # 시작 시간 
          lecture_start_time = self.init_time(servRecvMsg, lecture_start_time)
          count+=1
      
        else:
          lecture_end_time = self.init_time(servRecvMsg, lecture_end_time)
          count+=1
          TIME = True
    
      else:
        # 강의가 시작했거나, 아직 끝나지 않았는지 검사
        if (self.isLectureTime(nowHour, nowMinute, int(lecture_start_time[0]), int(lecture_start_time[1]), LectureTime.START) == True) and\
          (self.isLectureTime(nowHour, nowMinute, int(lecture_end_time[0]), int(lecture_end_time[1]), LectureTime.END) == False):
          
          if not servRecvMsg: # 수신한 메시지 없음
            break

          flag = True
        # 수신한 메시지 있음
          self.scr_servDisplay.delete("1.0", "end")
          self.scr_servDisplay.insert(tk.INSERT,"출석: " + servRecvMsg + "명  (" + str(now.time()) + ")" + "\n")
          AttendanceCount = int(servRecvMsg)
          #print(AttendanceCount)
          self.scr_servDisplay.insert(tk.INSERT,"재실 인원: " + str(CameraCount) + "명  (" + str(now.time()) + ")" + "\n")
          #print("강의실 내 인원수:  ", CameraCount)

        else: # 강의 시간이 아님
          self.scr_servDisplay.delete("1.0", "end")
          self.scr_servDisplay.insert(tk.INSERT,"** 강의 시간이 아닙니다.\n" )
          st = self.isLectureTime(nowHour, nowMinute, int(lecture_start_time[0]), int(lecture_start_time[1]), LectureTime.START) 
          ed = self.isLectureTime(nowHour, nowMinute, int(lecture_end_time[0]), int(lecture_end_time[1]), LectureTime.END)
          if (st==False):
            print("강의 시작 안 함")
          if (ed==True):
            print("강의 이미 끝남")
      
      
    self.conn.close()

  def isLectureTime(self, nowHour, nowMinute, hour, minute, lectureTime): # 강의가 시작했는지, 마친 시간인지 검사하는 함수
    if (lectureTime == LectureTime.START): # 강의가 시작했는지 검사하길 요구
      if (hour < nowHour): # 지금 시간이 강의시작 시간을 지났음 -> 당연히 강의 시작
        return True
      elif (hour == nowHour): # 지금 시간이 강의시작 시간과 같음 -> 분까지 검사해야 함
        if (minute <= nowMinute): # 지금 분이 강의시작 분을 지났음
          return True
        else: # 아직 강의시작 분을 넘지 않음
          return False
      else:
        return False # 강의 시작 시간이 아님
        
    else: # 강의가 끝났는지 검사하길 요구
      if (hour < nowHour): # 지금 시간이 강의종료 시간을 지났음 -> 당연히 강의 끝
        return False
      elif (hour == nowHour): # 지금 시간이 강의종료 시간과 같음 -> 분까지 검사해야 함
        if (minute <= nowMinute): # 지금 시간이 강의종료 시간을 넘었음
          return False # 수업 끝
        else:
          return True
      else: 
        return False
  

  def SendCompare(self):
    while True:
      if (flag == False):
        #print("쉴게요")
        sleep(1)

      else:
        #print("감지할게요")
        if (self.countCompare() < 0):
          messagebox.showinfo("부정 출석 방지 시스템","부정 출석이 감지되었습니다!") #메시지 박스를 띄운다.
          sleep(60)

=======
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
>>>>>>> d54fa8f0f95d534503d981fdad381459f4890949

  def _quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

<<<<<<< HEAD
  def countCompare(self): # 재실 인원과 출결시스템 인원을 비교하는 함수
    global CameraCount
    global AttendanceCount
    #gap = CameraCount - 0.85 * registerStudentCount
    a = AttendanceCount - CameraCount # 출결인원과 재실인원 차이가 
    b = AttendanceCount * 0.15 # 오차 범위 
    gap = b - a # 오차 범위보다 크면 음수 오차범위보다 작으면 양수
    #print("a = ", a, ", b = ", b, ", gap = ", gap)
    #gap = CameraCount - 0.15 * AttendanceCount

    return gap

=======
>>>>>>> d54fa8f0f95d534503d981fdad381459f4890949
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


<<<<<<< HEAD




def receive_all(sock, count):
        buffer = b''
        while count:
            new_buffer = sock.recv(count)
            if not new_buffer:
                return None
            buffer += new_buffer
            count = count - len(new_buffer)
        return buffer

def person_detection(img_name):

    # Yolo Load
    net = cv2.dnn.readNet("D:\Python_project\yolo\yolov3.weights", "D:\Python_project\yolo\yolov3.cfg")
    classes = []
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Get Image
    img = cv2.imread(img_name)
    img = cv2.resize(img, None, fx=1, fy=1)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (608, 608), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Calc
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id==0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)


    # Remove Noise
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    #Print Screen
    total_people = 0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 1)
            total_people += 1

    return total_people, img

def person_cognition():
    while(True):
        global CameraCount
        CameraCount, img = person_detection("sample13.jpg")

        #current_time = datetime.now()
        #print("\n\n강의실 내 인원수: ", CameraCount)
        #print("마지막 업데이트 시각: ", current_time.hour, "시 ", current_time.minute, "분 ", current_time.second, "초")
        
        if flag==True:
            cv2.destroyAllWindows()
            cv2.imshow("Image", img)
            cv2.waitKey(5000)



###################### main ######################
t = threading.Thread(target=person_cognition)
t.start()
=======
#======================
# Start GUI
#======================
print("부정 출석 방지 시스템 실행")
>>>>>>> d54fa8f0f95d534503d981fdad381459f4890949
sockChat = ServerCompare("ServerCompare")
sockChat.win.mainloop()
