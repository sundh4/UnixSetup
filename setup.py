#!/usr/bin/env python
# title           :setup.py
# description     :Interactive menu on CLI to Setup Linux Computer
# author          :Surya
# date            :2017-10-03
# version         :0.4
# usage           :python setup.py --public|--private
# notes           :Tested on Ubuntu 14.04
# python_version  :2.7.6
# =======================================================================

# Import the modules needed to run the script.
import sys
import os
import subprocess
import platform
# import socket
from shutil import copy
from subprocess import PIPE, Popen

# Script path variable
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# Arguments checker for public or private networks
if len(sys.argv) != 2:
    print "USAGE: \n------\npython %s <--public> or <--private>" % str(sys.argv[0])
    sys.exit(2)
else:
    ARG_OPTION = str(sys.argv[1])
    if ARG_OPTION == '--public':
        ZABBIX_SERVER = '10.153.64.48'
        WHICH_NETWORK = 'Public'
    elif ARG_OPTION == '--private':
        ZABBIX_SERVER = '10.153.64.65'
        WHICH_NETWORK = 'Private'
        # For sourcing list of Rprofile
        SOURCING2 = '.source4Efunction.r'
        SOURCING1 = '.sourceAlfunction.r'
    else:
        print "USAGE: \n------\npython %s <--public> or <--private>" % str(sys.argv[0])
        sys.exit(2)

# Link Download zabbix agent for ubuntu version 12 above
site_ub12 = "wget http://repo.zabbix.com/zabbix/2.2/ubuntu/pool/main/z/zabbix/zabbix-agent_2.2.14-1+precise_amd64.deb \
            -P /tmp/"
site_ub14 = "wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb \
            -P /tmp"
# site_ub13 = "wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb"
# site_ub15 = "wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb"
# site_fbsd = "wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb"


# Main definition - constants
menu_actions = {}
menu_mandatory = {}
menu_opt = {}

# ======================= #
#     MENUS FUNCTIONS     #
# ======================= #


# Execute Main Menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return


