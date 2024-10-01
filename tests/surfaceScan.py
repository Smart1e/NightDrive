import subprocess

def run_disk_check(disk_identifier):
    """
    Runs a disk check using macOS's diskutil command.

    :param disk_identifier: String representing the disk identifier (e.g., 'disk1')
    :return: Tuple containing (output, error) from the diskutil command
    """
    try:
        # Constructing the diskutil command
        command = ["diskutil", "verifyDisk", disk_identifier]

        # Executing the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decoding the output and error from byte format to string
        return stdout.decode(), stderr.decode()
    except Exception as e:
        return "", str(e)

# Example usage:
disk_id = "disk2"  # Replace with your disk identifier
output, error = run_disk_check(disk_id)

print("Disk Check Output:")
print(output)

if error:
    print("Error:")
    print(error)
