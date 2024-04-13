import sys

print(sys.version)

from bluepy.btle import Scanner

scanner = Scanner()
devices = scanner.scan(10.0)


for device in devices:
    print(device.addr)
    if device.addr == "5c:e9:1e:6a:b7:88" :
        print("Found Ground Station MAC Address")

    