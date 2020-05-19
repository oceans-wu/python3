import os
import pymysql
import psutil
import math
import random
import sys
import configparser, paramiko
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException
from pymysql import OperationalError
from pymysql import Connection
from pymysql import cursors


class Global(object):
    data = {
        "mysqld": {"binlog_cache_size": 131072,
                   "binlog_stmt_cache_size": 32768,
                   "bulk_insert_buffer_size": 4194304,  # *******************
                   "delayed_insert_limit": 100,
                   "delayed_queue_size": 1000,
                   "host_cache_size": 500,
                   "innodb_additional_mem_pool_size": 2097152,
                   "join_buffer_size": 262144,
                   "sort_buffer_size": 1048576,  # 大于1G 就填这个数 *************
                   "table_definition_cache": 512,  # 大于1G 就填这个数 **************
                   "table_open_cache": 2000,  # 大于基准就是4000*************
                   "thread_cache_size": 100,
                   "tmp_table_size": 2097152,
                   "max_connections": 500,  # x500
                   "max_user_connections": 500,  # x500
                   "innodb_buffer_pool_size": 524288000,  # x500
                   "innodb_log_file_size": 209715200,  # 当x=8时400M
                   "innodb_write_io_threads": 1,
                   "innodb_read_io_threads": 1,
                   },
    }
    Role = "master"
    Cpus = 1
    Memorys = 1024
    MasterIp = "192.168.44.111"
    SlaveIp = "192.168.44.112"
    Port = 22
    Ip = ""
    ServerId = []
    MasterUser = "root"
    MasterPass = "root"
    MasterMysqlUser = "root"
    MasterMysqlPass = "yisu.com#*yun"
    SlaveUser = "root"
    SlavePass = "root"
    SlaveMysqlUser = "root"
    SlaveMysqlPass = "yisu.com#*yun"
    Replication = "replica"
    ReplicationPass = "yisu.com#*yun"
    Database = "mysql"
    Path = "/etc/my.cnf"
    MasterFile = ""
    MasterPos = ""
    SlaveFile = ""
    SlavePos = ""
    Mlstate = ""
    NetCard = "eth0"                 # 需要获取ip的网卡名

    @classmethod
    def getcpumemory(cls):
        cls.Cpus = psutil.cpu_count()
        cls.Memorys = math.ceil(psutil.virtual_memory()[0] / 1024 / 1024 / 1024)
        cls.ServerId.append(random.randint(1, 499))
        cls.ServerId.append(random.randint(500, 999))

    @classmethod
    def changedata(cls):
        if cls.Memorys > 1:
            cls.data["mysqld"]["innodb_buffer_pool_size"] = math.ceil((cls.Memorys * 1024 * 1024 * 1024) * 0.8)
            if cls.Memorys < 4:
                cls.data["mysqld"]["innodb_write_io_threads"] = 1
                cls.data["mysqld"]["innodb_read_io_threads"] = 1
            else:
                cls.data["mysqld"]["innodb_write_io_threads"] = math.ceil(cls.Memorys / 4)
                cls.data["mysqld"]["innodb_read_io_threads"] = math.ceil(cls.Memorys / 4 * 3)

    @classmethod
    def getip(cls):
        com = "ip a"
        ipstr = os.popen(com).readlines()
        for line in ipstr:
            line = line.strip()
            if line.startswith("inet") and line.endswith("{}".format(cls.NetCard)):
                cls.Ip = line.split()[1].split("/")[0]
                break
            else:
                print("没有获取到Ip")
                exit()

    @classmethod
    def sshslave(cls):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=cls.SlaveIp, port=cls.Port, username=cls.SlaveUser, password=cls.SlavePass,
                        allow_agent=True)
            return ssh
        except AuthenticationException as e:
            print(f"远程主机连不上:{e}")
            sys.exit()
        except NoValidConnectionsError as e:
            print(f"远程主机密码错误:{e}")
            sys.exit()
        except Exception as ex:
            print(f"远程不上从机:{ex}")
            sys.exit()

    @classmethod
    def connetmysql(cls, username, userpass):
        try:
            condb = Connection(host="localhost", user=username, password=userpass, database="mysql", charset="utf8")
            cursor = condb.cursor(cursors.DictCursor)
            return cursor
        except OperationalError as e:
            print(f"连不上mysql:{e}")
            sys.exit()
        except Exception as e:
            print(f"连不上mysql:{e}")
            sys.exit()


    @classmethod
    def changepass(cls, ipadress, mysqluser, mysqlpass, database, newpass):
        database = pymysql.connect(cls, ipadress, mysqluser, mysqlpass, database)
        cursor = database.cursor()
        sql = "alter user 'root'@'localhost' identified by {};".format(newpass)
        cursor.execute(sql)
        cursor.execute("flush privileges;")
        cursor.commit()
        cursor.close()
        print("mysql 修改密码完成")

    @classmethod
    def changemasterconf(cls):
        """修改主配置文件"""
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(cls.Path)
        print("开始修改master配置文件")
        for key in cls.data["mysqld"].keys():
            config.set("mysqld", key, str(cls.data["mysqld"][key]))
            config.set("mysqld", "server-id", str(cls.ServerId[0]))
            config.set("mysqld", "auto_increment_increment", "2")
            config.set("mysqld", "auto_increment_offset", "1")
            config.write(open(cls.Path, "w"))
        print("保存master配置文件完成")

    @classmethod
    def changeslaveconf(cls):
        """修改从配置文件"""
        ssh = cls.sshslave()
        com = f"cat {cls.Path}"
        stdin, stdout, stderr = ssh.exec_command(com)
        out, err = stdout.read(), stderr.read()
        out = out.decode()
        if err:
            print("获取不到从机配置文件")
            exit()
        print("开始修改slave配置文件")

        config = configparser.ConfigParser(allow_no_value=True)
        config.read_string(out, source='<string>')
        for key in cls.data["mysqld"].keys():
            config.set("mysqld", key, str(cls.data["mysqld"][key]))
        config.set("mysqld", "server-id", str(cls.ServerId[1]))
        config.set("mysqld", "auto_increment_increment", "2")
        config.set("mysqld", "auto_increment_offset", "2")
        sftp = ssh.open_sftp()
        conf = sftp.open(cls.Path, "w")
        config.write(conf)
        sftp.close()
        print("保存slave配置文件完成")

    @classmethod
    def masterslave(cls):

        state = os.system(f"mysql -u'{cls.MasterMysqlUser}' -p'{cls.MasterMysqlPass}' -e 'show status;'")
        if not state:
            os.system("systemctl start mysql")

        my_dict = {}
        ssh = cls.sshslave()
        sql1 = f"grant replication slave, replication client on *.* to '{cls.Replication}'@'{cls.SlaveIp}' identified by '{cls.ReplicationPass}';"
        sql2 = "reset master;"
        sql3 = "show master status"
        sql4 = "flush privileges;"
        sql5 = "start salve;"
        sql6 = r"show slave status\G;"
        for i in [0, 1]:
            if i == 0:
                cursor = cls.connetmysql(cls.MasterMysqlUser, cls.MasterMysqlPass)
                cursor.execute(sql2)
                cursor.execute(sql1)
                cursor.execute(sql3)
                result = cursor.fetchone()
                cursor.execute(sql4)
                cursor.close()
                cls.MasterFile = result.get("File")
                cls.MasterPos = result.get("Position")

            if i == 1:
                    com = f"change master to master_host='{cls.MasterIp}',master_user='{cls.Replication}',master_password='{cls.ReplicationPass}',master_port=3306,master_log_file='{cls.MasterFile}',master_log_pos={cls.MasterPos};"
                    com1 = f"""mysql -uroot -p'{cls.SlaveMysqlPass}' -e "{com}" """
                    com2 = f"mysql -uroot -p'{cls.SlaveMysqlPass}' -e '{sql2}'"
                    com5 = f"mysql -uroot -p'{cls.SlaveMysqlPass}' -e '{sql6}'"
                    ssh.exec_command(com2)
                    stdin, stdout, stderr = ssh.exec_command(com1)
                    out, err = stdout.read(), stderr.read()
                    strerr = err.decode().strip().split("\n")

                    if len(strerr) == 1 and strerr[0] == "Warning: Using a password on the command line interface can be insecure.":

                        print("从机配置主从同步成功")
                        print("开启主从同步")
                        ssh.exec_command(f"mysql -uroot -p'{cls.SlaveMysqlPass}' -e '{sql5}'")
                        print("准备重启mysql服务")
                        std_in, std_out, std_er = ssh.exec_command("systemctl restart mysql")
                        strout, strer = std_out.read(), std_er.read()

                        if strer:
                            print("重启mysql服务失败")
                            exit(1)
                        else:
                            ssh.exec_command(f"mysql -uroot -p'{cls.SlaveMysqlPass}' -e '{sql5}'")
                            str_in, str_out, str_err = ssh.exec_command(com5)
                            sout = str_out.read().decode()
                            strout = sout.split("\n")[1:-1]
                            ssh.close()
                            for i in strout:
                                stri = i.split(":")
                                my_dict[stri[0].strip()] = stri[1].strip()
                            if my_dict.get("Slave_IO_Running") == "Yes" and my_dict.get("Slave_SQL_Running") == "Yes":
                                print("主从同步成功")
                                cls.Mlstate = 0
                            else:
                                print("主从同步失败")
                                cls.Mlstate = 1

                    else:
                        print(f"主从配置失败:{strerr[1]}")


    @classmethod
    def mastermaster(cls):
        if cls.Mlstate != 0:
            sys.exit()
        ssh = cls.sshslave()
        sql = f"""mysql -u{cls.SlaveMysqlUser} -p'{cls.SlaveMysqlPass}' -e "grant replication slave, replication client on *.* to '{cls.Replication}'@'{cls.MasterIp}' identified by '{cls.ReplicationPass}';" """
        sql1 = f"mysql -u{cls.SlaveMysqlUser} -p'{cls.SlaveMysqlPass}' -e 'show master status;'"

        stin, stout, ster = ssh.exec_command(sql)
        sout, ser = stout.read().decode(), ster.read().decode().strip().split('\n')
        if len(ser) == 1 and ser[0] == 'Warning: Using a password on the command line interface can be insecure.':
            print("从机授权完成")
            stdin, stdout, stderr = ssh.exec_command(sql1)
            out, err = stdout.read().decode(), stderr.read().decode().strip().split("\n")
            if len(err) == 1 and err[0] == 'Warning: Using a password on the command line interface can be insecure.':
                cls.SlaveFile = out.strip().split("\t")[-2].split("\n")[1]
                cls.SlavePos = out.strip().split("\t")[-1]
                com = f"change master to master_host='{cls.SlaveIp}',master_user='{cls.Replication}',master_password='{cls.ReplicationPass}',master_port=3306,master_log_file='{cls.SlaveFile}',master_log_pos={cls.SlavePos};"
                print("开始配置主机同步信息")
                cursor = cls.connetmysql(cls.MasterMysqlUser, cls.MasterMysqlPass)
                cursor.execute(com)
                print("配置主主同步完成")
                cursor.execute("start slave")
                print("开启主主同步完成")
                starstr = os.system("systemctl restart mysql")
                if starstr == 0:
                    print("mysql 重启完成")
                    cursor = cls.connetmysql(cls.MasterMysqlUser, cls.MasterMysqlPass)
                    cursor.execute("show slave status")
                    result = cursor.fetchone()
                    if result.get("Slave_IO_Running") == result.get("Slave_SQL_Running") == "Yes":
                        print("主从同步成功")
                        cursor.close()
                    else:
                        print("主从同步失败")
                        cursor.close()
                else:
                    print("mysql重启失败")
            else:
                print("获取从机master状态失败")
        else:
            print("从机授权同步用户失败")


    @staticmethod
    def gogo():
        Global.getcpumemory()
        Global.changedata()
        Global.changemasterconf()
        Global.changeslaveconf()
        Global.masterslave()
        Global.mastermaster()     # 配置主主同步


if __name__ == "__main__":
    Global.gogo()
