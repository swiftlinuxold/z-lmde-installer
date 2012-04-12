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
os.system ('echo =======================================')
os.system ('echo BEGIN ADDING AND CHANGING THE INSTALLER')

# Replace text in a file        
def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)
    
def add_pkg (packages):
    os.system ('echo INSTALLING ' + packages)
    os.system ('apt-get install -qq ' + packages)
    
def remove_line_from_file (filename, string_trigger):
    for line in fileinput.input(filename,inplace =1):
        line = line.strip()
        if not string_trigger in line:
            print line 

# Adding the live-installer package
add_pkg ('live-installer')
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

src = dir_develop + '/installer/usr_share_live-installer/languages'
dest = '/usr/share/live-installer/languages'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/usr_share_live-installer/locales'
dest = '/usr/share/live-installer/locales'
shutil.copyfile (src, dest)


# Replace /etc/issue, /etc/issue.net, /etc/lsb-release, and /etc/linuxmint/info
src = dir_develop + '/installer/etc/issue'
dest = '/etc/issue'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/etc/issue.net'
dest = '/etc/issue.net'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/etc/lsb-release'
dest = '/etc/lsb-release'
shutil.copyfile (src, dest)

src = dir_develop + '/installer/etc_linuxmint/info'
dest = '/etc/linuxmint/info'
shutil.copyfile (src, dest)

# Install apt-rdepends to recursively obtain list of live-installer package dependencies
os.system ('dpkg -i ' + dir_develop + '/installer/deb/apt-rdepends*.deb')
file_deps = 'list.txt'
os.system ('rm ' + file_deps)
os.system ('apt-rdepends live-installer >> ' + file_deps)

# Alter the list so it can be used in an apt-get install command
import fileinput
for line in fileinput.input(file_deps,inplace =1):
    line = line.split("(")[0] # In each line, remove '(' and everything that comes afterwards
    print line
change_text (file_deps, '  Depends: ', '')
change_text (file_deps, '  PreDepends: ', '')
change_text (file_deps, '\n\n ', '\n')
# Remove from package installation list the packages with no installation candidate
remove_line_from_file (file_deps, 'debconf-2.0')
remove_line_from_file (file_deps, 'awk')
remove_line_from_file (file_deps, 'libgl1')
remove_line_from_file (file_deps, 'libblas.so.3gf')
remove_line_from_file (file_deps, 'liblapack.so.3gf')
list_with_newlines = open(file_deps, 'r').read()
list_with_spaces = list_with_newlines.replace ('\n', ' ')
os.system ('rm ' + file_deps)
os.system ('echo RECURSIVELY UPDATING live-installer and dependencies')
os.system ('echo PRE-CORRECTING installation errors')
add_pkg ('libgl1-mesa-swx11 libgl1-mesa-glx')
add_pkg ('debconf cdebconf')
add_pkg ('libblas3gf libatlas3gf-base')
add_pkg ('liblapack3gf libatlas3gf-base')
add_pkg ('original-awk mawk gawk')
os.system ('echo NOW UPDATING live-installer and dependencies')
add_pkg (list_with_spaces)
os.system ('echo FINISHED ADDING AND CHANGING THE INSTALLER')
os.system ('echo ==========================================')
