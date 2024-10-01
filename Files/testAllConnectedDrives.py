"""
Use me to test / surface scan all connected drives

"""

import main3 as baseMods
import pusher as databaseAPI
import qlprint
from surfaceScan import surfaceScan
import tkinter
import threading

diskInformationDict = {}
if __name__ == "__main__":
    
    
    root = tkinter.Tk()
    connectedDriveList = baseMods.findConnectedDrives()


    diskNameList = []
    for drive in connectedDriveList:
        diskNameList.append(baseMods.getDiskName(drive))
        
    diskTypeList = []
    for drive in diskNameList:
        if "D" == drive.split(" ")[0]:
            diskTypeList.append("HDD")
        elif "hdd" in drive.lower():
            diskTypeList.append("HDD")
        elif "ssd" in drive.lower():
            diskTypeList.append("SSD")
        else:
            diskTypeList.append("UNKNOWN")
            
    diskSizeList = []
    for drive in connectedDriveList:
        diskSizeList.append(baseMods.getDiskSize(drive))

    print("Connected drives:")
    print(f"{len(connectedDriveList)} drives connected.")
    print(diskSizeList)
    for drive in connectedDriveList:
        indexOfLists = connectedDriveList.index(drive)
        print(f"{drive} | {diskNameList[indexOfLists]} | {diskTypeList[indexOfLists]}")
        
        surfaceScanThreads = {}
    
    for drive in connectedDriveList:
        surfaceScanThreads[drive] = threading.Thread(target=surfaceScan, args=(drive, diskNameList, diskTypeList, diskSizeList, root, connectedDriveList, True,))
        surfaceScanThreads[drive].daemon = True
        surfaceScanThreads[drive].start()
        
    root.mainloop()

def setGirthVariable(variable, value, btn25, btn35, window):
    global diskInformationDict
    if value == '2.5"':
        btn35.deselect()
        diskInformationDict["diskGirth"] = "2.5\""
    else:
        btn25.deselect()
        diskInformationDict["diskGirth"] = "3.5\""
    window.update()
    variable = value
    return variable

def setDiskTypeVariable(variable, value, btnHDD, btnSSD, window, diskStorageSizeDropdown, diskSizeVar):
    global diskInformationDict
    SSDSizes = ["128GB", "256GB", "512GB", "1TB", "2TB", "4TB", "Other"]
    HDDSizes = ["160GB", "250GB", "320GB", "500GB", "750GB", "1TB", "2TB", "3TB", "4TB", "Other"]
    diskStorageSizeDropdown['menu'].delete(0, 'end'); [diskStorageSizeDropdown['menu'].add_command(label=size, command=lambda size=size: diskSizeVar.set(size)) for size in (HDDSizes if value == 'HDD' else SSDSizes)]

    if value == 'HDD':
        btnSSD.deselect()
        diskInformationDict["diskType"] = "HDD"
    else:
        btnHDD.deselect()
        diskInformationDict["diskType"] = "SSD"
    window.update()
    variable = value
    return variable

def submit(infoDict, printLabelVar, finalDiskSize):
    global diskInformationDict
    infoDict = diskInformationDict
    infoDict["diskSize"] = finalDiskSize.get()
    
    for value in infoDict.items():
        print(value)
        if value[1] == "":
            print("Please fill out all fields")
            return
    databaseAPI.toDatabaseHDD(databaseAPI.returnPartTypeID(infoDict))
    qlprint.main("text", None, f"{databaseAPI.getMostRecentPart()}\n{diskInformationDict['diskGirth']} {diskInformationDict['diskType']} ({diskInformationDict['diskSize']})", 20)
    print("Will print as a label" if printLabelVar.get() == 1 else "Will not print as a label")
    print("Submitted")
    
