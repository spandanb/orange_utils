import paramiko 

def remote_fetch(ip_addr, username, cmd):
    """
    Fetch the result of some 
    command executed on a remote system
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip_addr, username=username)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.readlines() 

def get_tun_ip(ip_addr, username):
    """
    Get TUN IP of remote host
    """
    cmd = "ifconfig tun0 | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'" 
    tun_ip = remote_fetch(ip_addr, username, cmd)[0].strip()
    return tun_ip

def overlay_ip(ip):
    """Returns the overlay IP 
    i.e. X.X.A.B -> 192.168.A.B
    """
    return "192.168.{}.{}".format( *ip.split(".")[2:])

