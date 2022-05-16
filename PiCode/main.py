import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model
import requests
import json
import os
import sound02
import socket
import img_post

try:
    a = os.listdir("/home/pi/Detection")
    count = int(len(a))+1
except:
    count=1
    
datas = {
    "to":"cTFzrNd6SMS0Q2LT0t4QUe:APA91bGxYIKGSzMPp9hJr2NPDhxboZmj76iAV_y59b8nqp-PIJaJSi1uKLfVpuHCU7iVT7oNsc9cXQzWE9gVXDQDZYfJlAXg_bFFtAXFOhBY0HAOtQLloy-DmyLTqA01Z3Rug3pJKsw5",
    "priority" : "high",
    "data":{
        "title":"알림",
        "message":"질식위험발생"
    }
}
app_url = "https://fcm.googleapis.com/fcm/send"
insert_url="http://192.168.10.40:5000/insert"
headers = {"Content-Type":"application/json",
           "Authorization":"key=AAAAvZIu-LY:APA91bHq84RkuUkFzeEhFTXp7lTU01PBOTLFCVKsASJZKWKViNPl3ySvscmfyKwfGDQV4SNTJkAc-OQXZkzlCoP7dLX3_kQ5-5HaHKn3OK6gtOiZQ6YDDPuVNPZzWvPaRVF8zy1w3cxG"}
categories = ["front", "side", "back"]


act = 0
count_act = 0
thresh = 35
max_diff = 5

a, b, c = None, None, None
cap = cv2.VideoCapture()
cap.open('http://192.168.10.41:8080/')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if cap.isOpened():
    ret, a = cap.read()[0],cap.read()[1][0:450,0:]
    ret, b = cap.read()[0],cap.read()[1][0:450,0:]
    while ret:
        ret, c = cap.read()[0],cap.read()[1][0:450,0:]
        draw = c.copy()
        if not ret:
            break

        a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)

        diff1 = cv2.absdiff(a_gray, b_gray)
        diff2 = cv2.absdiff(b_gray, c_gray)

        ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(diff1_t, diff2_t)

        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

        diff_cnt = cv2.countNonZero(diff)

        if count_act > 200 :
            act = 0
            count_act = 0
        if diff_cnt > max_diff:
            if count_act == 0:
                act = 1
            nzero = np.nonzero(diff)
            cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),
                          (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
            cv2.putText(draw, "Motion detected!!", (10, 30),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))

        if act == 1 and count_act == 0 :
            count_act = 1
        if count_act > 0:
            count_act += 1
        if count_act == 100 :

            print ("motion detected!")
            ret, image = cap.read()
            image = cv2.resize(image, (640, 480))
            cv2.imwrite('/home/pi/Detection/image%s.jpg' % count, image)
            
            cap.release()
            model = load_model('/home/pi/model1023.h5')
            img = cv2.imread('/home/pi/Detection/image%s.jpg' % count)

            img = cv2.resize(img, (64, 64))
            data = np.asarray(img)
            data = data / 255
            a = np.reshape(data,(1,64,64,3))
            predict = model.predict_classes(a)
            print(categories[predict[0]])
            cap.open('http://192.168.10.41:8080/')
            
            if categories[predict[0]] == 'back':
                cap.release()
                response = requests.post(app_url, data=json.dumps(datas), headers=headers)
                print("status code: ", response.status_code)
                sound02.sound()

                #img_post.req_post("http://192.168.30.3:5000/pyupload",count)
                requests.get(insert_url)
                cap.open('http://192.168.10.41:8080/')

            count += 1

        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('motion', stacked)

        a = b
        b = c
        if count_act % 100 == 0 and count_act != 0:
            print(count_act)
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
`