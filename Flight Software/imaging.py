from picamera2 import Picamera2, Preview
import time

def setup():
    global picam2
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start()

    

    time.sleep(2)



def capture_image():
    #for i in range(10):
    time.sleep(0.2)
    img = picam2.capture_image("main")
    drawn_img = img
    imagepath = "test.jpg"
    img.save(imagepath)

    return imagepath

        
