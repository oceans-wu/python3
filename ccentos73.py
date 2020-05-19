import os
import random
import string
import uuid
import sys


class Config(object):

    vir_cpu = 1
    vir_memory = 1024 * 1024
    vir_name = "test"
    vir_uuid = "8f2bb4a7-c7ed-32aa-3676-9fb05923260d"
    vir_old_disk = "/root/clone/centos73/modle73.qcow2"
    vir_new_disk = "/data/vmfs/"
    vir_vncport = "5955"
    vir_new_mac1 = "52:54:00:1a:93:1e"
    vir_new_mac2 = "52:54:00:73:6b:ee"
    vir_new_mac3 = "52:54:00:74:1f:37"
    config_mould_file = "/root/clone/centos73/modle73.xml"
    config_new_file = "/data/image/test.xml"
    vir_eth0 = "/data/ipdir/ifcfg-eth0"
    vir_eth1 = "/data/ipdir/ifcfg-eth1"
    vir_eth2 = "/data/ipdir/ifcfg-eth2"
    vir_ip_dir = "/etc/sysconfig/network-scripts/"
    vir_ip = "192.168.144.178"
    vir_netmask = "255.255.0.0"
    vir_gateway = "192.168.2.1"
    vir_net_file = "/data/ipdir/70-persistent-net.rules"
    vir_net_dir = "/etc/udev/rules.d/"

    def __init__(self, v_name, v_cpu=1, v_memory=1024):
        self.v_name = v_name
        self.v_cpu = v_cpu
        self.v_memroy = v_memory

    def kvm_name(self):
        Config.vir_name = self.v_name
        if os.path.isfile(Config.vir_name):
            os.remove(Config.vir_name)
        con = "cp {} /data/vmfs/{}.qcow2".format(Config.vir_old_disk, self.v_name)
        Config.vir_new_disk = "/data/vmfs/{}.qcow2".format(self.v_name)
        Config.config_new_file = "/data/image/{}.xml".format(self.v_name)
        if int(self.v_cpu) != 1:
            Config.vir_cpu = self.v_cpu
        if int(self.v_memroy) != 1024:
            Config.vir_memory = int(self.v_memroy) * 1024
        os.system(con)


    @classmethod
    def uuid_mac(cls):

        cls.vir_uuid = uuid.uuid1()
        mac_list1 = [0x60, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        mac_list2 = [0x60, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        mac_list3 = [0x60, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        cls.vir_new_mac1 = ':'.join(map(lambda x: "%02x" % x, mac_list1))
        cls.vir_new_mac2 = ':'.join(map(lambda x: "%02x" % x, mac_list2))
        cls.vir_new_mac3 = ':'.join(map(lambda x: "%02x" % x, mac_list3))

    @classmethod
    def vnc_port(cls):
        con = "netstat -antpu | grep kvm"
        ports_list = []
        vnc_ports = os.popen(con).readlines()
        for line in vnc_ports:
            port = line.split()[3].split(":")[1]
            ports_list.append(port)
        while True:
            i = 0
            port = "59" + ''.join(random.sample('0123456789', 2))
            if port not in ports_list:
                cls.vir_vncport = port
                return port
            i += 1


    def kvm_ip(self, vir_ip0=None, vir_ip1=None, vir_ip2=None):

        com = "virt-copy-in -d {} {} {}".format(kvm_name, Config.vir_eth0, Config.vir_ip_dir)
        com1 = "virt-copy-in -d {} {} {}".format(kvm_name, Config.vir_eth1, Config.vir_ip_dir)
        com2 = "virt-copy-in -d {} {} {}".format(kvm_name, Config.vir_eth2, Config.vir_ip_dir)
        com3 = "virt-copy-in -d {} {} {}".format(kvm_name, Config.vir_net_file, Config.vir_net_dir)

        eth0_file = []
        if vir_ip0 != None:
            with open(Config.vir_eth0) as f:
                for line in f.readlines():
                    if line.startswith("IPADDR"):
                        eth0_file.append("IPADDR={}\n".format(vir_ip0))
                    elif line.startswith("NETMASK"):
                        eth0_file.append("NETMASK={}\n".format(Config.vir_netmask))
                    elif line.startswith("GATEWAY"):
                        eth0_file.append("GATEWAY={}\n".format(Config.vir_gateway))
                    else:
                        eth0_file.append(line)
            with open(Config.vir_eth0, "w") as f:
                for line in eth0_file:
                    f.write(line)
            os.system(com)
        else:
            pass

        eth1_file = []
        if vir_ip1 != None:
            with open(Config.vir_eth1) as f:
                for line in f.readlines():
                    if line.startswith("IPADDR"):
                        eth1_file.append("IPADDR={}\n".format(vir_ip1))
                    elif line.startswith("NETMASK"):
                        eth1_file.append("NETMASK={}\n".format(Config.vir_netmask))
                    else:
                        eth1_file.append(line)
            with open(Config.vir_eth1, "w") as f:
                for line in eth1_file:
                    f.write(line)
            os.system(com1)
        else:
            pass

        eth2_file = []
        if vir_ip2 != None:
            with open(Config.vir_eth2) as f:
                for line in f.readlines():
                    if line.startswith("IPADDR"):
                        eth2_file.append("IPADDR={}\n".format(vir_ip2))
                    elif line.startswith("NETMASK"):
                        eth2_file.append("NETMASK={}\n".format(Config.vir_netmask))
                    else:
                        eth2_file.append(line)
            with open(Config.vir_eth2, "w") as f:
                for line in eth2_file:
                    f.write(line)
            os.system(com2)
        else:
            pass
        os.system(com3)



def change_config():
    config_list = []
    with open(Config.config_mould_file) as f:
        for line in f.readlines():
            if "<name>" and "</name>" in line:
                config_list.append("  <name>{}</name>\n".format(Config.vir_name))
            elif "  <uuid>" and "</uuid>" in line:
                config_list.append("  <uuid>{}</uuid>\n".format(Config.vir_uuid))
            elif "  <memory" and "</memory>" in line:
                config_list.append("  <memory unit='KiB'>{}</memory>\n".format(Config.vir_memory))
            elif "currentMemory" and "</currentMemory>" in line:
                config_list.append("  <currentMemory unit='KiB'>{}</currentMemory>\n".format(Config.vir_memory))
            elif "vcpu" and "</vcpu>" in line:
                config_list.append("  <vcpu placement='static'>{}</vcpu>\n".format(Config.vir_cpu))
            elif "<source file" in line:
                config_list.append("      <source file='{}'/>\n".format(Config.vir_new_disk))
            elif "mac address" in line:
                if "52:54:00:1a:93:1e" in line:
                    config_list.append("      <mac address='{}'/>\n".format(Config.vir_new_mac1))
                elif "52:54:00:73:6b:ee" in line:
                    config_list.append("      <mac address='{}'/>\n".format(Config.vir_new_mac2))
                elif "52:54:00:74:1f:37" in line:
                    config_list.append("      <mac address='{}'/>\n".format(Config.vir_new_mac3))
                else:
                    config_list.append("      <mac address='{}'/>\n".format(Config.vir_new_mac1))
            elif "graphics type" and "vnc" in line:
                config_list.append("    <graphics type='vnc' port='{}' autoport='no' listen='0.0.0.0'>\n".format(Config.vir_vncport))
            else:
                config_list.append(line)
    with open(Config.config_new_file, "w") as f:
        for line in config_list:
            f.write(line)

def kvmnames():
    kvmnames = {}
    namelist = 'virsh list --all'
    kvmname = os.popen(namelist).readlines()[2:-1]
    for i in kvmname:
        b = i.split()
        kvmnames[b[1]] = b[2]
    return kvmnames

def del_kvm():
    kvm_names = kvmnames()
    while True:
        KvmName = input("请输入需要删除的虚拟机(q或quit退出):" )
        if KvmName == "q" or "quit":
            sys.exit()
        if KvmName in kvm_names:
            os.system(f"virsh destroy {KvmName}")
            os.system(f"virsh undefine {KvmName}")
            os.system(f"rm -rf /data/vmfs/{KvmName}.qcow2")
            os.system(f"rm -rf /data/image/{KvmName}.qcow2")
            print(f"虚拟机<{KvmName}>已经删除")
        else:
            print("没有虚拟机")
            break




def make_kvm(kvm_name, kvm_cpu=1, kvm_memory=1024, vir_ip0=None, vir_ip1=None, vir_ip2=None):

    vir_kvms = kvmnames()
    print(vir_kvms)
    if kvm_name in vir_kvms:
        print("虚拟机已经存在")
        return
    kvmname = Config(kvm_name, kvm_cpu, kvm_memory)
    kvmname.kvm_name()
    Config.uuid_mac()
    vir_vnc_port = Config.vnc_port()
    change_config()
    con = "virsh define {}".format(Config.config_new_file)
    os.system(con)
    kvmname.kvm_ip(vir_ip0, vir_ip1, vir_ip2)
    print(f"虚拟机的ip:{vir_ip0}")
    print("虚拟机正在启动 vnc 端口是:{}".format(vir_vnc_port))
    os.system("virsh start {}".format(kvm_name))

if __name__ == "__main__":
    kvm_name = "jumpserver2"
    kvm_cpu = 2
    kvm_memory = 2048
    vir_ip0 = "192.168.44.100"
    vir_ip1 = None
    vir_ip2 = None
    while True:
        print("="*40)
        print("|[1] 创建虚拟机   | [2] 删除虚拟机   |")
        print("="*40)
        num = input("请输入编号(q或quit退出):")
        if num == "q" or "quit":
            sys.exit()
        if num == "1":
            make_kvm(kvm_name, kvm_cpu, kvm_memory, vir_ip0, vir_ip1, vir_ip2)
        if num == "2":
            del_kvm()

