import subprocess


def run_command(command):
    words = command.split(" ")

    process = subprocess.Popen(words, stdout=subprocess.PIPE)

    message = None
    for line in process.stdout:
        message = line

    if message != None and len(message)>0:
        return message.strip()
    
    return message

def bluetooth_setup():
    power_on = run_command("bluetoothctl power on")
    agent_on = run_command("bluetoothctl agent on")
    default_agent = run_command("bluetoothctl default-agent")
    discoverable_on = run_command("bluetoothctl discoverable on")
    pairable_on = run_command("bluetoothctl pairable on")
    #cancel_pairing = run_command("bluetoothctl cancel-pairing 5C:E9:1E:6A:B7:88")
    pair = run_command("bluetoothctl pair 5C:E9:1E:6A:B7:88")
    disconnect = run_command("bluetoothctl disconnect 5C:E9:1E:6A:B7:88")

    connect = run_command("bluetoothctl connect 5C:E9:1E:6A:B7:88")
    print(connect)

    messages = [power_on, agent_on, default_agent, discoverable_on, pairable_on, pair, disconnect, connect]

    if "success" in str(connect.lower()):
        return True, messages
    else:
        return False, messages



def bluetooth_disconnect():
    disconnect = run_command("bluetoothctl disconnect 5C:E9:1E:6A:B7:88")


def send_image(image_name, mac_address):
    c = "obexftp -b " + mac_address +" -p " + image_name
    #subprocess.run([c])
    process = subprocess.Popen(c,shell=True)
    return process

 
# subprocess.run(['bluetoothctl',  'agent' , 'on'], stdout=subprocess.PIPE)


# subprocess.run(['bluetoothctl',  'default-agent'], stdout=subprocess.PIPE)


# subprocess.run(['bluetoothctl',  'discoverable' , 'on'], stdout=subprocess.PIPE)


# subprocess.run(['bluetoothctl',  'pairable' , 'on'], stdout=subprocess.PIPE)

# subprocess.run(['bluetoothctl',  'scan' , 'on'], stdout=subprocess.PIPE)

#subprocess.run(["bluetoothctl agent on"])



#subprocess.Popen(["bluetoothctl"], stdout=subprocess.PIPE, stdin=subprocess.PIPE,bufsize=1)
#print("asd")


import subprocess as sub

# p = sub.Popen(["python", "-i"], stdin=sub.PIPE, stdout=sub.PIPE)
# print("The process said: " + p.communicate("help")[0])
#open_blue = subprocess.Popen(["bluetoothctl power on", "bluetoothctl agent on", "bluetoothctl scan on", "bluetoothctl pair 5C:E9:1E:6A:B7:88", "bluetoothctl connect 5C:E9:1E:6A:B7:88"], shell=True, stdout=subprocess.PIPE,
                            # stderr=subprocess.STDOUT, stdin=subprocess.PIPE)



# while True:  # lets wait for 'user' prompt
#     line = open_blue.stdout.readline().rstrip()
#     if str(line).endswith("#"):  # this is the prompt, presumably, so stop reading STDOUT
#         break
#     print(line)  # print the subprocesses STDOUT
#     print("\n")

# open_blue.stdin.write("help\n")  # send the `help` command

# while True:  # lets repeat the above process
#     line = open_blue.stdout.readline().rstrip()
#     if line.endswith("#"):  # this is the prompt, presumably, so stop reading STDOUT
#         break
#     print(line + "\n")  # print the subprocesses STDOUT

# # now you can issue another command... and so on.