import subprocess
import re
import json
import os


def get_physical_main_drive_sizes():
    # Run diskutil command
    result = subprocess.run(['diskutil', 'list', 'physical'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # Split the output into lines
    lines = output.split('\n')

    # Dictionary to hold disk sizes
    disk_sizes = {}

    # Iterate through the lines to find disk numbers and sizes
    for line in lines:
        if line.startswith('/dev/disk'):
            # Extract disk number
            disk_number = re.search(r'disk(\d+)', line).group(1)

            # Find the next line with the disk size
            size_line_index = lines.index(line) + 2  # Size is two lines down from the disk identifier
            size_line = lines[size_line_index]

            # Extract size in GB
            size_match = re.search(r'\*(\d+\.\d+) GB', size_line)
            if size_match:
                size = float(size_match.group(1))
                disk_sizes[f"disk{disk_number}"] = size
    del disk_sizes['disk0']
    return disk_sizes


def guess_drive_type_and_size(size):
    # Common SSD sizes in GB (approximated, including some real-world values like 960GB)
    ssd_sizes = [128, 256, 512, 960, 1024, 2048, 4096, 8192]

    # Closest match to the given size
    closest_size = min(ssd_sizes, key=lambda x: abs(x - size))

    # Guess if it's an SSD or HDD, using a smaller threshold for approximation
    if abs(closest_size - size) < 10:  # 12GB threshold for approximation
        if closest_size < 960:
            return 'SSD', '2.5"', str(closest_size) + "GB"
        else:
            return 'SSD', '2.5"', str(int(round(closest_size / 1024, 0))) + "TB"
    else:
        # Ask the user for the size of the HDD
        while True:
            hdd_size = input("Is the HDD 2.5 inches or 3.5 inches?: ")
            if "2" in hdd_size:
                if closest_size < 960:
                    return 'HDD', '2.5"', str(closest_size) + "GB"
                else:
                    return 'HDD', '2.5"', str(int(round(closest_size / 1024, 0))) + "TB"
            elif "3" in hdd_size:
                if closest_size < 960:
                    return 'HDD', '3.5"', str(closest_size) + "GB"
                else:
                    return 'HDD', '3.5"', str(int(round(closest_size / 1024, 0))) + "TB"
            else:
                print("Invalid input. Please try again.")
        

def matchToDatabase(driveType, driveSize, driveGirth):
    
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
    driveString = driveGirth + ' ' + driveType + ' ' + driveSize
    for key, value in databaseTypeIDs.items():
        if driveString == key:
            return value
        
        
def printLabel(label_images):
    backend = 'network'
    model = 'QL-700'
    printer = '192.168.1.181'
    
    
#Imports config file

try:
    with open('~/Documents/DrivePush/config.json') as path:
        config = json.load(path)
        printer = config['printer']
        labelFontSize = config['labelFontSize']
except FileNotFoundError:
    print("Config file not found! Creting now...")
    config = {
        "printer": "192.168.1.181",
        "labelFontSize": 10,
        "backend": "network"
        }
    
    # Create directory if it doesn't exist
    drive_push_dir = os.path.expanduser('~/Documents/DrivePush')
    os.makedirs(drive_push_dir, exist_ok=True)
    
    # Create the config file
    # Expand the tilde to the home directory
    file_path = os.path.expanduser('~/Documents/DrivePush/config.json')

    # Open the file for writing
    with open(file_path, 'w') as outfile:
        # Write some data to the file
        outfile.write(str(config))
    print("Config file created!")

    

# Get sizes of physical main drives
drive_sizes = get_physical_main_drive_sizes()
print("Main Drive Sizes:")
print(drive_sizes)
# Guess for each main drive
for disk, size in drive_sizes.items():
    drive_type, drive_girth, size = guess_drive_type_and_size(size)
    print(f"{disk} size: {size} is likely an {drive_type} ({drive_girth})")
    print(matchToDatabase(drive_type, str(size), drive_girth))
    