def finishDiskCheck(diskNumber, diskNameList, diskTypeList, diskSizeList, root, connectedDriveList):
    if "disk" not in diskNumber:
        diskNumber = f"disk{diskNumber}"
    print(f"Finished surface scan on {diskNumber}")
    global diskInformationDict
    
    diskInformationDict["diskNumber"] = diskNumber
    diskInformationDict["diskType"] = diskTypeList[connectedDriveList.index(diskNumber)]
    diskInformationDict["diskSize"] = diskSizeList[connectedDriveList.index(diskNumber)]
    diskInformationDict["diskGirth"] = ""
    
    diskPushing = tkinter.Toplevel(root)
    diskPushing.title(f"{diskNumber.title()} Pusher")
    
    diskTypeButtonHDD = tkinter.Checkbutton(diskPushing, text='HDD', command=lambda: setDiskTypeVariable(diskInformationDict["diskType"], "HDD", diskTypeButtonHDD, diskTypeButtonSSD, diskPushing, diskStorageSizeDropdown, finalDiskSize))
    diskTypeButtonSSD = tkinter.Checkbutton(diskPushing, text='SSD', command=lambda: setDiskTypeVariable(diskInformationDict["diskType"], "SSD", diskTypeButtonHDD, diskTypeButtonSSD, diskPushing, diskStorageSizeDropdown, finalDiskSize))
    
    diskGirthButton25 = tkinter.Checkbutton(diskPushing, text='2.5"', command=lambda: setGirthVariable(diskInformationDict["diskGirth"], "2.5\"", diskGirthButton25, diskGirthButton35, diskPushing))
    diskGirthButton35 = tkinter.Checkbutton(diskPushing, text='3.5"', command=lambda: setGirthVariable(diskInformationDict["diskGirth"], "3.5\"", diskGirthButton25, diskGirthButton35, diskPushing))
    
    reportedDiskSizeLabel = tkinter.Label(diskPushing, text="Reported Disk Size: " + diskSizeList[connectedDriveList.index(diskNumber)])
    
    
    SSDSizes = ["128GB", "256GB", "512GB", "1TB", "2TB", "4TB", "Other"]
    HDDSizes = ["160GB", "250GB", "320GB", "500GB", "750GB", "1TB", "2TB", "3TB", "4TB", "Other"]
    finalDiskSize = tkinter.StringVar()
    if diskTypeList[connectedDriveList.index(diskNumber)] == "SSD":
        diskTypeButtonSSD.select()
        diskStorageSizeDropdown = tkinter.OptionMenu(diskPushing, finalDiskSize, "128GB", "256GB", "512GB", "1TB", "2TB", "4TB", "Other")
        if diskInformationDict["diskSize"] in SSDSizes:
            diskStorageSizeDropdown.setvar("Other")
        else:
            diskStorageSizeDropdown.setvar("Other")
            
            
    elif diskTypeList[connectedDriveList.index(diskNumber)] == "HDD":
        diskTypeButtonHDD.select()
        diskStorageSizeDropdown = tkinter.OptionMenu(diskPushing, finalDiskSize, "160GB", "250GB", "320GB", "500GB", "750GB", "1TB", "2TB", "3TB", "4TB", "Other")
        if diskInformationDict["diskSize"] in HDDSizes:
            diskStorageSizeDropdown.setvar(diskInformationDict["diskSize"])
        else:
            diskStorageSizeDropdown.select(HDDSizes.index("Other"))
    
    else:
        print("Unknown disk type")
        diskStorageSizeDropdown = tkinter.OptionMenu(diskPushing, finalDiskSize, "Other")
            
    printLabelVar = tkinter.IntVar()
    printLabelCheckbox = tkinter.Checkbutton(diskPushing, text="Print Label", variable=printLabelVar)
    printLabelCheckbox.select()
    
    submitButton = tkinter.Button(diskPushing, text="Submit", command=lambda: submit(diskInformationDict, printLabelVar, finalDiskSize))
    
    diskTypeButtonHDD.pack()
    diskTypeButtonSSD.pack()
    
    diskGirthButton25.pack()
    diskGirthButton35.pack()
    
    reportedDiskSizeLabel.pack()
    
    diskStorageSizeDropdown.pack()
    
    printLabelCheckbox.pack()
    
    submitButton.pack()
    
    
    
    
    
    
    
    