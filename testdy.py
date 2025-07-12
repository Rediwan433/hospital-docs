import socket
import hl7

HOST = "172.20.20.245"  # Standard loopback interface address (localhost)
PORT = 5600  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(2048)
            response = data.decode("utf-8")
            
            #id = (str(data.splitlines()[0]).split('|')[9])
            print('received {} bytes from {}'.format((data), addr))
