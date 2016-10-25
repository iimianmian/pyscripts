#!/usr/bin/env python
# coding:utf-8
import subprocess

def split_Num(pid_num):
    cmd = "cat /proc/%s/status|grep VmRSS" % pid_num
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    data = p.communicate()[0]
    mem_proc = data.split()[1]
    return mem_proc

def get_App_Mem(app_server):
    app_mem = 0
    cmd = "ps aux|grep %s|grep -v grep" % app_server
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    data = p.communicate()[0].split('\n')[:-1]
    for i in data:
        num = int(i.split()[1])
        app_mem += int(split_Num(num))
    return app_mem

def mem_Total():
    cmd = "grep MemTotal /proc/meminfo"
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    data = p.communicate()[0]
    mem_total = data.split()[1]
    return mem_total

def get_Proportion(app_server):
    if get_App_Mem(app_server) == 0:
        print '%s Total VmRSS: 0' % app_server
    else:
        app_mem = float(get_App_Mem(app_server))
        mem_total = int(mem_Total())
        return app_mem/mem_total

if __name__ == "__main__":
    print get_App_Mem('httpd')
    print mem_Total()
    print get_Proportion('httpd')

