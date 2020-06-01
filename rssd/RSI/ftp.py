import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

myHostname = "192.168.1.160"
myUsername = "root"
myPassword = "iluvr0hde"
remotePath = '/home/instrument/fw/data/iqrecorder/'
localPath  = 'C:\\Users\\lim_m\\Desktop\\CMPTEstData\\'
filename   = 'IQFile.iqw'

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:
    print("Connection succesfully established ... ")

    sftp.get(remotePath+filename, localPath+filename)
    # sftp.cwd(remotePath)
    # data = sftp.listdir_attr()            # Get the directory and file listing

# for i in data:                  # Prints out the directories and files, line by line
#     print(f'{i.filename} {i.st_size}')
