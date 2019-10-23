import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None 

myHostname = "yourserverdomainorip.com"
myUsername = "root"
myPassword = "12345"

srv = pysftp.Connection(host="192.168.1.160", username="root",password="iluvr0hde",cnopts=cnopts)
srv.cwd('/home/instrument/fw/data')
data = srv.listdir()            # Get the directory and file listing
srv.
srv.close()                     # Closes the connection
for i in data:                  # Prints out the directories and files, line by line

    print(i)