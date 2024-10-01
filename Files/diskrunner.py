"""
Use me to erase or test individual drives

"""

import main3 as main
disks = main.findConnectedDrives()

from surfaceScan import basicSurfaceScan

# basicSurfaceScan("disk3")
main.eraseDrive("disk6")


"""
sudo -S fsck_hfs -fy -S /dev/disk3 && curl -d "Disk finished scanning" beansissue.hopto.org:1234/hddtest || curl -d "Disk has bad blocks" beansissue.hopto.org:1234/hddtest
"""