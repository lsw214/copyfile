#coding:utf-8
#
# Copyright (c) 2013-2023, vanstor.com
# All rights reserved.
#
import sys,os
import platform
if platform.system()=="Windows":
    import win32file
sys.path.append('config')
import hashlib
import logging
import subprocess
import config_filecopy
import logging.config
import smtplib
from email.mime.text import MIMEText
from email.header import Header

logging.config.fileConfig("config/logging.config")
logger = logging.getLogger("example01")
sender = 'lsw214@163.com'
receiver = 'liangshiwei@vanstor.com'
subject = 'Copy file error!'
smtpserver = 'smtp.163.com'
username = 'lsw214'
password = 'lswzzz520'

def sendmail(context):
    try:
        msg = MIMEText(context,'plain','utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        logging.info("Email send success!")
    except Exception,ex:
        logging.error("Email send failed!")
        logging.error(ex)

def subprocess_nor(arg):
    ex = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    return ex.stdout.read()

def copy_dir_win(srcdir,desdir):
    try:
        win32file.CopyFile(srcdir,desdir,0)
    except Exception,ex:
        print ex

def getplatform():
    ex = platform.system()
    return ex

def rename(desdir):
    try:
        os.rename(desdir,desdir+"failed")
        logging.info("failed file rename success!")
    except Exception,ex:
        logging.error(ex)

def checkdisk_linux(desdir):              #check linux disk whether enough
    str1="df -k|grep "+desdir[:-1]
    ex=subprocess_nor(str1).split()
    size = ex[3]
    logging.info("Available: "+str(int(size)/1024/1024)+"G")
    if int(size)-20*1024*1024>0:
        return 1
    else:
        logging.info(desdir+" not enough to available space!")
        return 0

def srcfile_init_linux(srcdir,filename):
    os.chdir(srcdir)
    str1 = "find ./"+filename+" -type f -print0 | xargs -0 md5sum > ./"+filename+".md5"
    logging.info("Create srcdir MD5 ")
    os.popen(str1)      #create src file md5

def checkdisk_win(desdir):
    ex = "wmic LogicalDisk where \"Caption='"+desdir[0]+":'\" get FreeSpace,Size /value"
    freespace = subprocess_nor(ex).split()[0].split('=')[1]
    if int(freespace) < 21474836480:
        logging.info("Freespace is not enough 20G!")
        return 0
    else:
        return 1

def calmd5_hash(calcdir,md5file,filename_1):#把目录calcdir中的文件md5值计算到MD5file文件中。
    i = len(calcdir)-len(filename_1)   #从目录文件名filename_1开始往后截取目录
    f1 =open(md5file,'w+')
    f1.truncate()
    f1.close()
    try:
        f1 =open(md5file,'a+')
        logging.info("Calc file md5 start")
        for dirpath,dirname,filenames in os.walk(calcdir):
            for filename in filenames:
                filedir = os.path.join(dirpath,filename)
                myhash = hashlib.md5()
                f = open(filedir,'rb')
                while True:
                    big = f.read(8096)
                    if not big:
                        break
                    myhash.update(big)
                f.seek(0)
                md5 = myhash.hexdigest()
                f.close()
                f1.write(md5+' '+os.path.join(dirpath[i-1:],filename)+"\n")  #把计算的md5值与文件的目录写入md5file文件中
        f1.close()
        logging.info("Calc file md5 success")
    except Exception,ex:
        logging.error("Calc file md5 failed!")
        logging.error(ex)

if __name__ == '__main__':
    pass