import os
import multiprocessing
import time
import queue
import threading
import subprocess


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
        
def guessDriveType(drive):
    name = getDiskName(drive)
    
    polishedAndRounded = name.lower().replace(" ", "").replace("-", "").replace("_", "")
    
    if polishedAndRounded[:2] == "hd":
        return "HDD"
    elif "hdd" in polishedAndRounded or "wdc" in polishedAndRounded:
        return "HDD"
    elif "ssd" in polishedAndRounded or "kingston" in polishedAndRounded or "samsung" in polishedAndRounded:
        return "SSD"
    else:
        return "Unknown"

def getAllInfo():
    connectedDrives = findConnectedDrives()
    returnJSONArray = []
    for drive in connectedDrives:
        returnJSON = {'identifier': drive, 'size': getDiskSize(drive), 'type': guessDriveType(drive), 'physical_size': ''}
        returnJSONArray.append(returnJSON)
    return returnJSONArray

def surfaceScan(diskNumber, result_label, notify_function=None, alertUserWhenComplete=False):
    noti_server = "http://beansissue.hopto.org:1234/hddtest"
    
    def notify(message):
        os.system(f"curl -H 'Surface scan on disk{diskNumber}' -d '{message}' {noti_server}")
    
    def run_fsck_hfs(output_queue, diskNumber):
        cmd = ["sudo", "-A", "fsck_hfs", "-fy", "-S", "-n", f"/dev/{diskNumber}"]
        fsck_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        full_output = ""
        
        while True:
            output = fsck_process.stdout.readline()
            if output == "" and fsck_process.poll() is not None:
                break
            if output:
                full_output += output
                output_queue.put(output.strip())
        
        # Ensure any remaining output is read
        remaining_output, remaining_error = fsck_process.communicate()
        full_output += remaining_output + remaining_error
        if remaining_output:
            output_queue.put(remaining_output.strip())
        if remaining_error:
            output_queue.put(remaining_error.strip())
        
        output_queue.put("DONE")
        output_queue.put(full_output.strip())
    
    def read_output(output_queue):
        if stop_thread.is_set():
            return
        try:
            while True:
                line = output_queue.get_nowait()
                if line == "DONE":
                    check_final_status(output_queue)
                    return
                elif "No bad blocks found." in line or "Bad blocks found!" in line:
                    result_label.config(
                        text=line,
                        foreground="green" if "No bad blocks found." in line else "red",
                        font=("Helvetica", 16, "bold")
                    )
                else:
                    print(line)  # You could also update the label with this info if desired
        except queue.Empty:
            pass

    def check_final_status(output_queue):
        try:
            full_output = output_queue.get_nowait()
            if "volumeType is 0" in full_output:
                result_label.config(
                    text="No bad blocks found!",
                    foreground="green",
                    font=("Helvetica", 16, "bold")
                )
                driveIsHappy = True
            else:
                result_label.config(
                    text="Bad blocks found!",
                    foreground="red",
                    font=("Helvetica", 16, "bold")
                )
                driveIsHappy = False
        except queue.Empty:
            return  # No final output yet, return and wait for the next attempt

        if alertUserWhenComplete:
            notify(f"Surface scan {'reported no bad blocks' if driveIsHappy else 'found bad blocks'} for {diskNumber}")

        if notify_function:
            notify_function(diskNumber, driveIsHappy)
    
    # Start the scan
    global fsck_process, stop_thread
    stop_thread = threading.Event()
    stop_thread.clear()

    output_queue = queue.Queue()
    password = "hhh"

    scan_thread = threading.Thread(target=run_fsck_hfs, args=(output_queue, diskNumber))
    scan_thread.start()
    read_output(output_queue)
