import os
def surfaceScan(diskNumber, Name, Type, Size, root, connectedDriveList, alertUserWhenComplete=False):
    noti_server = "http://beansissue.hopto.org:1234/hddtest"


    def notify(message):
        os.system(f"curl -H 'Surface scan on disk{diskNumber}' -d '{message}' {noti_server}")
    try:
        diskNumber.replace("disk", "")
    except:
        pass
    command = f"echo hhhh | sudo -S fsck_hfs -fy -S -n /dev/{diskNumber}"
    output = os.popen(command).read()
    if "*** no match ***" in output or "non I/O error" in output or "volumeType is 0" not in output:
        output = None
    if output:
        print(output)
        if alertUserWhenComplete:
            notify(f"Surface scan reported no bad blocks for {diskNumber}")
        driveIsHappy = True
    else:
        print("No output")
        if alertUserWhenComplete:
            notify(f"Surface scan failed for {diskNumber}")
        driveIsHappy = False
    if driveIsHappy:
        from testAllConnectedDrives import finishDiskCheck
        finishDiskCheck(diskNumber, Name, Type, Size, root, connectedDriveList)

def basicSurfaceScan(diskNumber, alertUserWhenComplete=True):
    noti_server = "http://beansissue.hopto.org:1234/hddtest"
    def notify(message):
        os.system(f"curl -H 'Surface scan on disk{diskNumber}' -d '{message}' {noti_server}")
    try:
        diskNumber.replace("disk", "")
    except:
        pass
    command = f"echo hhhh | sudo -S fsck_hfs -fy -S -n /dev/{diskNumber}"
    output = os.popen(command).read()
    if "*** no match ***" in output or "non I/O error" in output or "volumeType is 0" not in output:
        output = None
        
    if output:
        print(output)
        if alertUserWhenComplete:
            notify(f"Surface scan reported no bad blocks for {diskNumber}\n\n{output}")
    else:
        print("No output")
        if alertUserWhenComplete:
            notify(f"Surface scan failed for {diskNumber}\n\n{output}")

def scanAndEmailResults(diskNumber, targetEmails=["loukas@re-macs.com"]):
    noti_server = "http://beansissue.hopto.org:1234/hddtest"
    def notify(message):
        os.system(f"curl -H 'Surface scan on disk{diskNumber}' -d '{message}' {noti_server}")

    
    
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg.set_content("Surface scan results")
    msg["Subject"] = "Surface scan results"
    msg["From"] = "Surface Surfer"
    msg["To"] = targetEmails
    
    try:
        diskNumber.replace("disk", "")
    except:
        print("Disknumber did not contain 'disk'")
        
    command = f"echo hhhh | sudo -S fsck_hfs -fy -S -n /dev/{diskNumber}"
    output = os.popen(command).read()
    if "*** no match ***" in output or "non I/O error" in output or "volumeType is 0" not in output:
        output = None
    
    
if __name__ == "__main__":
    basicSurfaceScan("disk6")
    basicSurfaceScan("disk7")