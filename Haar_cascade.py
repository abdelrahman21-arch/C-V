# I’m using the opencv and imutils library, which allows multi-threading of the analysis processes
#from imutils.video.pivideostream import PiVideoStream
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import imutils
import time
import serial
import cv2

# This sets up Serial communication with the Arduino
ser = serial.Serial('COM5', 9600)
# This sets up the face cascades (one of which is unused) and the image resolution to process
cascadePathFront = "haarcascade_frontalface_default.xml"
cascadePathProfile = "haarcascade_profileface.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+cascadePathFront)
profileCascade = cv2.CascadeClassifier(cv2.data.haarcascades+cascadePathProfile)
font = cv2.FONT_HERSHEY_SIMPLEX
widthImage = 640
#positionHolder = 0
#org=(200,200)
# from the imutils library. The pi can read in raw image matrices and also process them at the same time.
vs =cv2.VideoCapture(1)
time.sleep(2.0)
centerImage = widthImage / 2  # x coordinate of center of image
distance_temp=0
f1=0
f2=0


# Waiting for the PIR sensor to activate before doing anything.
loop_break = 'a'
#while loop_break != 's':
 #   loop_break = ser.read(1)
count=0
i=0
# main loop of the program. It continuously scans for faces here, and sends instructions as appropriate to the #Arduino.
while (1):
    _,img = vs.read()
    # resizes it here in order to decrease processing time. A lot of the other options here are just to get the image right #side up and gray.
    img = imutils.resize(img, width=widthImage)
    height =vs.get(cv2.CAP_PROP_FRAME_HEIGHT)

    center_y=height/2
    #img = imutils.rotate(img, angle=90)
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Used within the loops to be used for logic later.
    distance = widthImage

    xf = 0
    yf = 0
    wf = 0
    hf = 0

    # I am using two separate Haar cascades to get both the front and side of the face.
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(int(20), int(20)),
    )

    # The other cascade works well enough and removing this increases the speed.
    profiles = profileCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 4,
        minSize = (int(20), int(20)),
            )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        distance_temp = centerImage - (x + w / 2)

        distance_tempy=center_y-(y+h/2)
        if abs(distance_temp) < abs(distance):
            distance = distance_temp
            xf = x
            yf = y
            wf = w
            hf = h

    for(x,y,w,h) in profiles:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        distance_temp=centerImage-(x+w/2)

        distance_tempy = center_y - (y + h / 2)
        if abs(distance_temp)<abs(distance):
            distance=distance_temp
            xf=x
            yf=y
            wf=w
            hf=h

    # using only the x-distance from the center will allow me to position the turret in
    # optimal position for shooting.

    cv2.rectangle(img, (xf, yf), (xf + wf, yf + hf), (0, 0, 255), 2)
    loop_break = 'a'

    if distance < widthImage:
        '''if abs(distance) < 25:  # 20 seemed to be an accurate value that will also allow the
            # program to operate without infinitely correcting itself
            center=centerImage-75
            cv2.putText(img, "**Bang**", org=(int(center),30), fontFace=font, fontScale=1,color=(0,0,255),thickness=2)
            ser.write(b't')
            positionHolder = 0;
            while loop_break != 'h':
                loop_break = ser.read(1)'''

        if distance > 0 : #and abs(lst[i] - lst[i-1])>10 or abs(lst2[i]-lst2[i-1])>10 :
            center2 = centerImage - 75
            cv2.putText(img, "**Bang**l", org=(int(center2), 30), fontFace=font, fontScale=1,color=(0,0,255),thickness=2)
            #print(distance)
            print('moving left')
            #ratio = float( distance / widthImage)
            #steps=round((ratio * 90) / 1.8)
            #x=0
            #ser.write(b'steps')
            ser.write(b'l')

           # while x < steps:
            #    ser.write(b'l')



            ser.flushOutput()

        elif distance<0 : #and abs(lst[i] - lst[i-1])>10 or abs(lst2[i]-lst2[i-1])>10 :
            print(distance)
            print('moving right')
            cv2.putText(img, "**Bang**r", org=(int(centerImage) , 30), fontFace=font, fontScale=1,color=(0,0,255),thickness=2)
            #ratio = float(distance / widthImage)
            #steps = round((ratio * 90) / 1.8)
            #x = 0
           # ser.write(steps.encode())
            ser.write(b'r')



            #while x < steps:
             #   ser.write(b'r')


            ser.flushOutput()



        '''elif distance < 120  and distance_tempy < 50 and distance_tempy > -50:
            print('doing nothing ')'''

    count=count+1
    i=i+1
    print(i)
    cv2.imshow('camera', img)
    xf = 0
    yf = 0
    wf = 0
    hf = 0



    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()
ser.flushOutput()
#vs.stop()