#A hack of COLLOSAL proportions.
#In order to automate the screen shot process using D3 rendering
#Listens for a web-socket connection from a browser and saves SVG data as PNG
#img for appropriate crossing
import socket

def main():
    MAX_SIZE = 200000

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('127.0.0.1', 9998))
    serversocket.listen(1)
    print 'Server bound to local host'

    while True:
        (csocket, addr) = serversocket.accept()
        print 'Accepted Connection'
        #svg = serversocket.recv(MAX_SIZE)
        
        print 'Printing SVG'
        #print svg






if __name__=="__main__":
    main()
