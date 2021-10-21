import socket
from IPy import IP

def scan(target):
    converted_ip = check_ip(target)
    print('\n'+'[+ Scanning Target]'+str(target))
    for port in range (1,100):
        scan_port(converted_ip,port)

def scan_port(ipaddress,port):
    try:
        sock = socket.socket()
        sock.settimeout(0.3)
        sock.connect((ipaddress, port))
        try:
            banner = get_banner(sock)
            print('[+] Open port '+str(port)+' : '+str(banner.decode().strip('\n')))
        except:
            print('[+] Open port ' + str(port))
    except:pass

def get_banner(b):
    return b.recv(1024)

def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

if __name__=='__main__':
    targets = input('[+] Enter target/s (for multiple target use ,) : ')
    if ',' in targets:
        for ip_addr in targets.split(','):
            scan(ip_addr.strip(' '))
    else:
        scan(targets)
