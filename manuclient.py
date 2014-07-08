import thread
import telnetlib
import time

# Server details
HOST = "serverip"
PORT = "port"

# User details
user = "username"
password = "password"

# Color mapping - allows for remapping
colors = {"^0":"\033[0;30m",
          "^1":"\033[0;31m",
          "^2":"\033[0;32m",
          "^3":"\033[0;33m",
          "^4":"\033[0;34m",
          "^5":"\033[0;35m",
          "^6":"\033[0;36m",
          "^7":"\033[0;37m",
          "^8":"\033[0;38m",
          "^9":"\033[0;39m"}

# Key mapping (here, f is restricted)
keymap = {"g":"getinfo players\n",
          "b":"!cmdlist\n"}

# Connect to server
tn = telnetlib.Telnet(HOST, PORT)
tn.read_until("User: ")
tn.write(user + "\n")
tn.read_until("Password: ")
tn.write(password + "\n")
          
# Read the console from sever
def read_console():
   while True:
       response = tn.read_until("\n")
       for k, v in colors.iteritems():
           response = response.replace(k, v)
       print time.strftime('%X'),":",response.replace("\n",""),"\033[0;37m"
       if len(response)<1:
           break

# Handle interaction
def key_hook():
    free_chat = 0
    while True:
        key = raw_input('')
        if free_chat == 1:
            tn.write(key+"\n")
            free_chat = 0
        else:
            if key == "f":
                free_chat = 1
            if keymap.has_key(key):
                tn.write(keymap[key])

# Start the threads
try:
   thread.start_new_thread(read_console,())
   thread.start_new_thread(key_hook,())
except:
   print "Error: unable to start threads"
   tn.close()

while 1:
   time.sleep(0.001)
   pass
