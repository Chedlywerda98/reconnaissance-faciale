import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Servo
import time
import RPi.GPIO as gpio
from imutils.video import VideoStream

#definition des pins
pinBtn =2
led =16
GPIO.setmode(GPIO.BCM)
#definition des pins en entree sortie
GPIO.setup(pinBtn ,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)
myGPIO=17
servo=Servo(myGPIO)
servo.min()

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im):
    nb_emp=0
    #Select GPIO mode
    GPIO.setmode(GPIO.BCM)
    #Disable warnings (optional)
    GPIO.setwarnings(False)
    #Set buzzer - pin 23 as output
    buzzer=23
    GPIO.setup(buzzer,GPIO.OUT)  
    """
    will find all of the faces in a given image and label
    them if it knows what they are
    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

    # use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
        print ("entrée validé")
        servo.max()
        nb_emp=nb_emp+1
        print(nb_emp)
        sleep(30)
        print ("servo activé")
        face_names.append(name)
    else:
        #Run forever loop
        for i in range(3):
            GPIO.output(buzzer,GPIO.HIGH)
            print ("Beep")
            sleep(0.5) # Delay in seconds
            GPIO.output(buzzer,GPIO.LOW)
            print ("No Beep")
            sleep(0.5)
        face_names.append(name)    
        #exit()

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)


    # Display the resulting image
    while True:
        cv2.namedWindow("Vp", cv2.WINDOW_NORMAL)
        imgs = cv2.resize(img, (960, 540))
        cv2.imshow('Vp', imgs)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names

print ("start")


n=0


while True:
etat=GPIO.input(pinBtn)
if(etat==0):
print ("appui detecte")
GPIO.output(16,True)
n=n+1
print (n)
for i in range (n):
            camera = PiCamera()
           
            camera.start_preview()
            sleep(5)
            camera.capture('/home/pi/Desktop/face_rec/imagee.jpg')
            camera.stop_preview()
            print(classify_face("imagee.jpg"))  
       
else:
GPIO.output(16,False)
time.sleep(0.3)
# n=n+1
# print (n)
# camera = PiCamera()
 #       camera.start_preview()

#        sleep(5)
 #       camera.capture('/home/pi/Desktop/face_rec/imagee.jpg')
 #       camera.stop_preview()
 #       print(classify_face("imagee.jpg"))


# else:
# GPIO.output(16,False)
# time.sleep(0.3)
# print(n)
#print(classify_face("test.jpg"))
#camera= PiCamera()
#while True:

#Get values from button presses

# inputCamera = gpio.input(2)

# If the Video Button is Pressed, Record for Ten Seconds and Save File With Current Date and Time


# If The Camera Button is Pressed Take a Photo and Save With Current Date and Time
# if inputCamera == False:
# print('Camera Button Pressed')
# camera.capture('/home/pi/Desktop/face_rec/imagee.jpg')
#camera.capture('/home/pi/Documents/' +  datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.png')
#        print(classify_face("imagee.jpg"))