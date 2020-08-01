#coding-utf-8
import cv2
import os
from PIL import Image

path = "d://vf//videoFrame//"       #视频所在的路径
name = ""
suffix = ".mp4"      #视频的后缀名

wholeName = path+name+suffix
folderName = path+name+"//"


def readFrame():
    if os.path.exists(folderName)==False:
        os.mkdir(folderName)
    cap = cv2.VideoCapture(wholeName)
    c=1
    flag, frame = cap.read()
    while(flag):
        frame = rotate(frame, 0)        #控制旋转
        frameName = "{}_{:0>3d}.jpg".format(name, c)        #设置前导零，使下面图片转视频按名称排序时不会有2在10之后
        cv2.imwrite(folderName+frameName, frame)
        c+=1
        cv2.waitKey(1)
        flag, frame = cap.read()
    cap.release()


def writeFrame():
    ''' 可指定视频帧编码
        H264编码十六进制对应的ascii码是AVC1，MPEG4编码是MP4V，还有MJPG
        Windows下推荐使用DIVX，Fedora下推荐使用XVID，OS X下推荐使用mp4v或者avc1
    '''
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    images = sorted(os.listdir(folderName))
    image = Image.open(folderName + images[0])
    vw = cv2.VideoWriter(path+name+".avi", fourcc, 2, image.size)        #第三个参数修改帧率
    for i in images:
        frame = cv2.imread(folderName+i)
        vw.write(frame)
    vw.release()


def rotate(frame, case):
    if case==0:
        return frame
    frame = cv2.transpose(frame)
    if case==-1:        #逆时针90度
        frame = cv2.flip(frame, 0)
    elif case==1:       #顺时针90度
        frame = cv2.flip(frame, 1)
    elif case==2:       #180度
        frame = cv2.flip(frame, 1)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 1)
    return frame


def getCode():      #获取视频的编码
    cap = cv2.VideoCapture(wholeName)
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    print ('codec is ' + chr(codec&0xFF) + chr((codec>>8)&0xFF) + chr((codec>>16)&0xFF) + chr((codec>>24)&0xFF))


readFrame()
#writeFrame()
print("finished")