def write_data(data):

    labels = ["Altitude","Battery charge", "Battery Temperature", "Roll", "Pitch", "Yaw"]
    file = open("data.txt",'w')
    i = 0
    for l in labels:
        file.write(l+": " + str(data[i])+"\n")
        i += 1


    file.close()
    print("data saved")
