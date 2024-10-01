"""
Use me to erase all connected drives

"""


import tkinter as tk
import os
import multiprocessing
import time

inch25Button = None
inch35Button = None
def girthButtonPressed(girth):
    unactiveButtonColour = "darkgrey"
    activeButtonColour = "blue"
    if girth == "2.5\"":
        inch25Button.config(fg=activeButtonColour)
        inch35Button.config(fg=unactiveButtonColour, )
    elif girth == "3.5\"":
        inch25Button.config(fg=unactiveButtonColour)
        inch35Button.config(fg=activeButtonColour)
    inch25Button.update()
    inch35Button.update()
    print(girth)
    return girth

def getDiskName(diskNumber):
    diskNumber = diskNumber.replace("disk", "")
    diskInformation = os.popen(f"diskutil info /dev/disk{diskNumber}").read()
    diskInformation = diskInformation.split("\n")
    diskName = ""
    for line in diskInformation:
        if "Device / Media Name" in line:
            diskName = line.split(":")[1].strip()
            break
    return diskName


def findConnectedDrives():
    driveList = os.popen("diskutil list | grep /dev/disk").read()
    externalDrives = []
    # Split the output into lines
    driveList = driveList.split('\n')
    # Ensure is only the full drives
    for drive in driveList:
        if "external, physical" in drive:
            diskNumber = ""
            diskNumber = drive.split(" ")[0].split("/")[2]
            externalDrives.append(diskNumber)

            
    return externalDrives        

def getDiskSize(driveNumber):
    if "disk" not in driveNumber:
        driveNumber = f"disk{driveNumber}"
    diskSizeOut = os.popen(f"diskutil info {driveNumber} | grep 'Disk Size:'").read()
    diskSize = diskSizeOut.split(":")[1].strip().split(" ")[0].split(".")[0] + " " + diskSizeOut.split(":")[1].strip().split(" ")[1]
    
    return diskSize.replace(" ", "")

def getSMARTData(driveNumber):
    smartData = os.popen(f"smartctl -a /dev/{driveNumber}").read()

        
    print(smartData)

def eraseDrive(drive):
    command = f"say Erasing {drive} && diskutil secureErase 0 {drive} && (curl -d '{drive} erased' beansissue.hopto.org:1234/hddtest && say '{drive} successfully erased.') || (curl -d '{drive} failed to erase' beansissue.hopto.org:1234/hddtest && say '{drive} failed to erase.')"
    os.system(command)

def eraseConnectedDrives():
    print("Erasing connected drives")
    connectedDrives = findConnectedDrives()  # Make sure this function returns a list of drives

    # Create a process for each drive
    processes = []
    for drive in connectedDrives:
        print(f"Erasing {drive}")
        process = multiprocessing.Process(target=eraseDrive, args=(drive,))
        processes.append(process)
        process.start()
        time.sleep(1.5)
        
if __name__ == "__main__":
    eraseConnectedDrives()
    print(findConnectedDrives())
    root = tk.Tk()
    root.title("HDD Pusher")
    root.geometry("300x500")

    title = tk.Label(root, text="HDD Pusher", font=("Helvetica", 25))
    title.pack()

    tk.Frame(root, width=0, height=70).pack() # Spacer


    driveTypeGirthFrame = tk.Frame(root)
    inch25Button = tk.Button(driveTypeGirthFrame,
                            text="2.5\"",
                            width=10,
                            height=5,
                            borderwidth=0,
                            relief=tk.FLAT,
                            command=lambda: girthButtonPressed("2.5\"")
                            )
    inch25Button.pack(side=tk.LEFT)
    inch35Button = tk.Button(driveTypeGirthFrame,
                            text="3.5\"",
                            width=10,
                            height=5,
                            borderwidth=0,
                            relief=tk.FLAT,
                            command=lambda: girthButtonPressed("3.5\"")
                            )
    inch35Button.pack(side=tk.LEFT)
    driveTypeGirthFrame.pack()




    tk.Frame(root, width=100, height=100, bg="red").pack() # TestSquare

    root.mainloop()