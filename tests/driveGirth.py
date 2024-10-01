import subprocess

def run_command(command):
    """ Run a shell command and return its output """
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout

def check_drive_type(disk):
    """ Check if a disk is an SSD or HDD """
    info = run_command(f'diskutil info {disk}')
    if "Solid State: Yes" in info:
        return "SSD"
    elif "Solid State: No" in info:
        return "HDD"
    else:
        return "Unknown"

# List all disks
disks = run_command('diskutil list')

# Assuming you know the disk identifier (e.g., /dev/disk2)
disk_type = check_drive_type('/dev/disk1')
print(f"Disk Type: {disk_type}")
