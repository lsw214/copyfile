#coding:utf-8
#
# Copyright (c) 2013-2023, vanstor.com
# All rights reserved.
#
#!/usr/bin/python
import shutil
import os,sys,re
import hashlib
import multiprocessing
import copyfile_base
import time,threading
import subprocess
import logging
src_dir=copyfile_base.config_filecopy.src_dir[0]
file_name=copyfile_base.config_filecopy.file_name[0]

def copyfile(srcdir,desdir,filename,i):
    str4 = desdir+os.path.basename(srcdir)+str(i)           #directory folder
    try:
        if os.path.isdir(srcdir):           #check whether the dir src
            if os.path.exists(str4):        #check whether the file str4
                logging.info(str4+" exists!")
                logging.info("delete folder:"+str4)#delete des folder
                os.system('rm -rf '+str4)
                os.system('sync')
            logging.info("File "+str4+" copying start !")
            shutil.copytree(srcdir,str4)          #copy the source file to the destination file
        else:
            os.system('rm -rf '+str4)
            shutil.copyfile(srcdir,str4)
        os.system('sync')
        srcmd5 = srcdir+'//'+filename+".md5"
        shutil.copy(srcmd5,str4)        #copy the src md5
    except Exception,ex:
        logging.error(ex)
        # copyfile_base.sendmail(ex)
    
def checkmd5(srcdir,desdir,filename,i):
    str4 = desdir+os.path.basename(srcdir)+str(i)
    os.chdir(str4)
    try:
        logging.info(str4+": Check md5 start")
        str3 =  "md5sum -c "+filename+".md5 | grep FAILED"
        ex = copyfile_base.subprocess_nor(str3)
        return ex
    except Exception,ex:
        logging.error(str4+": + failed :"+ex)

def smallcopyfile1(srcdir,filename,desdir):
    i = 0    
    while True:
        # logging.info("times :"+str(m)+" "+str(i))
        str1=desdir+os.path.basename(srcdir)+str(i)
        logging.info("Desdir:"+str1)
        m = copyfile_base.checkdisk_linux(desdir)
        if m == 0 and (os.path.exists(str1)==0):
            logging.info("A finished wheel disk!")
            i = 0
        else:
            try:
                copyfile(srcdir,desdir,filename,i)
                time.sleep(1)
                str5 = checkmd5(srcdir,desdir,filename,i)
                if str5.find('FAILED') is -1:            #check whether the wrong copy
                    logging.info("file copy Agreement!")
                else:
                    logging.error("file copy Agreement failed!\n"+str5)
                    context = str5+'\n'+str1
                    # copyfile_base.sendmail(context)
                    copyfile_base.rename(str1)
                i += 1
            except Exception,ex:
                logging.error(ex)
                # copyfile_base.sendmail(ex)
                # sys.exit()

def testcase1():   #每个拷贝目录使用一个线程进行拷贝
    copyfile_base.srcfile_init_linux(src_dir,file_name)   #initialization file_name
    m = len(copyfile_base.config_filecopy.des_dir)
    for i in range(m):
        t1 = threading.Thread(target=smallcopyfile1,args=(src_dir,file_name,copyfile_base.config_filecopy.des_dir[i]))
        t1.start()
        time.sleep(1)

def testcase2():  
    for i in range(3):
        t1 = threading.Thread(target=testcase1)
        t1.start()
        time.sleep(600)  

if __name__ == '__main__':
    testcase1()
    #testcase2(number)




