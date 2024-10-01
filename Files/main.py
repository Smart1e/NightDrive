import subprocess
import sys

databaseTypeIDs = {
    '3.5" HDD 160GB': 'PartType364',
    '3.5" HDD 250GB': 'PartType365',
    '3.5" HDD 320GB': 'PartType366',
    '3.5" HDD 500GB': 'PartType367',
    '3.5" HDD 750GB': 'PartType368',
    
    '3.5" HDD 1TB': 'PartType369',
    '3.5" HDD 2TB': 'PartType370',
    '3.5" HDD 3TB': 'PartType371',
    '3.5" HDD 4TB': 'PartType372',
    
    '2.5" HDD 160GB': 'PartType373',
    '2.5" HDD 250GB': 'PartType374',
    '2.5" HDD 320GB': 'PartType375',
    '2.5" HDD 500GB': 'PartType376',
    '2.5" HDD 750GB': 'PartType377',
    
    '2.5" HDD 1TB': 'PartType378',
    '2.5" HDD 2TB': 'PartType379',
    
    '2.5" SSD 256GB': 'PartType380',
    '2.5" SSD 256GB': 'PartType381',
    '2.5" SSD 512GB': 'PartType382',
    
    '2.5" SSD 1TB': 'PartType383',
    '2.5" SSD 2TB': 'PartType384',
    '2.5" SSD 4TB': 'PartType385',
}
def ssd_size_round(num, Drivetype):
    """
    Rounds a number to the nearest SSD size.
    """
    num = float(num)
    if Drivetype =='SSD':
        if num <= 10:

            sizes = [1, 2, 4]
            nearest_size = min(sizes, key=lambda x:abs(x-int(num)))
            nearest_size = str(int(nearest_size)) + 'TB'
        else:
            sizes = [
                    128,
                    256,
                    512,
                    ]
            nearest_size = min(sizes, key=lambda x:abs(x-int(num)))
            nearest_size = str(int(nearest_size)) + 'GB'

    elif Drivetype == 'HDD':

        if num <= 10:

            sizes = [
                    1,
                    2,
                    3,
                    4
                    ]
            nearest_size = min(sizes, key=lambda x:abs(x-int(num)))
            nearest_size = str(int(nearest_size)) + 'TB'
        else:

            sizes = [
                    160,
                    250,
                    320,
                    500,
                    750
                    ]
            nearest_size = min(sizes, key=lambda x:abs(x-int(num)))
            nearest_size = str(int(nearest_size)) + 'GB'
            
    else:
        print("Unknown drive type")
    
    
    
    return nearest_size


def getDiskSize(info_text):
    info_text = str(info_text)
    if " TB" in info_text:
        info_text = info_text.split(" TB")[0]
    elif " GB" in info_text:
        info_text = info_text.split(" GB")[0]
    info_text = info_text.split(' ')[-1].split('.')[0]
    info_text = ssd_size_round(info_text, driveType)
    return info_text

  
def getDiskGirth(info_text):
    inches = {
        "4096": '2.5"',
        "512": '3.5"',
    }
    info_text = str(info_text)
    info_text = info_text.split("Device Block Size:")[-1].split("Bytes")[0].strip()
    for key, value in inches.items():
        if key in info_text:
            info_text = value
    inputtedGirth = input("Unable to find girth, please enter manually\n")
    if '3' in inputtedGirth:
        info_text = '3.5"'
    elif '2' in inputtedGirth:
        info_text = '2.5"'
    return info_text  


def getDiskType(info_text):

    info_text = str(info_text)
    solid = info_text.lower()
    solid = solid.split("solid state:")[1]
    solid = solid.split("\n")[0]
    
    if "yes" in solid:
        info_text = "SSD"
    elif "rotational" in info_text.strip().lower():
        info_text = "HDD"
    else:
        print(solid)
        info_text = input("Unable to find type, HDD or SSD?\n").upper()
    return info_text


diskNum = int(input("What is the disknumber?\ndisk"))
diskutilInfo = subprocess.run(["diskutil", "info", "disk" + str(diskNum)], capture_output=True, text=True)
if "Could not find disk: disk" + str(diskNum) in diskutilInfo.stderr:
    print("Disk not found")
    sys.exit()
else:
    driveType = getDiskType(diskutilInfo.stdout)
    driveSize = getDiskSize(diskutilInfo.stdout)
    driveGirth = getDiskGirth(diskutilInfo.stdout)
    
    if driveType == "SSD":
        driveGirth = "2.5\""
    finalOut = f"{driveGirth} {driveType} {driveSize}"

for key, value in databaseTypeIDs.items():
    if key in finalOut:
        print(value)
        print(finalOut)
        PushToDatabase = input("Push to database? (y/n)\n").lower()
        if 'y' in PushToDatabase:
            from pusher import toDatabaseHDD
            toDatabaseHDD(value)
            print("Pushed to database\nPrinting Label")
            try:
                from pusher import getMostRecentPart
                partnumber = getMostRecentPart()
            except:
                print("Unable to get part number, ending.")
                sys.exit()
            try:
                from qlprint import main
                labelString = f"Part Number: {partnumber}\n{finalOut}"
                main(mode = "text", text = labelString, fontsize = 18)
            except:
                print("pee pee poo poo") # Written by the robot
            sys.exit()
        else:
            sys.exit()
else:
    print("Drive not found in database")
    print(finalOut)
    sys.exit()