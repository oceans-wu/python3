import os
import sys

def  dayin():
    while True:
        print('--------------------[KVM操作面板]--------------------------')
        print('|   [1] 创建虚拟机        |   [2] 删除虚拟机               |')
        print('-' * 60)
        num = input('请输入相应数字(q或者quit退出):')
        if num == 'q' or num == 'quit':
            sys.exit()
        if num == '1':
            while True:
                print('---------------[请选择安装的系统]---------------------------')
                print('|  [1] Centos6.8      |   [2]   Centos7.3                  | ')
                print('-' * 60)
                print('|  [3] Windows 2008   |   [4]   Windows 2012               |')
                print('-' * 60)
                num = input('请选择要安装的系统(q或者quit退出)：')
                if num == 'q' or num == 'quit':
                    sys.exit()
                if num == '1':
                    print('准备安装Centos6.8 系统.')
                    return num
                if num == '2':
                    print('准备安装Centos7.3 系统.')
                    return num
                if num == '3':
                    print('准备安装Windows 2008 系统.')
                    return num
                if num == '4':
                    print('准备安装Windows 2012 系统.')
                    return num

        if int(num) == 2:
            return int(num)

def delkvm(kvmname):
    undefine = 'virsh undefine {}'
    rm = 'rm -rf /var/lib/libvirt/images/{}.qcow2 '
    os.popen(undefine.format(kvmname))
    os.popen(rm.format(kvmname))
    print('虚拟机{}已经删除'.format(kvmname))

def kvmnames():
    kvmnames = {}
    namelist = 'virsh list --all'
    kvmname = os.popen(namelist).readlines()[2:-1]
    for i in kvmname:
        b = i.split()
        kvmnames[b[1]] = b[2]
    return kvmnames

def makecentos6(kvmname, cpu , memory, disk, vncnum):
    # isodir = '/data/iso/CentOS-7.3_x86_64.iso'
    isodir = '/data/iso/CentOS-6.8_x86_64.iso'
    # isodir = '/data/iso/CentOS-6.5_x86_64.iso'


    diskdir = '/var/lib/libvirt/images/{}.qcow2'.format(kvmname)
    makedisk = 'qemu-img create -f qcow2 {} {}G'.format(diskdir,disk)
    con = 'virt-install --name={} --virt-type=kvm --vcpus={} --memory={},maxmemory={} --cdrom={} --disk path={} \
    --network bridge=br0 --vnc --vncport={} --vnclisten=0.0.0.0 --noautoconsole --autostart'.format(kvmname, cpu, memory, memory, isodir, diskdir, vncnum)
    os.popen(makedisk)
    os.popen(con)
def makecentos7(kvmname, cpu , memory, disk, vncnum):
    isodir = '/data/iso/CentOS-7.3_x86_64.iso'
    # isodir1 = '/data/iso/CentOS-6.8_x86_64.iso'
    # isodir = '/data/iso/CentOS-6.5_x86_64.iso'


    diskdir = '/var/lib/libvirt/images/{}.qcow2'.format(kvmname)
    makedisk = 'qemu-img create -f qcow2 {} {}G'.format(diskdir,disk)
    con = 'virt-install --name={} --virt-type=kvm --vcpus={} --memory={},maxmemory={} --cdrom={} --disk path={} \
    --network bridge=br0 --vnc --vncport={} --vnclisten=0.0.0.0 --noautoconsole --autostart'.format(kvmname, cpu, memory, memory, isodir, diskdir, vncnum)
    os.popen(makedisk)
    os.popen(con)

def kvmcount():
    kvmlist = kvmnames()
    for k, v in kvmlist.items():
        print(k)
    while True:
        kvmname = input('请输入虚拟机名字(字母加数,q或者quit退出)：')
        if kvmname == 'q' or kvmname == 'quit':
            sys.exit()
        if kvmname.isalnum():
            if kvmname in kvmlist:
                print('虚拟机名字已经存在')
            else:
                break
    while True:
        cpu = input("请输入CPU核数（1-4）：")
        if cpu.isdigit():
            if int(cpu) >=1 and int(cpu) < 5:
                break

    while True:
        memory = input('请输入内存大小(1024-4096)：')
        if  memory.isdigit():
            if int(memory) > 1023 and int(memory) < 4097:
                break
    while True:
        disk = input('请输入磁盘大小(20-50)：')
        if disk.isdigit():
            if int(disk) > 19 and int(disk) < 51:
                break
    portlist = []
    com = 'netstat -antpu |grep kvm'
    vncports = os.popen(com).readlines()
    for line in vncports:
        port = line.split()[3].split(':')[1]
        portlist.append(port)
    print(portlist)
    while True:
        vncnum = input('请输入ＶＮＣ端口号(5910-5999)：')
        if vncnum.isdigit():
            if vncnum in portlist:
                print('端口号已经被使用')
            else:
                if int(vncnum) > 5910 and int(vncnum) < 5999:
                    break
    return kvmname, cpu, memory, disk, vncnum

def whiskvm():
    a = dayin()
    if a == 2:
        kvmlist = kvmnames()
        for k, v in kvmlist.items():
            print(k, v)
        while True:
            delname = input('请输入要删除的虚拟机名(q或quit退出)：')
            if delname == "q" or "quit":
                sys.exit()
            if delname not in kvmlist:
                if delname == "":
                    print("请输入虚拟机名")
                else:
                    print('虚拟机名不存在')
            else:
                print('正在删除虚拟机{}'.format(delname))
                if kvmlist[delname] == 'running':
                    shutdown = 'virsh destroy {}'
                    os.popen(shutdown.format(delname))
                    delkvm(delname)
                    print('虚拟机{}已经删除'.format(delname))
                else:
                    delkvm(delname)
                    print('虚拟机{}已经删除'.format(delname))
    if a == "1":
        kvmname, cpu, memory, disk, vncnum  = kvmcount()
        makecentos6(kvmname, cpu, memory, disk, vncnum)
        print('虚拟机创建完成'.format(kvmname))
        print('请链接VNC安装,VNC端口号：{}'.format(vncnum))
    if a == "2":
        kvmname, cpu, memory, disk, vncnum  = kvmcount()
        makecentos7(kvmname, cpu, memory, disk, vncnum)
        print('虚拟机创建完成'.format(kvmname))
        print('请链接VNC安装,VNC端口号：{}'.format(vncnum))

if __name__ == '__main__':
    whiskvm()
