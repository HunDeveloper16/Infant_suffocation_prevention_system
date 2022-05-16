import requests
import os

def req_post(url,count):
    try:
        upload = {"img" : open('/home/pi/Detection/image'+str(count)+'.jpg', 'rb')}
        r = requests.post(url, files = upload)
        print(r.text)
    except:
        print("File upload ERROR")