# Execute menu mandatory
def exec_mandatory(choice1):
    os.system('clear')
    ch = choice1.lower()
    if ch == '':
        menu_mandatory['menu_mandatory']()
    else:
        try:
            menu_mandatory[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_mandatory['menu_mandatory']()
    return


# Execute menu opt
def exec_opt(choice2):
    os.system('clear')
    ch = choice2.lower()
    if ch == '':
        menu_opt['menu_opt']()
    else:
        try:
            menu_opt[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_opt['menu_opt']()
    return


# Function to install Linux Library Agent
def library():
    print "Installing Linux Library & Dependencies !\n"
    # os.system('clear')
    print("Checking update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print("Starting to install libraries.....")
    print "(It depends on connection)"
    '''
    os.system("apt-get install -y libxml2 libxml2-dev gfortran curl libcurl3 libcurl3-dev libgfortran3 \\"
              "libpaper-utils cifs-utils ess tcl tcl-dev tk \\"
              "sssd libsss-sudo krb5-user nfs-common autofs pdftk netcdf-* liblzma-dev lzma lzma-dev \\"
              "gcc libtool libreadline-dev g++ xorg-dev mesa-common-dev libcgal-dev ssh libxml-descent-perl \\"
              'texlive latex2html imagemagick graphviz htop libodbc1 libbz2-dev;')
    '''
    os.system("apt-get install -y libxml2 libxml2-dev gfortran curl libcurl3 libcurl3-dev libgfortran3 \\"
              "libpaper-utils cifs-utils ess tcl tcl-dev tk \\"
              "sssd libsss-sudo krb5-user nfs-common autofs pdftk netcdf-* liblzma-dev lzma lzma-dev \\"
              "libtool libreadline-dev libcgal-dev ssh libxml-descent-perl enscript \\"
              "libmyodbc freetds-* unixodbc unixodbc-dev libcairo2 libcairo2-dev tdsodbc \\"
              'texlive latex2html imagemagick graphviz htop libodbc1 libbz2-dev libnss3-1d;')
    print "Finsih Installing Library"
    os.system('sleep 5')
    return


# Function to install OpenJDK JAVA 7
def java():
    print "Installing OpenJDK JAVA 7 !\n"
    print("Checking update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print("Starting to install OpenJDK Java 7.....")
    os.system('apt-get install -y --force-yes openjdk-7-jdk')
    os.system('sleep 5')
    return


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


# Function to install Tomcat7
def tomcat():
    print "Installing Tomcat7 !\n"
    # os.system('clear')
    tomusr = "$(sed -re 's/(TOMCAT7_USER=)[^=]*$/\\1root/' /etc/default/tomcat7 -i)"
    tomgrp = "$(sed -re 's/(TOMCAT7_GROUP=)[^=]*$/\\1root/' /etc/default/tomcat7 -i)"
    print("Checking update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print("Starting to install Tomcat7.....")
    os.system('apt-get install -y tomcat7')
    subprocess.call(tomusr, shell=True)
    subprocess.call(tomgrp, shell=True)
    os.system("echo 'R_HOME=/usr/lib/R' >>/etc/default/tomcat7")
    os.system('service tomcat7 stop')
    os.system('killall -9 java')
    # Checking For firewall
    ufwstatus = "sudo ufw status |grep Status |awk '{print $2}'"
    if str(cmdline(ufwstatus)) == "active\n":
        print 'Firewall: ' + str(cmdline(ufwstatus)) + 'Allowing Java & Tomcat port....'
        os.system("sudo ufw allow 8080")
        os.system("sudo ufw allow 85")
        os.system("sudo ufw allow 1234")
    else:
        print 'Firewall:' + str(cmdline(ufwstatus))
    os.system('service tomcat7 start')
    os.system('sleep 5')
    return


# Function to install Zabbix Agent
def zabbix():
    # Check OS Version First
    os_name = platform.dist()[0]
    os_vers = platform.dist()[1]
    print os_name + ' ' + os_vers
    if os_name == 'Ubuntu':
        if os_vers == '12.04':
            alamat = site_ub12
        elif os_vers == '14.04':
            alamat = site_ub14
        else:
            print "Ubuntu Version:" + os_vers
    else:
        print "This machine version is:" + os_name + ' ' + os_vers
    # print alamat

    # Start to Install Zabbix Agent
    print "Installing Zabbix Agent !\n"
    print("Downloading Zabbix Packages from online repository")
    subprocess.call([alamat], shell=True)
    subprocess.call(["dpkg -i /tmp/zabbix*.deb"], shell=True)
    print("Checking update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print("Starting to install Zabbix Agent.....")
    os.system('apt-get install -y zabbix-agent >/dev/null 2>&1')

    # Setup zabbix agent config:
    # Backup first
    subprocess.call(["cp /etc/zabbix/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf.ORIG"], shell=True)

    # Edit Config for Server IP
    # ip = raw_input("Enter Zabbix Server IP Address: ")
    #ip = '10.153.64.4'
    pasf_serv = 'sed -re' + ' "s/(Server=)[^=]*$/\\1' + str(ZABBIX_SERVER) + '/"' + ' /etc/zabbix/zabbix_agentd.conf -i'
    actv_serv = 'sed -re' + ' "s/(ServerActive=)[^=]*$/\\1' + str(ZABBIX_SERVER) + '/"' + ' /etc/zabbix/zabbix_agentd.conf -i'
    subprocess.call(pasf_serv, shell=True)
    subprocess.call(actv_serv, shell=True)

    # Edit config for zabbix agent hostname
    hostnm = 'sed -i' + ' "s/^Hostname=Zabbix server/#Hostname=/g"' + ' /etc/zabbix/zabbix_agentd.conf'
    hostitm = 'sed -i' + ' "s/^# HostnameItem=system.hostname/HostnameItem=system.hostname/g"' + \
              ' /etc/zabbix/zabbix_agentd.conf'
    remtcommand = 'sed -i' + ' "s/^# EnableRemoteCommands=0/EnableRemoteCommands=1/g"' + \
                  ' /etc/zabbix/zabbix_agentd.conf'
    subprocess.call(hostnm, shell=True)
    subprocess.call(hostitm, shell=True)
    subprocess.call(remtcommand, shell=True)

    # Edit for host metadata
    meta_value = "Linux    21df83bf21bf0be663090bb8d4128558ab9b95fba66a6dbf834f8b91ae5e08ae"
    meta_edit = 'sed -i' + ' "s/^# HostMetadata=/HostMetadata=/g"' + ' /etc/zabbix/zabbix_agentd.conf'
    subprocess.call(meta_edit, shell=True)
    metadata = 'sed -re' + ' "s/(HostMetadata=)[^=]*$/\\1' + str(meta_value) + '/"' + \
               ' /etc/zabbix/zabbix_agentd.conf -i'
    subprocess.call(metadata, shell=True)

    # Config done & now restart zabbix agent
    os.system('service zabbix-agent restart')
    os.system('rm /tmp/*.deb')
    os.system('sleep 5')
    return


# Functions to update libmaodbc using the latest version support for ssl
def updateLibMaODBC():
    copy('/mnt/public/IT/unixAdmin/libmaodbc.so', '/usr/local/lib/libmaodbc.so')
    copy('/etc/odbcinst.ini', '/etc/odbcinst.ini.backup')
    copy('/mnt/public/IT/DSN/unix/odbcinst.ini', '/etc/')
    os.system('ln -sv /usr/lib/x86_64-linux-gnu/libodbcinst.so.1.0.0 /usr/lib/x86_64-linux-gnu/libodbcinst.so.2')
    return


# Function to install R base
def rSetup():
    print "Installing R in Progress....."
    os.system('sudo apt-add-repository "deb http://cran.rstudio.com/bin/linux/ubuntu $(lsb_release -cs)/"')
    os.system('gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9')
    os.system('gpg -a --export E084DAB9 | sudo apt-key add -')
    print("Checking for update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print "Installing....."
    os.system('apt-get install -y --force-yes r-base-core=3.2.2-1trusty0 r-base-dev=3.2.2-1trusty0 && echo "Installing R Finish"')
    copy('/mnt/public/IT/DSN/unix/odbc.ini', '/etc/')
    copy('/mnt/public/IT/DSN/unix/odbcinst.ini', '/etc/')
    os.system('cp /mnt/public/IT/Libs/R/Rprofile.site /usr/lib/R/etc/Rprofile.site')
    # Configure R depend on Public networks or 4E networks
    if WHICH_NETWORK == 'Public':
        # For sourcing list of Rprofile
        SOURCING1 = '.source4Efunction.r'
        SOURCING2 = '.sourceAlfunction.r'
        os.system("sed -i 's/" + str(SOURCING1) + "/" + str(SOURCING2) + "/g' /etc/R/Rprofile.site")
    else:
        # Call functions update lib my odbc
        updateLibMaODBC()
        print(" ")
    print("R has been Setup!")
    os.system('sleep 5')
    return


# Function to install R Studio IDE
def rstudio_ide():
    print "Installing Rstudio IDE in Progress....."
    print("Checking for update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print "Installing....."
    os.system('apt-get install -y --force-yes r-base-core=3.2.2-1trusty0 r-base-dev=3.2.2-1trusty0 gdebi-core')
    os.system('wget https://download1.rstudio.org/rstudio-1.1.383-amd64.deb -P /tmp/')
    os.system('gdebi -n /tmp/rstudio-1.1.383-amd64.deb && echo "Installation Finish!"')
    os.system('sleep 5')
    return


# Function to install R Studio Server
def rstudio_server():
    print "Installing Rstudio Server in Progress....."
    print("Checking for update.....")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print "Installing....."
    os.system('apt-get install -y --force-yes r-base-core=3.2.2-1trusty0 r-base-dev=3.2.2-1trusty0 gdebi-core')
    os.system('wget https://download2.rstudio.org/rstudio-server-1.1.383-amd64.deb -P /tmp/')
    os.system('gdebi -n /tmp/rstudio-server-1.1.383-amd64.deb && echo "Installation  Finish!"')
    os.system('sleep 5')
    return


# Function to install Emacs & ESS
def emac_ess():
    print("Installing ESS......")
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    os.system('apt-get install -y ess emacs emacs24')
    os.system('sleep 5')
    return


# Function to install Gluster Client
def gluster_client():
    print("Installing Gluster Client......")
    os.system('add-apt-repository -y ppa:gluster/glusterfs-3.8')
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    os.system('apt-get install -y glusterfs-client')
    return


# Function to Mount all Drive available for Public or Private Networks
def mounting():
    print "Mouting Drive, please wait....."

    # Function to mount and add it to fstab
    def addfstab():
        # Fstab Variable
        pub = '//10.153.64.10/Public   /mnt/public/            cifs    rw,guest,iocharset=utf8,file_mode=0777,dir_mode=0777,nounix,sec=ntlm  0 0'
        weath = '//10.153.64.44/fileserv /mnt/weather/           cifs    rw,guest,iocharset=utf8,file_mode=0777,dir_mode=0777,nounix,sec=ntlm  0 0'
        #backtest = '//10.153.64.47/Backtest /mnt/backtest/          cifs    rw,guest,iocharset=utf8,file_mode=0777,dir_mode=0777,nounix,sec=ntlm  0 0'
        simu = '//10.153.64.7/Simulations /mnt/Simulations/     cifs    rw,guest,iocharset=utf8,file_mode=0777,dir_mode=0777,nounix,sec=ntlm  0 0'
        ecshare = '4ecapsvsg15.fourelements.sg:/shared          /4ECAP          nfs'
        backup = '//10.153.64.20/Volume_1   /mnt/backup_drive/            cifs    rw,guest,uid=0,gid=0,file_mode=0777,dir_mode=0777,nounix,sec=ntlm  0 0'
        gluster = '4ecappcsg53:/glusterAL	/mnt/gluster/	glusterfs	acl,defaults,transport=tcp,_netdev,log-level=WARNING 0 0'
        home_gluster = '/mnt/gluster/Home      /home    none    bind  0  0'

        # Modify fstab based on networks
        if WHICH_NETWORK == 'Private':
            # Creating all directory to use for mounting drive
            os.system('mkdir -p /mnt/weather')
            os.system('mkdir -p /mnt/backtest')
            os.system('mkdir -p /mnt/Simulations')
            os.system('mkdir -p /mnt/backup_drive')
            os.system('mkdir -p /mnt/public')
            subprocess.call(['echo "' + str(pub) + '">>/etc/fstab'], shell=True)
            subprocess.call(['echo "' + str(weath) + '">>/etc/fstab'], shell=True)
            #subprocess.call(['echo "' + str(backtest) + '">>/etc/fstab'], shell=True)
            subprocess.call(['echo "' + str(simu) + '">>/etc/fstab'], shell=True)
            subprocess.call(['echo "' + str(ecshare) + '">>/etc/fstab'], shell=True)
            subprocess.call(['echo "' + str(backup) + '">>/etc/fstab'], shell=True)
            os.system('mount -a > /dev/null 2>&1')
        else:
            proc = subprocess.Popen(["dpkg -l |grep 'glusterfs-client' |awk '{print $1}'"], stdout=subprocess.PIPE, shell=True)
            (installed, err) = proc.communicate()
            installed = installed.strip()
            if installed != 'ii':
                gluster_client()
            else:
                print("Gluster Client already installed!!")
            print("Setting up Gluster, please wait......")
            os.system('mkdir -p /mnt/gluster')

            # This is checker on fstab. So there will be no multiple line on fstab
            fstb_gluster = subprocess.Popen(["grep 'glusterAL' -o /etc/fstab |awk 'NR==1'"],
                                            stdout=subprocess.PIPE, shell=True)
            (_gluster_there, err) = fstb_gluster.communicate()
            _gluster_there = _gluster_there.strip()
            if _gluster_there != 'glusterAL':
                subprocess.call(['echo "' + str(gluster) + '">>/etc/fstab'], shell=True)

            # Check if GlusterFS already mounted or not
            proc = subprocess.Popen(["df -h |grep /mnt/gluster |awk '{print $6}'"], stdout=subprocess.PIPE, shell=True)
            (mounted, err) = proc.communicate()
            # Strip New line on the version
            mounted = mounted.strip()
            if mounted != '/mnt/gluster':
                print("Mounting gluster now....")
                os.system('mount /mnt/gluster > /dev/null 2>&1')
            else:
                print("Gluster Mounted!")
            # Symlink checker exist or not
            # If not exist, create symlink.
            DRIVE_LINK = os.path.islink('/Drive')
            PUBLIC_LINK = os.path.islink('/mnt/public')
            if str(DRIVE_LINK) == 'False':
                print("/Drive not exists, creating symlink....")
                os.system('ln -sv /mnt/gluster/Alphien/ /Drive')
            if str(PUBLIC_LINK) == 'False':
                print("Public Drive not exists, creating symlink....")
                proc = subprocess.Popen(["df -h |grep /mnt/public |awk '{print $6}'"], stdout=subprocess.PIPE,
                                        shell=True)
                (mounted, err) = proc.communicate()
                mounted = mounted.strip()
                if mounted != '/mnt/public':
                    os.system('rm -rf /mnt/public')
                    os.system('ln -sv /mnt/gluster/Public/ /mnt/public')
            # This is checker on fstab. So there will be no multiple line on fstab
            checkhome = subprocess.Popen(["grep -e '^/mnt/gluster/Home' -o /etc/fstab |awk 'NR==1'"],
                                         stdout=subprocess.PIPE, shell=True)
            (_home_there, err) = checkhome.communicate()
            _home_there = _home_there.strip()
            if _home_there != '/mnt/gluster/Home':
                subprocess.call(['echo "' + str(home_gluster) + '">>/etc/fstab'], shell=True)
            os.system('mount /home > /dev/null 2>&1')
        return

    # Check and Editing FQDN
    cond_fstab = os.path.exists('/etc/fstab.ori')
    if str(cond_fstab) == 'True':
        # print ("file fstab.ori exists")
        os.system('cp /etc/fstab.ori /etc/fstab')
        addfstab()
    else:
        # print ("file fstab still original one not modified")
        os.system('cp /etc/fstab /etc/fstab.ori')
        addfstab()
    os.system('sleep 5')
    return


# Set profile for Java, R and Tomcat
def set_profile():
    copy(SCRIPT_PATH + '/java.sh', '/etc/profile.d/java.sh')
    os.system('chmod +x /etc/profile.d/java.sh')
    os.system('/etc/profile.d/java.sh')
    return


# Join Domain Function
def join_domain():
    print ("Joining host into domain.....")
    # Update repository cache
    print("Updating repo...")
    os.system('apt-get update > /dev/null 2>&1')
    # Install packages and libraries needed
    os.system('apt-get install -y sssd libsss-sudo krb5-user nfs-common autofs cifs-utils')
    # Configure SSSD service
    if os.path.exists('/etc/sssd/sssd.conf'):
        os.system('mv /etc/sssd/sssd.conf /etc/sssd/sssd.conf.ori')
    copy(SCRIPT_PATH + '/sssd.conf', '/etc/sssd/sssd.conf')
    os.system('chmod 600 /etc/sssd/sssd.conf')
    os.system('initctl start sssd && service sssd restart')
    # Configure Kerberos
    os.system('mv /etc/krb5.conf /etc/krb5.conf.ori')
    copy(SCRIPT_PATH + '/krb5.conf', '/etc/krb5.conf')
    # Block code to create principal on kerberos
    os.system('clear && echo "Creating kerberos principal...."')
    from subprocess import Popen, PIPE
    # Initialize stderr value
    stderr = "1"
    # Main looping and connection checker to kerberos server if:
    # 1. Password correct or not
    # 2. Able to resolve kerberos server or others problems
    while stderr != '':
        admin_pass = raw_input("Input Kerberos Admin Password= ")
        cmd = "kadmin -p administrator/admin -w " + admin_pass + " -q 'q'"
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        (stdout, stderr) = proc.communicate()
        stderr = stderr.strip()
        if stderr == '':
            break
        else:
            err_pass_str = 'Incorrect password'
            if err_pass_str in stderr:
                print("( ERROR ): Incorrect password for Kerberos Admin!")
            else:
                print("( ERROR ):\n %s" % stderr)
                print("Please check networks connection and able to resolve kerberos name!")
                exit(1)
    # NFS and Home domain
    os.system('kadmin -p administrator/admin -w ' + admin_pass + ' -q "addprinc -randkey nfs/$(hostname -f)"')
    os.system('kadmin -p administrator/admin -w ' + admin_pass + ' -q "ktadd nfs/$(hostname -f)"')
    # Kerberize SSH
    os.system('kadmin -p administrator/admin -w ' + admin_pass + ' -q "addprinc -randkey host/$(hostname -f)"')
    os.system('kadmin -p administrator/admin -w ' + admin_pass + ' -q "ktadd host/$(hostname -f)"')
    gssauth = 'sed -i' + ' "s/^#GSSAPIAuthentication no/GSSAPIAuthentication yes/g" /etc/ssh/sshd_config'
    gsscln = 'sed -i' + ' "s/^#GSSAPICleanupCredentials yes/GSSAPICleanupCredentials yes/g" /etc/ssh/sshd_config'
    subprocess.call(gssauth, shell=True)
    subprocess.call(gsscln, shell=True)
    comstr = 'yes'
    nfscom = 'sed -re' + ' "s/(NEED_GSSD=)[^=]*$/\\1' + str(comstr) + '/"' + ' /etc/default/nfs-common -i'
    subprocess.call(nfscom, shell=True)

    # Setting autofs for private Networks
    if WHICH_NETWORK == 'Private':
        automaster = 'sed -i' + ' "s/^+auto.master/#+auto.master/g" /etc/auto.master'
        subprocess.call(automaster, shell=True)
        os.system('touch /etc/auto.home && chmod 644 /etc/auto.home')
        os.system('echo "/home   /etc/auto.home" >> /etc/auto.master')
        os.system('echo "*   -fstype=nfs4,rw,hard,intr,sec=krb5   4ecapsvsg15.fourelements.sg:/home/&" > /etc/auto.home')
        os.system('echo "*   -fstype=nfs4,rw,hard,intr,sec=krb5   4ecapsvsg15.fourelements.sg:/shared/&" >> /etc/auto.home')
        os.system('mkdir -p /4ECAP')
        os.system('service autofs restart')
    os.system('cp /etc/nsswitch.conf /etc/nsswitch.conf.ORIG')
    copy(SCRIPT_PATH + '/nsswitch.conf', '/etc/nsswitch.conf')
    os.system('chmod 644 /etc/nsswitch.conf')
    polkit = 'sed -i' + ' "s/^AdminIdentities=/#AdminIdentities=/g" /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf'
    subprocess.call(polkit, shell=True)
    os.system('echo "AdminIdentities=unix-group:sudo;unix-group:admin;unix-group:10000" >> /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf')
    copy(SCRIPT_PATH + '/lightdm.conf', '/etc/lightdm/lightdm.conf')
    os.system('chmod 664 /etc/lightdm/lightdm.conf')
    print ("Please Reboot your computer to take the effect...")
    os.system('sleep 5')
    return


# Function Edit FQDN hosts & hostname also for dns host list
def fqdn_func():
    hstname = raw_input("Input Hostname= ")
    ipaddrs = raw_input("Input IP Address= ")

    with open('/etc/hosts', "r+") as f:
        first_line = f.readline()
        if first_line != str(ipaddrs + ' ' + hstname + '.fourelements.sg ' + hstname + "\n"):
            lines = f.readlines()
            f.seek(0)
            f.write(str(ipaddrs + ' ' + hstname + '.fourelements.sg ' + hstname + "\n"))
            f.write(first_line)
            f.writelines(lines)

    text_hostnm = open("/etc/hostname", "w")
    text_hostnm.write(str(hstname) + "\n")
    text_hostnm.close()
    # Comment 127.0.1.1
    tchost = 'sed -i' + ' "s/^127.0.1.1/#127.0.1.1/g" /etc/hosts'
    subprocess.call(tchost, shell=True)
    # Update DNS host list
    full_name = str(ipaddrs + ' ' + hstname + '.fourelements.sg ' + hstname)
    print full_name
    print("Adding host into DNS.....")
    update_list = 'ssh root@10.153.64.15 "echo %s >> /etc/hosts.dnsmasq"' % full_name
    subprocess.call(update_list, shell=True)
    return


# Function for New Installation
def new_install():
    library()
    os.system('mkdir -p /4ECAP/')
    os.system('mkdir -p /4EUtils/')
    # ipaddrs = socket.gethostbyname(socket.gethostname())

    # Check and Editing FQDN
    cond_host = os.path.exists('/etc/hosts.ori')
    if str(cond_host) == 'True':
        # Backup of original file exist then use back the original file
        os.system('cp /etc/hosts.ori /etc/hosts')
        fqdn_func()
    else:
        # Backup of original file not exist then create a backup
        os.system('cp /etc/hosts /etc/hosts.ori')
        fqdn_func()
    # Network interface configuration based on which network
    if WHICH_NETWORK == 'Public':
        print("Comment DNSMasq.....")
        os.system("sed -r 's/^dns=/#dns=/g' -i /etc/NetworkManager/NetworkManager.conf")
    mounting()
    java()
    tomcat()
    rSetup()
    # Set java & R profile
    set_profile()
    os.system('cp -rv /mnt/public/IT/puttyKey/.ssh/ /root/')
    os.system('chmod -R 600 /root/.ssh/')
    os.system('chown root:root /root/.ssh/')
    zabbix()
    gitSetup()
    ntp_setup()
    maven_install()
    pip_install()
    os.system('clear')
    join_domain()
    return


# Function To install Google Chrome browser
def gchrome():
    print ("**Google Chrome Installation**")
    # Adding key
    os.system('wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -')
    # Adding repository
    chrome_repo = 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main'
    subprocess.call(['echo "' + str(chrome_repo) + '" | sudo tee /etc/apt/sources.list.d/google-chrome.list'], shell=True)
    print ("Checking for update.....")
    os.system('apt-get update >/dev/null 2>&1')
    print ("Installing Chrome.....")
    os.system('apt-get install -y google-chrome-stable')
    print ("Google Chrome Installed")
    os.system('sleep 5')
    return


# Function To install and update firefox
def firefox_updt():
    print ("**Mozilla Firefox Installation**")
    print ("Checking for update.....")
    os.system('apt-get update >/dev/null 2>&1')
    print ("Installing Firefox.....")
    os.system('apt-get install -y firefox')
    print ("Firefox Installed")
    os.system('sleep 5')
    return


# Function to Join Domain Only
def joind():
    os.system('mkdir -p /4ECAP/')
    os.system('mkdir -p /4EUtils/')
    cond_host = os.path.exists('/etc/hosts.ori')
    if str(cond_host) == 'True':
        # print ("file asli ada")
        os.system('cp /etc/hosts.ori /etc/hosts')
        fqdn_func()
    else:
        # print ("file masih ori")
        os.system('cp /etc/hosts /etc/hosts.ori')
        fqdn_func()
    # Check if GlusterFS already mounted or not
    proc = subprocess.Popen(["df -h |grep /mnt/public |awk '{print $6}'"], stdout=subprocess.PIPE, shell=True)
    (mounted, err) = proc.communicate()
    # Strip New line on the version
    mounted = mounted.strip()
    if mounted != '/mnt/public':
        print("Mounting public drive now....")
        # Symlink checker exist or not
        # If not exist, create symlink.
        public_link = os.path.islink('/mnt/public')
        if str(public_link) == 'True':
            os.system('unlink /mnt/public')
        os.system('mount /mnt/public > /dev/null 2>&1')
    else:
        print("Public drive mounted!")
    updateLibMaODBC()
    join_domain()
    return


# Function to install MariaDB Server
def mariadbs():
    input_version = raw_input("Input MariaDb version { 5.5 | 10.2 } = ")
    if input_version == '5.5':
        print "Installing MariaDB Server %s......" %input_version
        os.system("apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db")
        os.system("add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://download.nus.edu.sg/mirror/mariadb/repo/5.5/ubuntu trusty main'")
        os.system('apt-get update >/dev/null 2>&1')
        os.system('apt-get install mariadb-server-5.5')
    elif input_version == '10.2':
        print "Installing MariaDB Server %s......" % input_version
        os.system("apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db")
        os.system("add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://download.nus.edu.sg/mirror/mariadb/repo/10.2/ubuntu trusty main'")
        os.system('apt-get update >/dev/null 2>&1')
        os.system('apt-get install mariadb-server-10.2')
    else:
        print "Please input the correct version { 5.5 | 10.2 }"
        return mariadbs()
    proc = subprocess.Popen(["mysql --version |awk '{print $5}' |cut -d '-' -f 1"], stdout=subprocess.PIPE, shell=True)
    (vers, err) = proc.communicate()
    vers = vers.strip()
    print "MariaDB Server V%s Installed" %vers
    os.system('sleep 5')
    phpmyadmins()
    return


# Function for installing PHPMyAdmin
def phpmyadmins():
    os.system('apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    print ("Installing PHPMyAdmin")
    os.system('apt-get install -y apache2 php5 phpmyadmin libapache2-mod-php5 php5-mcrypt apache2-utils')
    os.system('ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf')
    os.system('a2enconf phpmyadmin')
    #os.system('echo "# Added for PHPMyAdmin\nInclude /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf')
    os.system('service apache2 restart')
    print "PHPMyAdmin Installed!"
    os.system('sleep 5')
    return


# Postfix Installation
def postfixx():
    print "Installing Postfix....."
    os.system('sudo apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    os.system('sudo apt-get install -y postfix postfix-mysql && echo "Installation Finish!"')
    return


# Git Installation
def gitSetup():
    print "Installing git....."
    os.system('sudo apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    os.system('sudo apt-get install -y git && echo "Installation Finish!"')
    os.system("sleep 5")
    return


# Setup Machine as a peer
def peersetup():
    print ("Setuping machine as a peer....")
    # Installing git
    gitSetup()

    # Setting up R and Rserve
    rSetup()
    # Setting up Rserve
    #os.system("R -e \"if (require('Rserve')) install.packages('Rserve', repos = 'http://cran.rstudio.com/')\"")
    os.system("R -e \"install.packages('Rserve', repos = 'http://cran.rstudio.com/')\"")
    copy(SCRIPT_PATH + '/autostart_peer.sh', '/4EUtils/')
    os.system('chmod +x /4EUtils/autostart_peer.sh')
    # Setup /etc/rc.local so Rserve will be run even reboot the machine
    rclocal = 'sed -i' + ' "s/^exit 0/#exit 0/g" /etc/rc.local'
    subprocess.call(rclocal, shell=True)
    os.system('echo "/4EUtils/autostart_peer.sh" >>/etc/rc.local')
    os.system('echo "exit 0" >>/etc/rc.local')

    # Installing Java 7
    java()

    # Installing Tomcat7
    tomcat()

    # Set profile
    set_profile()

    # Deploying peer v2.1.0
    subprocess.call([SCRIPT_PATH + '/deployPeer.sh', '2.1.0', '--fresh'])
    os.system('/4EUtils/autostart_peer.sh')
    os.system('sleep 5')
    return


# Function to install Jupyter Notebook
def jupyter_notebook():
    print "Installing Jupyter Notebook....."
    # Install pip and python-dev on the system
    os.system('sudo apt-get update > /dev/null 2>&1 && echo "Finish Checking Update"')
    os.system('sudo apt-get install -y python-pip python-dev')
    # Check if pip run by python2.7 or not by default
    proc = subprocess.Popen(["python -m pip -V |grep -o 'python2.7'"], stdout=subprocess.PIPE, shell=True)
    (python_pip, err) = proc.communicate()
    python_pip = python_pip.strip()
    if python_pip == "python2.7":
        # Upgrade pip version to the latest version 9
        os.system("python -m pip install -U pip")
        # Install Jupyter notebook and upgrade with the latest version
        os.system("python -m pip install jupyter")
        os.system("python -m pip install -U jupyter")
    else:
        # Upgrade pip version to the latest version 9
        os.system("python2.7 -m pip install -U pip")
        # Install Jupyter notebook and upgrade with the latest version
        os.system("python2.7 -m pip install jupyter")
        os.system("python2.7 -m pip install -U jupyter")
    # Check jupyter notebook version
    proc = subprocess.Popen(["jupyter-notebook --version"], stdout=subprocess.PIPE, shell=True)
    (jupy_version, err) = proc.communicate()
    # Strip New line on the version
    jupy_version = jupy_version.strip()
    # Condition to check if Jupyter notebook installation Success or not
    if jupy_version != "":
        print('Installation Jupyter Notebook V%s Done!') % jupy_version
    else:
        print("Installation Jupyter Notebook Failed!")
    os.system("sleep 5")
    return


# Function to install Maven 3.5.2 (Refer to wiki page)
def maven_install():
    print("Installing Maven....")
    url = 'http://www-eu.apache.org/dist/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz'
    os.system('wget ' + url + ' -P /tmp/')
    os.system('tar -xzvf /tmp/apache-maven-3.5.2-bin.tar.gz -C /usr/local/')
    os.system('rm -rf /tmp/apache-maven-3.5.2-bin.tar.gz')
    # Symlink maven
    MVN_LINK = os.path.islink('/usr/local/apache-maven')
    if str(MVN_LINK) == 'False':
        print("Creating Maven symlink.....")
        os.system('ln -sv /usr/local/apache-maven-3.5.2/ /usr/local/apache-maven')
    else:
        print("Re-creating Maven symlink.....")
        os.system('unlink /usr/local/apache-maven')
        os.system('ln -sv /usr/local/apache-maven-3.5.2/ /usr/local/apache-maven')
    # Set environments path for Maven
    maven_path = 'export PATH=/usr/local/apache-maven/bin${PATH:+:${PATH}}'
    m2_home = 'export M2_HOME=/usr/local/apache-maven'
    os.system("echo '" + maven_path + "' >>/etc/profile.d/java.sh")
    os.system("echo '" + m2_home + "' >>/etc/profile.d/java.sh")
    print("Maven 3.5.2 installed! Please reboot the machine")
    os.system('sleep 5')
    return


# Function to install NVIDIA Driver
def nvidia_install():
    print("Installing NVIDIA Driver......")
    os.system('sudo add-apt-repository ppa:graphics-drivers/ppa -y')
    os.system('sudo apt-get update > /dev/null 2>&1')
    os.system('apt-get install nvidia-384')
    os.system('sleep 5')
    return


# Function to install CUDA 8 for Pascal VGA
def cuda_install():
    print("Installing CUDA 8.......")
    cuda_repo_url = 'http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_8.0.61-1_amd64.deb'
    os.system("wget " + cuda_repo_url + " -P /tmp/")
    os.system('dpkg -i /tmp/cuda-repo-ubuntu1404_8.0.61-1_amd64.deb')
    os.remove('/tmp/cuda-repo-ubuntu1404_8.0.61-1_amd64.deb')
    print("Checking update.....")
    os.system('apt-get update > /dev/null 2>&1')
    os.system('apt-get install -y cuda=8.0.61-1')
    # Setup cuda environment path
    cuda_visible_device = 'export CUDA_VISIBLE_DEVICES=0'
    cuda_path = 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}'
    cuda_ld_path = 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}'
    cuda_home = 'export CUDA_HOME=/usr/local/cuda'
    os.system("echo '" + cuda_visible_device + "' >/etc/profile.d/cuda.sh")
    os.system("echo '" + cuda_path + "' >>/etc/profile.d/cuda.sh")
    os.system("echo '" + cuda_ld_path + "' >>/etc/profile.d/cuda.sh")
    os.system("echo '" + cuda_home + "' >>/etc/profile.d/cuda.sh")
    os.system('chmod +x /etc/profile.d/cuda.sh')
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    LINUX_PATH = os.environ["PATH"]
    LINUX_PATH = "/usr/local/cuda-8.0/bin:" + LINUX_PATH
    CONDT = "LD_LIBRARY_PATH" in os.environ
    if str(CONDT) == 'False':
        LD_PATH = "/usr/local/cuda-8.0/lib64"
    else:
        LD_PATH = os.environ["LD_LIBRARY_PATH"]
        LD_PATH = "/usr/local/cuda-8.0/lib64:" + LD_PATH
    os.environ["PATH"] = LINUX_PATH
    os.environ["LD_LIBRARY_PATH"] = LD_PATH
    # Install cuDNN
    print("Installing cuDNN v6 for CUDA 8......")
    os.system('tar -xzvf /mnt/public/Infrastructure/Linux_Unix/cudnn-8.0-linux-x64-v6.0.tgz -C /4EUtils/')
    os.system('sudo cp -v /4EUtils/cuda/include/cudnn.h /usr/local/cuda/include')
    os.system('sudo cp -v /4EUtils/cuda/lib64/libcudnn* /usr/local/cuda/lib64')
    os.system('sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*')
    os.system('sleep 5')
    return


# Function to install Python Pip and mandatory python packages
def pip_install():
    print("Installing latest python pip........")
    os.system('apt-get update > /dev/null 2>&1')
    os.system('sudo apt-get install -y python-pip python-dev python3-pip python3-dev')
    os.system("python2.7 -m pip install -U pip")
    os.system("python2.7 -m pip install pandas")
    os.system("python2.7 -m pip install numpy")
    os.system("python2.7 -m pip install sklearn")
    os.system("python2.7 -m pip install scipy")
    os.system("python2.7 -m pip install matplotlib")
    os.system("python2.7 -m pip install 'rpy2==2.8.5'")
    os.system("python3 -m pip install -U pip")
    return


# Function to install Tensorflow GPU
def tensor_install():
    print("Installing Tensorflow with GPU........")
    pip_install()
    os.system('apt-get install -y libcupti-dev python-virtualenv')
    os.system('python -m pip install tensorflow-gpu')
    os.system('python -m pip install -U tensorflow-gpu')
    return


# Function to setup GPU Peer
def gpu_peer():
    print("Setup GPU Peer........")
    # Install nvidia driver
    nvidia_install()
    # Install CUDA & cuDNN
    cuda_install()
    # Install tensorflow GPU
    tensor_install()
    # Deploy Peer
    peersetup()
    print("Please restart computer to take effect!")
    os.system('sleep 5')
    return


# Function to install eclipse mars IDE
def eclipse_setup():
    print("Installing Eclipse Mars IDE.......")
    os.system('sleep 5')
    eclipse_src = '/mnt/public/Infrastructure/Linux_Unix/eclipse-java-mars-2-linux-gtk-x86_64.tar.gz'
    os.system("tar -xzvf " + eclipse_src + " -C /opt/")
    copy(SCRIPT_PATH + '/eclipse.desktop', '/usr/share/applications/')
    print("Eclipse Mars installed!")
    os.system('sleep 5')
    return


# Function to setup ntp
def ntp_setup():
    print("Installing ntp....")
    os.system('apt-get install -y ntp')
    copy(SCRIPT_PATH + '/ntp.conf', '/etc/')
    os.system('service ntp restart')
    # Setup /etc/rc.local so NTP will be run even reboot the machine
    rclocal = 'sed -i' + ' "s/^exit 0/#exit 0/g" /etc/rc.local'
    subprocess.call(rclocal, shell=True)
    os.system('echo "ntpdate -u 10.153.64.15" >>/etc/rc.local')
    os.system('echo "exit 0" >>/etc/rc.local')
    print("NTP installed!")
    os.system('sleep 5')
    return


# Main menu
def main_menu():
    os.system('clear')
    print "===================WELCOME===================\n"

    file_readme = open(SCRIPT_PATH + '/README', 'r')
    print file_readme.read()+"\n"
    file_readme.close()

    print "Please choose the menu number:"
    print "1. New Installation"
    print "2. Mandatory Installation"
    print "3. Join Domain"
    print "4. Optional"
    print "\nq. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Mandatory Menu
def mandatory():
    os.system('clear')
    print "===================WELCOME===================\n"
    print "Please choose the menu number:"
    print "1. Unix Library"
    print "2. JAVA"
    print "3. Tomcat"
    print "4. Zabbix Agent"
    print "5. R"
    print "6. Maven"
    print "7. Mount Drive"
    print "8. Python pip"
    print "9. NTP"
    print "\n0. Back to main Menu"
    print "q. Quit"
    choice1 = raw_input(" >>  ")
    exec_mandatory(choice1)
    return mandatory()


# Optional Installation Function
def opt_install():
    os.system('clear')
    print ("Choose optional packages to Install:")
    print ("1. Rstudio IDE")
    print ("2. Rstudio Server")
    print ("3. Google Chrome")
    print ("4. MariaDB Server")
    print ("5. PHPMyAdmin")
    print ("6. Postfix")
    print ("7. Github")
    print ("8. Peer Setup")
    print ("9. GPU Peer")
    print ("10. Firefox")
    print ("11. Jupyter Notebook")
    print ("12. Cuda 8")
    print ("13. NVIDIA Driver")
    print ("14. Tensorflow-GPU")
    print ("15. Eclipse Mars")
    print ("16. Emacs ESS")
    print ("\n0. Back to Main Menu")
    print ("q. Quit Program")
    choice2 = raw_input(" >>  ")
    exec_opt(choice2)
    return opt_install()


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# ======================= #
#    MENUS DEFINITIONS    #
# ======================= #


# Main Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': new_install,
    '2': mandatory,
    '3': joind,
    '4': opt_install,
    'q': exit,
}


# Main Menu definition
menu_mandatory = {
    'menu_mandatory': mandatory,
    '1': library,
    '2': java,
    '3': tomcat,
    '4': zabbix,
    '5': rSetup,
    '6': maven_install,
    '7': mounting,
    '8': pip_install,
    '9': ntp_setup,
    '0': back,
    'q': exit,
}


# Menu Optional Install definition
menu_opt = {
    'menu_opt': opt_install,
    '1': rstudio_ide,
    '2': rstudio_server,
    '3': gchrome,
    '4': mariadbs,
    '5': phpmyadmins,
    '6': postfixx,
    '7': gitSetup,
    '8': peersetup,
    '9': gpu_peer,
    '10': firefox_updt,
    '11': jupyter_notebook,
    '12': cuda_install,
    '13': nvidia_install,
    '14': tensor_install,
    '15': eclipse_setup,
    '16': emac_ess,
    '0': back,
    'q': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
