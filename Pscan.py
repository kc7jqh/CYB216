#!
#importing options/socket/thread
import optparse
import sys
from socket import *
from threading import *
import io

screenLock = Semaphore(value=1)

# List file 
    
#create socket connection to specific host / port 
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('hello\r\n')
  #      results = connSkt.recv(100)
        screenLock.acquire()
        print( "[+]" + str(tgtPort) + "/tcp open")
    except:
        screenLock.acquire()
        print( "[-]" + str(tgtPort) + "/tcp closed")
    finally:
        screenLock.release()
        connSkt.close()

#get host status and port status
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print( "[-] Cannot resolve" + tgtHost + ": Unknown hosts")
        return
    
    try:
        tgtName = gethostbyaddr(tgtIP)
        print( "\n[+] Scan Results for: "+ tgtName[0])
    except:
        print("\n[+] Scan Results for: "+ tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

#portscan execution with help option

def Main(argv):
    
    parser = optparse.OptionParser('usage %prog -H <target host> ' + '-p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target hosts')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by a comma')
    #parser.add_option('-l', dest='tgtPort', type='list', help='use a list of ports')
    (options, args) = parser.parse_args()
    
    if (options.tgtHost == None):
        print( parser.usage )
        exit(0)
    else:
        tgtHost = options.tgtHost
        print()
        
    try:    
        filehandler = open("./ports.txt","r")
    except IOError:
        print ("Error")
        
        
    while True:
        line = filehandler.readline()
        if not line:
            break; 
        connScan(tgtHost,int(line))
#handle = open( 'ports.txt', 'r')
#for line in handle :
#    ll = line.split(',')


        
if __name__ == '__main__':
    Main(sys.argv)
