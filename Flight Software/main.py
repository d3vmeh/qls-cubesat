import comms
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from picamera2 import Picamera2
import adcs
import imaging
import store_data
import time


gs_address = "5C:E9:1E:6A:B7:88"

def on_launch():

    adcs.calibrate_gyro()
    adcs.calibrate_mag

    return comms.bluetooth_setup()


success, logs = on_launch()

if success:
    print("CubeSat setup success.")
    imaging.setup()

    while True:
        send_image = 'y'#input("Send image?")
        store_data.write_data([400,0.75,12.13,32.5,146.12,3.6])
        image_path = imaging.capture_image()
        
        if send_image == 'y':
            print("Sending Image to Ground Station...")
            print(comms.send_image(image_path,gs_address))

            time.sleep(4)
            



else:
    print("Cubesat setup failed. See following list for errors: ")
    for l in logs:
        print(l)




comms.bluetooth_disconnect()