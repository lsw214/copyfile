#coding:utf-8
#-------------------------------------------------------------------------------
# Name:        filecopy
# Purpose:
#
# Author:      liangshiwei
#
# Created:     22/09/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/python
import os,sys,re
import hashlib
import multiprocessing
import time,threading
import subprocess
import logging
import copyfile_base
import copyfile_win,copyfile_linux

platform = copyfile_base.getplatform()
src_dir=copyfile_base.config_filecopy.src_dir[0]
src_len=len(copyfile_base.config_filecopy.des_dir)
file_name=copyfile_base.config_filecopy.file_name[0]

def win_check(srcdir,desdir,m):
    i = 0
    desdir = desdir+"thread"+str(m)+"\\"
    express = True
    while express:
        str1=desdir+file_name+str(i)
        if os.path.exists(str1)!=0:
            i += 1
        else:
            logging.info("Check Desdir:"+str1)
            str5 = copyfile_win.checkmd5(srcdir,desdir,i)
            if str5 == 1:
                copyfile_base.rename(str1)
            i += 1
        if i == 2000:
            logging.info("check complete!")
            express = False

def linux_check(srcdir,filename,desdir):
    i = 0
    express = True
    while express:
        str1=desdir+os.path.basename(srcdir)+str(i)
        if os.path.exists(str1)!=0:
            i += 1
        else:
            logging.info("Desdir:"+str1)
            str5 = copyfile_linux.checkmd5(srcdir,desdir,filename,i)
            if str5.find('FAILED') is -1:            #check whether the wrong copy
                logging.info("file copy Agreement!")
            else:
                logging.error(str1+" copy Agreement failed!\n"+str5)
                # context = str5+'\n'+str1
                # copyfile_base.sendmail(context)
                copyfile_base.rename(str1)
            i += 1
        if i == 2000:
            logging.info("check complete!")
            express = False


def win_testcase1():
    for i in range(src_len):
        t = threading.Thread(target=win_check,args=(src_dir,copyfile_base.config_filecopy.des_dir[i],i),)
        t.start()
        time.sleep(10)

def linux_testcase1():   #每个拷贝目录使用一个线程进行拷贝
    m = len(copyfile_base.config_filecopy.des_dir)
    for i in range(m):
        t1 = threading.Thread(target=linux_check,args=(src_dir,file_name,copyfile_base.config_filecopy.des_dir[i]))
        t1.start()
        time.sleep(1)

if __name__ == '__main__':
    if platform == 'Windows':
        win_testcase1()
    else:
        linux_testcase1()



