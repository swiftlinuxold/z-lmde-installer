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

src = dir_develop + '/installer/etc_live-installer/install.conf'
dest = '/etc/live-installer/install.conf'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_lib_live-installer_frontend/gtk_interface.py'
dest = '/usr/lib/live-installer/frontend/gtk_interface.py'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_lib_live-installer/installer.py'
dest = '/usr/lib/live-installer/installer.py'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_share_icons/live-installer.png'
dest = '/usr/share/icons/live-installer.png'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_share_icons/live-installer.xpm'
dest = '/usr/share/icons/live-installer.xpm'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_share_live-installer/logo.png'
dest = '/usr/share/live-installer/logo.png'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_share_live-installer/logo.svg'
dest = '/usr/share/live-installer/logo.svg'
shutil.copyfile (src, dest)

print 'FINISHED ADDING AND CHANGING THE INSTALLER'
print '=========================================='
