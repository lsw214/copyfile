文件拷贝脚本使用说明：

1、windows系统下脚本使用说明：

执行脚本：copyfile_win.py

	testcase1() //每一个目录一个线程进行拷贝

	testcase2() //每一个目录N个线程，N需要自己在脚本中配置

配置脚本：config/config_filecopy.py文件

    if platform.system() == "Windows":
    
    	src_dir=['D:\\src']     //源文件目录，此目录中有两个子目录，一个是文件目录（如：bigfile），一个目录存放md5文件（如：md5）
    
    	des_dir=['d:\\/']       //目标文件目录   
    
    	file_name = ['bigfile'] //需要拷贝的源文件目录中的目录名称

2、linux系统下脚本使用说明

