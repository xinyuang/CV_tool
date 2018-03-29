import cv2

video = cv2.VideoCapture('./ori.mp4')
count = 0
read_img = True
while read_img == True:
    ret,frame = video.read()
    print(type(frame))
    count = count + 1

    if frame is None:
        read_img = False
    cv2.imwrite("./ori_frame/ori_frame{0}.jpg".format(count), frame)    
video.release()
cv2.destroyAllWindows()