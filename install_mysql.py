import os
import sys
import re
import pymysql


class Global(object):
    """"""
    group = "mysql"
    user = "mysql"
    defaultpass = ""  # mysql初始密码
    mysqlpass = ""  # mysql密码
    version = ""  # mysql版本参数有:mysql5.6  mysql5.7
    system = ""  # 系统 Centos6 或者 Centos7
    batdir = "/root/mysql/"
    bat = ""
    datadir = "/data/mysql/data"
    data = "/data/mysql"
    redologdir = "/data/mysql/redolog"
    undologdir = "/data/mysql/undolog"
    tmpdir = "/data/mysql/tmp"
    innodbtmpdir = "/data/mysql/innodb_tmp"
    logdir = "/data/logs/mysql/"
    logfile = "/data/logs/mysql/mysql-error.log"
    generalogfile = "/data/logs/mysql/mysql.log"
    myfile = "/etc/my.cnf"

    @classmethod
    def get57_mycnf(cls):
        mycnf = f"""[client]
port = 3306
socket = /data/mysql/mysql.sock
[mysqld]
###############################基础设置#####################################
server-id = 1
port = 3306 
#skip-grant-tables
datadir = {cls.datadir}
tmpdir  = {cls.tmpdir}
innodb_tmpdir = {cls.innodbtmpdir}
log_error = {cls.logfile}
socket  = /data/mysql/mysql.sock
#只能用IP地址检查客户端的登录，不用主机名
#skip_name_resolve = 1

default-storage-engine = InnoDB
back_log = 3000
flush_time = 0
group_concat_max_len = 10240
ft_max_word_len = 84
ft_min_word_len = 4
ft_query_expansion_limit = 20
join_buffer_size = 16M

query_cache_size = 64M
query_cache_limit = 1M
character-set-server = utf8mb4
collation-server = utf8mb4_general_ci
init_connect=SET NAMES utf8mb4
lower_case_table_names = 1 
max_connect_errors = 100
tmp_table_size = 134217728
max_heap_table_size = 134217728
open_files_limit = 65535

#################################################################################
max_user_connections = 100
max_connections = 400
innodb_buffer_pool_size = 600M
################CPU多核处理能力设置，假设CPU是2颗4核的，设置如下
#################读多，写少可以设成2:6的比例
innodb_write_io_threads = 4
innodb_read_io_threads = 4
binlog_stmt_cache_size = 32768
bulk_insert_buffer_size = 4M
sort_buffer_size = 2097152
thread_cache_size = 64
innodb_log_file_size = 124M
####################################################################################

explicit_defaults_for_timestamp = true
max_allowed_packet = 10G
interactive_timeout = 86400
wait_timeout = 86400
binlog_cache_size = 10485760
slow_query_log = 1
slow_query_log_file = /data/mysql/mysql-slow.log
log_queries_not_using_indexes = 1
log_throttle_queries_not_using_indexes = 5
log_slow_slave_statements = 1
long_query_time = 2
min_examined_row_limit = 100
expire_logs_days = 7
log-bin = /data/mysql/mysql-bin
binlog_format = ROW
binlog_checksum = CRC32
block_encryption_mode = "aes-128-ecb"
log_slave_updates
relay_log_recovery = 1
slave_skip_errors = ddl_exist_errors
innodb_flush_log_at_trx_commit = 2
sync_binlog = 1
net_read_timeout = 30
net_write_timeout = 60
net_retry_count = 10
innodb_page_size = 8192
innodb_adaptive_max_sleep_delay = 150000
innodb_log_buffer_size = 16777216
innodb_autoinc_lock_mode = 2
innodb_buffer_pool_dump_at_shutdown = ON
innodb_buffer_pool_load_at_startup = ON
innodb_buffer_pool_dump_pct = 40
#################UnIDB更改缓冲区的最大大小，作为缓冲池总大小的百分比。对于具有大量插入、更新和删除活动的mysql服务器，可以增加该值，对于具有用于报告的不变数据的mysql服务器，可以减少该值。
innodb_change_buffer_max_size =25

innodb_commit_concurrency = 0
innodb_flush_method = O_DIRECT
innodb_file_format = Barracuda
innodb_io_capacity = 500
innodb_lock_wait_timeout = 30
innodb_log_group_home_dir = {cls.redologdir}
innodb_undo_directory = {cls.undologdir}
innodb_log_files_in_group = 3
innodb_max_dirty_pages_pct = 90
innodb_open_files = 3000
innodb_undo_log_truncate = 1
innodb_undo_tablespaces = 3
innodb_undo_logs = 128
innodb_large_prefix = 1
innodb_purge_threads = 4
innodb_thread_concurrency = 0
innodb_concurrency_tickets = 5000
innodb_ft_cache_size = 8000000
innodb_ft_enable_diag_print = off
innodb_ft_enable_stopword = on
innodb_ft_max_token_size = 84
innodb_ft_min_token_size = 3
innodb_ft_num_word_optimize = 2000
innodb_ft_result_cache_limit = 2000000000
innodb_ft_sort_pll_degree = 2
innodb_ft_total_cache_size = 640000000
innodb_io_capacity_max = 40000
############################其他内容 设置##########################################
[mysqldump]
quick
max_allowed_packet = 500M
[mysql]
no-auto-rehash
[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M
[mysqlhotcopy]
interactive-timeout
[mysqld_safe]
################增加每个进程的可打开文件数量.
pid-file=/data/mysql/mysqld.pid
open-files-limit = 28192
"""
        return mycnf

    @classmethod
    def get56_mycnf(cls):
        mycnf = f"""[client]
socket = /data/mysql/mysql.sock
[mysqld]
back_log=3000
binlog_cache_size=131072
binlog_checksum=CRC32
binlog_order_commits=ON
binlog_rows_query_log_events=OFF
binlog_row_image=full
binlog_stmt_cache_size=32768
bulk_insert_buffer_size=4194304
character_set_filesystem=binary
character_set_server=utf8
concurrent_insert=1
connect_timeout=10
default_storage_engine=InnoDB
default_week_format=0
delayed_insert_limit=100
delayed_insert_timeout=300
delayed_queue_size=1000
delay_key_write=ON
disconnect_on_expired_password=ON
div_precision_increment=4
end_markers_in_json=OFF
eq_range_index_dive_limit=10
explicit_defaults_for_timestamp=false
flush_time=0
ft_max_word_len=84
ft_min_word_len=4
ft_query_expansion_limit=20
group_concat_max_len=1024
host_cache_size=512
innodb_adaptive_flushing=ON
innodb_adaptive_flushing_lwm=10
innodb_adaptive_hash_index=ON
innodb_adaptive_max_sleep_delay=150000
innodb_additional_mem_pool_size=2097152
innodb_autoextend_increment=64
innodb_autoinc_lock_mode=2
innodb_buffer_pool_dump_at_shutdown=OFF
innodb_buffer_pool_instances=8
innodb_buffer_pool_load_at_startup=OFF
innodb_change_buffering=all
innodb_change_buffer_max_size=25
innodb_checksum_algorithm=innodb
innodb_cmp_per_index_enabled=OFF
innodb_commit_concurrency=0
innodb_compression_failure_threshold_pct=5
innodb_compression_level=6
innodb_compression_pad_pct_max=50
innodb_concurrency_tickets=5000
innodb_disable_sort_file_cache=ON
innodb_flush_method=O_DIRECT
innodb_flush_neighbors=1
innodb_ft_cache_size=8000000
innodb_ft_enable_diag_print=OFF
innodb_ft_enable_stopword=ON
innodb_ft_max_token_size=84
innodb_ft_min_token_size=3
innodb_ft_num_word_optimize=2000
innodb_ft_result_cache_limit=2000000000
innodb_ft_sort_pll_degree=2
innodb_ft_total_cache_size=640000000
innodb_io_capacity=1500
innodb_io_capacity_max=4000
innodb_large_prefix=OFF
innodb_lock_wait_timeout=50
innodb_log_compressed_pages=OFF
innodb_lru_scan_depth=1024
innodb_max_dirty_pages_pct=75
innodb_max_dirty_pages_pct_lwm=0
innodb_max_purge_lag=0
innodb_max_purge_lag_delay=0
innodb_old_blocks_pct=37
innodb_old_blocks_time=1000
innodb_online_alter_log_max_size=134217728
innodb_open_files=65535
innodb_optimize_fulltext_only=OFF
innodb_print_all_deadlocks=OFF
innodb_purge_batch_size=300
innodb_purge_threads=1
innodb_random_read_ahead=OFF
innodb_read_ahead_threshold=56
innodb_read_io_threads=4
innodb_rollback_on_timeout=OFF
innodb_rollback_segments=128
innodb_sort_buffer_size=1048576
innodb_spin_wait_delay=6
innodb_stats_auto_recalc=ON
innodb_stats_method=nulls_equal
innodb_stats_on_metadata=OFF
innodb_stats_persistent=ON
innodb_stats_persistent_sample_pages=20
innodb_stats_sample_pages=8
innodb_stats_transient_sample_pages=8
innodb_status_output=OFF
innodb_status_output_locks=OFF
innodb_strict_mode=OFF
innodb_support_xa=ON
innodb_sync_array_size=1
innodb_sync_spin_loops=100
innodb_table_locks=ON
innodb_thread_concurrency=0
innodb_thread_sleep_delay=10000
innodb_write_io_threads=4
interactive_timeout=7200
innodb_log_group_home_dir = {cls.redologdir}
innodb_undo_directory = {cls.undologdir}

join_buffer_size=262144
key_cache_age_threshold=300
key_cache_block_size=1024
key_cache_division_limit=100
lock_wait_timeout=31536000
log_queries_not_using_indexes=OFF
log_slow_admin_statements=OFF
log_throttle_queries_not_using_indexes=0
long_query_time=2
low_priority_updates=0
master_verify_checksum=OFF
max_allowed_packet=1073741824
max_binlog_stmt_cache_size=18446744073709547520
max_connect_errors=100
max_error_count=64
max_heap_table_size=16777216
max_join_size=18446744073709551615
max_length_for_sort_data=1024
max_prepared_stmt_count=16382
max_seeks_for_key=18446744073709551615
max_sort_length=1024
max_sp_recursion_depth=0
max_write_lock_count=102400
metadata_locks_cache_size=1024
min_examined_row_limit=0
myisam_sort_buffer_size=262144
net_buffer_length=16384
net_read_timeout=30
net_retry_count=10
net_write_timeout=60
old_passwords=0
open_files_limit=65535
optimizer_prune_level=1
optimizer_search_depth=62
optimizer_trace_limit=1
optimizer_trace_max_mem_size=16384
performance_schema=OFF
preload_buffer_size=32768
query_alloc_block_size=8192
query_cache_limit=1048576
query_cache_min_res_unit=4096
query_cache_size=3145728
query_cache_type=0
query_cache_wlock_invalidate=OFF
query_prealloc_size=8192
range_alloc_block_size=4096
slave_net_timeout=60
slow_launch_time=2
slow_query_log=ON
sort_buffer_size=1048576
stored_program_cache=256
table_definition_cache=512
table_open_cache=2000
table_open_cache_instances=1
thread_cache_size=100
thread_stack=262144
tmp_table_size=2097152
transaction_alloc_block_size=8192
transaction_prealloc_size=4096
updatable_views_with_limit=YES
wait_timeout=864000

##############################
#不进行反解析
###############################
skip-name-resolve
##########################
#summary
##########################
port=3306
datadir = {cls.datadir}
socket = /data/mysql/mysql.sock
tmpdir  = {cls.tmpdir}
innodb_tmpdir = {cls.innodbtmpdir}
user = mysql
pid-file = /data/mysql/data/mysql.pid
#############################
#connection
############################
max_connections = 500
max_user_connections = 500

#############################
#log bin
###############################
server-id=86
log-bin=/data/mysql/mysql-bin
binlog_format = row
log-slave-updates   
#级联复制，从库扩展需要·
##############################
#read
###############################
read_buffer_size = 2M
read_rnd_buffer_size = 6M

#######################################
#relay-log  slave mysql需要
########################################
relay-log-index = /data/mysql/mysqld-relay-bin
relay-log-info-file = /data/mysql/relay-log.info
relay-log = /data/mysql/mysqld-relay-bin
###################################
#log general
###################################
general_log = off
general_log_file={cls.generalogfile}
expire_logs_days=30
#########################
#log error
#######################
log-error={cls.logfile}

########################
#slow 慢查询
#####################
slow_query_log_file=/data/mysql/mysql-slow.log

###############################################
# password
#############################################
#skip-grant-tables
################################################
#innodb
##############################################
innodb_buffer_pool_size=500M     
################################################
#innodb_flush和sync_binlog为1保持数据一致性，每次事务提交都会把log buffer 刷到文件中，并调用文件‘flush’操作刷新到磁盘，数据库对IO要求非常高。硬件提供IOPS比较差，可能数据库并发受到硬件IO问题无法提升
###############################################
innodb_flush_log_at_trx_commit=1 
sync_binlog=1 
innodb_log_file_size=200M 

[mysqldump]
quick
max_allowed_packet = 500M
[mysql]
no-auto-rehash
[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M
[mysqlhotcopy]
interactive-timeout
[mysqld_safe]
################增加每个进程的可打开文件数量.
pid-file=/data/mysql/mysqld.pid
open-files-limit = 28192 
"""
        return mycnf

    @classmethod
    def makedir(cls):

        os.system(f"groupadd  {cls.group}")
        os.system(f"useradd -g {cls.group}  {cls.user}")
        if not os.path.isdir(cls.batdir):
            os.mkdir(cls.batdir)
        if not os.path.isdir(cls.datadir):
            os.makedirs(cls.datadir)
            os.mkdir(cls.redologdir)
            os.mkdir(cls.undologdir)
            os.mkdir(cls.tmpdir)
            os.mkdir(cls.innodbtmpdir)
            os.makedirs(cls.logdir)
        os.system(f"touch {cls.logfile}")
        os.system(f"touch {cls.generalogfile}")
        os.system(f"chown mysql:mysql {cls.logfile}")
        os.system(f"chown mysql:mysql {cls.generalogfile}")
        os.system(f"chown -R mysql:mysql {cls.data}")

    @classmethod
    def getsystem(cls):
        sysstr = os.popen("cat /etc/redhat-release")
        release = sysstr.read().strip()
        sumlist = re.findall(r"\d", release)
        if len(sumlist) >= 1:
            if sumlist[0] == "6":
                cls.system = "Centos6"
                print("当前系统为Centos6")

            elif sumlist[0] == "7":
                cls.system = "Centos7"
                print("当前系统为Centos7")

            else:
                print("系统不匹配")
        else:
            print("获取不到系统信息")
            sys.exit()

    @staticmethod
    def selinux():
        state = os.popen("getenforce")
        sta = state.read().strip()
        if sta != "Disabled":
            os.system("sed -i '/SELINUX/ s/enforcing/disabled/g' /etc/selinux/config")
            os.system("setenforce 0")

    @classmethod
    def install(cls):
        """"""
        if "5.7" in cls.bat:
            cls.version = "mysql5.7"
            print("正在安装mysql5.7")
            com = "yum -y install  perl-Data-Dumper perl-JSON numactl perl-Time-HiRes.x86_64 net-tools"
            com1 = "yum -y remove mysql-libs-5.1.73-7.el6.x86_64 mariadb-libs"
            com2 = "rpm -ivh mysql-*.rpm"
            os.system(com)
            os.system(com1)
            os.system(f"mv /root/{cls.bat} {cls.batdir}")
            os.chdir(cls.batdir)
            os.system(f"tar -xf {cls.bat}")
            state = os.system(com2)
            if state:
                print("mysql 安装失败")
                sys.exit()
            else:
                print("mysql5.7安装完成")
                cls.writecnf()
                os.system("/usr/sbin/mysqld --initialize --user=mysql --datadir=/data/mysql/data")
                with open(cls.logfile, "r") as f:
                    for line in f:
                        if "temporary" in line and "password" in line and "generated" in line:
                            cls.defaultpass = line.split(": ")[-1]
                            cls.defaultpass = cls.defaultpass.replace("\n",
                                                                      "")  # 或者 cls.defaultpass = cls.defaultpass.strip()

                            print("数据库初始化完成")
                            print(f"系统默认密码是：{cls.defaultpass}")
        if "5.6" in cls.bat:
            cls.version = "mysql5.6"
            print("正在安装mysql5.6 依赖包")
            con = "yum -y install  perl-Data-Dumper perl-JSON  net-tools"
            con1 = "yum -y remove mariadb-libs"
            os.system(con)
            os.system(con1)
            os.system(f"mv /root/{cls.bat} {cls.batdir}")
            os.chdir(cls.batdir)
            os.system(f"tar -xf {cls.bat}")
            os.system("rpm -ivh MySQL-*.rpm")
            print("mysql5.6安装完成")
            cls.writecnf()
            print("正在初始化...")
            os.system("/usr/bin/mysql_install_db --defaults-file=/etc/my.cnf  --user=mysql")
            print("初始化完成")

    @classmethod
    def changepass(cls):
        com = "flush privileges;"
        if cls.system == "Centos6":
            if cls.version == "mysql5.6":
                os.system("service mysql start")
                os.system("chkconfig mysql on")
            elif cls.version == "mysql5.7":
                os.system("service mysqld start")
                os.system("chkconfig mysqld on")
            else:
                pass
        if cls.system == "Centos7":
            if cls.version == "mysql5.6":
                os.system("systemctl start mysql")
                os.system("systemctl enable mysql")
            elif cls.version == "mysql5.7":
                os.system("systemctl start mysqld")
                os.system("systemctl enable mysqld")
            else:
                pass
        print(cls.version)
        if cls.version == "mysql5.6":
            # 此方法修改密码 用pymysql连不上
            # os.system(f"/usr/bin/mysqladmin -u root password '{cls.mysqlpass}'")
            # print("mysql5.6密码修改成功!!")
            # print(f"密码是:{cls.mysqlpass}")

            # 此方法修改密码 可以用pymysql连不上
            database = pymysql.connect(host="localhost", user="root", password=cls.defaultpass, database="mysql",
                                       charset="utf8")
            cursor = database.cursor()
            cursor.execute(f"update mysql.user set password=password('{cls.mysqlpass}') where user='root';")
            cursor.execute(com)
            print("mysql5.6密码修改成功!!")
            print(f"密码是:{cls.mysqlpass}")
            database.close()

        if cls.version == "mysql5.7":

            con = f"""mysql -uroot -p'{cls.defaultpass}' --connect-expired-password -e "alter user 'root'@'localhost' identified by '{cls.mysqlpass}';" """
            try:
                assert not os.system(con)
                print("mysql5.7密码修改成功!!")
                print(f"密码是:{cls.mysqlpass}")
            except AssertionError:
                print("密码修改出现异常")

    @classmethod
    def decide(cls, batname, mysqlpass):
        cls.bat = batname
        cls.mysqlpass = mysqlpass
        if os.path.isfile(f"/root/{cls.bat}"):
            print("开始安装数据库")
        else:
            print(f"没有安装包{cls.bat}")
            sys.exit()

    @classmethod
    def writecnf(cls):
        if os.path.isfile(cls.myfile):
            os.system(f"cp {cls.myfile}  {cls.myfile}.bak")
        if "5.6" in cls.bat:
            os.system(f"echo '{cls.get56_mycnf()}' > {cls.myfile}")
        if "5.7" in cls.bat:
            os.system(f"echo '{cls.get57_mycnf()}' > {cls.myfile}")

    @staticmethod
    def gogo():

        # 查看linux系统
        Global.getsystem()
        # 创建目录
        Global.makedir()
        # selinux检查配置
        Global.selinux()
        # 安装数据库
        Global.install()
        # 修改密码
        Global.changepass()


if __name__ == '__main__':
    """传递一个安装包参数,mysql密码"""
    mysql_pass = "yisu.com#*yun"
    installbat = "MySQL-5.6.47-1.el7.x86_64.rpm-bundle.tar"
    Global.decide(installbat, mysql_pass)
    Global.gogo()
