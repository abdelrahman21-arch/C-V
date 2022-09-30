
# Copyright 2018 Satya Mallick (LearnOpenCV.com)

# Import modules
import cv2, sys, os , serial,struct, time,threading

ser=serial.Serial('COM5',9600,timeout=1)
list = []
count=0





if not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''

    print(errorMsg)
    sys.exit()

# Create tracker
tracker = cv2.TrackerGOTURN_create()

# Read video
video = cv2.VideoCapture(0)
time.sleep(1)

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
ok, frame = video.read()

if not ok:
    print("Cannot read video file")
    sys.exit()

# Define a bounding box
#bbox = (276, 23, 86, 320)

# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)
arm_initalpos=0
def moveToposition(box_centerx,box_centery) :

    cx = width / 2
    cy = height / 2
    print(f'Box center {box_centerx}\n')
    global arm_initalpos
    ratio=float(abs((arm_initalpos- box_centerx))/width)


    #for i in range(len(list)):
        #k = ser.read(1)
        #print(k)

        #while k!=b'f':
    if cx<box_centerx :
        Nextpostion_steps = round((ratio * 90) / 1.8)
        Nextpostion_stepsSent = str(Nextpostion_steps)
        i=0
        while i < Nextpostion_steps:
            ser.write(b'l')

            i+=1


        print('moving left')
            #time.sleep(2)
            # print(f'arm inital pos when dir is 1 {Nextpostion_steps}')
    if cx > box_centerx:
        Nextpostion_steps = round((ratio * 90) / 1.8)
        Nextpostionn_stepsSent2 = str(Nextpostion_steps)
        i=0
        while i < Nextpostion_steps:
            ser.write(b'r')



        print('moving right')
            #time.sleep(2)
        #while k==b'f':
         #   print('waiting to finish move ')
            # print(f'arm inital pos when dir is 0 {Nextpostion_steps}')












while True:
    # Read a new frame
    ok, frame = video.read()

    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()
    width = video.get(cv2. CAP_PROP_FRAME_WIDTH)  # float `width`
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)



    # Update tracker
    ok, bbox = tracker.update(frame)
    print(bbox)
    xmin, ymin, xmax, ymax = bbox
    print(xmin,xmax)
    box_centerx = abs(float((xmax - xmin)) / 2)+ xmin
   # list.append(box_centerx)
    #list.append(box_centerx)

    box_centery = int((ymax - ymin) * 480) / 2
#    bbox1=list(bbox)
 #   bbox1.append([int(ymin *640),int(xmin*480) , int((ymax-ymin)*640), int((xmax-xmin)*480)])


    moveToposition(box_centerx, box_centery)
    #time.sleep(2)
    ser.flushOutput()







    distancei = (2 * 3.14 * 180) / (xmax + ymax * 360) * 1000 + 3
    distance2=distancei*2.54
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,
                "distance "+str(distance2)+"cm",
                (50, 50),
                font, 1,
                (0, 255, 255),
                2,
                cv2.LINE_4)
    print("DISTANCE   "+str(distance2)+"  Cm")



    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display tracker type on frame
  #  cv2.putText(frame, "GOTURN Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display FPS on frame
  #  cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
    #count=count+1
    print(height, width)
    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break


