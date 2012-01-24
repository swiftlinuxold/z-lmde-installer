#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

import shutil
print '======================================='
print 'BEGIN ADDING AND CHANGING THE INSTALLER'

# Adding the live-installer package
os.system('apt-get install -y live-installer')
# os.system('') # Automatically clicks on OK.  Without this command, you would have to do this manually.

# mint-debian-installer files:
# /etc/skel/Desktop/mint-debian-installer.desktop
# /usr/bin/mint-debian-installer
# /usr/lib/linuxmint/mint-debian-installer/icon.png (change)
# /usr/lib/linuxmint/mint-debian-installer/mint-debian-installer.glade (change)
# /usr/lib/linuxmint/mint-debian-installer/mint-debian-installer.py (change)
# /usr/lib/linuxmint/mint-debian-installer/version.py
# /usr/share/applications/mint-debian-installer.desktop

# src = dir_develop + '/installer/mint-debian-installer/icon.png'
# dest = '/usr/lib/linuxmint/mint-debian-installer/icon.png'
# shutil.copyfile (src, dest)

# src = dir_develop + '/installer/mint-debian-installer/mint-debian-installer.glade'
# dest = '/usr/lib/linuxmint/mint-debian-installer/mint-debian-installer.glade'
# shutil.copyfile (src, dest)

# src = dir_develop + '/installer/mint-debian-installer/mint-debian-installer.py'
# dest = '/usr/lib/linuxmint/mint-debian-installer/mint-debian-installer.py'
# shutil.copyfile (src, dest)


print 'FINISHED ADDING AND CHANGING THE INSTALLER'
print '=========================================='
