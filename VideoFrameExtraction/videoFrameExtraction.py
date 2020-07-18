#coding-utf-8
import cv2
import os

name = ""
path = "d://videoFrame//"+name
os.mkdir(path)
cap = cv2.VideoCapture(path+".mp4")
c=1

flag = True
while flag:
    flag, frame = cap.read()
    if(flag==True):
        # frame = cv2.flip(frame,90)
        cv2.imwrite(path+"//"+name+"_"+str(c)+".jpg",frame)
        c+=1
    cv2.waitKey(1)
cap.release()
print("finished")
