#coding:utf-8
#
# Copyright (c) 2013-2023, vanstor.com
# All rights reserved.
#
import shutil
import os,sys,re
import hashlib
import multiprocessing
import time,threading
import subprocess
import logging
import copyfile_base
import filecmp

platform = copyfile_base.getplatform()
src_dir=copyfile_base.config_filecopy.src_dir[0]
src_len=len(copyfile_base.config_filecopy.des_dir)
file_name=copyfile_base.config_filecopy.file_name[0]

def init_srcfile():  #获取源文件MD5值
    calcdir = src_dir+"\\"+file_name
    md5_dir = src_dir + "\\md5"
    if os.path.isdir(md5_dir)==False:
        os.makedirs(md5_dir)
    md5file = md5_dir+"\\md5.txt"
    copyfile_base.calmd5_hash(calcdir,md5file,file_name)

def copyfile(srcdir,desdir,i):
    # str4 = desdir+os.path.basename(srcdir)+str(i)           #directory folder
    str4 = desdir+file_name+str(i)
    try:
        if os.path.exists(str4):        #check whether the file str4
            shutil.rmtree(str4)
            logging.info("Delete the existing dir:"+str4) #delete des folder
        logging.info("File "+str4+" copying start !")
        shutil.copytree(srcdir+"\\"+file_name,str4+"\\"+file_name)             #copy the source file to the destination file
        shutil.copytree(srcdir+"\\md5",str4+"\\md5")
        logging.info("File "+str4+" copying complete !")
    except Exception,ex:
        logging.error(ex)
        #copyfile_base.sendmail(ex)
        return 1

def checkmd5(srcdir,desdir,i):
    try:
        str4 = desdir+file_name+str(i)
        calcdir = str4+"\\"+file_name
        md5file = str4+"\\md5\\desmd5.txt"
        copyfile_base.calmd5_hash(calcdir,md5file,file_name)
        logging.info("Check file:"+str4+" md5 start!")
        if filecmp.cmp(str4+"\\md5\\desmd5.txt",str4+"\\md5\\md5.txt"):
            logging.info("Check md5 success!")
            return 0
        else:
            logging.info("Check md5 failed!")
            return 1
    except Exception,ex:
        logging.info(ex)

def smallcopyfile1(srcdir,desdir,m):
    i = 0
    desdir = desdir+"thread"+str(m)+"\\"
    express = True
    while express:
        str1=desdir+file_name+str(i)
        logging.info("Desdir:"+str1)
        m = copyfile_base.checkdisk_win(desdir)

        if m == 0 and os.path.exists(str1) == False:
            #磁盘剩余空间小于20G且文件目录不存在，开始从头写文件。
            logging.info("A finished wheel disk!")
            i = 0
        elif m == 1 and os.path.exists(str1) == True:
            #磁盘剩余空间大于20G且文件存在，则跳过此文件
            i += 1
        else:
            try:
                copyfile(srcdir,desdir,i)
                time.sleep(1)        #logging.info("times :"+str(i))
                str5 = checkmd5(srcdir,desdir,i)
                if str5 == 0:
                    logging.info("file copy Agreement!")
                else:
                    logging.error("file copy Agreement failed!")
                    copyfile_base.rename(str1)
                i += 1
            except Exception,ex:
                logging.error(ex)
                #copyfile_base.sendmail(ex)
                logging.info("copy file is over!")
                express = False

def testcase1():
    # init_srcfile()
    for i in range(src_len):
        t = threading.Thread(target=smallcopyfile1,args=(src_dir,copyfile_base.config_filecopy.des_dir[i],i),)
        t.start()
        time.sleep(10)

def testcase2():
    # init_srcfile()
    for i in range(2):
        t = threading.Thread(target=smallcopyfile1,args=(src_dir,copyfile_base.config_filecopy.des_dir[0],i),)
        t.start()
        time.sleep(10)

if __name__ == '__main__':
    init_srcfile()
    testcase1()
    # # testcase2()




